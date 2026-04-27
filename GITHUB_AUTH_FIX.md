# 🔐 GitHub认证失败解决方案

## ❌ 错误信息
```
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/frank-TD/franktd.git/'
```

---

## ✅ 解决方案

### 方法1：使用Personal Access Token (PAT) - 推荐

#### 步骤1：创建Personal Access Token

1. **访问GitHub**
   - 登录GitHub：https://github.com
   - 点击右上角头像 → Settings

2. **创建Token**
   - 左侧菜单：Developer settings
   - 点击：Personal access tokens → Tokens (classic)
   - 点击：Generate new token → Generate new token (classic)

3. **配置Token**
   - **Note**: 输入描述，例如：`franktd-project-push`
   - **Expiration**: 选择过期时间，推荐：`No expiration` 或 `90 days`
   - **Select scopes**: 勾选：
     - ✅ `repo` (完整的仓库访问权限)
     - ✅ `workflow` (允许GitHub Actions)

4. **生成并保存**
   - 点击 "Generate token"
   - **重要**：立即复制token，只显示一次！

#### 步骤2：使用Token推送代码

**在命令行执行：**

```bash
# 方式1：使用git命令时输入token
git push -u origin main
# 当提示输入用户名时，输入：frank-TD
# 当提示输入密码时，粘贴你的Personal Access Token（不是GitHub密码！）

# 方式2：使用token直接推送（更安全）
git remote set-url origin https://YOUR_TOKEN@github.com/frank-TD/franktd.git
git push -u origin main
```

**示例：**
```bash
# 将YOUR_TOKEN替换为你的实际token
git remote set-url origin https://ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx@github.com/frank-TD/franktd.git
git push -u origin main
```

---

### 方法2：使用GitHub CLI (gh)

如果您的系统安装了GitHub CLI：

```bash
# 安装GitHub CLI（如果还没有）
# Ubuntu/Debian:
sudo apt install gh

# Mac:
brew install gh

# 登录GitHub
gh auth login

# 按提示操作：
# 1. 选择：GitHub.com
# 2. 选择：Login with a web browser
# 3. 在浏览器中完成认证

# 推送代码
git push -u origin main
```

---

### 方法3：使用SSH密钥

#### 步骤1：生成SSH密钥

**在您的本地电脑上执行（不是沙箱环境）：**

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "frank-TD@github.com"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 或
cat ~/.ssh/id_rsa.pub
```

#### 步骤2：添加SSH密钥到GitHub

1. **复制公钥内容**（从 `cat ~/.ssh/id_ed25519.pub` 的输出）

2. **添加到GitHub**
   - 访问：https://github.com/settings/keys
   - 点击：New SSH key
   - **Title**: 输入描述，例如：`franktd-ssh-key`
   - **Key**: 粘贴公钥内容（整个内容）
   - 点击：Add SSH key

3. **测试SSH连接**
```bash
ssh -T git@github.com
# 应该看到：Hi frank-TD! You've successfully authenticated...
```

#### 步骤3：使用SSH推送

```bash
# 修改远程仓库地址为SSH
git remote set-url origin git@github.com:frank-TD/franktd.git

# 推送代码
git push -u origin main
```

---

### 方法4：在GitHub网页上直接上传

如果以上方法都不行，可以使用网页上传：

1. **访问你的仓库**
   - 打开：https://github.com/frank-TD/franktd

2. **上传代码**
   - 如果仓库是空的，点击 "uploading an existing file"
   - 或者使用 GitHub Desktop 客户端

---

## 🎯 推荐方案

### 最简单：方法1 (Personal Access Token)

**优点：**
- ✅ 最简单快速
- ✅ 不需要额外安装工具
- ✅ 可以立即使用

**步骤总结：**
1. 访问：https://github.com/settings/tokens/new
2. 勾选 `repo` 和 `workflow`
3. 生成token并复制
4. 运行：
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/frank-TD/franktd.git
   git push -u origin main
   ```

### 最安全：方法3 (SSH密钥)

**优点：**
- ✅ 最安全
- ✅ 不需要每次输入密码
- ✅ 适合长期使用

**适用场景：**
- 需要频繁推送
- 多人协作
- 长期项目

---

## 🔒 安全提示

1. **妥善保管Token**
   - 不要分享给他人
   - 不要提交到代码仓库
   - 定期更换

2. **设置过期时间**
   - 推荐设置过期时间
   - 到期后重新生成

3. **使用SSH密钥（长期项目）**
   - 比token更安全
   - 不需要频繁更换

4. **不要在代码中硬编码**
   - 使用环境变量
   - 使用secrets管理

---

## 📞 如果还有问题

### 问题1：Token过期怎么办？

**解决：**
- 访问：https://github.com/settings/tokens
- 删除旧token
- 生成新token
- 重复方法1的步骤

### 问题2：推送失败，提示"Permission denied"？

**检查：**
- 确认token有 `repo` 权限
- 确认token没有过期
- 确认仓库地址正确

### 问题3：如何检查远程仓库是否正确？

```bash
git remote -v
# 应该显示：
# origin  https://github.com/frank-TD/franktd.git (fetch)
# origin  https://github.com/frank-TD/franktd.git (push)
```

---

## 🚀 快速开始（推荐）

**如果您现在就想推送，请按以下步骤操作：**

1. **获取Token**（2分钟）
   - 访问：https://github.com/settings/tokens/new
   - 勾选：`repo` 和 `workflow`
   - 生成并复制token

2. **告诉我要推送**
   - 回复我你的token（我会帮你配置）
   - 或者自己在命令行执行：
     ```bash
     git remote set-url origin https://YOUR_TOKEN@github.com/frank-TD/franktd.git
     git push -u origin main
     ```

3. **等待推送完成**
   - 看到成功提示
   - 访问：https://github.com/frank-TD/franktd 确认

---

**请选择一个方案，或者告诉我你的token（我会帮你完成推送）** 🚀
