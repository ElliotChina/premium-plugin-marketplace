#!/usr/bin/env bash
# mirror-check.sh — prototypes/ 与生产源码文件级一一对应的机械化校验（prototype-app 硬规则 2）
# 用法: mirror-check.sh [项目根目录] [生产源码根，默认 src]
# 规则: prototypes/ 下每个代码文件首 6 行必须声明其一——
#   「镜像生产 <路径>」: 生产对应物必须存在，且一个生产文件只被映射一次
#   「原型私有」:       挂具/私有实现，跳过对应检查
# PrototypeRoot.* 为挂具入口，自动豁免。
set -uo pipefail

root="${1:-.}"
src="${2:-src}"
proto="$root/prototypes"
tmp="$(mktemp)"
fail=0

[ -d "$proto" ] || { echo "未找到 $proto"; exit 1; }

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

if [ "$fail" -eq 0 ]; then
  echo "mirror check 通过"
else
  exit 1
fi
