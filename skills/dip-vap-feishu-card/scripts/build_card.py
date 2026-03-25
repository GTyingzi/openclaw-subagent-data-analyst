#!/usr/bin/env python3
"""
build_card.py — 飞书卡片模板构建器

从模板注册表加载模板，用数据替换占位符，输出完整卡片 JSON。
可选自动调用 feishu-card.js 发送。

用法:
  python3 build_card.py --template trend_line --data /tmp/query_data.json
  python3 build_card.py --template trend_line --data /tmp/query_data.json --to oc_xxx --send
  python3 build_card.py --template rank_bar --data /tmp/query_data.json --output /tmp/my_card.json
"""

import argparse
import json
import os
import re
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "templates")
REGISTRY_FILE = os.path.join(TEMPLATES_DIR, "_registry.json")
FEISHU_CARD_JS = os.path.join(SCRIPT_DIR, "feishu-card.js")


def load_registry():
    """加载模板注册表"""
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_template(registry, template_id):
    """根据 ID 查找模板配置"""
    for tpl in registry.get("templates", []):
        if tpl["id"] == template_id:
            return tpl
    return None


def load_template(template_file):
    """加载模板 JSON 文件"""
    filepath = os.path.join(TEMPLATES_DIR, template_file)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def replace_placeholders(obj, data):
    """
    递归替换模板中的 {{placeholder}} 占位符。
    
    - 如果整个字符串就是一个占位符 "{{key}}"，直接替换为 data[key] 的原始类型（列表、字典等）
    - 如果是字符串中嵌入占位符 "xxx {{key}} yyy"，替换为字符串
    - 递归处理嵌套的字典和列表
    """
    if isinstance(obj, str):
        # 完整匹配: 整个字符串就是 "{{key}}"
        full_match = re.fullmatch(r"\{\{(\w+)\}\}", obj.strip())
        if full_match:
            key = full_match.group(1)
            if key in data:
                return data[key]
            return obj  # 未找到则保留原占位符

        # 部分匹配: 字符串中包含多个或嵌入式 {{key}}
        def replacer(m):
            key = m.group(1)
            if key in data:
                val = data[key]
                if isinstance(val, (dict, list)):
                    return json.dumps(val, ensure_ascii=False)
                return str(val)
            return m.group(0)

        return re.sub(r"\{\{(\w+)\}\}", replacer, obj)

    elif isinstance(obj, dict):
        return {k: replace_placeholders(v, data) for k, v in obj.items()}

    elif isinstance(obj, list):
        return [replace_placeholders(item, data) for item in obj]

    return obj


def build_card(template_id, data):
    """构建卡片: 加载模板 + 替换占位符"""
    registry = load_registry()
    tpl_config = find_template(registry, template_id)
    if not tpl_config:
        available = [t["id"] for t in registry.get("templates", [])]
        print(f"❌ 未找到模板 '{template_id}'，可用模板: {available}", file=sys.stderr)
        sys.exit(1)

    template = load_template(tpl_config["file"])
    card = replace_placeholders(template, data)
    return card


def send_card(receive_id, card_json_path):
    """调用 feishu-card.js 发送卡片"""
    cmd = ["node", FEISHU_CARD_JS, receive_id, f"@{card_json_path}"]
    print(f"📤 发送卡片: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="飞书卡片模板构建器")
    parser.add_argument("--template", "-t", help="模板 ID（如 trend_line, rank_bar, comparison_table, kpi_summary）")
    parser.add_argument("--data", "-d", help="数据 JSON 文件路径")
    parser.add_argument("--output", "-o", default="/tmp/card.json", help="输出卡片 JSON 路径（默认 /tmp/card.json）")
    parser.add_argument("--send", "-s", action="store_true", help="自动发送卡片")
    parser.add_argument("--to", dest="receive_id", help="发送目标 ID（oc_xxx 群组 / ou_xxx 用户）")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有可用模板")

    args = parser.parse_args()

    # 列出模板
    if args.list:
        registry = load_registry()
        print("可用模板:")
        for tpl in registry.get("templates", []):
            print(f"  {tpl['id']:20s} — {tpl['name']} (chart_type: {tpl['chart_type']})")
        return

    # 校验必填参数
    if not args.template or not args.data:
        parser.error("--template 和 --data 为必填参数（使用 --list 可查看可用模板）")

    # 读取数据
    try:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取数据文件失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 构建卡片
    card = build_card(args.template, data)

    # 输出
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(card, f, ensure_ascii=False, indent=2)
    print(f"✅ 卡片已生成: {args.output}")

    # 发送
    if args.send:
        if not args.receive_id:
            print("❌ 使用 --send 时必须指定 --to <receive_id>", file=sys.stderr)
            sys.exit(1)
        send_card(args.receive_id, args.output)


if __name__ == "__main__":
    main()
