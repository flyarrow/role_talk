import subprocess
import time
import os
import sys

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def start_api():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    start_script = os.path.join(script_dir, "open_terminal_and_start_api.sh")

    if is_port_in_use(9880):
        print("API已经在运行，端口9880被占用。")
        return

    print("正在新终端窗口中启动API...")
    
    # 使用新脚本在新终端窗口中启动API
    subprocess.run(['bash', start_script], check=True)

    # 等待API启动
    for _ in range(60):  # 等待时间为60秒
        if is_port_in_use(9880):
            print("API已成功启动。")
            return
        time.sleep(1)
        print("等待API启动...", flush=True)

    print("API启动超时。请检查新打开的终端窗口以获取更多信息。")
    sys.exit(1)

if __name__ == "__main__":
    start_api()