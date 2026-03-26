# Memory — 数据分析助手（data-analyst）

本文件是 metric-query 和 metric-attribution 两个 skill 的常用 API 速查手册。

---

## Gateway API 端点速查

| 用途 | 方法 | 端点 |
|------|------|------|
| 搜索指标 | GET | `https://gateway.can.aloudata.com/api/metrics/search?keyword={词}&pageSize={n}` |
| 指标目录 | GET | `https://gateway.can.aloudata.com/api/metrics/categories` |
| 指标列表 | GET | `https://gateway.can.aloudata.com/api/metrics/list?pageNumber=1&pageSize=50` |
| 单指标维度 | GET | `https://gateway.can.aloudata.com/api/metrics/{metricName}/dimensions` |
| 批量指标维度 | GET | `https://gateway.can.aloudata.com/api/metrics/dimensions?metricNames={m1,m2}` |
| 执行查询 | POST | `https://gateway.can.aloudata.com/api/metrics/query` |

---

## curl 调用铁律

**铁律 1**：所有请求必须带认证头 `-H "X-API-Key: $CAN_API_KEY"`
> `CAN_API_KEY` 从仓库根目录 `config.json` 读取，格式 `{"CAN_API_KEY":"cgk-xxxxxxxx"}`
> 读取方式：`CAN_API_KEY=$(python3 -c "import json; print(json.load(open('../../config.json'))['CAN_API_KEY'])")`

**铁律 2**：URL 中文参数必须 URL 编码，使用 `--data-urlencode "keyword=客单价" -G`

**铁律 3**：POST 查询必须用 heredoc（因 timeConstraint 含单引号）：
```bash
curl -X POST "https://gateway.can.aloudata.com/api/metrics/query" \
  -H "X-API-Key: $CAN_API_KEY" -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"metrics": ["AOV"], "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"}
EOF
```

---

## timeConstraint 速查表

| 用户说 | timeConstraint |
|--------|----------------|
| 昨天 | `"['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"` |
| 上月 | `"DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"` |
| 本月 | `"DateTrunc(['metric_time'], \"MONTH\") = DateTrunc(NOW(), \"MONTH\")"` |
| 上季 | `"DateTrunc(['metric_time'], \"QUARTER\") = DATEADD(DateTrunc(NOW(), \"QUARTER\"), -1, \"QUARTER\")"` |
| 本年 | `"DateTrunc(['metric_time'], \"YEAR\") = DateTrunc(NOW(), \"YEAR\")"` |
| 近7天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -7, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近30天 | `"DateTrunc(['metric_time'], \"DAY\") >= DATEADD(DateTrunc(NOW(), \"DAY\"), -30, \"DAY\") AND ['metric_time__day'] < DateTrunc(NOW(), \"DAY\")"` |
| 近12个月 | `"DateTrunc(['metric_time'], \"MONTH\") >= DATEADD(DateTrunc(NOW(), \"MONTH\"), -12, \"MONTH\") AND DateTrunc(['metric_time'], \"MONTH\") < DateTrunc(NOW(), \"MONTH\")"` |

> ⚠️ 除用户指定具体日期外，一律使用 NOW()，禁止硬编码日期

---

## 九条铁律核心摘要

| # | 规则 | 常见违反 |
|---|------|---------|
| 1 | 相对时间必须用 `NOW()`，禁止硬编码日期 | 把昨天写成 `"2026-03-24"` |
| 2 | `metricDefinitions` 中每个 key（含辅助指标）都必须在 `metrics` 中注册 | 辅助指标 `total` 只在 expr 里用，没加进 metrics |
| 3 | 占比/排名 + `filters` = 分母/范围被缩小 → 用 `resultFilters` | filters 筛了渠道再算占比，恒 100% |
| 4 | "同比"默认=`yoy`；"环比"按粒度选 `dod/wow/mom/qoq` | 把月环比写成 yoy |
| 5 | 一个指标只能做一次快速计算，不可链式叠加 | `retail_amt__sameperiod__mom__growth__rank__desc__channel` |
| 6 | `MetricMatches` 只能在 `metricDefinitions.filters` 中 | 把 MetricMatches 放在顶层 filters |
| 7 | 日粒度限制的派生指标不可在月/季/年粒度 timeConstraint 下使用 | 用 `sales_yoy` 查上月数据 |
| 8 | 月趋势占比/排名的范围维度必须是 `metric_time__month` | 范围维度留空 |
| 9 | 上下文不足时返回 `{}`，禁止虚构指标或维度 | 猜测了不存在的指标名 |

---

## 同环比偏移粒度速查

| 用户说 | 偏移粒度 | 示例 |
|--------|---------|------|
| 同比 / 年同比 | `yoy` | `retail_amt__sameperiod__yoy__growth` |
| 月同比 | `mom` | `retail_amt__sameperiod__mom__growth` |
| 周同比 | `wow` | `retail_amt__sameperiod__wow__growth` |
| 季同比 | `qoq` | `retail_amt__sameperiod__qoq__growth` |
| 日环比 | `dod` | `retail_amt__sameperiod__dod__growth` |

**方法后缀**：`value`（对比期原值）、`growthvalue`（增量）、`growth`（增长率）

---

## 常用查询模板

### 上月按维度分组 + 环比
```json
{
    "metrics": ["retail_amt", "retail_amt__sameperiod__mom__growth"],
    "dimensions": ["first_channel"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"
}
```

### 全局占比（resultFilters 展示筛选，避免恒 100%）
```json
{
    "metrics": ["retail_amt", "retail_amt__proportion__"],
    "dimensions": ["first_channel"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "resultFilters": ["[first_channel]= \"Wholesale\""]
}
```

### 本年至今 + 年同比（period + indirections）
```json
{
    "metrics": ["ytd_val", "ytd_yoy_growth"],
    "metricDefinitions": {
        "ytd_val": {"refMetric": "retail_amt", "period": "grain_to_date 0 year of 0 day"},
        "ytd_yoy_growth": {"refMetric": "retail_amt", "period": "grain_to_date 0 year of 0 day", "indirections": ["sameperiod__yoy__growth"]}
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

### 日均（period + preAggs）
```json
{
    "metrics": ["daily_avg"],
    "metricDefinitions": {
        "daily_avg": {"refMetric": "retail_amt", "period": "to_date -29 day of 0 day", "preAggs": [{"granularity": "DAY", "calculateType": "AVG"}]}
    },
    "timeConstraint": "['metric_time__day']= DATEADD(DateTrunc(NOW(), \"DAY\"), -1, \"DAY\")"
}
```

### 环比增速 + 渠道内排名（多步拆分，铁律5）
```json
{
    "metrics": ["retail_amt", "mom_growth", "mom_growth__rankDense__desc__first_channel"],
    "metricDefinitions": {
        "mom_growth": {"refMetric": "retail_amt", "indirections": ["sameperiod__mom__growth"]}
    },
    "dimensions": ["first_channel", "product_brand_name"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")",
    "resultFilters": ["[mom_growth__rankDense__desc__first_channel] <= 3"]
}
```

---

## metric-attribution 归因诊断流程

```
Step 1 → 确认波动事实（总体变化量，避免基准选错）
Step 2 → 因子拆解（GMV = UV × 转化率 × 客单价，定性哪个环节出了问题）
Step 3 → 维度归因（针对主因子，定位问题集中在哪个渠道/地区/品牌）
Step 4 → 外部事件关联（节假日/竞对/天气/政策）
Step 5 → 综合结论（完整因果链 + 归因报告）
```

**归因贡献度**：`贡献度 = 维度值变化量 / |总变化量| × 100%`
- 🔴 ≥ 30%：主要贡献者，重点下钻
- 🟡 10%~30%：次要贡献者，可选下钻

**常用归因查询（上月环比）**：
```json
{
    "metrics": ["retail_amt", "retail_amt__sameperiod__mom__value", "retail_amt__sameperiod__mom__growthvalue", "retail_amt__sameperiod__mom__growth"],
    "timeConstraint": "DateTrunc(['metric_time'], \"MONTH\") = DATEADD(DateTrunc(NOW(), \"MONTH\"), -1, \"MONTH\")"
}
```

---

## period 常用语法速查

| 场景 | period 写法 |
|------|------------|
| 本年至今 | `grain_to_date 0 year of 0 day` |
| 本月至今 | `grain_to_date 0 month of 0 day` |
| 近30天 | `to_date -29 day of 0 day` |
| 近7天 | `to_date -6 day of 0 day` |
| 上月 | `relative_date -1 month of 0 day` |
| 上年同期至今 | `grain_to_date -1 year of -1 day` |
| 上年末 | `SPECIFY_DATE end day of -1 year` |

> `of 0 day` 表示锚定到昨天（需 timeConstraint 锚定到天粒度）
