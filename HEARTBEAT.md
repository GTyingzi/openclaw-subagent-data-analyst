# Heartbeat

本文件定义 **数据分析助手（data-analyst）** 的健康检查规范，供 OpenClaw 主框架进行存活探测和状态验证。

---

## 存活探测方式

OpenClaw 可通过以下方式验证本 subagent 是否处于可用状态：

**方式一：配置文件检查（轻量，推荐日常探测）**
```bash
# 检查 API Key 配置是否存在
grep -q "^CAN_API_KEY=cgk-" ~/.openclaw/.env && echo "OK" || echo "FAIL"
```
- 返回 `OK`：配置存在，subagent 可启动
- 返回 `FAIL`：配置缺失，需要用户干预

**方式二：API 连通性检查（深度，按需执行）**
```bash
# 调用指标空间列表接口验证 API Key 有效性（返回 200 为健康）
curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $CAN_API_KEY" \
  "https://gateway.can.aloudata.com/api/metrics/categories"
```
- 返回 `200`：API Key 有效，服务可达
- 返回 `401`：API Key 无效或已过期
- 返回其他：网络问题或服务异常

---

## 健康检查清单

### 检查项 1：配置完整性

```bash
# 检查 ~/.openclaw/.env 存在且包含 CAN_API_KEY
[ -f ~/.openclaw/.env ] && grep -q "^CAN_API_KEY=cgk-" ~/.openclaw/.env
```

| 结果 | 状态 | 说明 |
|------|------|------|
| 通过 | 🟢 健康 | 配置文件存在且格式正确 |
| 失败 | 🔴 不可用 | 缺少配置，指标查询功能不可用 |

---

### 检查项 2：技能文件完整性

```bash
# 检查 4 个必需技能目录是否存在
for skill in metric-query metric-attribution dip-vap-dashboard dip-vap-feishu-card; do
  [ -d "skills/$skill" ] && echo "$skill: OK" || echo "$skill: MISSING"
done
```

| 结果 | 状态 | 说明 |
|------|------|------|
| 全部 OK | 🟢 健康 | 所有技能可用 |
| 部分 MISSING | 🟡 降级 | 对应技能不可用，其他功能正常 |

---

### 检查项 3：Gateway API 连通性

```bash
# 验证 API Key 有效性
STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "X-API-Key: $CAN_API_KEY" \
  "https://gateway.can.aloudata.com/api/metrics/categories")
echo "HTTP Status: $STATUS"
```

| HTTP 状态码 | 状态 | 说明 |
|-------------|------|------|
| 200 | 🟢 健康 | API Key 有效，服务正常 |
| 401 | 🔴 不可用 | API Key 无效或已过期 |
| 000 / 5xx | 🟡 网络异常 | 服务不可达，可能是网络问题 |

---

## 故障排查指引

### 检查项 1 失败：配置文件缺失或格式错误

```
排查步骤：
1. 确认文件存在：ls -la ~/.openclaw/.env
2. 查看文件内容：cat ~/.openclaw/.env（注意不要泄露密钥）
3. 确认格式正确：行内容应为 CAN_API_KEY=cgk-xxxxxxxxxxxx
4. 如文件不存在：mkdir -p ~/.openclaw && echo "CAN_API_KEY=cgk-your-key" >> ~/.openclaw/.env
5. 重新运行健康检查
```

### 检查项 2 失败：技能文件缺失

```
排查步骤：
1. 进入项目目录：cd /path/to/openclaw-subagent-data-analyst
2. 确认 skills/ 目录结构：ls skills/
3. 如技能目录缺失，重新克隆或拉取仓库：git pull origin main
4. 重新运行健康检查
```

### 检查项 3 失败：Gateway API 返回 401

```
排查步骤：
1. 确认 CAN_API_KEY 值正确（前缀为 cgk-，没有多余空格或换行）
2. 联系数据平台管理员确认 Key 是否已过期或被吊销
3. 获取新 Key 后更新 ~/.openclaw/.env 中的值
4. 重新运行连通性检查
```

### 检查项 3 失败：Gateway API 网络异常

```
排查步骤：
1. 检查网络连接：curl -I https://gateway.can.aloudata.com
2. 确认是否需要 VPN 或代理访问
3. 如在企业内网，确认防火墙放通了 gateway.can.aloudata.com:443
```
