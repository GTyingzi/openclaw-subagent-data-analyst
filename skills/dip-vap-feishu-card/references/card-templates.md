# 卡片模板示例

---

## 模板 1: 标准数据报告

**适用场景**: 指标趋势分析、周报月报

**结构**: 摘要 + 趋势图 + 明细表 + 洞察

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 数据报告标题"},
    "subtitle": {"tag": "plain_text", "content": "2026年3月"},
    "template": "blue"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {
        "tag": "markdown",
        "content": "**区域**：全国｜**指标**：订单量｜**周期**：2026年3月"
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "**📈 趋势图**"
      },
      {
        "tag": "chart",
        "chart_spec": {
          "type": "line",
          "data": {
            "values": [
              {"date": "03-01", "value": 12345},
              {"date": "03-02", "value": 12456},
              {"date": "03-03", "value": 12567}
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
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "**📋 明细数据**"
      },
      {
        "tag": "table",
        "columns": [
          {"data_type": "text", "name": "date", "display_name": "日期", "width": "auto"},
          {"data_type": "number", "name": "value", "display_name": "订单量", "format": {"precision": 0, "separator": true}},
          {"data_type": "number", "name": "mom", "display_name": "环比", "format": {"precision": 1, "symbol": "%"}}
        ],
        "rows": [
          {"date": "03-01", "value": 12345, "mom": 2.3},
          {"date": "03-02", "value": 12456, "mom": 0.9},
          {"date": "03-03", "value": 12567, "mom": 0.9}
        ],
        "row_height": "low",
        "header_style": {"background_style": "grey", "bold": true},
        "page_size": 10
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "### 💡 数据洞察\n\n**整体趋势**：3月前3天订单量稳步增长，日均12,456单。\n\n**关键发现**：\n- 🔺 峰值：03-03达到12,567单，创近期新高\n- 📊 环比：整体环比增长1.0%，表现稳定"
      }
    ]
  }
}
```

---

## 模板 2: Top N 排名榜

**适用场景**: 城市排名、车型排名、门店排名

**结构**: 标题 + 横向条形图

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "🏆 Top 10 城市排名"},
    "subtitle": {"tag": "plain_text", "content": "按订单量"},
    "template": "indigo"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {
        "tag": "markdown",
        "content": "**周期**：2026年3月｜**指标**：订单量"
      },
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "bar",
          "direction": "horizontal",
          "data": {
            "values": [
              {"city": "深圳", "value": 1382},
              {"city": "杭州", "value": 1380},
              {"city": "成都", "value": 1239},
              {"city": "重庆", "value": 1156},
              {"city": "苏州", "value": 1089},
              {"city": "北京", "value": 987},
              {"city": "上海", "value": 876},
              {"city": "广州", "value": 765},
              {"city": "南京", "value": 654},
              {"city": "武汉", "value": 543}
            ]
          },
          "xField": "value",
          "yField": ["city"],
          "label": {"visible": true}
        },
        "preview": true,
        "color_theme": "brand",
        "height": "500px"
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "### 💡 排名洞察\n\n🥇 **冠军**：深圳以1,382单领跑\n🥈 **亚军**：杭州1,380单紧随其后\n🥉 **季军**：成都1,239单位列第三\n\n**头部集中**：Top 3 占总量的 40%"
      }
    ]
  }
}
```

---

## 模板 3: 占比分析

**适用场景**: 车型占比、区域占比、分类占比

**结构**: 饼图 + 表格 + 洞察

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 车型占比分析"},
    "subtitle": {"tag": "plain_text", "content": "新增保有量"},
    "template": "purple"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {
        "tag": "markdown",
        "content": "**周期**：近7天｜**合计**：7,849辆"
      },
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "pie",
          "data": {
            "values": [
              {"model": "i6", "value": 5291},
              {"model": "L6", "value": 887},
              {"model": "L7", "value": 550},
              {"model": "L8", "value": 361},
              {"model": "i8", "value": 335},
              {"model": "L9", "value": 201},
              {"model": "MEGA", "value": 112}
            ]
          },
          "categoryField": "model",
          "valueField": "value",
          "label": {"visible": true}
        },
        "preview": true,
        "color_theme": "brand"
      },
      {"tag": "hr"},
      {
        "tag": "table",
        "columns": [
          {"data_type": "text", "name": "model", "display_name": "车型"},
          {"data_type": "number", "name": "value", "display_name": "新增量", "format": {"precision": 0, "separator": true}},
          {"data_type": "number", "name": "ratio", "display_name": "占比", "format": {"precision": 1, "symbol": "%"}}
        ],
        "rows": [
          {"model": "i6", "value": 5291, "ratio": 67.4},
          {"model": "L6", "value": 887, "ratio": 11.3},
          {"model": "L7", "value": 550, "ratio": 7.0},
          {"model": "L8", "value": 361, "ratio": 4.6},
          {"model": "i8", "value": 335, "ratio": 4.3},
          {"model": "L9", "value": 201, "ratio": 2.6},
          {"model": "MEGA", "value": 112, "ratio": 1.4}
        ],
        "row_height": "low",
        "header_style": {"background_style": "grey", "bold": true},
        "page_size": 10
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "### 💡 占比洞察\n\n**主力车型**：i6 占据主导地位，占比67.4%\n**第二梯队**：L6 占比11.3%，位居第二\n**长尾车型**：MEGA 占比1.4%，排名最后"
      }
    ]
  }
}
```

---

## 模板 4: 对比分析

**适用场景**: 同比环比、AB对比、多维对比

**结构**: 对比图 + 表格 + 洞察

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 订单vs交付对比"},
    "subtitle": {"tag": "plain_text", "content": "2026年3月"},
    "template": "green"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {
        "tag": "markdown",
        "content": "**区域**：全国｜**周期**：2026年3月前10天"
      },
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "bar",
          "data": {
            "values": [
              {"date": "03-01", "type": "订单", "value": 12345},
              {"date": "03-01", "type": "交付", "value": 11234},
              {"date": "03-02", "type": "订单", "value": 12456},
              {"date": "03-02", "type": "交付", "value": 11345},
              {"date": "03-03", "type": "订单", "value": 12567},
              {"date": "03-03", "type": "交付", "value": 11456}
            ]
          },
          "xField": ["date", "type"],
          "yField": "value",
          "seriesField": "type",
          "legends": {"visible": true, "orient": "bottom"}
        },
        "preview": true,
        "color_theme": "brand",
        "height": "300px"
      },
      {"tag": "hr"},
      {
        "tag": "table",
        "columns": [
          {"data_type": "text", "name": "date", "display_name": "日期"},
          {"data_type": "number", "name": "order", "display_name": "订单量", "format": {"precision": 0, "separator": true}},
          {"data_type": "number", "name": "delivery", "display_name": "交付量", "format": {"precision": 0, "separator": true}},
          {"data_type": "number", "name": "diff", "display_name": "差值", "format": {"precision": 0, "separator": true}}
        ],
        "rows": [
          {"date": "03-01", "order": 12345, "delivery": 11234, "diff": 1111},
          {"date": "03-02", "order": 12456, "delivery": 11345, "diff": 1111},
          {"date": "03-03", "order": 12567, "delivery": 11456, "diff": 1111}
        ],
        "row_height": "low",
        "header_style": {"background_style": "grey", "bold": true},
        "page_size": 10
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "### 💡 对比洞察\n\n**差值稳定**：订单与交付差值保持在1,111单左右\n**转化率**：平均转化率约90%\n**趋势一致**：订单和交付量均呈上升趋势"
      }
    ]
  }
}
```

---

## 模板 5: 简洁摘要

**适用场景**: 快速回复、单一数据点

**结构**: 标题 + KPI 数值 + 简短说明

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 昨日数据"},
    "subtitle": {"tag": "plain_text", "content": "2026-03-12"},
    "template": "blue"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {
        "tag": "markdown",
        "content": "### 总订单量\n\n# 12,567\n\n环比 +2.3%"
      },
      {"tag": "hr"},
      {
        "tag": "markdown",
        "content": "**分车型**：\n- i6: 5,291单 (42%)\n- L6: 2,876单 (23%)\n- L7: 1,456单 (12%)\n- 其他: 2,944单 (23%)"
      }
    ]
  }
}
```

---

## 模板 6: 多图综合分析

**适用场景**: 复杂分析、综合报告

**结构**: 多个图表 + 多个表格 + 分段洞察

```json
{
  "schema": "2.0",
  "header": {
    "title": {"tag": "plain_text", "content": "📊 综合分析报告"},
    "subtitle": {"tag": "plain_text", "content": "2026年3月"},
    "template": "indigo"
  },
  "body": {
    "direction": "vertical",
    "padding": "12px",
    "elements": [
      {"tag": "markdown", "content": "## 第一部分：趋势分析"},
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "line",
          "data": {"values": [...]},
          "xField": "date",
          "yField": "value"
        },
        "preview": true,
        "color_theme": "brand",
        "height": "240px"
      },
      {"tag": "markdown", "content": "**洞察**：整体呈上升趋势"},
      {"tag": "hr"},
      {"tag": "markdown", "content": "## 第二部分：占比分析"},
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "pie",
          "data": {"values": [...]},
          "categoryField": "category",
          "valueField": "value"
        },
        "preview": true,
        "color_theme": "brand"
      },
      {"tag": "markdown", "content": "**洞察**：i6 占据主导地位"},
      {"tag": "hr"},
      {"tag": "markdown", "content": "## 第三部分：排名分析"},
      {"tag": "hr"},
      {
        "tag": "chart",
        "chart_spec": {
          "type": "bar",
          "direction": "horizontal",
          "data": {"values": [...]},
          "xField": "value",
          "yField": ["city"]
        },
        "preview": true,
        "color_theme": "brand",
        "height": "400px"
      },
      {"tag": "markdown", "content": "**洞察**：深圳领跑全国"},
      {"tag": "hr"},
      {"tag": "markdown", "content": "### 📌 总结\n\n综合以上三方面分析，数据表现良好..."}
    ]
  }
}
```

---

## 模板选择指南

| 数据特征 | 推荐模板 | 关键元素 |
|---------|---------|---------|
| 时间序列数据 | 模板 1（标准报告） | 折线图 + 表格 |
| 排名数据 | 模板 2（Top N） | 横向条形图 |
| 占比数据 | 模板 3（占比分析） | 饼图 + 表格 |
| 对比数据 | 模板 4（对比分析） | 分组柱状图 |
| 单一数值 | 模板 5（简洁摘要） | KPI 数值 |
| 复杂分析 | 模板 6（多图综合） | 多图 + 多表 |

---

## 模板使用注意事项

1. **数据格式**: 所有 data.values 必须是真实数据，不要用占位符
2. **数值精度**: 根据实际需要设置 format.precision
3. **颜色主题**: 根据内容选择合适的 template 颜色
4. **高度调整**: 数据量大时增加图表 height
5. **洞察内容**: 必须基于真实数据分析，不要空洞
