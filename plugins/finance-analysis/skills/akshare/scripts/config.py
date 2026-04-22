#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AKShare 技能文档配置
"""

from pathlib import Path

# 文档目录
DOCS_DIR = Path(__file__).parent.parent / "references"

# 在线文档源
DOC_SOURCES = {
    "installation": "https://akshare.akfamily.xyz/_sources/installation.md.txt",
    "stock": "https://akshare.akfamily.xyz/_sources/data/stock/stock.md.txt",
}
