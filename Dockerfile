FROM python:3.10

WORKDIR /app

# 简化依赖安装，跳过可能不稳定的 apt-get update
# 如果需要 ffmpeg，可以在运行环境动态处理或选择更大但更全的镜像
# 这里使用 python:3.10 (非 slim 版) 通常包含更多基础工具

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目所有文件
COPY . .

# 暴露 Streamlit 默认端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动命令
ENTRYPOINT ["streamlit", "run", "web_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
