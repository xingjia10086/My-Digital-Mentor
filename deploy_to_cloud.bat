@echo off
setlocal
chcp 65001 >nul

echo ==============================================================
echo 🚀 星佳数字分答后台 - 一键上云部署脚本 (Google Cloud Run)
echo ==============================================================
echo 准备将本地知识库 (1.8万切片) 和系统打包成镜像并上传至 GCP。
echo.

echo [1/3] 正在验证并配置 GCP 项目环境...
call gcloud config set project gen-lang-client-0834352502

echo.
echo [2/3] 正在发往云端构建容器并发布上线 (这可能需要几分钟，请耐心等待)...
call gcloud run deploy ai-mentor-web ^
  --source . ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --memory 4Gi ^
  --cpu 2 ^
  --max-instances 2 ^
  --port 8080

echo.
echo [3/3] 部署完成验证...
if %ERRORLEVEL% equ 0 (
    echo ✅ 部署成功！您可以将上方终端显示的 URL 发送给您的客户了。
    echo ⚠️ 访问口令为：xingjia2026
) else (
    echo ❌ 部署过程中发生错误，请检查。
)

pause
