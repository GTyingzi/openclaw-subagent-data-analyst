# Tools

本文件声明 **数据分析助手（data-analyst）** 可使用的所有工具及使用规范。

---

## Skill 工具

本 subagent 共有八个 skill，按使用场景分为数据查询类、分析类、报告类和输出类。

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

**触发时机**：用户查询指标数据、多维分析、同环比计算时

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

**触发时机**：用户询问指标为何上涨/下降、需要归因分析、排查异动原因时

**使用规范**
- 遵循"先因子拆解再维度归因"的诊断顺序
- 所有 API 调用规则与 metric-query 完全一致

---

### dip-vap-feishu-card
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/dip-vap-feishu-card/SKILL.md` |
| 依赖配置 | 飞书 appId/appSecret（从 `~/.openclaw/openclaw.json` 自动读取） |

**主要功能**
- **方式一（推荐，~90% 场景）**：直接输出 Markdown 文本，OpenClaw 自动渲染为飞书卡片
- **方式二（~10% 场景）**：通过脚本 `node skills/dip-vap-feishu-card/scripts/feishu-card.js` 发送含原生图表（折线/柱状/饼图）的自定义卡片 JSON

**触发时机**：用户需要发送飞书卡片、数据播报、在飞书中分享分析结果时

**使用规范**
- 优先使用方式一（直接回复 Markdown），只在需要原生图表时才用方式二
- 使用脚本（方式二）发送卡片后，**不再输出任何文字**，避免消息重复
- `receive_id` 格式：`ou_xxx`（私聊用户 open_id）或 `oc_xxx`（群聊 chat_id）

---

### dip-vap-dashboard
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/dip-vap-dashboard/SKILL.md` |
| 依赖配置 | 无（生成独立 HTML 文件，浏览器直接打开） |

**主要功能**
- 生成单文件可交互 HTML 仪表板，引入 Chart.js，无需服务器
- 支持折线图/柱状图/环形图、下拉过滤器、数据表格
- 文件保存到 `/tmp/dashboard-{主题}-{YYYYMMDD}.html`

**触发时机**：用户要求生成仪表板/可视化报告/HTML 看板、或查询结果超过 20 行且包含时间序列/多维度数据时

**使用规范**
- 单文件 HTML，UTF-8 编码，CDN 引入 Chart.js（`https://cdn.jsdelivr.net/npm/chart.js@4.5.1`）
- 生成完成后必须告知用户完整文件路径

---

### anomaly-detection
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/anomaly-detection/SKILL.md` |
| 数据来源 | 委派 `metric-query` 执行，不直接调用 Gateway API |

**主要功能**
- 对指标当前值与历史基线进行比较，判断是否存在异常波动
- 支持单指标检测和批量健康巡检（多指标异常扫描）
- 输出结构化异常检测报告（正常/异常/风险，附置信说明）

**触发时机**：用户询问指标是否正常/异常、做健康巡检或异常扫描、检查数据有没有问题时

**使用规范**
- 数据查询必须通过 `metric-query` Skill 完成，不直接调用 Gateway API
- 检测到异常时，可建议用户使用 `metric-attribution` 做进一步归因

---

### forecast-simulation
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/forecast-simulation/SKILL.md` |
| 数据来源 | 委派 `metric-query` 获取历史数据，本地做数学推算 |

**主要功能**
- 趋势预测：基于历史数据拟合，外推未来走势
- 目标缺口分析：计算当前进度与目标的差距，推算日均需要多少
- What-if 模拟：模拟某个条件改变后对指标的影响
- 耗尽/饱和预测：预测库存耗尽时间、容量饱和时间等

**触发时机**：用户询问未来走势、目标是否可达、或模拟假设场景（"月底能到多少""提升10%会怎样""还差多少"）时

**使用规范**
- 本 Skill 为数学推算（趋势拟合、公式模拟），**非机器学习预测模型**
- 所有推算结果必须附带前提假设和不确定性说明

---

### analysis-report
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/analysis-report/SKILL.md` |
| 数据来源 | 编排层，所有分析委派能力层 Skill 执行 |

**主要功能**
- 按报告模板（月报/周报/专项分析等）确定所需板块
- 依次调度 `metric-query`、`anomaly-detection`、`metric-attribution`、`forecast-simulation` 执行各板块分析
- 将各板块结果串联为连贯的分析叙事，输出完整文档

**触发时机**：用户需要一份完整的、多板块分析文档时（"出月报""做分析报告""数据复盘""经营简报"等）

**使用规范**
- 本 Skill 是**一次性执行**（现在就出一份报告）；若用户含"以后/每月/定期"等重复意图，转 `scheduled-report`
- 不包含分析逻辑，所有数据查询和分析工作委派给能力层 Skill

---

### scheduled-report
| 属性 | 值 |
|------|----|
| 文件位置 | `skills/scheduled-report/SKILL.md` |
| 依赖配置 | OpenClaw cron 调度器（`openclaw cron add`） |

**主要功能**
- 从当前对话中提取已完成的分析步骤（录制）
- 将分析步骤打包为自包含、可独立执行的 prompt（打包）
- 通过 `openclaw cron add` 创建定时任务，按指定频率自动重放（调度）

**触发时机**：用户表达中含"定时/定期/每X/以后都"等重复执行意图时（如"每周都跑一次""以后每月出月报"）

**使用规范**
- **前提条件**：对话中必须有已完成的分析历史；若无，应先引导用户完成一轮分析再触发本 Skill
- 本 Skill 不定义"怎么分析"，只负责"把你刚才做的分析录下来，变成能定时重放的任务"

---

## Bash / curl 工具

metric-query 和 metric-attribution 两个 skill 均通过 **curl** 调用 Gateway API，以下为统一规范。

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

| Skill | 依赖 CAN_API_KEY | 依赖飞书配置 | 配置位置 |
|-------|:---:|:---:|----------|
| metric-query（curl） | ✓ | — | `~/.openclaw/.env` |
| metric-attribution（curl） | ✓ | — | `~/.openclaw/.env` |
| anomaly-detection | — | — | 委派 metric-query，无直接依赖 |
| forecast-simulation | — | — | 委派 metric-query，无直接依赖 |
| analysis-report | — | — | 委派能力层 Skill，无直接依赖 |
| scheduled-report | — | — | 依赖 OpenClaw cron 调度器 |
| dip-vap-feishu-card | — | ✓ | `~/.openclaw/openclaw.json` |
| dip-vap-dashboard | — | — | 无需配置 |

> 若 `CAN_API_KEY` 未配置或无效，所有数据查询功能将返回 401 未授权错误。
> 飞书卡片发送依赖 OpenClaw 的飞书 account 配置，使用方式一（Markdown 回复）无需额外配置。
