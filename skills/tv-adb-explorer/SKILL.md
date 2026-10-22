---
name: tv-adb-explorer
description: 在 Windows 上配置 USB ADB，使用 Codex CLI 视觉决策自动探索指定 Android TV App，支持夜间无人值守、断点续跑，交付截图、界面结构、操作路径及覆盖缺口素材包。用于真机现状采集，不生成 H5 Demo。
---

# TV ADB 真机探索

交付本地素材包，供后续其他流程消费。范围是当前设备条件下可达界面，不承诺“所有界面”。素材不得自动上传 GitHub。

## 首次收到链接或新电脑安装

**先读取并执行 [首次使用引导](references/first-run.md)。** 默认用户已能使用 Codex 桌面版，其他依赖未知；自动检查和补齐，不要求用户自行预装。一次只请求一个当前必需的人工动作，操作后验证状态并继续。记录首次配置进度以便中断后接着做。

已经配置好的设备可跳过安装引导，复核依赖、USB、登录和目标 App 后继续下面流程。

## 先做开机前准备

读取 [Windows 与 USB 配置](references/windows.md)。确认包名、USB 序列号和输出目录；用户未指定运行预算时采用 8 小时、1200 步上限，任一触发即停止。不要在运行中反复询问。

1. 检查电脑上的官方 ADB，运行 `scripts/setup.ps1` 复用或安装；脚本不修改全局 PATH。下载 Android SDK 前让用户阅读并接受官方许可，不能代替用户接受。已有合法安装直接复用。
2. 电视必须支持 USB device/debug 模式，并使用厂商指定的调试端口和数据线；普通 USB host 接口不能靠安装驱动变成调试口。不要推荐不明双公 USB 线。不支持时明确报告，不能伪称配置成功。
3. 指导开启 USB 调试并在电视上接受 RSA 提示；驱动只使用厂商来源。手动步骤必须白天完成，夜间不能绕过授权。
4. `adb devices -l` 确认状态为 device；多设备必须明确选择序列号。检查目标包已安装、Launcher Activity 可启动。没有 Launcher 时核实入口并传 `-Activity`，不得盲扫启动所有 Activity。
5. 检查 Python 3.10+、官方 Codex CLI 及登录。桌面版可发起，夜间执行器依赖 CLI。缺少时按官方说明安装，先核对当前 `codex exec --help`。程序要求 `--image`、`--output-schema`、`--ephemeral`、`--ignore-user-config`；不支持则更新或明确阻塞，不能自行删除约束。
6. 说明截图和 XML 会提交给用户已登录的 Codex 服务做视觉判断，CLI 调用消耗该账号额度；素材文件留在本地。使用允许被 AI 处理的测试账号和测试内容。

## 验证后启动

先在前台跑 5 步小样（`-Hours 0.15 -MaxSteps 5`），检查 PNG 能打开、XML 状态、AI 返回结构、真实焦点和路径，以及素材索引。这是真机小样，不可用单元测试替代。

```powershell
& "$env:USERPROFILE\.agents\skills\tv-adb-explorer\scripts\start.ps1" -Package "com.example.tv" -Serial "USB_SERIAL" -Out "D:\TV-Captures\app-run" -Hours 0.15 -MaxSteps 5
```

小样通过后，使用同一目录启动夜间任务：

```powershell
& "$env:USERPROFILE\.agents\skills\tv-adb-explorer\scripts\start.ps1" -Package "com.example.tv" -Serial "USB_SERIAL" -Out "D:\TV-Captures\app-run" -Hours 8 -MaxSteps 1200 -Background
```

把示例包名/序列号/输出位置换成实际值。启动后读取状态与日志确认至少又完成一轮，不能只看到 PID 就宣布成功。用户未要求立即开始时，仅完成安装与可运行配置。

- 登录、验证码、购买、人工确认等分支：保存截图和原因，退回其他分支，不暂停整项探索。
- 全局条件故障（USB 长期断开、额度不足、无法截图等）：有限重试后落盘退出；这是部分完成，不能标记成功或假装持续运行。
- 不同焦点、tab、弹窗、滚动位置均作为观察保留；页名由 AI 归类，不能仅按 Activity 去重。
- 禁止修改系统设置、购买、删除、安装、输入账号、确认许可等。程序只开放方向/确定/返回/菜单、等待、重启目标 App。OK 仍需视觉语义判断；关键词拦截不是绝对保证，先在测试设备验证。
- 重启目标 App 最多 3 次，会丢失临时页面状态；不清除 App 数据、不重启电视、不杀掉共享 ADB 服务。
- 长时间无新页面/焦点时结束并报告剩余入口，不能机械反复按键凑时长。

## 停止、恢复与交付

读取 [素材与运行约定](references/materials.md)。在输出目录创建空 `STOP` 文件可请求停止，单次 CLI 等待最长默认 180 秒。中途结束后使用相同目录续跑，先删除用户主动创建的 STOP。遗留 `run.lock` 仅在核实 PID 已退出后删除。

最终报告：已观察页面/状态数量、阻塞原因、尚未覆盖入口、设备/App 版本、停止原因和素材路径。查看 `index.html`（无需网络），结合 `REPORT.md`、`pages.json`、`transitions.json`、`blocked.json` 和逐步截图/XML 交付。`state.json` 用于续跑。

明确区分原始截图、XML、AI 解释和推测；没有实测的返回/焦点恢复/动画不能编造。素材包不含 H5 Demo，不承诺导出原始设计图层、图片资源或字体。
