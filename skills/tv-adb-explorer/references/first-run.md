# 首次使用：由 Codex 带新人完成配置

适用起点：Windows 电脑已经能使用 Codex 桌面版或 CLI；其他环境可能完全没装。新人不需要先学命令或提供一份完整环境清单。

## 引导方式

- 先说：“我会先检查电脑环境，再补齐缺少的软件，最后带你连接电视并做 5 步试跑。需要你接线、授权或登录时，我会一次只提示一件事。”随后执行检查，不要只给用户一张安装清单。
- 检查、下载、解压、运行安装入口、版本验证、设备查询、包名查询、配置写入和小样结果整理，由 AI 自动做。沿用用户已授权的首次配置范围，不重复问是否执行每条普通命令。
- 必须人工完成时，给出当前唯一操作、完成标志和下一步。例如：“请看电视，勾选始终允许这台电脑并确认 USB 调试；完成后告诉我。”用户确认后立即重查实际状态，不能只凭口头确认判定通过。
- 登录、许可、管理员权限、接线是首次配置环节，不能像探索中的 App 登录页一样跳过。与 TV App 内部的登录分支区分：前者阻塞启动，后者记录并继续其他路径。
- 不展示密码、令牌或整个 Codex 配置；不要求用户把登录凭据发到聊天。软件许可、系统提权和浏览器登录交给用户本人处理。
- 使用 Windows 原生 PowerShell、Python、ADB 和 Codex CLI；此执行器不自动切换到 WSL，避免 USB 与路径跨环境问题。

## 0. 下载与安装 Skill（AI 执行）

若已经在完整仓库目录，直接读取文件并执行根目录 `install.ps1`。否则无需安装 Git，使用 PowerShell 下载 GitHub ZIP。下面代码中的变量只作用于当前会话：

```powershell
$tvBase = Join-Path $env:LOCALAPPDATA 'TVAdbExplorer'
$tvDownload = Join-Path $tvBase ('source-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Force -Path $tvDownload | Out-Null
$tvZip = Join-Path $tvDownload 'source.zip'
Invoke-WebRequest 'https://github.com/Autumnx7/tv-adb-explorer/archive/refs/heads/main.zip' -OutFile $tvZip -UseBasicParsing
Expand-Archive -Path $tvZip -DestinationPath $tvDownload
$tvRepo = Join-Path $tvDownload 'tv-adb-explorer-main'
```

检查 `$tvRepo\README.md`、`$tvRepo\skills\tv-adb-explorer\SKILL.md` 和安装脚本，随后执行：

```powershell
& (Join-Path $tvRepo 'install.ps1')
$tvSkill = Join-Path $env:USERPROFILE '.agents\skills\tv-adb-explorer'
```

已安装时先比较版本/文件内容，复用可用版本；升级先备份，不直接覆盖自定义内容。安装后在当前聊天读取 `$tvSkill\SKILL.md` 即可继续引导，不必强制新人重开聊天。新聊天是否自动发现技能取决于 Codex 版本，可显式调用 `$tv-adb-explorer`。

若下载失败，先检查网络或让用户下载 ZIP；不要让用户同时安装 Git、Android Studio 等非必要软件。若 PowerShell 执行策略阻止脚本，核对组织策略和具体错误；只处理被阻止的文件，不永久降低整机策略。

## 1. 自动检测，再只安装缺少的依赖

先执行只读检查并记录可执行文件位置和版本：

```powershell
$PSVersionTable.PSVersion
Get-Command py, python, node, npm, codex, adb, winget -ErrorAction SilentlyContinue |
    Select-Object Name, Source
```

对存在的命令单独验证，某项失败不要掩盖其他项的结果：

| 项目 | 实测方法 | 缺少时由 AI 执行 |
|---|---|---|
| Python 3.10+ | `py -3 --version`，没有 py 再检查 `python --version` | 用 WinGet 查找官方 Python，核对发布者、版本、安装器来源后安装；无 WinGet 时从 python.org 获取官方 Windows 安装器 |
| Codex CLI | `codex --version`、`codex exec --help` | 按当前官方 CLI 文档安装；有 npm 可用 `npm install -g @openai/codex` |
| Node.js / npm | 仅在选择 npm 安装 Codex 时检查 `node --version`、`npm --version` | 用 WinGet 查找 OpenJS Node.js LTS，核对后安装；已有独立 Codex CLI 则不必安装 Node |
| ADB | `adb version`；同时检查 Android SDK 与本工具已有安装 | 运行下一节 setup.ps1，复用现有官方安装或下载官方 Platform Tools |

WinGet 的常见候选 ID 为 `Python.Python.3.12`、`OpenJS.NodeJS.LTS`。**先用 `winget search` / `winget show --id ID --exact` 确认当前可用和来源，再执行 `winget install --id ID --exact --no-upgrade`**。它们是候选，不是保证永远存在的包名。优先用户范围（安装器支持时使用 `--scope user`）；不支持时让用户处理系统权限提示。不为了省步骤默认代替用户接受新协议或安装无关组件。

安装后新进程可能尚未读取 PATH，AI 可用已验证的绝对路径或重新载入 Machine/User PATH 到当前进程，再实测版本；不要仅凭安装器退出就宣布成功，也不要覆盖系统 PATH。若 `npm.ps1` 被策略阻止，可使用已验证的同目录 `npm.cmd`，不放宽整机执行策略。

## 2. 配置 ADB（AI 执行，许可由用户确认）

```powershell
& (Join-Path $tvSkill 'scripts\setup.ps1')
```

如果有官方 ADB 就复用。如果明确提示尚未接受 Android SDK 许可，向用户提供官方许可页面，让用户自行阅读并确认；获得确认后才传 `-AcceptAndroidSdkLicense` 重试。

- AI 自动下载、解压、运行 `adb version` 并读取生成的 `%LOCALAPPDATA%\TVAdbExplorer\config.json`。
- 设备还没连接时，空设备列表不代表 ADB 安装失败；保留配置，继续接线环节。
- 系统中多个 adb 版本时明确选择一个，后续始终用其绝对路径。

## 3. 首次连接电视（一次只引导一个人工操作）

1. **接线**：先让用户按厂商要求连接 USB 调试接口和数据线，再自动执行 `adb devices -l`。
2. **没有设备**：询问电视型号，查厂商官方调试端口和接线说明。Windows 设备管理器存在未识别设备时核查 OEM 驱动；AI 能定位和下载官方驱动，用户只处理必要的安装/管理员提示。不要把所有空列表都归因于驱动。
3. **开启调试**：指导用户按该机型开启 USB 调试，再自动查询。
4. **unauthorized**：只提示用户在电视上接受这台电脑的 RSA 授权，再自动查询。不可绕过或伪造授权。
5. **device**：单台实体设备可自动选定并告诉用户；多台设备才让用户选择。后续每条 ADB 命令都指定 `-s SERIAL`。

普通 USB host 口不保证支持 USB ADB。确认硬件不支持后明确说明此 Skill 的 USB 前提未满足，不循环安装驱动、不擅自改成网络连接。详细排错见 [windows.md](windows.md)。

## 4. 检查 Codex CLI 登录（AI 检查，用户登录）

先执行 `codex login status`，不要假设桌面版登录必然通用于 CLI。已登录则直接继续；没登录时指导用户在可见的本机终端执行 `codex login`，自行在浏览器完成，然后 AI 重查状态。若当前 CLI 不支持状态命令，读取该版本 `codex login --help`，以实际支持方式验证。

检查 `codex exec --help` 的必要参数；不支持则按官方方法更新 CLI，并再次检查。不要为了无人值守打开绕过审批/沙箱选项。

## 5. 确定 App 和素材目录（AI 查询，新人选择）

先问：“你要探索哪个 App？告诉我名字或包名即可。”如果用户已经提供，不重复问。

- 已提供包名：用 `adb -s SERIAL shell pm path PACKAGE` 验证。
- 只知道名称：列出包或让用户先在电视打开目标 App，再通过当前前台窗口识别候选包名。多个候选时只请用户选一次，不猜。
- 默认目录可建议为用户 Documents 下 `TV-Captures\包名-日期时间`，检查写权限、磁盘剩余量；用户指定目录优先。把实际路径告诉用户，不把个人路径提交仓库。
- 说明截图与 UI 文字会发送给已登录的 Codex 做判断并消耗额度，使用允许 AI 处理的测试内容；输出素材不自动上传 GitHub。

## 6. 先做 5 步小样，再准备无人值守

按 SKILL.md 使用实际 Package、Serial、Out 调用 `start.ps1 -Hours 0.15 -MaxSteps 5`。AI 自动：

- 检查程序退出状态、PNG 可打开、XML 成功或明确缺失、决策 JSON 和实际操作记录。
- 对照前后截图判断焦点或页面是否确实变化；若无法判断，告知用户并请看一次电视，不冒充真机验收完成。
- 打开素材索引，简述抓到了什么、缺了什么。
- 小样失败则排查后复跑，不启动整夜进程。

只发链接代表开始首次引导，不默认等于授权立即消耗整夜额度。完成小样后，若用户此前尚未要求开始夜间采集，简短询问一次是否现在开始（默认上限 8 小时 / 1200 步）；已有明确授权直接执行。

夜间启动后至少核实新增一条完成记录，而不是只看到 PID。提示用户电脑插电、不合盖、不关机，电视不要待机，电脑网络要可用。告诉用户素材路径和 STOP 停止方式。此后的 App 登录/人工分支按探索规则记录并跳过。

## 7. 留下可恢复的首次配置记录

把进度存到本地 `%LOCALAPPDATA%\TVAdbExplorer\onboarding.json`，每完成一阶段更新：

```json
{
  "schema_version": 1,
  "stage": "device_connected",
  "checks": {"skill": "passed", "python": "passed", "codex_cli": "passed", "adb": "passed", "device": "passed", "codex_login": "pending", "smoke_test": "pending"},
  "paths": {"skill": "actual path", "adb": "actual path", "python": "actual path"},
  "serial": "actual USB serial",
  "package": null,
  "output_dir": null,
  "next_action": "Check Codex CLI login"
}
```

这份记录由引导 AI 维护，探索脚本不会自动读取它；不能原样写入示例占位符或存密码/token。下次读取记录后仍复核程序、USB 和登录状态，从未完成环节继续。最后清楚区分“环境就绪”“小样通过”“夜间已启动”三种状态。

## 官方依据

- Codex CLI：https://learn.chatgpt.com/docs/codex/cli
- WinGet 安装与精确包选择：https://learn.microsoft.com/en-us/windows/package-manager/winget/install
- Android Platform Tools 与许可：https://developer.android.com/tools/releases/platform-tools
