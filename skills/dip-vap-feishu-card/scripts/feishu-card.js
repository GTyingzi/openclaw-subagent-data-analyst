#!/usr/bin/env node
/**
 * feishu-card.js
 * 发送飞书卡片消息
 * 用法: node feishu-card.js <receive_id> '<card_json>'
 *   receive_id: ou_xxx (用户) 或 oc_xxx (群组)
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

function getCredentials() {
  // 1. 环境变量
  if (process.env.FEISHU_APP_ID && process.env.FEISHU_APP_SECRET) {
    return { appId: process.env.FEISHU_APP_ID, appSecret: process.env.FEISHU_APP_SECRET };
  }
  // 2. OpenClaw 配置（支持 accounts 结构）
  const configPath = path.join(process.env.HOME || '/root', '.openclaw', 'openclaw.json');
  if (fs.existsSync(configPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const feishu = config?.channels?.feishu;
      // 优先从 accounts 读取（按 accountId 或 defaultAccount 或第一个）
      const accountId = process.env.FEISHU_ACCOUNT_ID || feishu?.defaultAccount;
      const accounts = feishu?.accounts || {};
      const acc = accounts[accountId] || accounts[Object.keys(accounts).find(k => accounts[k]?.appId)] || {};
      if (acc.appId && acc.appSecret) {
        return { appId: acc.appId, appSecret: acc.appSecret };
      }
      // 兼容旧的顶层结构
      if (feishu?.appId && feishu?.appSecret) {
        return { appId: feishu.appId, appSecret: feishu.appSecret };
      }
    } catch (e) {}
  }
  throw new Error('无法获取飞书凭证，请设置 FEISHU_APP_ID / FEISHU_APP_SECRET 环境变量');
}

function httpsPost(hostname, path, data, headers) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify(data);
    const req = https.request({
      hostname, path, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body), ...headers }
    }, (res) => {
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); } catch (e) { resolve(raw); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function getTenantToken(appId, appSecret) {
  const res = await httpsPost('open.feishu.cn', '/open-apis/auth/v3/tenant_access_token/internal', {
    app_id: appId, app_secret: appSecret
  });
  if (!res.tenant_access_token) throw new Error('获取 tenant_access_token 失败: ' + JSON.stringify(res));
  return res.tenant_access_token;
}

async function sendCard(token, receiveId, cardJson) {
  const receiveIdType = receiveId.startsWith('oc_') ? 'chat_id' : 'open_id';
  const res = await httpsPost('open.feishu.cn', `/open-apis/im/v1/messages?receive_id_type=${receiveIdType}`, {
    receive_id: receiveId,
    msg_type: 'interactive',
    content: JSON.stringify(cardJson)
  }, { Authorization: `Bearer ${token}` });
  return res;
}

(async () => {
  const [,, receiveId, cardJsonStr] = process.argv;
  if (!receiveId || !cardJsonStr) {
    console.error('用法: node feishu-card.js <receive_id> \'<card_json>\'');
    console.error('       node feishu-card.js <receive_id> @<file_path>  (从文件读取 JSON)');
    process.exit(1);
  }

  let cardJson;
  try {
    // 支持从文件读取：@/tmp/card.json
    const jsonInput = cardJsonStr.startsWith('@')
      ? fs.readFileSync(cardJsonStr.slice(1), 'utf8')
      : cardJsonStr;
    cardJson = JSON.parse(jsonInput);
  } catch (e) {
    console.error('卡片 JSON 解析失败:', e.message);
    process.exit(1);
  }

  const { appId, appSecret } = getCredentials();
  const token = await getTenantToken(appId, appSecret);
  const result = await sendCard(token, receiveId, cardJson);

  // 写入发送结果到文件，供其他脚本读取
  fs.writeFileSync('/tmp/card_send_result.json', JSON.stringify({
    success: result.code === 0,
    message_id: result.data?.message_id || null,
    error: result.code !== 0 ? result : null,
    timestamp: new Date().toISOString()
  }));

  if (result.code === 0) {
    console.log('✅ 飞书卡片发送成功', JSON.stringify(result.data?.message_id || ''));
  } else {
    console.error('❌ 发送失败:', JSON.stringify(result));
    process.exit(1);
  }
})();
