# TV ADB Explorer

面向新人：在 **Windows + Codex + USB ADB** 环境下，自动探索 Android TV 指定 App，整理真机现状素材包。支持夜间运行、记录并跳过登录/人工分支、断点续跑。**不生成 H5 Demo。**

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
