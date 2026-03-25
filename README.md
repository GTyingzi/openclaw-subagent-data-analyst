# openclaw-subagent-data-analyst

**数据分析助手** 是 [OpenClaw](https://github.com/openclaw) 生态中专注于数据查询与分析的 Subagent。它连接企业语义层（指标平台），帮助用户用自然语言完成从数据查询到可视化输出的全流程。

---

## 核心能力

| 能力 | 说明 | 技能 |
|------|------|------|
| 指标查询 | 语义层 API 查询，支持时间筛选、维度下钻、同环比/占比/排名 | `metric-query` |
| 归因分析 | 多维度归因诊断，识别贡献因子，生成结构化报告 | `metric-attribution` |
| 数据可视化 | 生成单文件可交互 HTML 仪表板（Chart.js，无需服务器） | `dip-vap-dashboard` |
| 飞书卡片集成 | 将分析结果封装为飞书消息卡片，支持 KPI 摘要、趋势图等 | `dip-vap-feishu-card` |

## 适用场景

- **日常数据查询** — "查一下本月各渠道的 GMV，按昨日对比上周同期"
- **指标异动归因** — "上周转化率下降了 5%，帮我分析一下原因"
- **报表仪表板生成** — "把近 30 天的销售数据做成可交互的仪表板"
- **飞书数据播报** — "生成一张本周核心指标的飞书卡片发给团队"
- **多维下钻分析** — "按品类和地区分析 Q1 的订单量分布"
- **同环比分析** — "对比今年和去年同期的客单价变化趋势"

---

## 安装

详见 [INSTALL.md](./INSTALL.md)，以下为快速流程：

### 前置条件

- OpenClaw 已运行
- 已获取 `CAN_API_KEY`（格式 `cgk-xxxxxxxx`，联系数据平台管理员）

### 1. 克隆仓库

```bash
cd $WORKSPACE/agents/
git clone <repo-url> data-analyst
```

### 2. 配置 API Key

```bash
mkdir -p ~/.openclaw
echo "CAN_API_KEY=cgk-your-api-key-here" >> ~/.openclaw/.env
```

### 3. 注册 Agent 并配置主 Agent

参见 [INSTALL.md](./INSTALL.md) Step 2，完成 OpenClaw 配置和主 Agent 的 TOOLS.md 更新。

### 4. 验证安装

```bash
openclaw status  # 确认 data-analyst 出现，且 default 标记在主 Agent
grep "CAN_API_KEY" ~/.openclaw/.env  # 确认 API Key 已配置
```

---

## 架构说明

```
用户
 └─ 飞书/webchat → 主 Agent
                     └─ sessions_send → data-analyst（本仓库）
                                           ├─ metric-query（curl → Gateway API）
                                           ├─ metric-attribution
                                           ├─ dip-vap-dashboard（生成 HTML）
                                           └─ dip-vap-feishu-card（发送飞书卡片）
```

**关键约束**：data-analyst 是子 Agent，不能设为 `default: true`，不能绑定飞书机器人，不能有独立的飞书 account 配置。违反任一条会导致消息重复响应。

---

## 目录结构

```
openclaw-subagent-data-analyst/
├── skills/
│   ├── metric-query/          # 指标查询技能
│   ├── metric-attribution/    # 归因分析技能
│   ├── dip-vap-dashboard/     # HTML 仪表板生成技能
│   └── dip-vap-feishu-card/   # 飞书卡片发送技能
├── version/                   # 版本发布记录
│   └── 0-1.md                 # v0.1 发布说明
├── IDENTITY.md                # 代理身份声明
├── SOUL.md                    # 价值观与回应风格
├── MEMORY.md                  # API 速查手册与查询铁律
├── TOOLS.md                   # 工具声明与使用规范
├── BOOTSTRAP.md               # 启动初始化规范
├── AGENTS.md                  # Claude Code 配置
├── INSTALL.md                 # 安装/升级向导
├── UNINSTALL.md               # 卸载向导
└── config.json                # 本地配置
```

---

## 版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| [v0.1](./version/0-1.md) | 2026-03-25 | 初始发布 |

---

## 配置依赖

| 技能 | 依赖 CAN_API_KEY | 依赖飞书配置 | 配置位置 |
|------|:---:|:---:|----------|
| metric-query | ✓ | — | `~/.openclaw/.env` |
| metric-attribution | ✓ | — | `~/.openclaw/.env` |
| dip-vap-feishu-card | — | ✓ | `~/.openclaw/openclaw.json` |
| dip-vap-dashboard | — | — | 无需配置 |

## 卸载

参见 [UNINSTALL.md](./UNINSTALL.md)。