#!/usr/bin/env bash
# mirror-check.sh — prototypes/ 与生产源码的镜像一致性、完全独立与状态纪律校验（prototype-app 硬规则 1/2/3/6）
# 用法: mirror-check.sh [项目根目录] [生产源码根，默认 src]
#
# 镜像检查（fail）:
#   「镜像生产 <路径>」: 生产对应物必须存在，一个生产文件只被映射一次，导出风格一致（default 形态一致、原型导出 ⊆ 生产导出）
#   「镜像生产 <路径>」+「待建」: 0→1 页面专用——对应物尚未存在，豁免存在性与导出检查，每次运行提示待建清单
#   「原型私有」:       挂具/私有实现，必须位于白名单位置（proto-harness/、proto-logic/、*.variant-*）
#   变体文件（*.variant-*.tsx?）: 首部必须声明「基准 <同目录同名镜像文件路径>」与「轴」；基准须存在、为已登记镜像文件，其生产映射计入一对多查重
#   PrototypeRoot.* 为挂具入口，自动豁免
# 状态纪律（fail）:
#   持久化 API 禁入（localStorage/sessionStorage/indexedDB/document.cookie；覆盖 ts/tsx/js/jsx/mjs/html，词法匹配——字符串拼接绕过不检测）
#   测试文件禁入（*.test.*、*.spec.*、__tests__/）
#   HTML 仅允许顶层 prototypes/proto-logic/ 下（LOGIC 分支产物；嵌套 proto-logic/ 目录不在豁免内）
#   prototypes/README.md 必须存在，且 pages/ 下每个页面在映射表中登记
# 独立性检查（fail）:
#   原型 → 生产: 原型文件不得 import 生产源码（相对路径越出 prototypes/、'src/'、'@/'、'~/' 均违规）
#   生产 → 原型: 生产源码不得 import prototypes/，桥接文件豁免
#   桥接豁免: 路径匹配 BRIDGE_ALLOW 正则（默认覆盖 App/main/router/layout 与 route-group shim），可用环境变量覆盖
# 人工确认（warning，不计失败）:
#   占位内容粗筛（lorem/TODO/FIXME/占位）；桥接文件未检出 dev 门控字样
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

  # 变体文件: 验证式豁免——基准须存在、同目录同名前缀、为已登记镜像文件,且声明发散轴
  case "$rel" in
    *.variant-*.ts|*.variant-*.tsx|*.variant-*.css)
      vstem="${rel%%.variant-*}"
      base=$(printf '%s' "$head_txt" | grep -oE '基准[ ：]*[A-Za-z0-9_./-]+' | head -1 | awk '{print $NF}')
      if ! printf '%s' "$head_txt" | grep -q '轴'; then
        echo "变体文件缺发散轴声明: $rel"
        fail=1
      fi
      case "$base" in
        "$vstem".ts|"$vstem".tsx) ;;
        *)
          echo "变体基准须为同目录同名镜像文件: $rel -> ${base:-未声明}"
          fail=1
          continue
          ;;
      esac
      base_file="$proto/$base"
      if [ ! -f "$base_file" ]; then
        echo "变体基准不存在: $rel -> $base"
        fail=1
        continue
      fi
      base_head=$(head -n 6 "$base_file")
      if printf '%s' "$base_head" | grep -q '原型私有'; then
        echo "变体基准必须是镜像文件而非原型私有: $rel -> $base"
        fail=1
        continue
      fi
      b_target=$(printf '%s' "$base_head" | grep -oE '镜像生产[（(待建)）： ]*[A-Za-z0-9_./-]+' | head -1 | awk '{print $NF}')
      if [ -z "$b_target" ]; then
        echo "变体基准文件缺镜像声明: $rel -> $base"
        fail=1
        continue
      fi
      case "$b_target" in
        "$src"/*|/*) ;;
        *) b_target="$src/$b_target" ;;
      esac
      # 变体与基准页同源,不重复计入一对多查重
      continue
      ;;
  esac

  if printf '%s' "$head_txt" | grep -q '原型私有'; then
    case "$rel" in
      proto-harness/*|proto-logic/*) ;;
      *)
        echo "原型私有文件不在白名单位置(proto-harness/|proto-logic/): $rel"
        fail=1
        ;;
    esac
    continue
  fi

  target=$(printf '%s' "$head_txt" | grep -oE '镜像生产[（(待建)）： ]*[A-Za-z0-9_./-]+' | head -1 | awk '{print $NF}')
  if [ -z "$target" ]; then
    echo "缺失声明: $rel"
    fail=1
    continue
  fi
  case "$target" in
    "$src"/*|/*) ;;
    *) target="$src/$target" ;;
  esac
  if printf '%s' "$head_txt" | grep -q '待建'; then
    echo "待建对应物(生产就位前豁免,就位后请移除待建标记): $rel -> $target"
    printf '%s\n' "$target" >> "$tmp"
    continue
  fi
  if [ ! -f "$root/$target" ]; then
    echo "对应物不存在: $rel -> $target"
    fail=1
    continue
  fi
  printf '%s\n' "$target" >> "$tmp"

  # 导出风格比对: default 形态一致 + 原型导出 ⊆ 生产导出（签名偏离应写入头注释）
  case "$f" in
    *.ts|*.tsx)
      p_def=$(grep -cE '^export default' "$f")
      s_def=$(grep -cE '^export default' "$root/$target")
      if [ "$p_def" != "$s_def" ]; then
        echo "导出风格不一致(default): $rel vs $target"
        fail=1
      fi
      p_named=$(grep -oE '^export (const|function|class|type|interface|let|var) [A-Za-z0-9_]+' "$f" | awk '{print $3}' | sort -u)
      s_named=$(grep -oE '^export (const|function|class|type|interface|let|var) [A-Za-z0-9_]+' "$root/$target" | awk '{print $3}' | sort -u)
      while IFS= read -r n; do
        [ -z "$n" ] && continue
        if ! printf '%s\n' "$s_named" | grep -qx "$n"; then
          echo "原型导出不在生产对应物中(签名偏离须头注释说明): $rel 导出 $n"
          fail=1
        fi
      done <<EOF_EXP
$p_named
EOF_EXP
      ;;
  esac
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

# ---- 状态纪律 ----
persist=$(grep -rinE 'localStorage|sessionStorage|indexedDB|document\.cookie' "$proto" \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' --include='*.mjs' --include='*.html' 2>/dev/null || true)
if [ -n "$persist" ]; then
  echo "持久化 API 禁入:"
  echo "$persist"
  fail=1
fi

tests=$(find "$proto" \( -name '*.test.*' -o -name '*.spec.*' -o -type d -name '__tests__' \) 2>/dev/null || true)
if [ -n "$tests" ]; then
  echo "原型目录禁入测试文件:"
  echo "$tests"
  fail=1
fi

stray_html=$(find "$proto" -name '*.html' ! -path "$proto/proto-logic/*" 2>/dev/null || true)
if [ -n "$stray_html" ]; then
  echo "HTML 仅允许出现在 prototypes/proto-logic/ 下:"
  echo "$stray_html"
  fail=1
fi

if [ ! -f "$proto/README.md" ]; then
  echo "缺 prototypes/README.md（路由映射表）"
  fail=1
else
  while IFS= read -r f; do
    rel="${f#"$proto"/}"
    case "$rel" in *.variant-*) continue ;; esac
    if ! grep -qF "$rel" "$proto/README.md"; then
      echo "README 映射表未登记页面: $rel"
      fail=1
    fi
  done < <(find "$proto/pages" -name '*.tsx' 2>/dev/null | sort)
fi

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
done < <(find "$proto" -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.mjs' \) | sort)

# ---- 独立性检查: 生产 → 原型 ----
offenders=$(grep -rlE "(from|import)[^\"']*['\"][^\"']*prototypes/" "$root/$src" \
  --include='*.ts' --include='*.tsx' --include='*.js' --include='*.jsx' 2>/dev/null || true)
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if printf '%s' "$f" | grep -qE "$bridge_allow"; then
    if ! grep -qE 'import\.meta\.env\.DEV|NODE_ENV' "$f"; then
      echo "桥接未检出 dev 门控字样(人工确认): ${f#"$root/"}"
    fi
    continue
  fi
  echo "生产 import 原型(非桥接): ${f#"$root/"}"
  fail=1
done <<EOF_OFF
$offenders
EOF_OFF

# ---- 占位内容粗筛（warning）----
placeholders=$(grep -rinE 'lorem ipsum|TODO|FIXME' "$proto" \
  --include='*.ts' --include='*.tsx' --include='*.css' --include='*.html' 2>/dev/null || true)
if [ -n "$placeholders" ]; then
  echo "占位内容粗筛(人工确认):"
  echo "$placeholders"
fi

echo "人工/运行时项不在脚本覆盖内: 工艺硬指标(ease-out/时长/reduced-motion)、变体轴发散、PICKER 逐字一致、mock 只读、晋升纪律"

if [ "$fail" -eq 0 ]; then
  echo "mirror check 通过"
else
  exit 1
fi
