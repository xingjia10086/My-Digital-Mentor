# 💾 C 盘空间分析报告

生成时间：2026-02-19

## 📊 磁盘空间概况

| 项目 | 大小 | 百分比 |
|------|------|--------|
| **C 盘总容量** | 120 GB | 100% |
| **已使用空间** | 113.28 GB | 94.4% |
| **剩余空间** | **6.72 GB** | **5.6%** |

⚠️ **警告**：C 盘使用率已达 94.4%，严重不足！建议立即清理。

---

## 📁 空间占用分析

### 主要文件夹占用

| 文件夹 | 大小 | 说明 |
|--------|------|------|
| C:\Windows | 25.84 GB | 系统文件 |
| C:\Program Files | 19.54 GB | 64位程序 |
| C:\Windows\WinSxS | 11.45 GB | Windows 组件存储 |
| C:\Program Files (x86) | 5.89 GB | 32位程序 |
| C:\Users | 5.46 GB | 用户文件 |
| C:\Python313 | 2.73 GB | Python 环境 |

### 用户文件夹详细占用

| 文件夹 | 大小 | 说明 |
|--------|------|------|
| .gemini | 2.19 GB | Gemini AI 缓存 |
| .qoder | 0.67 GB | Qoder 缓存 |
| .bun | 0.62 GB | Bun 运行时缓存 |
| Downloads | 0.60 GB | 下载文件 |
| .antigravity | 0.53 GB | Antigravity 缓存 |
| Videos | 0.24 GB | 视频文件 |
| .vscode | 0.17 GB | VS Code 配置 |
| .trae-cn | 0.12 GB | Trae 缓存 |

### 临时文件

| 类型 | 大小 |
|------|------|
| Windows Temp | 0.21 GB |
| 用户 Temp | 0.65 GB |
| 回收站 | 0 GB |

---

## 🗑️ 清理建议（按优先级）

### 🔴 高优先级（立即清理）- 可释放约 15-20 GB

#### 1. 清理 AI 工具缓存 ⭐⭐⭐
**可释放：~3.5 GB**

```powershell
# 清理 Gemini 缓存
Remove-Item -Path "C:\Users\xingj\.gemini\*" -Recurse -Force

# 清理 Qoder 缓存
Remove-Item -Path "C:\Users\xingj\.qoder\cache\*" -Recurse -Force

# 清理 Antigravity 缓存
Remove-Item -Path "C:\Users\xingj\.antigravity\cache\*" -Recurse -Force
```

**说明**：这些是 AI 工具的缓存文件，删除后会自动重新生成，不影响使用。

#### 2. 清理 Windows 更新文件 ⭐⭐⭐
**可释放：~5-10 GB**

**方法 A：使用磁盘清理工具**
```
1. Win + R 输入：cleanmgr
2. 选择 C 盘
3. 点击"清理系统文件"
4. 勾选：
   - Windows 更新清理
   - 临时文件
   - 缩略图
   - 回收站
5. 确定清理
```

**方法 B：使用命令行**
```powershell
# 清理 Windows 更新
Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase
```

#### 3. 清理临时文件 ⭐⭐⭐
**可释放：~1 GB**

```powershell
# 清理 Windows 临时文件
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue

# 清理用户临时文件
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue

# 清理浏览器缓存（Chrome）
Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue
```

#### 4. 清理下载文件夹 ⭐⭐
**可释放：~0.6 GB**

```powershell
# 查看下载文件夹内容
Get-ChildItem "C:\Users\xingj\Downloads" | Sort-Object Length -Descending | Select-Object Name, @{Name="SizeMB";Expression={[math]::Round($_.Length / 1MB, 2)}}

# 手动删除不需要的文件
```

---

### 🟡 中优先级（建议清理）- 可释放约 5-10 GB

#### 5. 卸载不常用的程序 ⭐⭐
**可释放：~5-10 GB**

**检查已安装程序**：
```powershell
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion, InstallDate, EstimatedSize | Sort-Object EstimatedSize -Descending | Format-Table -AutoSize
```

**建议卸载**：
- 不常用的游戏
- 旧版本的开发工具
- 重复的软件

**卸载方法**：
```
设置 → 应用 → 已安装的应用 → 选择不需要的程序 → 卸载
```

#### 6. 清理 Python 缓存 ⭐⭐
**可释放：~0.5-1 GB**

```powershell
# 清理 pip 缓存
pip cache purge

# 清理 Python 编译文件
Get-ChildItem C:\Python313 -Include __pycache__ -Recurse -Force | Remove-Item -Recurse -Force
```

#### 7. 清理 Bun 缓存 ⭐
**可释放：~0.3 GB**

```powershell
# 清理 Bun 缓存
bun pm cache rm
```

---

### 🟢 低优先级（可选清理）

#### 8. 禁用休眠文件
**可释放：~4-8 GB**

```powershell
# 禁用休眠（会删除 hiberfil.sys）
powercfg -h off
```

⚠️ **注意**：禁用后无法使用休眠功能，但可以使用睡眠。

#### 9. 减小虚拟内存
**可释放：~2-4 GB**

```
1. 右键"此电脑" → 属性
2. 高级系统设置 → 性能 → 设置
3. 高级 → 虚拟内存 → 更改
4. 取消"自动管理"
5. 设置为系统管理的大小或自定义较小值
```

#### 10. 清理 Windows.old 文件夹
**可释放：~10-20 GB（如果存在）**

```powershell
# 检查是否存在
Test-Path C:\Windows.old

# 使用磁盘清理工具删除
cleanmgr
# 勾选"以前的 Windows 安装"
```

---

## 🚀 一键清理脚本

我为你创建了一个安全的清理脚本：

### 使用方法：

1. 以管理员身份运行 PowerShell
2. 复制以下命令执行

```powershell
# 创建清理脚本
$script = @'
Write-Host "=== C 盘清理脚本 ===" -ForegroundColor Green
Write-Host ""

# 1. 清理临时文件
Write-Host "[1/6] 清理临时文件..." -ForegroundColor Yellow
Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ 临时文件已清理" -ForegroundColor Green

# 2. 清理 AI 工具缓存
Write-Host "[2/6] 清理 AI 工具缓存..." -ForegroundColor Yellow
Remove-Item -Path "C:\Users\xingj\.gemini\cache\*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "C:\Users\xingj\.qoder\cache\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ AI 缓存已清理" -ForegroundColor Green

# 3. 清理浏览器缓存
Write-Host "[3/6] 清理浏览器缓存..." -ForegroundColor Yellow
Remove-Item -Path "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "✓ 浏览器缓存已清理" -ForegroundColor Green

# 4. 清理 Python 缓存
Write-Host "[4/6] 清理 Python 缓存..." -ForegroundColor Yellow
pip cache purge 2>$null
Write-Host "✓ Python 缓存已清理" -ForegroundColor Green

# 5. 清理回收站
Write-Host "[5/6] 清理回收站..." -ForegroundColor Yellow
Clear-RecycleBin -Force -ErrorAction SilentlyContinue
Write-Host "✓ 回收站已清理" -ForegroundColor Green

# 6. 运行磁盘清理
Write-Host "[6/6] 运行系统磁盘清理..." -ForegroundColor Yellow
Start-Process cleanmgr -ArgumentList "/sagerun:1" -Wait
Write-Host "✓ 系统清理完成" -ForegroundColor Green

Write-Host ""
Write-Host "=== 清理完成！===" -ForegroundColor Green
Write-Host "建议重启电脑以释放所有空间" -ForegroundColor Yellow
'@

# 保存并执行
$script | Out-File -FilePath "C:\cleanup.ps1" -Encoding UTF8
Write-Host "清理脚本已保存到 C:\cleanup.ps1"
Write-Host "请以管理员身份运行：powershell -ExecutionPolicy Bypass -File C:\cleanup.ps1"
```

---

## 📈 长期优化建议

### 1. 移动大文件到其他盘
- 将下载文件夹移到 D 盘
- 将视频、图片等大文件移到其他盘
- 将开发项目移到其他盘

### 2. 使用存储感知
```
设置 → 系统 → 存储 → 存储感知
开启自动清理临时文件
```

### 3. 定期清理
- 每周清理一次临时文件
- 每月清理一次缓存
- 每季度检查并卸载不用的程序

### 4. 考虑扩容
如果经常空间不足，建议：
- 升级到更大的 SSD
- 或添加第二块硬盘
- 或使用外置硬盘存储大文件

---

## ⚠️ 注意事项

1. **备份重要文件**：清理前先备份重要数据
2. **不要删除系统文件**：只删除明确知道的文件
3. **谨慎使用清理工具**：某些第三方清理工具可能过度清理
4. **保留至少 10% 空间**：C 盘至少保留 10-15 GB 空间

---

## 📞 需要帮助？

如果需要我帮你：
1. 执行具体的清理命令
2. 检查某个文件夹是否可以删除
3. 创建自动化清理脚本

随时告诉我！

---

**预计可释放空间：20-30 GB**
**清理后预计剩余空间：25-35 GB**
