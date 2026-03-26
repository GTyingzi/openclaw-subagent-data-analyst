# INSTALL.md - 数据分析助手（data-analyst）安装指南

> **本文档面向 AI Agent 阅读。** 收到用户安装/升级指令后，按以下步骤执行。
> 本文档同时覆盖**首次安装**和**升级（含修复历史错误配置）**，你需要在 Step 0 自动判断场景。

> ⚠️ **核心原则：data-analyst 是子 Agent，不是主 Agent！**
> - data-analyst **不能**设为 `default: true`
> - data-analyst **不能**配 binding（不绑定飞书机器人）
> - data-analyst **不能**在 `channels.feishu.accounts` 中有自己的飞书 account 配置
> - 飞书机器人只绑定主 Agent（如 `main`），由主 Agent 通过 `sessions_send` 转发数据查询给 data-analyst
> - 违反以上任一条 → 消息同时到两个 Agent → 重复 session + 重复回复

## 前置条件

- OpenClaw 已运行
- Git 已安装（`git --version` 可正常运行）
- 已获取 **CAN_API_KEY**（格式为 `cgk-xxxxxxxx`，如未获取请联系数据平台管理员）

## Step 0: 判断场景（新装 vs 升级）

### 0a. 确定 Workspace 路径

> **关键**：不同环境的 OpenClaw workspace 路径不同，**不要硬编码**。

通过以下方式获取（按优先级）：
1. 你的当前工作目录（pwd）
2. `openclaw status` 的 workspace 字段
3. openclaw.json 中 `agents.defaults.workspace`

```bash
WORKSPACE=$(pwd)  # 或从上述方式获取
AGENT_DIR="$WORKSPACE/agents/data-analyst"
```

### 0b. 自动检测安装状态

```bash
# 检测 1：代码是否已存在
test -d "$AGENT_DIR/.git" && echo "CODE_EXISTS=true" || echo "CODE_EXISTS=false"

# 检测 2：Agent 是否已注册
openclaw status 2>/dev/null | grep -q "data-analyst" && echo "AGENT_REGISTERED=true" || echo "AGENT_REGISTERED=false"
```

然后用 `gateway config.get` 读取当前完整配置，检查以下项目：

| 检查项 | 怎么查 | 正常值 | 异常值（需修复） |
|--------|--------|--------|-----------------|
| data-analyst 是否 default | `agents.list` 中 data-analyst 对象有无 `"default": true` | 无此字段或 `false` | `"default": true` |
| data-analyst 是否有 binding | `bindings` 数组中有无 `agentId: "data-analyst"` 的条目 | 无 | 有（需删除） |
| data-analyst 是否有飞书 account | `channels.feishu.accounts` 中有无 `"data-analyst"` 键 | 无 | 有（需删除） |
| 主 Agent 是否 default | `agents.list` 中主 Agent 有 `"default": true` | 是 | 否（需设为 true） |
| agentToAgent 是否开启 | `tools.agentToAgent.enabled` | `true` | `false` 或不存在 |
| sessions.visibility | `tools.sessions.visibility` | `"all"` | 其他值或不存在 |
| 主 Agent allowAgents 含 data-analyst | 主 Agent 的 `subagents.allowAgents` | 包含 `"data-analyst"` | 不包含 |
| 主 Agent TOOLS.md 含 sessions_send 规范 | 读主 Agent workspace 的 TOOLS.md | 包含 `sessions_send` 调用规范 | 不包含 |

### 0c. 场景判定

| CODE_EXISTS | AGENT_REGISTERED | 场景 | 操作 |
|-------------|-----------------|------|------|
| false | false | **首次安装** | 执行全部 Step 1-4 |
| true | false | **代码已有但未注册** | 跳过 clone，执行 Step 1（pull）→ Step 2-4 |
| true | true | **升级/修复** | 执行 Step 1（pull）→ Step 2（含修复）→ Step 3-4 |

> **升级场景的关键**：Step 2 中会自动修复 0b 检测到的所有异常配置。修复时**只动 data-analyst 相关配置**，不触碰主 Agent 的其他 skill、model、identity、其他子 Agent 等任何已有配置。

## Step 1: 获取代码

```bash
mkdir -p "$WORKSPACE/agents"
cd "$WORKSPACE/agents/"

# 首次安装：clone（替换为实际仓库地址）
if [ ! -d "data-analyst" ]; then
  git clone https://github.com/your-org/openclaw-subagent-data-analyst.git data-analyst
fi

# 所有场景：拉取最新版本
cd data-analyst
git fetch origin
git checkout main
git pull origin main
```

> 仓库已包含完整的 skills/ 目录，无需额外复制。

## Step 2: 配置 OpenClaw

> 本步骤**同时处理首次安装和升级修复**。先用 `gateway config.get` 获取当前配置，按 Step 0b 的检查项逐一处理，最后**一次性 `config.patch`**，减少重启次数。
>
> **原则：只动 data-analyst 相关配置，不碰用户的其他配置。**

### 2a. 配置 CAN_API_KEY

`CAN_API_KEY` 存储在 data-analyst 仓库根目录的 `config.json` 中，读取方式：

```bash
CAN_API_KEY=$(cat "$AGENT_DIR/config.json" | python3 -c "import sys,json; print(json.load(sys.stdin)['CAN_API_KEY'])")
```

如果 `config.json` 中的值仍为占位符（`cgk-your-api-key-here`），需要先填入真实 Key：

```bash
# 查看当前值
cat "$AGENT_DIR/config.json"

# 修改为真实 Key（替换 cgk-your-api-key-here）
python3 -c "
import json, sys
path = '$AGENT_DIR/config.json'
cfg = json.load(open(path))
cfg['CAN_API_KEY'] = 'cgk-your-real-key-here'
json.dump(cfg, open(path,'w'), indent=2)
print('已更新 config.json')
"
```

验证：
```bash
python3 -c "import json; cfg=json.load(open('$AGENT_DIR/config.json')); print(cfg.get('CAN_API_KEY','未配置'))"
# 应输出：cgk-xxxxxx
```

> ⚠️ **必须执行**：`CAN_API_KEY` 未配置时，指标查询功能将返回 401 错误。

### 2b. 修复异常配置（升级场景，有异常才执行）

根据 Step 0b 检测结果，构造修复 patch。以下是每种异常的修复方式：

#### 异常 1：data-analyst 被设为 `default: true`

在 `agents.list` 中找到 data-analyst 对象，移除 `"default": true`。
同时确认主 Agent 有 `"default": true`（如果主 Agent 也没有，给主 Agent 加上）。

> 需要 config.get 拿到完整 agents.list，修改 data-analyst 条目后用 config.apply 写回。
> **写回时保留 agents.list 中所有其他 Agent 的完整配置不变。**

#### 异常 2：data-analyst 有 binding

在 `bindings` 数组中删除所有 `agentId: "data-analyst"` 的条目。保留其他 binding 不动。

#### 异常 3：data-analyst 有飞书 account 配置

在 `channels.feishu.accounts` 中删除 `"data-analyst"` 键及其整个对象。保留其他 account 不动。

#### 多个异常同时存在

**合并为一次 config.apply**：
1. `gateway config.get` 获取完整配置
2. 在内存中修复所有异常
3. 同时应用 2c 的新增配置
4. 一次性 `gateway config.apply` 写回

### 2c. 注册/更新 data-analyst Agent 配置

**如果 2b 需要 config.apply（有异常要修复）**，把以下配置合并到 config.apply 的完整配置中。

**如果 2b 无异常（首次安装或配置已正确）**，用 `config.patch` 追加：

```json
{
  "agents": {
    "list": [
      {
        "id": "data-analyst",
        "name": "数据分析助手",
        "workspace": "<AGENT_DIR 的绝对路径>",
        "identity": {
          "name": "数据分析助手",
          "emoji": "📊"
        },
        "tools": {
          "allow": ["read", "write", "edit", "exec", "memory_search", "memory_get", "message"]
        }
      }
    ]
  },
  "tools": {
    "agentToAgent": {
      "enabled": true,
      "allow": ["<主Agent的id>", "data-analyst"]
    },
    "sessions": {
      "visibility": "all"
    }
  }
}
```

> ⚠️ **注意**：
> - `workspace` 必须填**绝对路径**（如 `/home/user/.openclaw/workspace/agents/data-analyst`），不要用 `~` 或变量
> - **不要**加 `"default": true`
> - **不要**添加 binding
> - **不要**添加飞书 account
> - **不要写死 model**（不设 `model.primary`），让子 Agent 继承 `agents.defaults` 的默认模型
> - `agentToAgent.allow` 必须同时包含主 Agent id 和 `"data-analyst"`（如果已有其他子 Agent，也要保留）
> - 如果主 Agent id 不是 `"main"`，用 `openclaw status` 确认后替换

### 2d. 主 Agent 的 subagents.allowAgents

确认主 Agent 配置中包含 data-analyst：

```json
{
  "agents": {
    "list": [
      {
        "id": "<主Agent的id>",
        "subagents": {
          "allowAgents": ["data-analyst"]
        }
      }
    ]
  }
}
```

> 如果主 Agent 已有 `allowAgents`（如 `["sentiment"]`），追加 `"data-analyst"` 即可，不要覆盖已有的。

### 2e. 配置超时

```json
{
  "agents": {
    "defaults": {
      "subagents": {
        "runTimeoutSeconds": 600,
        "announceTimeoutMs": 120000
      },
      "timeoutSeconds": 600
    }
  }
}
```

### 2f. 更新主 Agent 的 TOOLS.md（最重要！）

读取主 Agent workspace 的 TOOLS.md。

**升级场景**：如果 TOOLS.md 中已有 data-analyst 相关内容，**整段替换**为下面的新版内容。
**首次安装**：在 TOOLS.md 末尾**追加**以下内容。

> **不要动 TOOLS.md 中其他内容**（如用户自定义的其他子 Agent 规范）。只替换/追加 data-analyst 这一段。

````markdown
## 📊 数据分析助手（data-analyst）

数据分析助手，负责业务指标查询、趋势分析、归因分析、仪表板生成、飞书卡片图表。

**何时转发**：用户问到 GMV、订单量、转化率、客单价、留存率、归因分析等业务数据时。

**调用方式**：

用 `sessions_send` 发送到 data-analyst 的隔离 session。**session key 根据当前会话来源构造**，确保每个群/用户各自独立：

- 群聊来源 → `sessions_send(sessionKey="agent:data-analyst:proxy:<当前群的chatId>", ...)`
- 私聊来源 → `sessions_send(sessionKey="agent:data-analyst:proxy:<用户的openId>", ...)`
- webchat/其他 → `sessions_send(sessionKey="agent:data-analyst:proxy:default", ...)`

**chatId 和 openId 从当前消息的 inbound context 中提取**（GroupSubject 或 SenderId）。

完整调用：
```
sessions_send(sessionKey="agent:data-analyst:proxy:<来源标识>", message="[用户: 张三, chat: oc_abc123, type: group] 查一下昨天的 GMV", timeoutSeconds=300)
```

- session 不存在时会**自动创建**，无需预建
- 同一来源的后续追问自动复用同一个 session，**上下文连续**
- 不同群/用户各自隔离，**互不干扰、不排队**

**消息格式**：必须在消息开头带上用户信息前缀：
- `用户`: 真实姓名（从 SenderName 获取）
- `chat`: 当前会话的 chatId 或 openId
- `type`: `group` 或 `p2p`

格式：`[用户: 张三, chat: oc_abc123, type: group] 实际问题`

> chat 和 type 用于数据分析助手直接向飞书发送图表卡片。如果拿不到这些信息，只填用户名也行（`[用户: 张三] 问题`），会降级为纯文字回复。

**处理返回结果**：
- `reply` 有完整内容且不含"卡片已发送" → **直接转发给用户**，不要修改或追问
- `reply` 含"卡片已发送"或"图表已发送" → 告知用户"结果已通过飞书卡片发送"
- `reply` 是 `"NO_REPLY"` 或空 → 告知用户"结果已通过飞书卡片发送"
- `status` 是 `"timeout"` → 告知用户查询超时，建议重试
- **不要**因 reply 不满意就反复追问（浪费 token + ping-pong）

**ping-pong 处理**：收到来自 data-analyst 的 `inter_session` 消息 → 直接回复 `REPLY_SKIP` 终止循环。
````

> **关键**：这段内容必须**完整**写入。主 Agent 每次新 session 读取 TOOLS.md 来学习怎么调用子 Agent，缺少就不知道怎么转发。

### 2g. 更新主 Agent 的 AGENTS.md

读取主 Agent workspace 的 AGENTS.md，确保包含以下内容。**不要覆盖用户已有的其他配置**，只追加或合并缺失的部分。

```markdown
## 每次会话

1. 读 `TOOLS.md` — 子 Agent 调用规范
2. 读 `memory/YYYY-MM-DD.md`（今天+昨天）— 近期上下文

## 记忆

- 日志：`memory/YYYY-MM-DD.md`（每天一个文件）
- 长期：`MEMORY.md`（重要决策和经验）
- 想记住的东西写文件，不要"心里记着"

## 子 Agent 调度

当用户提问涉及特定领域时，转发给对应子 Agent 处理。调用规范见 `TOOLS.md`。

**转发原则：**
- 识别到数据/指标类问题 → 转发给数据分析助手
- 其他问题自己回答

**转发后：**
- `reply` 有完整内容且不含"卡片已发送" → 直接转发给用户
- `reply` 含"卡片已发送"或"图表已发送" → 告知用户"结果已通过飞书卡片发送"
- `reply` 为空或 NO_REPLY → 告知用户"结果已通过飞书卡片发送"
- `status` 为 timeout → 告知用户查询超时
- 收到 `inter_session` 回复 → 回复 `REPLY_SKIP` 终止循环
```

### 2h. 使配置生效

优先**热加载**，避免重启中断正在进行的对话。

#### 热加载（推荐）

Step 2b-2e 的配置变更通过 `config.patch` 或 `config.apply` 写入时**已自动生效**。

Step 2f-2g 的 workspace 文件变更需要让主 Agent 重新读取：

```
# 通过飞书或 webchat 发消息给主 Agent：
"你的 TOOLS.md 和 AGENTS.md 已更新，包含数据分析助手（data-analyst）子 Agent 的调用规范。请用 read 工具重新阅读这两个文件，确认你了解：1) sessions_send 调用方式 2) 消息格式含 chat/type 字段 3) 子 Agent 调度规则。"
```

#### 重启（备选，最可靠但会中断对话）

```bash
openclaw gateway restart
```

## Step 3: 验证

```bash
# 检查 skills 目录
ls "$AGENT_DIR/skills/"

# 检查 API Key 配置
python3 -c "
import json
cfg = json.load(open('$AGENT_DIR/config.json'))
key = cfg.get('CAN_API_KEY','')
print('✅ API Key 配置正常' if key.startswith('cgk-') else '❌ API Key 未配置或格式错误')
"

# 检查 agent 注册
openclaw status
```

验证要点（**必须全部通过**）：

- [ ] `openclaw status` 显示 data-analyst，且 **default 标记在主 Agent 上**（不是 data-analyst）
- [ ] data-analyst **没有** binding（`bindings` 数组中无 `agentId: "data-analyst"` 条目）
- [ ] `channels.feishu.accounts` 中**没有** `"data-analyst"` 键
- [ ] 主 Agent 的 TOOLS.md 包含 `sessions_send` 调用规范
- [ ] `tools.agentToAgent.enabled` 为 `true`，allow 列表含主 Agent 和 data-analyst
- [ ] `config.json` 中 `CAN_API_KEY` 存在且以 `cgk-` 开头

> 如果任一项不通过，回到 Step 2 修复。

## Step 4: 初始化验证（安装后必做）

安装完成后，通过主 Agent 向数据分析助手发送测试消息：

```
@data-analyst 帮我看看有哪些可用的指标分类
```

验证：
- [ ] 主 Agent 正确转发请求给 data-analyst（不自己回答）
- [ ] data-analyst 调用 Gateway API 返回指标目录
- [ ] reply 通过主 Agent 完整转发给用户

## 常见错误

| 错误 | 现象 | 原因 | 修复 |
|------|------|------|------|
| data-analyst 被设为主 Agent | 飞书消息直接到 data-analyst，不经过主 Agent | `default: true` 或有 binding | Step 2b 移除 default + binding |
| 两个 session 同时响应 | 用户问一个问题，收到两个回复 | data-analyst 有自己的 binding 或飞书 account | Step 2b 删除 binding 和 account |
| 主 Agent 不转发 | 数据查询问题主 Agent 自己回答 | TOOLS.md 没写调用规范 | Step 2f |
| sessions_send forbidden | 主 Agent 调用 data-analyst 被拒绝 | agentToAgent 未开启或 allow 列表不全 | Step 2c |
| API Key 401 | 指标查询返回未授权错误 | CAN_API_KEY 未配置或无效 | Step 2a |

## 故障排查

| 问题 | 解决 |
|------|------|
| CAN_API_KEY 401 | 确认 `config.json` 中 Key 格式正确，以 `cgk-` 开头，无多余空格 |
| Gateway 连接超时 | 检查网络连接，确认可以访问 gateway.can.aloudata.com |
| 子 Agent 超时 | 调大 `runTimeoutSeconds`（推荐 600-1800） |
| 飞书卡片发送失败 | 检查飞书 appId/appSecret 配置 |

## 卸载

如需卸载数据分析助手并将 OpenClaw 恢复到安装前的状态，参见 [UNINSTALL.md](./UNINSTALL.md)。
