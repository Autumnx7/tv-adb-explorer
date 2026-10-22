# TV ADB Explorer

面向新人：在 **Windows + Codex + USB ADB** 环境下，自动探索 Android TV 指定 App，整理真机现状素材包。支持夜间运行、记录并跳过登录/人工分支、断点续跑。**不生成 H5 Demo。**

## 新人只发链接，从这里开始

新电脑只需已经能使用 **Codex 桌面版并登录**。不要求提前安装 Git、ADB、Python 或 Codex CLI。

把本仓库链接发给 Codex，即可让它读取下面的首次引导；如果它只介绍仓库，补一句“请开始首次安装配置”。**链接本身不是自动运行程序，仍需要 Codex 能联网读取仓库并执行本机命令。**

### 给收到链接的 Codex

请先读 [首次使用引导](skills/tv-adb-explorer/references/first-run.md) 和 [Skill 入口](skills/tv-adb-explorer/SKILL.md)，从环境检查开始实际推进。能自动完成的不要交给新人手动敲命令；遇到必要人工操作，一次只提示一件事，完成后自动验证并继续。

| 阶段 | Codex 自动完成 | 新人必要时操作 |
|---|---|---|
| 下载 Skill | 下载 ZIP、解压、检查文件、安装到用户技能目录 | 处理本机权限提示 |
| 补齐依赖 | 检查并复用/安装 Python、Codex CLI、ADB；仅必要时装 Node | 确认软件许可或系统安装提示 |
| 连接电视 | 查询设备、识别连接问题、保存 ADB 路径 | 接调试线、开启 USB 调试、电视确认 RSA；必要时安装 OEM 驱动 |
| CLI 登录 | 检查状态、登录后复核 | 按提示完成一次 CLI 登录；已登录就跳过 |
| 确认 App | 查询包名、检查安装和入口、准备素材目录 | 告诉 AI App 名称或包名 |
| 试跑与夜间 | 5 步抓取验证、整理索引、按授权启动后台探索 | 必要时看一次电视；保持设备工作 |

第一次需要有人配合接线和授权，完成配置与小样后才适合无人值守。普通电视 USB 插口不一定支持 ADB，需要厂商支持的 USB 调试连接。

## 直接把这段给 Codex

> 请下载并安装这个 Skill：https://github.com/Autumnx7/tv-adb-explorer 。先阅读仓库 README 和 skills/tv-adb-explorer/SKILL.md，将 Skill 安装到我的用户技能目录。然后帮我配置 Windows USB ADB，检查电视连接，询问目标 App 包名，跑 5 步小样验证，再准备夜间自动探索。遇到登录和需要人工处理的分支只记录并跳过，素材保存在本地。不要把实机素材上传 GitHub。

AI 可使用 Git 克隆，或下载 GitHub 的仓库 ZIP（无需 Git），解压后阅读文件，再在仓库根目录执行：

```powershell
.\install.ps1
```

默认安装到 `%USERPROFILE%\.agents\skills\tv-adb-explorer`。不会覆盖已有同名 Skill。重新打开 Codex 对话以加载；也可以在当前对话明确要求读取已安装的 SKILL.md。

## 具体流程

1. **准备环境**：复用/下载官方 ADB，检查 Python、Codex CLI 和登录。
2. **连接电视**：检查 USB 调试口、OEM 驱动、RSA 授权、设备序列号和 App 包名。
3. **小样验收**：AI 操作 5 步，验证截图、界面树、真实操作和结果索引。
4. **夜间探索**：本地 Python 运行程序逐步调用 Codex CLI 看图判断，通过 ADB 发送单个遥控按键。默认最多 8 小时 / 1200 步，支持后台进程。
5. **晨间查看**：打开本地 `index.html` 浏览截图，读 `REPORT.md` 看阻塞与未覆盖范围。相同目录可续跑。

### 最终素材

原始截图、可读取的 UI XML、页面归类、遥控操作关系、焦点/返回/滚动观察、登录等阻塞清单、设备与 App 版本、断点文件。可供下一阶段结合其他材料制作离线 H5；截图不等于设计图层和原始图片资源。

### 新人需要知道的边界

- 普通电视 USB host 插口不一定能用 ADB；必须有厂商支持的 USB 调试连接，Skill 不能改变硬件能力。
- **首次授权、驱动和 Codex 登录需有人操作**。之后的 App 登录分支会跳过；USB/网络/AI 额度等全局故障有限重试后保存并结束。
- 桌面版负责发起也可以；整夜程序仍需已登录的 **Codex CLI**，不依赖桌面聊天持续运行。
- 截图、XML 和摘要会提交给 Codex 做 AI 判断，会消耗账号额度。使用获准的测试内容；素材不会自动上传 GitHub。
- 不保证穷尽所有页面。登录后界面、外设条件页、安全黑屏等会形成缺口；报告不虚构覆盖率。
- 只执行导航类操作；购买、删除、安装、账号输入等跳过。AI 的语义风险判断仍需在测试环境验证。
- 电脑/电视要保持工作；闭合电脑、自动重启、电视休眠可能中断。

## 文件

- [Skill 入口](skills/tv-adb-explorer/SKILL.md)
- [Windows 首次配置](skills/tv-adb-explorer/references/windows.md)
- [素材和续跑约定](skills/tv-adb-explorer/references/materials.md)
- `scripts/setup.ps1`、`scripts/start.ps1` 位于 Skill 目录中。

## 验证状态

见 [VALIDATION.md](VALIDATION.md)。本仓库尚未在真实 Windows + USB 电视上完成验收；自动化模拟通过也不能代替 5 步真机小样。

本地测试：`python -m unittest discover -s tests -v`。GitHub Actions 在 Windows 和 Linux 上运行同样的模拟测试，并在 Windows 上检查 PowerShell 脚本语法。测试不会连接真实电视或调用付费 AI。
