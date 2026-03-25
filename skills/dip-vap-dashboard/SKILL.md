---
name: dip-vap-dashboard
description: 生成可交互的 HTML 数据仪表板。当数据量较大（>20行）、包含时间序列/多维度数据、或用户明确要求可视化时使用此 skill。生成的 HTML 文件无需服务器即可在浏览器中直接打开。
version: 2.0.0
tags: [仪表板, HTML, Chart.js, 可视化, 交互]
---

# HTML 仪表板生成 Skill

## 触发条件

满足以下任一条件时使用此 skill：

| 条件 | 示例 |
|------|------|
| 查询结果超过 20 行 | 按天查近30天的数据 |
| 包含时间序列 + 多维度 | 各渠道月度趋势 |
| 用户明确要求 | "生成仪表板"、"做个可视化报告"、"给我个图表" |

---

## 文件路径约定

生成的 HTML 文件保存到：

```
/tmp/dashboard-{主题}-{YYYYMMDD}.html
```

示例：`/tmp/dashboard-sales-20260325.html`

生成后必须告知用户完整路径：
```
✅ 仪表板已生成：/tmp/dashboard-sales-20260325.html
在浏览器中直接打开即可查看。
```

---

## 生成规范

### 必须满足

1. **独立可运行**：单个 HTML 文件，无需服务器，浏览器直接打开
2. **CDN 引入 Chart.js**：`https://cdn.jsdelivr.net/npm/chart.js@4.5.1`
3. **UTF-8 编码**：`<meta charset="UTF-8">`
4. **中文标题和标签**：与查询主题一致

### 推荐结构

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{查询主题} 数据仪表板</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1"></script>
  <style>
    /* 专业样式：深色/浅色主题，响应式布局 */
    body { font-family: -apple-system, sans-serif; margin: 0; padding: 20px; background: #f5f7fa; }
    .dashboard { max-width: 1200px; margin: 0 auto; }
    .kpi-row { display: flex; gap: 16px; margin-bottom: 24px; }
    .kpi-card { background: white; border-radius: 8px; padding: 20px; flex: 1; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
    .chart-container { background: white; border-radius: 8px; padding: 20px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  </style>
</head>
<body>
  <div class="dashboard">
    <h1>{标题}</h1>

    <!-- KPI 卡片区 -->
    <div class="kpi-row">
      <div class="kpi-card">
        <div class="label">总量</div>
        <div class="value">{值}</div>
        <div class="change">{变化率}</div>
      </div>
    </div>

    <!-- 图表区 -->
    <div class="chart-container">
      <canvas id="mainChart"></canvas>
    </div>

    <!-- 下拉过滤器（如有多维度） -->
    <select id="filter" onchange="updateChart()">
      <option value="all">全部</option>
    </select>

    <!-- 数据表格 -->
    <table id="dataTable">...</table>
  </div>

  <script>
    // 数据
    const data = { /* 查询结果 */ };

    // 图表
    const ctx = document.getElementById('mainChart').getContext('2d');
    new Chart(ctx, { type: 'line', data: {...}, options: {...} });

    // 过滤器
    function updateChart() { /* 根据选择更新图表 */ }
  </script>
</body>
</html>
```

### 图表类型选择

| 数据特征 | 推荐图表 |
|---------|---------|
| 时间趋势 | `line`（折线图） |
| 分类对比 | `bar`（柱状图） |
| 占比构成 | `doughnut`（环形图） |
| 多维度对比 | 分组 `bar` |

### 交互功能

- **下拉过滤器**：当有多个维度值时，添加下拉过滤（如渠道、地区）
- **数据表格**：在图表下方附带完整数据表格，支持点击排序

---

## 使用模板

项目提供基础模板：
```bash
cp skills/dip-vap-dashboard/assets/templates/base-dashboard.html /tmp/my-dashboard.html
```

在 `// DATA HERE` 位置替换为查询结果数据。

---

## 常见问题

| 问题 | 解决方法 |
|------|---------|
| 控制台报 `Chart is not defined` | 确认 `<head>` 中已引入 Chart.js CDN |
| 中文显示乱码 | 添加 `<meta charset="UTF-8">` |
| 图表不显示 | 检查数据格式（`labels` 和 `data` 长度必须一致） |
| 柱状图 xField 报错 | 分组柱状图的 xField 应为数组 `["category"]` |
