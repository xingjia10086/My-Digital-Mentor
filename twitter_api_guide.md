# 全自动推特分发机 (Twitter Agent) - API 密钥申请指南

为了让你的“数字分身”能够在后台全自动发推，你需要从 Twitter 官方获取 4 把安全钥匙。本指南将带你用 3 分钟完成申请。

**⚠️ 准备工作：**
确保你用来申请的 Twitter / X 账号已经绑定了**手机号**，并且不是刚刚注册的纯白板小号。

---

## 第一步：注册开发者并创建应用

1. 浏览器打开并登录 [Twitter 开发者中心 (Developer Portal)](https://developer.twitter.com/en/portal/dashboard)。
2. 按照屏幕提示，开通 **Free Tier (免费版)** 开发者权限。
   - 这完全免费，每月配额足足有 1500 条推文。
   - 填写申请理由时，可以直接复制这句英文：“`I am building a simple personal script to post my daily reading notes automatically.`”
3. 开通成功后，系统会默认或要求你创建一个 **App (Project)**。创建完成便会进入应用面板（App Dashboard）。

---

## 第二步：极其关键！开启写权限 (Read and Write)

拿到钥匙前，必须先赋权！如果跳过这一步，机器人发推时会报错（Forbidden）。

1. 在你的 App 面板中，往下滚动，找到 **User authentication settings**（用户验证设置）。
2. 点击右侧的 **Set up** 或 **Edit**。
3. **App permissions (应用权限)**：必须选择 **Read and write** (或者 *Read and write and Direct message* )。
4. **Type of App (应用类型)**：选择 **Web App, Automated App or Bot**。
5. **App info (应用信息)**：
   - *Callback URI / Redirect URL*：随便填个合法的网址，比如 `https://x.com/`，或者你自己的博客。
   - *Website URL*：填同样的网址即可。
6. 点击页面最下方的 **Save (保存)**。

*(如果你刚才操作正确，现在回到 App 面板，`OAuth 1.0a` 区域下方的小字应该显示为“Read and Write”。)*

---

## 第三步：生成并复制 4 把神秘钥匙

权限搞定后，我们需要拿代码！

1. 切换到顶部的 **Keys and Tokens** 选项卡。

### 获取前两把钥匙 (API Key)
2. 找到 **Consumer Keys**（有些地方也叫 OAuth 1.0 Keys / API Keys）。
3. 点击右侧的 **Regenerate (重新生成)** 按钮。
4. 弹出的黑框里会出现两串乱码：
   - `API Key` (也叫 Consumer Key)
   - `API Key Secret` (也叫 Consumer Secret)
5. **立刻复制这两串代码并保存在电脑记事本里！**（弹窗一关就再也看不到了）。然后关闭弹窗。

### 获取后两把钥匙 (Access Token)
6. 接着往下找，找到 **Authentication Tokens** 下的 **Access Token and Secret**。
7. 点击右侧的 **Generate**（或者 Regenerate）按钮。
8. 同样会弹出一个黑框，此时会提示（Permissions: Read and Write）。复制下方的两串乱码：
   - `Access Token` 
   - `Access Token Secret` 
9. **同样把它们保存在刚才那份记事本里。**

---

## 🎉 第四步：大功告成

现在，你的记事本里应该有四行长短不一的代码了。

**请直接把这 4 把钥匙以文字的形式回复给我（发在聊天框里），我立刻帮你完成 `twitter_auto_agent.py` 的最后拼图！**
