#!/usr/bin/env bash
# mirror-check.sh — prototypes/ 与生产源码的镜像一致性与完全独立校验（prototype-app 硬规则 2/3）
# 用法: mirror-check.sh [项目根目录] [生产源码根，默认 src]
#
# 镜像检查: prototypes/ 下每个代码文件首 6 行必须声明其一——
#   「镜像生产 <路径>」: 生产对应物必须存在，且一个生产文件只被映射一次
#   「原型私有」:       挂具/私有实现，跳过对应检查
#   PrototypeRoot.* 为挂具入口，自动豁免
#
# 独立性检查:
#   原型 → 生产: 原型文件不得 import 生产源码（相对路径越出 prototypes/、'src/'、'@/'、'~/' 均违规）
#   生产 → 原型: 生产源码不得 import prototypes/，桥接文件豁免
#   桥接豁免: 路径匹配 BRIDGE_ALLOW 正则（默认覆盖 App/main/router/layout 与 route-group shim），可用环境变量覆盖
set -uo pipefail

root="${1:-.}"
src="${2:-src}"
proto="$root/prototypes"
bridge_allow="${BRIDGE_ALLOW:-\(prototype\)|/prototype/|(App|main|router|routes?|layout)\.(ts|tsx|js|jsx)$}"
tmp="$(mktemp)"
fail=0

[ -d "$proto" ] || { echo "未找到 $proto"; exit 1; }

# ---- 镜像检查 ----
while IFS= read -r f; do
  rel="${f#"$proto"/}"
  head_txt=$(head -n 6 "$f")
  if printf '%s' "$head_txt" | grep -q '原型私有'; then continue; fi
  target=$(printf '%s' "$head_txt" | grep -oE '镜像生产[ ：]*[A-Za-z0-9_./-]+' | head -1 | awk '{print $NF}')
  if [ -z "$target" ]; then
    echo "缺失声明: $rel"
    fail=1
    continue
  fi
  case "$target" in
    "$src"/*|/*) ;;
    *) target="$src/$target" ;;
  esac
  if [ ! -f "$root/$target" ]; then
    echo "对应物不存在: $rel -> $target"
    fail=1
    continue
  fi
  printf '%s\n' "$target" >> "$tmp"
done < <(find "$proto" -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.css' \) ! -name 'PrototypeRoot.*' | sort)

if [ -s "$tmp" ]; then
  dups=$(sort "$tmp" | uniq -d)
  if [ -n "$dups" ]; then
    echo "同一生产文件被多个原型文件映射(合并嫌疑):"
    echo "$dups"
    fail=1
  fi
fi
rm -f "$tmp"

# ---- 独立性检查: 原型 → 生产 ----
while IFS= read -r f; do
  rel="${f#"$proto"/}"
  depth=$(printf '%s' "$rel" | tr -cd '/' | wc -c)
  imports=$(grep -ohE "(from|import)[[:space:]]*[\(]?['\"][^'\"]+['\"]" "$f" 2>/dev/null \
    | sed -E "s/.*['\"]([^'\"]+)['\"].*/\1/")
  while IFS= read -r imp; do
    [ -z "$imp" ] && continue
    hit=""
    case "$imp" in
      @/*|~/*|"$src"/*) hit="$imp" ;;
      ./*|../*)
        ups=0
        rest="$imp"
        while [ "${rest#../}" != "$rest" ]; do ups=$((ups + 1)); rest="${rest#../}"; done
        [ "$ups" -gt "$depth" ] && hit="$imp"
        ;;
    esac
    if [ -n "$hit" ]; then
      echo "越界 import(原型→生产): $rel -> $imp"
      fail=1
    fi
  done <<EOF_IMP
$imports
EOF_IMP
done < <(find "$proto" -type f \( -name '*.ts' -o -name '*.tsx' \) | sort)

# ---- 独立性检查: 生产 → 原型 ----
offenders=$(grep -rlE "(from|import)[^\"']*['\"][^\"']*prototypes/" "$root/$src" \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' 2>/dev/null || true)
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if printf '%s' "$f" | grep -qE "$bridge_allow"; then continue; fi
  echo "生产 import 原型(非桥接): ${f#"$root/"}"
  fail=1
done <<EOF_OFF
$offenders
EOF_OFF

if [ "$fail" -eq 0 ]; then
  echo "mirror check 通过"
else
  exit 1
fi
