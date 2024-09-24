#!/bin/bash

# 获取当前脚本的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 构建 start_api.sh 的完整路径
START_API_SCRIPT="$SCRIPT_DIR/start_api.sh"

# 使用 osascript 打开一个新的终端窗口并执行 start_api.sh
osascript <<EOF
tell application "Terminal"
    do script "bash '$START_API_SCRIPT'"
    activate
end tell
EOF

echo "正在启动API服务..."

# 等待API启动
max_wait_time=60
start_time=$(date +%s)
while true; do
    if nc -z 127.0.0.1 9880; then
        echo "API服务已成功启动。"
        break
    fi

    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))
    if [ $elapsed_time -ge $max_wait_time ]; then
        echo "API服务启动超时，请检查日志。"
        exit 1
    fi

    sleep 1
done

echo "API服务正在运行。新打开的终端窗口将保持运行状态。"