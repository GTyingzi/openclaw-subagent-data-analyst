# 卡片元素详解

---

## Markdown（富文本）

### 基础语法

```json
{
  "tag": "markdown",
  "content": "**粗体** *斜体* ~~删除线~~",
  "text_align": "left"
}
```

---

### 飞书特殊语法

#### Emoji
- `:OK:` - ✓ 对勾
- `:THUMBSUP:` - 👍 点赞
- `:STAR:` - ⭐ 星星
- `:FIRE:` - 🔥 火焰

#### 颜色文本
```markdown
<font color='red'>红色文本</font>
<font color='green'>绿色文本</font>
<font color='blue'>蓝色文本</font>
```

#### @提醒
```markdown
<at id=all></at>  # @所有人
<at id=ou_xxx></at>  # @特定用户
```

---

### 粗体格式注意事项

**正确格式**（冒号在粗体外）:
```markdown
**区域**：四川
**指标**：订单量
**周期**：2026年3月
```

**错误格式**（冒号在粗体里会显示异常）:
```markdown
**区域：**四川
**指标：**订单量
```

---

### 标题和层级

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
```

---

### 列表

```markdown
**无序列表**:
- 项目1
- 项目2
- 项目3

**有序列表**:
1. 第一步
2. 第二步
3. 第三步
```

---

## HR（分割线）

```json
{"tag": "hr"}
```

**作用**: 分隔不同内容区域，提升可读性

---

## Chart（图表）

### 柱状图（纵向）

**适用场景**: 分类对比、月度数据

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "bar",
    "data": {
      "values": [
        {"category": "L9", "value": 100},
        {"category": "L8", "value": 200},
        {"category": "L7", "value": 150}
      ]
    },
    "xField": ["category"],
    "yField": "value",
    "label": {"visible": true}
  },
  "preview": true,
  "color_theme": "brand",
  "height": "auto"
}
```

---

### 条形图（横向）

**适用场景**: Top N 排名、城市对比

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "bar",
    "direction": "horizontal",
    "data": {
      "values": [
        {"city": "深圳", "value": 1382},
        {"city": "杭州", "value": 1380},
        {"city": "成都", "value": 1239}
      ]
    },
    "xField": "value",
    "yField": ["city"],
    "label": {"visible": true}
  },
  "preview": true,
  "color_theme": "brand",
  "height": "400px"
}
```

**关键点**:
- `direction: "horizontal"` - 必须指定
- `xField` 是数值字段（字符串，不是数组）
- `yField` 是分类字段（数组格式）
- 数据按值**降序排列**（最大的在前）
- 高度建议 400px 以上（数据量大时）

---

### 折线图

**适用场景**: 时间序列趋势、按天/周/月数据

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "line",
    "data": {
      "values": [
        {"date": "2026-03-01", "value": 100},
        {"date": "2026-03-02", "value": 120},
        {"date": "2026-03-03", "value": 110}
      ]
    },
    "xField": "date",
    "yField": "value",
    "point": {"visible": true},
    "label": {"visible": true}
  },
  "preview": true,
  "color_theme": "brand",
  "height": "240px"
}
```

---

### 饼图

**适用场景**: 占比构成、份额分布

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "pie",
    "data": {
      "values": [
        {"category": "i6", "value": 5291},
        {"category": "L6", "value": 887},
        {"category": "L7", "value": 550}
      ]
    },
    "categoryField": "category",
    "valueField": "value",
    "label": {"visible": true}
  },
  "preview": true,
  "color_theme": "brand"
}
```

---

### 分组柱状图

**适用场景**: 多维度对比、分组数据

```json
{
  "tag": "chart",
  "chart_spec": {
    "type": "bar",
    "data": {
      "values": [
        {"month": "1月", "type": "订单", "value": 100},
        {"month": "1月", "type": "交付", "value": 80},
        {"month": "2月", "type": "订单", "value": 120},
        {"month": "2月", "type": "交付", "value": 110}
      ]
    },
    "xField": ["month", "type"],
    "yField": "value",
    "seriesField": "type",
    "legends": {"visible": true, "orient": "bottom"}
  },
  "preview": true,
  "color_theme": "brand"
}
```

---

## Table（表格）

### 基础表格

```json
{
  "tag": "table",
  "columns": [
    {
      "data_type": "text",
      "name": "col1",
      "display_name": "列1",
      "width": "auto"
    },
    {
      "data_type": "number",
      "name": "col2",
      "display_name": "列2",
      "format": {"precision": 0}
    }
  ],
  "rows": [
    {"col1": "值1", "col2": 100},
    {"col1": "值2", "col2": 200}
  ],
  "row_height": "low",
  "header_style": {
    "background_style": "grey",
    "bold": true
  },
  "page_size": 10
}
```

---

### 数据类型

| data_type | 说明 | 示例值 |
|-----------|------|--------|
| `text` | 文本 | "字符串" |
| `number` | 数值 | 123 |
| `date` | 日期 | "2026-03-13" |

---

### 数值格式化

```json
{
  "data_type": "number",
  "name": "value",
  "display_name": "数值",
  "format": {
    "precision": 0,       // 小数位数
    "symbol": "%",        // 符号（%、¥等）
    "separator": true     // 千位分隔符
  }
}
```

**示例**:
- `{"precision": 0}` → 123
- `{"precision": 1, "symbol": "%"}` → 12.3%
- `{"precision": 0, "separator": true}` → 1,234,567

---

### ⚠️ Rows 格式（极易出错）

**正确格式**（直接用字符串或数字）:
```json
{
  "rows": [
    {"col1": "值1", "col2": 100},
    {"col1": "值2", "col2": 200}
  ]
}
```

**错误格式**（不要用嵌套对象）:
```json
{
  "rows": [
    {
      "col1": {"tag": "plain_text", "content": "值1"},
      "col2": {"tag": "plain_text", "content": "100"}
    }
  ]
}
```

**错误结果**: 会显示为 `map[content:xxx tag:plain_...]`

---

### 行高和分页

| 参数 | 可选值 | 说明 |
|------|--------|------|
| `row_height` | `low` / `middle` / `high` | 行高 |
| `page_size` | 数字 | 每页显示行数 |

---

## Column Set（分栏布局）

**适用场景**: 左右对比、多图并列

```json
{
  "tag": "column_set",
  "columns": [
    {
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "左侧内容"}
      ]
    },
    {
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "右侧内容"}
      ]
    }
  ]
}
```

---

## 注意事项

### 1. Schema 2.0 不支持的元素

- ❌ `note` 标签（用 markdown 替代）
- ❌ 部分旧版语法

---

### 2. 图表配置层级

**正确**（preview 和 color_theme 在 chart 元素层级）:
```json
{
  "tag": "chart",
  "chart_spec": {...},
  "preview": true,
  "color_theme": "brand"
}
```

**错误**（不要放在 chart_spec 里）:
```json
{
  "tag": "chart",
  "chart_spec": {
    "preview": true,
    "color_theme": "brand"
  }
}
```

---

### 3. Data 格式

**正确**（必须是对象，包含 values 数组）:
```json
"data": {"values": [...]}
```

**错误**（不是直接数组）:
```json
"data": [...]
```

---

### 4. xField 格式

**正确**（用数组格式）:
```json
"xField": ["category"]
"xField": ["category1", "category2"]
```

**错误**（不是字符串）:
```json
"xField": "category"
```

**例外**: 横向条形图的 xField 是字符串（数值字段）

---

## 颜色主题

| 颜色 | template 值 | 适用场景 |
|------|-----------|---------|
| 蓝色 | `blue` | 常规报告 |
| 绿色 | `green` | 正向数据 |
| 橙色 | `orange` | 警告信息 |
| 红色 | `red` | 异常数据 |
| 紫色 | `purple` | 重要通知 |
| 靛蓝 | `indigo` | 高级分析 |
