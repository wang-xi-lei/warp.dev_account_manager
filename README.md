# Warp Account Manager / Warp 账户管理器

[English](#english) | [中文](#中文)

---

## English

![Warp Account Manager](img/en.png)

### ✨ Features

- 🔄 Easy account switching across multiple Warp.dev accounts
- 🛡️ Ban prevention with automatic ID rotation
- 🌐 Chrome extension for one-click account import
- 📊 Real-time limit tracking
- 🔒 Built-in proxy (mitmproxy) integration
- 🌍 Multi-language: English and Chinese (中文)
- 🏗️ Modular architecture for maintainability

### 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/wang-xi-lei/warp.dev_account_manager.git
   cd warp.dev_account_manager
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

### 🚀 Quick Start

1. On first launch, install the mitmproxy certificate (auto prompt)
2. Add accounts via Chrome extension or manual JSON
3. Enable Proxy (Start Proxy button)
4. Activate an account (Start button)
5. Use Warp.dev with the selected account

### 📚 Usage Video

https://youtu.be/5_itpYHZGJc

### ⚠️ Disclaimer

This project is designed to facilitate the use of Warp.dev. Use at your own risk; no responsibility is accepted for any consequences.

### 📁 Project Structure

```
warp.dev_account_manager/
├── api/              # Warp API & Firebase integration
├── bridge/           # Bridge server for Chrome extension
├── core/             # Core logic (proxy, accounts, certificates)
├── database/         # Account database management
├── ui/               # User interface components
├── utils/            # Utility functions
├── languages.py      # Multi-language support
└── main.py           # Application entry point
```

---

## 中文

![Warp 账户管理器](img/en.png)

### ✨ 功能特性

- 🔄 多账户轻松切换
- 🛡️ 自动轮换 ID，降低封禁风险
- 🌐 Chrome 扩展一键导入账户
- 📊 实时查看账户额度
- 🔒 内置 mitmproxy 代理集成
- 🌍 支持中英文界面
- 🏗️ 模块化架构，易于维护

### 📦 安装

1. 克隆仓库：
   ```bash
   git clone https://github.com/wang-xi-lei/warp.dev_account_manager.git
   cd warp.dev_account_manager
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行程序：
   ```bash
   python main.py
   ```

### 🚀 快速开始

1. 首次启动时按提示安装 mitmproxy 证书
2. 通过 Chrome 扩展或手动 JSON 添加账户
3. 点击“启动代理”按钮启用代理
4. 点击“开始”激活目标账户
5. 使用 Warp.dev 继续工作

### 📚 使用视频

https://youtu.be/5_itpYHZGJc

### ⚠️ 免责声明

本项目仅为便捷使用 Warp.dev 而设计，使用风险由您自行承担，作者不对任何后果负责。

### 📁 项目结构

```
warp.dev_account_manager/
├── api/              # Warp API 和 Firebase 集成
├── bridge/           # Chrome 扩展桥接服务器
├── core/             # 核心逻辑（代理、账户、证书）
├── database/         # 账户数据库管理
├── ui/               # 用户界面组件
├── utils/            # 工具函数
├── languages.py      # 多语言支持
└── main.py           # 应用程序入口
```
