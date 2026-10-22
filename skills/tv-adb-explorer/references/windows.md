# Windows / USB 首次配置

## 新人需要提供

目标 App 包名；支持 USB ADB 的电视及调试线；存放素材的位置。包名不确定时通过 `adb -s SERIAL shell pm list packages` 帮助筛选，不凭 App 显示名猜包名。

## 必要条件

- Windows 10/11，PowerShell 5.1+，Python 3.10+（仅标准库）。
- ADB 来自 Android 官方 Platform Tools；已有 Android Studio 的可直接复用。
- Codex CLI 单独可运行并已登录；桌面版能聊天不代表命令行已登录。执行 `codex login` 完成人工登录，再用小样确认实际调用可用。
- 使用官方 Codex CLI 安装方式；npm 版需 Node.js 和 `npm install -g @openai/codex`。不要为夜间运行关闭全局审批或使用 `--dangerously-bypass-approvals-and-sandbox`。
- Windows 的 App execution alias 可能把 `python.exe` 指向商店；`start.ps1` 优先尝试 `py -3` 并校验版本。
- PowerShell 若阻止脚本，先按组织策略解决签名/下载文件限制。不能静默修改整机执行策略。

`setup.ps1` 优先复用 PATH 中的 adb.exe；否则装到 `%LOCALAPPDATA%\TVAdbExplorer\platform-tools`，保存绝对路径到 config.json。可直接给 `start.ps1 -Adb` 指定官方工具位置。不安装 Android Studio，不改注册表和全局 PATH。

## USB 检查顺序

1. 查电视厂商文档，确认哪个接口支持 USB device/ADB 和所需线材。有些电视只有 USB host，ADB 只能走网络或专用工程接口；此时先报告硬件限制。
2. 电视开启开发者选项 / USB 调试；不同厂商路径不同，不保证连续点击版本号适用所有电视。
3. Windows 设备管理器检查 Android ADB Interface；异常则安装对应 OEM 官方驱动。Google USB Driver 不适用于所有厂商。
4. `adb devices -l`：空列表查端口/线/驱动；unauthorized 到电视接受 RSA；offline 检查连接，重新插线。不要删 adbkey、关闭驱动签名或重置电视。
5. 指定序列号确认 `adb -s SERIAL get-state` 输出 device，`adb -s SERIAL shell pm path PACKAGE` 找到包。
6. 程序自动解析 LEANBACK_LAUNCHER，失败再试 LAUNCHER。均失败时人工查明确切入口，传 `PACKAGE/.Activity`。

## 无人值守前

插电、保持网络供 Codex 使用、确认电脑不会合盖/重启；程序只在运行期间请求 Windows 保持系统唤醒，不永久改电源计划。电视自动待机、锁屏和 USB 断连仍可能发生，需用真实机器小样验证。不可保证合盖后继续工作。

建议先 5 步，然后 30 分钟，再整夜。8 小时和 1200 步是停止上限，不是必须耗尽的时长，也不代表费用预算；每次视觉调用消耗 Codex 额度，模型重试也可能消耗额度。

## 官方资料（制作时核对：2026-10-22）

- https://developer.android.com/tools/adb
- https://developer.android.com/tools/releases/platform-tools
- https://developer.android.com/studio/run/oem-usb
- https://learn.chatgpt.com/docs/non-interactive-mode
- https://developers.openai.com/codex/cli
- https://learn.chatgpt.com/docs/build-skills
