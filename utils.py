import time
import os
import threading
import subprocess
import socket

# 为了debug我封装了一些函数...

def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

def path_exists(path):
    path = os.path.expanduser(path)
    return os.path.exists(path)

def exec(command):
    # print('\n\n\nExecuting:', command, sep=' ')
    os.system(command)
    time.sleep(1/10)

def start(func):
    # print('\n\n\nstarting:', func.__name__)
    thread = threading.Thread(target=func)
    thread.start()
    time.sleep(1/10)
    return thread

def _get_local_ip():
    # 获取本机ip
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 任意创建一个socket，观察操作系统提供的ip
    s.connect(('google.com', 12346))
    ip = s.getsockname()[0]
    s.close()
    return ip

local_ip = _get_local_ip()

# 下载编译好的masquerade，保存在~/masque-linux
# if not path_exists('~/masque-linux'):
#     exec('''
#         cd ~
#         rm -rf ~/masque-linux
#         sudo git clone https://github.com/dx2102/masque-linux
#         cd ~/masque-linux
#         sudo chmod a+rwx -R .
#         ''')
#     time.sleep(0.5)

def kill_process_on_port(port, wait=0.1):
    try:
        # 使用 lsof 命令查找监听指定端口的进程并获取其PID
        cmd = f"lsof -i :{port} -t"
        output = subprocess.check_output(cmd, shell=True)
        pids = output.decode('utf-8').split('\n')
        
        for pid in pids:
            if pid:
                pid = int(pid)
                # 终止进程
                subprocess.call(['kill', '-9', str(pid)])
                print(f"Terminated process with PID {pid}")
    except subprocess.CalledProcessError:
        print(f"No process found listening on port {port}")
    finally:
        time.sleep(wait)
