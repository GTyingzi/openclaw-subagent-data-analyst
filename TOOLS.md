# Tools

本文件声明 **数据分析助手（data-analyst）** 可使用的所有工具及使用规范。

---

## Skill 工具

本 subagent 的数据获取能力由以下两个 skill 提供，均通过 **curl + Gateway API** 实现，不依赖 MCP 工具。

### metric-query
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/metric-query/skill.md` |
| 数据来源 | `https://gateway.can.aloudata.com/api/` |
| 依赖配置 | `CAN_API_KEY`（从 `~/.openclaw/.env` 读取） |

**主要功能**
- 通过 Gateway 搜索接口检索指标名称、维度信息
- 构建语义层查询请求体，调用 `POST /api/metrics/query` 获取指标数据
- 支持时间限定、维度分组、同环比/占比/排名等快速衍生计算

**使用规范**
- 查询前先用 Gateway 搜索接口确认指标编码，禁止猜测指标名称
- 相对时间（昨天、上月、近N天等）必须用 `NOW()` 表达，禁止硬编码日期

---

### metric-attribution
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/metric-attribution/skill.md` |
| 数据来源 | `https://gateway.can.aloudata.com/api/`（复用 metric-query 的 Gateway API 体系） |
| 依赖配置 | `CAN_API_KEY`（从 `~/.openclaw/.env` 读取） |

**主要功能**
- 对指标波动进行综合归因诊断（确认波动事实 → 因子拆解 → 维度归因 → 外部事件关联 → 综合结论）
- 识别导致指标变化的关键因子、维度和外部事件
- 输出结构化归因报告

**使用规范**
- 遵循"先因子拆解再维度归因"的诊断顺序
- 所有 API 调用规则与 metric-query 完全一致

---

## Bash / curl 工具

两个 skill 均通过 **curl** 调用 Gateway API，以下为统一规范。

### Gateway API
| 属性 | 值 |
|------|----|
| 工具 | `curl`（通过 Bash 工具执行） |
| 基础地址 | `https://gateway.can.aloudata.com/api/` |
| 依赖配置 | `CAN_API_KEY`（从 `~/.openclaw/.env` 读取） |

**主要接口**
- 搜索指标：`GET /api/metrics/search?keyword=...`
- 单指标维度：`GET /api/metrics/{metricName}/dimensions`
- 批量指标维度：`GET /api/metrics/dimensions?metricNames=...`
- 指标列表：`GET /api/metrics/list`
- 指标目录：`GET /api/metrics/categories`
- 执行查询：`POST /api/metrics/query`

**鉴权规范（两条铁律）**
1. **所有请求必须携带 API Key 头**：`-H "X-API-Key: $CAN_API_KEY"`，从环境变量读取，不得硬编码
2. **URL 中文参数必须 URL 编码**：使用 `--data-urlencode` + `-G`，禁止中文字符直接拼入 URL

```bash
# 示例：搜索中文关键词
curl -H "X-API-Key: $CAN_API_KEY" \
  "https://gateway.can.aloudata.com/api/metrics/search?pageSize=5" \
  --data-urlencode "keyword=客单价" -G
```

---

## 配置依赖汇总

| 工具 | 依赖 CAN_API_KEY | 配置位置 |
|------|:---:|----------|
| metric-query skill（curl） | ✓ | `~/.openclaw/.env` |
| metric-attribution skill（curl） | ✓ | `~/.openclaw/.env` |

> 若 `CAN_API_KEY` 未配置或无效，所有数据查询功能将返回 401 未授权错误。
