---
name: dip-vap-feishu-card
description: 发送飞书卡片消息。当需要展示数据图表、表格、富文本等复杂内容时使用此 skill。支持柱状图、折线图、饼图、表格等元素。优先推荐直接回复 markdown（自动渲染为卡片），只在需要原生图表时才用脚本发送。
version: 2.0.0
tags: [飞书, 卡片, 图表, 可视化]
---

# 飞书卡片输出 Skill

## 核心原则

**优先使用方式一（直接回复），只在需要原生图表时才用方式二（脚本发送）！**

---

## 发送方式选择

### 方式一：直接回复 Markdown（推荐，90% 场景）

Agent 输出 markdown 文本作为回复，OpenClaw 自动渲染为飞书卡片。

**输出格式规范**：

```markdown
## {查询主题标题}

| 列1 | 列2 | 列3 |
|-----|----:|----:|
| 值1 | 值2 | **值3** |

**洞察**：{关键数字加粗的数据洞察，至少一条}
```

**规则**：
- 完整表格（含表头和所有数据行，不截断）
- 关键数字加粗（百分比、极值、异常值）
- 至少一条洞察（趋势/异常/关键结论）

**适用场景**：数据查询结果 + 表格 + 文字洞察（~90%）

---

### 方式二：脚本发送自定义卡片（10% 场景）

需要飞书原生 chart 组件（折线图、柱状图、饼图等 markdown 无法表达的可视化）时：

```bash
node skills/dip-vap-feishu-card/scripts/feishu-card.js <receive_id> '<card_json>'
# 或从文件读取 JSON
node skills/dip-vap-feishu-card/scripts/feishu-card.js <receive_id> @/tmp/card.json
```

**认证**：从 `~/.openclaw/openclaw.json` 的 `channels.feishu.accounts` 自动读取，无需手动配置。

**⚠️ 使用脚本发卡片后必须不再输出任何文字**，避免消息重复/乱序。所有洞察文字放在卡片 JSON 内部。

**适用场景**：需要折线图/柱状图/饼图等原生图表（~8%）；复杂布局（分栏、多图组合）（~2%）

---

### 选择原则

| 场景 | 方式 |
|------|------|
| 数据 + 表格 + 文字洞察 | 方式一（直接回复） |
| 需要折线图/柱状图/饼图 | 方式二（脚本发送），发送后不再输出文字 |
| 复杂多图布局 | 方式二（脚本发送），发送后不再输出文字 |

---

## 卡片 JSON 基础结构（方式二）

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 标题"},
    "subtitle": {"tag": "plain_text", "content": "副标题"},
    "template": "blue"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": []
  }
}
```

**header.template** 颜色：`blue` / `green` / `orange` / `red` / `purple` / `indigo`

---

## 常用元素（方式二）

### Chart（图表）

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "line",
    "data": {"values": [{"date": "2026-01", "value": 1234}]},
    "xField": "date",
    "yField": "value"
  },
  "height": "240px"
}
```

支持类型：`line`（折线）、`bar`（柱状）、`pie`（饼图）

**柱状图 xField 注意**：分组柱状图的 xField 为数组 `["category"]`；横向条形图的 xField 是字符串（数值字段）。

### Table（表格）

```json
{
  "tag": "table",
  "columns": [
    {"data_type": "text", "name": "col1", "display_name": "列1"},
    {"data_type": "number", "name": "col2", "display_name": "列2", "format": {"precision": 0}}
  ],
  "rows": [
    {"col1": "值1", "col2": 100}
  ]
}
```

**⚠️ rows 值必须是简单类型**（字符串/数字），不能嵌套 `{"tag": "plain_text", ...}`。

### Markdown

```json
{"tag": "markdown", "content": "**粗体** *斜体*"}
```

---

## receive_id 类型

- `ou_xxx` → 用户 open_id（私聊）
- `oc_xxx` → 群组 chat_id（群聊）

---

## 常见错误

| 错误 | 原因 | 解决 |
|------|------|------|
| rows 显示 `map[...]` | rows 用了嵌套对象格式 | 改用 `{"col": "值"}` 简单类型 |
| 图表不显示 | data 格式错误 | 改为 `"data": {"values": [...]}` |
| 柱状图 xField 报错 | 分组柱状图用了字符串 | 改为数组 `["category"]` |
| 发送后消息重复 | 脚本发送后又输出了文字 | 脚本发送后不再输出任何内容 |
| schema 2.0 note 报错 | 2.0 不支持 note 标签 | 改用 `markdown` 标签 |

---

## 详细参考

- `references/card-elements.md`：卡片元素详解
- `references/card-templates.md`：6种常用模板示例
- `templates/`：预定义 JSON 模板（kpi_summary、trend_line、rank_bar、comparison_table）
