README.md — Educational RAT Agent
# Educational RAT Agent

## Overview

This project demonstrates a **Remote Access Tool (RAT) agent** for Windows in a **controlled, educational environment**.  
It is designed to show **how malware-like agents interact with a command-and-control (C2) system** and execute commands on a Windows machine safely.

The agent’s core functionality includes:

- Polling a C2 server (here simulated via GitHub) for commands  
- Executing various system commands on the target machine  
- Reading local files if proper paths are provided  
- Sending results back to the C2 server  
- Demonstrating persistence techniques for educational purposes  

> ⚠️ **This project is strictly for learning purposes. Do not deploy on real systems or networks without explicit permission.**

---

## Features

### 1. Command Execution
The agent can execute a variety of commands provided in a text-based task file (`commands.txt`). Supported command types include:

- **System commands**: e.g., `whoami`, `hostname`, `dir <path>`  
- **Windows version info**: e.g., `systeminfo | findstr /B /C:"OS Name" /C:"OS Version"`, `ver`  
- **File reading**: e.g., `readfile <filepath>` to read a text file on the local machine  
- Commands can include **pipes (`|`) and arguments**  
- Commands are executed line by line in order, and the results are appended to the output file  

---

### 2. Results Reporting
- All output is sent back to a central location (simulated as `result.txt` in GitHub)  
- Outputs include both the command executed and its result  
- Example format:

```text
[CMD] <executed command>
<output>

This allows easy verification of the agent’s actions and demonstrates C2-style reporting

3. Persistence

The agent demonstrates basic persistence by copying itself to the Windows Startup folder

Ensures the agent runs automatically when the user logs in

Persistence is user-level only and works within a controlled environment

4. C2 Communication

The agent fetches commands and sends results via a remote server

In this project, GitHub simulates a C2 server:

commands.txt contains the list of tasks

result.txt collects the outputs

Conceptually, this can be replaced with a cloud-hosted Flask server, AWS, or Firebase

5. Safety Features

Only reads files that are safe and accessible

Does not modify system-critical files or directories

Designed to run in a sandboxed VM for demonstration purposes

Demonstrates RAT architecture without causing harm

Agent Capabilities (General)

The agent can:

Poll a remote server for commands

Execute system commands line by line

Read local files if paths are provided (readfile <path>)

Handle piped commands

Append output to a results file

Demonstrate basic persistence via Startup folder

Report results in a structured format to the C2

Example Commands (Demonstration)

Commands can be general-purpose and safe, for example:

whoami                  # Shows current user
hostname                # Shows target machine name
dir C:\Users            # Lists all user folders
readfile C:\Users\Public\Documents\example.txt  # Reads a safe file
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"  # OS info
ver                     # Windows version

The agent is not limited to these commands; any Windows command compatible with cmd /c can be executed

readfile works only if the file path is valid and readable

Setup and Usage
1. Clone Repository
git clone https://github.com/<username>/rat-demo.git
cd rat-demo
2. Install Dependencies
pip install requests
3. Run Agent
Option 1: Python Script
python agent.py
Option 2: Convert to Executable
pip install pyinstaller
pyinstaller --onefile agent.py

Run the generated dist/agent.exe on the target VM

4. Adding Commands

Edit commands.txt on the C2 server (or GitHub)

Agent polls the file periodically and executes any new commands

5. Viewing Results

Check result.txt on the C2 server

Shows both the command and its output

Notes

Persistence is user-level only

Reading protected system files may fail if not run as admin

The project demonstrates RAT concepts safely in a VM

C2 architecture can be swapped for Flask, Firebase, or other cloud services in conceptual demonstrations
