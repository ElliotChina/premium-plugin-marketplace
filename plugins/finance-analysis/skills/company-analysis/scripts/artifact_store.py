"""Hardened, shared artifact storage: immutable atomic installs under run directories."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import errno
import os
from pathlib import Path
import stat
import uuid

import evidence_contract


class ContractError(ValueError):
    """Raised for invalid artifact store usage."""


class StateError(ValueError):
    """Raised when an otherwise-valid install conflicts with existing content."""

    def __init__(self, message: str, **details: object) -> None:
        super().__init__(message)
        self.details = details


TRANSACTION_SCHEMA = "company-analysis-valuation-transaction-v1"


_SAFE_DIRECTORY_OPERATIONS = (os.open, os.stat, os.unlink, os.link, os.mkdir)
_SAFE_DIRECTORY_PRIMITIVES_AVAILABLE = all(
    operation in os.supports_dir_fd for operation in _SAFE_DIRECTORY_OPERATIONS
)


def _hash(value: object) -> str:
    return evidence_contract.content_hash(value)


def _require_safe_artifact_name(name: str) -> str:
    # lexical relative_to checks pass names like "../x.json"; dir_fd calls would
    # then resolve outside the target directory, so only plain file names are valid.
    if (
        not isinstance(name, str) or not name or "/" in name or name.startswith(".")
        or name in {".", ".."}
    ):
        raise ContractError("artifact name must be a plain file name without path separators")
    return name


def atomic_install(target_dir: Path, name: str, data: Mapping) -> bool:
    _require_safe_artifact_name(name)
    payload = evidence_contract.canonical_json_bytes(data)
    directory_descriptor, expected_identity = open_stable_dir(target_dir, create=False)
    temporary_name = None
    created: list[tuple[str, int, int]] = []
    try:
        existing = _read_dir_artifact_bytes(directory_descriptor, name)
        if existing is not None:
            if existing == payload:
                return False
            raise StateError("immutable artifact conflicts with existing content")
        temporary_name = _stage_dir_artifact(directory_descriptor, payload)
        assert_dir_identity(target_dir, expected_identity)
        _publish_staged_artifact(directory_descriptor, temporary_name, name, payload, created)
        temporary_name = None
        assert_dir_identity(target_dir, expected_identity)
        os.fsync(directory_descriptor)
        return True
    except Exception:
        _rollback_created_artifacts(directory_descriptor, created)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=directory_descriptor)
            except FileNotFoundError:
                pass
        raise
    finally:
        os.close(directory_descriptor)


def _require_safe_directory_primitives() -> None:
    required_flags = ("O_DIRECTORY", "O_NOFOLLOW")
    if any(not hasattr(os, flag) for flag in required_flags):
        raise ContractError("safe directory descriptor operations are unavailable")
    if not _SAFE_DIRECTORY_PRIMITIVES_AVAILABLE:
        raise ContractError("safe directory descriptor operations are unavailable")


def _directory_identity(directory_descriptor: int) -> tuple[int, int]:
    metadata = os.fstat(directory_descriptor)
    if not stat.S_ISDIR(metadata.st_mode):
        raise ContractError("artifact directory must be a stable directory")
    return metadata.st_dev, metadata.st_ino


def _open_directory_no_follow(path: str, *, directory_descriptor: int | None = None) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    try:
        if directory_descriptor is None:
            opened_descriptor = os.open(path, flags)
        else:
            opened_descriptor = os.open(path, flags, dir_fd=directory_descriptor)
    except OSError as exc:
        raise ContractError("artifact directory must be a stable directory, not a symlink") from exc
    try:
        _directory_identity(opened_descriptor)
    except Exception:
        os.close(opened_descriptor)
        raise
    return opened_descriptor


def _open_absolute_directory_no_follow(path: Path) -> int:
    _require_safe_directory_primitives()
    if not path.is_absolute():
        raise ContractError("run directory must be an absolute path")
    current_descriptor = _open_directory_no_follow("/")
    try:
        for component in path.parts[1:]:
            next_descriptor = _open_directory_no_follow(component, directory_descriptor=current_descriptor)
            os.close(current_descriptor)
            current_descriptor = next_descriptor
        return current_descriptor
    except Exception:
        os.close(current_descriptor)
        raise


def _open_or_create_directory_no_follow(parent_descriptor: int, name: str, *, create: bool) -> int:
    try:
        return _open_directory_no_follow(name, directory_descriptor=parent_descriptor)
    except ContractError:
        if not create:
            raise
    try:
        os.mkdir(name, 0o700, dir_fd=parent_descriptor)
    except FileExistsError:
        pass
    except OSError as exc:
        raise ContractError("artifact directory cannot be created safely") from exc
    return _open_directory_no_follow(name, directory_descriptor=parent_descriptor)


def open_stable_dir(
    target_dir: Path,
    *,
    create: bool = False,
) -> tuple[int, tuple[tuple[int, int], tuple[int, int], tuple[int, int]]]:
    if target_dir.parent.name != "analysis":
        raise ContractError("artifact directory path is invalid")
    run_dir = target_dir.parent.parent
    run_descriptor = _open_absolute_directory_no_follow(run_dir)
    analysis_descriptor = None
    try:
        analysis_descriptor = _open_or_create_directory_no_follow(run_descriptor, "analysis", create=create)
        valuation_descriptor = _open_or_create_directory_no_follow(analysis_descriptor, target_dir.name, create=create)
    except Exception:
        if analysis_descriptor is not None:
            os.close(analysis_descriptor)
        os.close(run_descriptor)
        raise
    identities = (
        _directory_identity(run_descriptor),
        _directory_identity(analysis_descriptor),
        _directory_identity(valuation_descriptor),
    )
    os.close(analysis_descriptor)
    os.close(run_descriptor)
    return valuation_descriptor, identities


def assert_dir_identity(
    target_dir: Path,
    expected_identity: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
) -> None:
    directory_descriptor, current_identity = open_stable_dir(target_dir, create=False)
    os.close(directory_descriptor)
    if current_identity != expected_identity:
        raise ContractError("artifact directory changed during publication")


def _read_dir_artifact_bytes(directory_descriptor: int, name: str) -> bytes | None:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(name, flags, dir_fd=directory_descriptor)
    except FileNotFoundError:
        return None
    except OSError as exc:
        if exc.errno == errno.ELOOP:
            raise ContractError(f"installed artifact must not be a symlink") from exc
        raise ContractError(f"installed artifact cannot be read") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ContractError(f"installed valuation artifact {name} must be a regular file")
        chunks = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _stage_dir_artifact(directory_descriptor: int, payload: bytes) -> str:
    temporary_name = f".company-valuation-{os.getpid()}-{uuid.uuid4().hex}.tmp"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(temporary_name, flags, 0o600, dir_fd=directory_descriptor)
    try:
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
        os.fsync(descriptor)
    except Exception:
        try:
            os.close(descriptor)
        finally:
            try:
                os.unlink(temporary_name, dir_fd=directory_descriptor)
            except FileNotFoundError:
                pass
        raise
    os.close(descriptor)
    return temporary_name


def _publish_staged_artifact(
    directory_descriptor: int,
    temporary_name: str,
    final_name: str,
    payload: bytes,
    created: list[tuple[str, int, int]],
) -> None:
    existing = _read_dir_artifact_bytes(directory_descriptor, final_name)
    if existing is not None:
        if existing != payload:
            raise StateError("immutable artifact conflicts with existing content")
        os.unlink(temporary_name, dir_fd=directory_descriptor)
        return
    try:
        os.link(
            temporary_name,
            final_name,
            src_dir_fd=directory_descriptor,
            dst_dir_fd=directory_descriptor,
            follow_symlinks=False,
        )
    except FileExistsError:
        existing = _read_dir_artifact_bytes(directory_descriptor, final_name)
        if existing == payload:
            os.unlink(temporary_name, dir_fd=directory_descriptor)
            return
        raise StateError("immutable artifact conflicts with existing content") from None
    except OSError as exc:
        raise ContractError("artifact cannot be published safely") from exc
    metadata = os.stat(final_name, dir_fd=directory_descriptor, follow_symlinks=False)
    created.append((final_name, metadata.st_dev, metadata.st_ino))
    os.unlink(temporary_name, dir_fd=directory_descriptor)


def _rollback_created_artifacts(directory_descriptor: int, created: Sequence[tuple[str, int, int]]) -> None:
    for name, expected_device, expected_inode in reversed(created):
        try:
            metadata = os.stat(name, dir_fd=directory_descriptor, follow_symlinks=False)
        except FileNotFoundError:
            continue
        if metadata.st_dev == expected_device and metadata.st_ino == expected_inode:
            os.unlink(name, dir_fd=directory_descriptor)


def transaction_marker(operation: str, artifacts: Mapping[str, Mapping]) -> dict:
    return {
        "schema_version": TRANSACTION_SCHEMA,
        "operation": operation,
        "artifacts": {
            name: _hash(artifacts[name])
            for name in sorted(artifacts)
        },
    }


def install_all(target_dir: Path, operation: str, items: Sequence[tuple[str, Mapping]], artifacts: Mapping[str, Mapping]) -> Mapping:
    if not {name for name, _data in items} <= set(artifacts):
        raise ContractError("transaction artifacts must cover the install item set")
    marker = transaction_marker(operation, artifacts)
    all_items = list(items) + [("transaction.json", marker)]
    seen_names = set()
    payloads: dict[str, bytes] = {}
    for name, data in all_items:
        if name in seen_names:
            raise ContractError("duplicate valuation artifact install target")
        seen_names.add(name)
        _require_safe_artifact_name(name)
        payloads[name] = evidence_contract.canonical_json_bytes(data)

    directory_descriptor, expected_identity = open_stable_dir(target_dir, create=True)
    staged: list[tuple[str, str | None]] = []
    created: list[tuple[str, int, int]] = []
    try:
        for name, _data in all_items:
            existing = _read_dir_artifact_bytes(directory_descriptor, name)
            if existing is not None:
                if existing != payloads[name]:
                    raise StateError("immutable artifact conflicts with existing content")
                staged.append((name, None))
            else:
                staged.append((name, _stage_dir_artifact(directory_descriptor, payloads[name])))
        for name, temporary_name in staged:
            assert_dir_identity(target_dir, expected_identity)
            if temporary_name is not None:
                _publish_staged_artifact(directory_descriptor, temporary_name, name, payloads[name], created)
        assert_dir_identity(target_dir, expected_identity)
        os.fsync(directory_descriptor)
    except Exception:
        _rollback_created_artifacts(directory_descriptor, created)
        for _name, temporary_name in staged:
            if temporary_name is None:
                continue
            try:
                os.unlink(temporary_name, dir_fd=directory_descriptor)
            except FileNotFoundError:
                pass
        try:
            os.fsync(directory_descriptor)
        except OSError:
            pass
        raise
    finally:
        os.close(directory_descriptor)
    return marker
