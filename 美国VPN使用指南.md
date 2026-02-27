# 🇺🇸 美国 Oregon VPN 完整使用指南

---

## 一、VPN 信息总览

| 项目 | 详情 |
|------|------|
| **服务器 IP** | `136.118.235.211` |
| **服务器位置** | 🇺🇸 Oregon（免税州） |
| **GCE 实例名** | `wireguard-vpn`（us-west1-b） |
| **月费** | 运行中 ~$7-8 / 关机仅保留 IP ~$1.46 |
| **赠金** | $300（可用 37+ 个月） |

### 可用协议

| 协议 | 端口 | 适用设备 |
|------|------|----------|
| **Shadowsocks** | TCP 8388 | 💻 Windows（Clash Verge）/ 📱 iPhone（Shadowrocket） |
| **WireGuard** | UDP 51820 | 📱 iPhone（WireGuard App） |

### 客户端 IP 分配

| 设备 | 内网 IP | 配置文件 |
|------|---------|----------|
| 💻 Windows | 通过 SS 代理 | [clash-us-wireguard.yaml](file:///D:/GPT/AI-demo/clash-us-wireguard.yaml) |
| 📱 iPhone | `10.66.66.3` | [wireguard-iphone.conf](file:///D:/GPT/AI-demo/wireguard-iphone.conf) |

> [!TIP]
> 两台设备可以**同时连接**，互不干扰。

---

## 二、Windows 电脑使用（Clash Verge）

### 2.1 导入配置

1. 打开 **Clash Verge** → 左侧点击 **订阅**
2. 将文件**拖拽**到 Clash Verge 窗口：
   ```
   D:\GPT\AI-demo\clash-us-wireguard.yaml
   ```
3. 点击新配置卡片使其**高亮选中**

> [!WARNING]
> **不要**把路径粘贴到顶部 URL 输入框，那是给远程订阅用的。本地文件请用**拖拽方式**导入。

### 2.2 代理组说明

| 代理组 | 用途 | 包含的网站 |
|--------|------|-----------|
| **Proxy** | 通用海外 | Google、YouTube、Twitter、GitHub 等 |
| **Bank** | 美国银行 | Chase、BOA、Citi、Wells Fargo 等 |
| **AI** | AI 服务 | ChatGPT、Claude、Gemini、Midjourney 等 |
| **Direct** | 国内直连 | 百度、B站、知乎、淘宝、京东 等 |

### 2.3 代理模式切换

在右上角切换三种模式：

````carousel
### 🌐 全局模式（Global）
**所有流量**都走美国代理

适合：需要确保全部流量经过美国 IP

```
右上角 → 点击「全局」
```
<!-- slide -->
### 📋 规则模式（Rule）⭐ 推荐日常使用
**自动分流**：海外走代理，国内走直连

适合：日常使用，兼顾速度和功能

```
右上角 → 点击「规则」
```
<!-- slide -->
### 🔌 直连模式（Direct）
**关闭代理**，所有流量直连

适合：暂时不需要代理时

```
右上角 → 点击「直连」
```
````

### 2.4 验证 IP

1. 开启全局或规则模式
2. 浏览器访问 https://whatismyipaddress.com
3. 确认显示 **IP**: `136.118.235.211`，**Location**: Oregon, US

### 2.5 添加自定义规则

编辑 [clash-us-wireguard.yaml](file:///D:/GPT/AI-demo/clash-us-wireguard.yaml)，在 `rules:` 部分添加：

```yaml
- DOMAIN-SUFFIX,example.com,Proxy
```

修改后在 Clash Verge 中**刷新配置**即可生效。

---

## 三、iPhone 使用

IPhone 有两种方式可选：

| 方案 | App | 费用 | 特点 |
|------|-----|------|------|
| **Shadowrocket** ⭐推荐 | 小火箭 | $2.99（美区） | 与 Windows 同协议，支持规则分流 |
| **WireGuard** | WireGuard | 免费 | 简单直接，全局 VPN |

---

### 方案 A：Shadowrocket（推荐）

#### 安装
App Store **美区账号**搜索 **Shadowrocket** → 购买安装（$2.99）

#### 导入（二选一）

**方式 1 — 链接导入（最快）**

在 iPhone Safari 中打开以下链接，自动跳转到 Shadowrocket 添加节点：
```
ss://YWVzLTI1Ni1nY206N2VCZUhHUzhyUnBFVmNlWXFXMTRwQT09QDEzNi4xMTguMjM1LjIxMTo4Mzg4#US-Oregon
```

**方式 2 — 手动添加**

打开 Shadowrocket → 右上角 **+** → 类型选 **Shadowsocks**：

| 字段 | 值 |
|------|----|
| **地址** | `136.118.235.211` |
| **端口** | `8388` |
| **密码** | `7eBeHGS8rRpEVceYqW14pA==` |
| **算法** | `aes-256-gcm` |
| **备注** | `US-Oregon` |

#### 使用
- 点击节点开关即可连接，状态栏出现 VPN 图标即为已连接
- **全局路由**设置：`设置 → 全局路由 → 代理`（全走美国）或 `配置`（按规则分流）

---

### 方案 B：WireGuard

#### 安装
App Store 搜索 **WireGuard** → 安装官方 App（免费）

#### 导入（二选一）

**方式 1 — 文件传输**

将电脑上的文件通过微信/邮件/AirDrop 发送到 iPhone，用 WireGuard App 打开：
```
D:\GPT\AI-demo\wireguard-iphone.conf
```

**方式 2 — 手动输入**

打开 WireGuard App → **+** → **手动创建**：

| 字段 | 值 |
|------|----|
| **名称** | US-Oregon |
| **私钥** | `yPQYGGGrgDW5T0zYes6AjAQ06AHSy93iMAcVDTad5lw=` |
| **地址** | `10.66.66.3/24` |
| **DNS** | `8.8.8.8, 8.8.4.4` |
| **对端公钥** | `CZZRmXeagcaUMvMAxFoawnooNTaFcquAFuviBOeCeFo=` |
| **端点** | `136.118.235.211:51820` |
| **允许的 IP** | `0.0.0.0/0` |
| **持久保活** | `25` |

#### 使用
- WireGuard App 内拨动开关，或在 **设置 → VPN** 中快速开关
- 状态栏出现 **VPN** 图标即为已连接

---

## 四、服务器管理

### 日常命令

```powershell
# 查看状态
gcloud compute instances describe wireguard-vpn --zone=us-west1-b --format="table(name,status,networkInterfaces[0].accessConfigs[0].natIP)"

# ⏸️ 关机省钱（静态 IP 保留，下次开机 IP 不变）
gcloud compute instances stop wireguard-vpn --zone=us-west1-b

# ▶️ 开机
gcloud compute instances start wireguard-vpn --zone=us-west1-b

# SSH 登录（从中国连接需 IAP 隧道）
echo y | gcloud compute ssh wireguard-vpn --zone=us-west1-b --tunnel-through-iap
```

### 费用参考

| 状态 | 月费 |
|------|------|
| 运行中 | ~$7-8 |
| 已关机（仅保留 IP） | ~$1.46 |

> [!IMPORTANT]
> **不用时记得关机！** 执行 `stop` 命令即可，IP 地址会保留。

### 完全删除

```powershell
gcloud compute instances delete wireguard-vpn --zone=us-west1-b --quiet
gcloud compute addresses delete vpn-static-ip --region=us-west1 --quiet
gcloud compute firewall-rules delete allow-wireguard --quiet
gcloud compute firewall-rules delete allow-shadowsocks --quiet
```

---

## 五、常见问题

| 问题 | 解决方案 |
|------|----------|
| Clash Verge 导入失败 | 不要粘贴路径到 URL 框，用**拖拽方式**导入 |
| 连接后 IP 没变 | 确认系统代理已开启，模式为全局或规则 |
| YouTube 打不开 | 确认使用 Shadowsocks 版配置（非 WireGuard 版） |
| 连接不稳定 | 运营商可能限制 UDP，SS 用 TCP 更稳定 |
| 银行检测到 VPN | 这是数据中心 IP，部分银行可能识别，配合验证码可通过 |
| 添加更多设备 | 需要在服务器生成新密钥 |

---

## 六、安全提醒

> [!CAUTION]
> 以下信息包含你的 VPN 密钥/密码，**请妥善保管，不要分享**：
> - `clash-us-wireguard.yaml`（Shadowsocks 密码）
> - `wireguard-iphone.conf`（WireGuard 私钥）
> - Shadowrocket SS 链接（含密码）
