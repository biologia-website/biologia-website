# 佰洛生物官网 — 域名绑定 & ICP 备案完整指南

---

## 第一部分：GitHub Pages 部署 + 域名绑定（今天就能上线）

### 前置条件
- [ ] 拥有 www.biologia.cn 域名的 DNS 管理权限（在域名注册商处）
- [ ] 一个 GitHub 账号（没有的话去 https://github.com 免费注册）

---

### 步骤 1：在 GitHub 创建仓库

1. 登录 https://github.com
2. 点击右上角 **+** → **New repository**
3. 仓库名填写：`biologia-website`（或你喜欢的名字）
4. 选择 **Public**（公开，免费）或 **Private**（私有）
5. **不要勾选** "Add a README file"、"Add .gitignore"、"Choose a license"
6. 点击 **Create repository**

### 步骤 2：推送代码到 GitHub

仓库创建后，GitHub 会显示推送指引。在终端中执行：

```bash
cd "C:\Users\valle\WorkBuddy\2026-06-11-11-11-10"

# 添加远程仓库（把 YOUR_USERNAME 换成你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/biologia-website.git

# 推送代码
git push -u origin main
```

> 提示：推送时需要输入 GitHub 用户名和 **Personal Access Token**（不是密码）
> 获取 Token：GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token，勾选 `repo` 权限

### 步骤 3：启用 GitHub Pages

1. 进入仓库 → **Settings** → **Pages**
2. **Source** 选择：`Deploy from a branch`
3. **Branch** 选择：`main`，目录选 `/ (root)`，点击 **Save**
4. 等待 1-2 分钟，页面会显示部署地址：`https://YOUR_USERNAME.github.io/biologia-website/`
5. **Custom domain** 栏填入：`www.biologia.cn`，点击 **Save**
6. 勾选 ✅ **Enforce HTTPS**（自动申请 SSL 证书）

### 步骤 4：配置 DNS

登录你的域名注册商（阿里云/腾讯云/GoDaddy 等）DNS 管理面板，添加一条记录：

| 类型 | 主机记录 | 记录值 |
|------|----------|--------|
| **CNAME** | `www` | `YOUR_USERNAME.github.io` |

> 示例：如果你的 GitHub 用户名是 `bailuo-bio`，记录值就是 `bailuo-bio.github.io`

等待 DNS 生效（通常 5-30 分钟），然后访问 **https://www.biologia.cn** 即可看到网站！

---

## 第二部分：腾讯云 ICP 备案完整流程

> ⚠️ 备案与 GitHub Pages 部署互不影响，可以同时进行。

### 备案前准备清单

| 材料 | 说明 |
|------|------|
| 📄 企业营业执照 | 佰洛生物，彩色扫描件或照片 |
| 🆔 法人身份证 | 正反面彩色扫描件 |
| 👤 网站负责人身份证 | 如果和法人不同，需要额外授权书 |
| 🌐 域名证书 | 在域名注册商后台下载 biologia.cn 的证书 |
| 📧 邮箱 + 手机号 | 用于接收审核通知 |
| 💻 腾讯云账号 | https://cloud.tencent.com 注册并实名认证 |

---

### 步骤 1：购买云服务（获取备案服务号）

腾讯云备案需要「备案服务号」，需先购买：

**推荐方案：COS 对象存储（最便宜）**
1. 进入腾讯云 COS：https://console.cloud.tencent.com/cos
2. 创建存储桶 → 名称任意 → 地域选「中国大陆」
3. 购买资源包（约 ¥10/月或按量计费）

备案通过后，这个 COS 就是你的网站托管平台，可以配置 CDN 加速。

---

### 步骤 2：开始备案

1. 登录腾讯云备案系统：https://console.cloud.tencent.com/beian
2. 点击 **开始备案**
3. 按提示填写：

#### 主体信息
| 字段 | 填写内容 |
|------|----------|
| 主办单位性质 | 企业 |
| 主办单位名称 | 佰洛生物科技有限公司（营业执照全称） |
| 证件类型 | 营业执照 |
| 证件号码 | 营业执照统一社会信用代码 |
| 证件地址 | 营业执照上的注册地址 |
| 投资人或主管单位 | 可不填或填法人姓名 |
| 主体负责人 | 法人姓名 |
| 主体负责人证件 | 法人身份证信息 |

#### 网站信息
| 字段 | 填写内容 |
|------|----------|
| 网站名称 | 佰洛生物官网（不能包含"中国""中华"等字样） |
| 网站域名 | biologia.cn |
| 网站首页 | www.biologia.cn |
| 服务内容 | 单位门户网站 |
| 网站语言 | 中文简体 |
| 前置审批 | 不涉及（生物科技不属于前置审批行业） |
| 网站负责人 | 同法人或指定负责人 |

---

### 步骤 3：上传证件 + 真实性核验

- 上传营业执照扫描件
- 上传法人/负责人身份证正反面
- 上传域名证书截图
- **真实性核验**：用手机微信扫码，按提示完成人脸识别和活体检测

---

### 步骤 4：提交审核 + 等待

1. 确认所有信息无误后提交
2. **腾讯云初审**：1-2 个工作日（会电话核实）
3. **提交管局**：自动提交到省通信管理局
4. **管局审核**：7-20 个工作日（各省速度不同）
5. **审核通过**：短信 + 邮件通知，获得 **ICP 备案号**（如：粤ICP备XXXXXXXX号）

---

### 步骤 5：备案后处理

备案号下发后需要：
1. ✅ 在网站底部添加备案号（如：`粤ICP备XXXXXXXX号`）
2. ✅ 30 天内完成**公安备案**（https://beian.mps.gov.cn）
3. ✅ 将腾讯云 COS 绑定 www.biologia.cn，停用 GitHub Pages 或保留做备用

---

## 时间线总览

```
今天 ──→ 部署 GitHub Pages + DNS 配置（30 分钟）
        └─→ www.biologia.cn 可访问 ✅

本周 ──→ 准备备案材料 + 购买腾讯云 COS
        └─→ 提交备案申请

2-4 周后 ──→ 备案通过
            └─→ 迁移到腾讯云 COS + CDN
            └─→ 国内访问速度大幅提升 🚀
```

---

## 附录：网站后续更新流程

```bash
# 更新网站文件后：
cd "C:\Users\valle\WorkBuddy\2026-06-11-11-11-10"
git add -A
git commit -m "更新描述"
git push

# GitHub Pages 会自动重新部署（约1分钟生效）
# 如果迁移到腾讯云 COS，使用 COS 上传工具同步文件即可
```

---

> 📌 **当前状态**：Git 仓库已初始化，CNAME 文件已创建（www.biologia.cn），等待推送到 GitHub。
