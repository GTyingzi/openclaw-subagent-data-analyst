# UNINSTALL.md - 数据分析助手（data-analyst）卸载指南

> **本文档面向 AI Agent 阅读。** 收到用户卸载指令后，按以下步骤执行。
> 目标：将 OpenClaw 恢复到安装数据分析助手**之前**的状态，不影响其他 Agent 和配置。

## 卸载原则

- **只动 data-analyst 相关配置**，不触碰主 Agent 的其他配置
- **不删除主 Agent 中与其他子 Agent 相关的配置**
- 主 Agent 的 TOOLS.md 和 AGENTS.md 中**只删除 data-analyst 相关段落**，保留其余内容
- `agentToAgent.allow` 中只移除 `"data-analyst"`，若还有其他 Agent 则保留列表
- 如果 `agentToAgent` 和 `sessions.visibility` 在安装前就存在且被其他 Agent 依赖，**不要删除**，只移除 data-analyst 相关部分

---

## Step 0: 确认当前状态

### 0a. 确定路径

```bash
WORKSPACE=$(pwd)  # 或从 openclaw status 获取
AGENT_DIR="$WORKSPACE/agents/data-analyst"
echo "AGENT_DIR=$AGENT_DIR"
```

### 0b. 检测已安装内容

```bash
# 检测 1：代码目录是否存在
test -d "$AGENT_DIR/.git" && echo "CODE_EXISTS=true" || echo "CODE_EXISTS=false"

# 检测 2：Agent 是否已注册
openclaw status 2>/dev/null | grep -q "data-analyst" && echo "AGENT_REGISTERED=true" || echo "AGENT_REGISTERED=false"
```

然后用 `gateway config.get` 读取当前完整配置，逐项检查：

| 检查项 | 怎么查 | 需要清理的状态 |
|--------|--------|----------------|
| data-analyst 是否在 agents.list | `agents.list` 中有无 `"id": "data-analyst"` | 有 → 需要删除 |
| data-analyst 是否有 binding | `bindings` 中有无 `agentId: "data-analyst"` | 有 → 需要删除 |
| data-analyst 是否有飞书 account | `channels.feishu.accounts` 中有无 `"data-analyst"` 键 | 有 → 需要删除 |
| 主 Agent allowAgents 含 data-analyst | 主 Agent 的 `subagents.allowAgents` | 含 → 需要移除该项 |
| agentToAgent allow 含 data-analyst | `tools.agentToAgent.allow` | 含 → 需要移除该项 |
| 主 Agent TOOLS.md 含 data-analyst 段 | 读主 Agent workspace 的 TOOLS.md | 含 → 需要删除该段 |
| 主 Agent AGENTS.md 含 data-analyst 内容 | 读主 Agent workspace 的 AGENTS.md | 含 → 需要清理相关内容 |

---

## Step 1: 清理 OpenClaw 配置

> 所有配置变更**合并为一次 `config.apply`**，减少重启次数。

### 流程

1. `gateway config.get` 获取完整配置
2. 在内存中完成以下所有修改
3. 一次性 `gateway config.apply` 写回

### 1a. 从 agents.list 移除 data-analyst

在 `agents.list` 中找到 `"id": "data-analyst"` 的条目，**整个对象删除**。

保留列表中所有其他 Agent 的完整配置不变。

### 1b. 从 bindings 移除 data-analyst（如有）

在 `bindings` 数组中删除所有 `agentId: "data-analyst"` 的条目。保留其他 binding 不动。

### 1c. 从 feishu accounts 移除 data-analyst（如有）

在 `channels.feishu.accounts` 中删除 `"data-analyst"` 键及其整个对象。保留其他 account 不动。

### 1d. 从主 Agent 的 allowAgents 移除 data-analyst

在主 Agent 的 `subagents.allowAgents` 数组中，移除 `"data-analyst"` 这一项。

- 如果移除后数组为空，可以删除 `allowAgents` 字段
- 如果还有其他 Agent（如 `"sentiment"`），保留它们

### 1e. 从 agentToAgent.allow 移除 data-analyst

在 `tools.agentToAgent.allow` 数组中移除 `"data-analyst"`。

- 如果移除后 allow 列表只剩主 Agent 自己，且没有其他子 Agent 依赖此配置，可以将 `agentToAgent.enabled` 设为 `false`
- 如果还有其他子 Agent 依赖此配置，保留 `enabled: true`，只移除 `"data-analyst"`

### 1f. sessions.visibility（谨慎处理）

`tools.sessions.visibility` 如果在安装前就存在（或有其他子 Agent 依赖），**不要修改**。

如果确认是安装本 subagent 时新增的，且没有其他 Agent 依赖，可以删除该字段。

---

## Step 2: 清理主 Agent 的 workspace 文件

> 原则：只删除 data-analyst 相关段落，保留文件中其他所有内容。

### 2a. 清理主 Agent 的 TOOLS.md

读取主 Agent workspace 的 TOOLS.md，找到并删除以下整个段落（从 `## 📊 数据分析助手（data-analyst）` 开始到该章节末尾）：

```
## 📊 数据分析助手（data-analyst）
...（整个章节内容）...
```

保留文件中其他所有章节不动。

> 如果文件中没有该段落，跳过此步。

### 2b. 清理主 Agent 的 AGENTS.md

读取主 Agent workspace 的 AGENTS.md，检查并清理 data-analyst 相关内容：

**需要删除的内容：**
- 「转发原则」中 `识别到数据/指标类问题 → 转发给数据分析助手` 这一行
- 「子 Agent 调度」章节中关于数据分析助手的转发规则（如整个章节都是为本 subagent 新增的，可整节删除）

**不要删除的内容：**
- 「每次会话」章节（通用配置）
- 「记忆」章节（通用配置）
- 其他子 Agent 的调度规则

---

## Step 3: 删除代码目录（可选）

> ⚠️ 此操作**不可逆**，删除前请确认不再需要代码。

```bash
# 确认路径再删除
echo "即将删除: $AGENT_DIR"
rm -rf "$AGENT_DIR"
```

如果用户只是想停用而保留代码（方便日后重装），可以跳过此步，只执行 Step 1-2。

---

## Step 4: 使配置生效

### 热加载（推荐）

Step 1 的配置变更通过 `config.apply` 写入时**已自动生效**。

Step 2 的 workspace 文件变更需要让主 Agent 重新读取：

```
# 通过飞书或 webchat 发消息给主 Agent：
"你的 TOOLS.md 和 AGENTS.md 已更新，已移除数据分析助手（data-analyst）相关配置。请用 read 工具重新阅读这两个文件确认。"
```

### 重启（备选）

```bash
openclaw gateway restart
```

---

## Step 5: 验证卸载完成

```bash
openclaw status
```

验证要点（**必须全部通过**）：

- [ ] `openclaw status` 不显示 data-analyst
- [ ] `gateway config.get` 的 `agents.list` 中无 `"id": "data-analyst"` 条目
- [ ] `bindings` 数组中无 `agentId: "data-analyst"` 条目
- [ ] `channels.feishu.accounts` 中无 `"data-analyst"` 键
- [ ] 主 Agent 的 TOOLS.md 不含 `## 📊 数据分析助手（data-analyst）` 章节
- [ ] 主 Agent 的 `subagents.allowAgents` 不含 `"data-analyst"`

> 如果任一项未通过，回到 Step 1 或 Step 2 补充清理。

---

## 常见问题

| 问题 | 解决 |
|------|------|
| 卸载后主 Agent 仍尝试转发给 data-analyst | TOOLS.md 或 AGENTS.md 中仍有旧内容，重新执行 Step 2 |
| 卸载后其他子 Agent 也失效 | 检查是否误删了 `agentToAgent` 配置，恢复 `enabled: true` 和 allow 列表 |
| 想保留数据只停用 Agent | 只执行 Step 1（不删除代码），将来重装只需重新执行 Step 2 注册 |
| 想完全重装 | 先按本文档完整卸载，再按 INSTALL.md 重新安装 |
