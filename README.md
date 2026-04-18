# 🚀 Server Monitoring & Auto-Healing Tool (AWS + Python)

## 📌 Overview
A lightweight, agentless server monitoring and auto-healing tool built using Python and deployed on Amazon Web Services (AWS).

This project monitors key Linux system metrics such as CPU usage, memory utilization, disk usage, uptime, and service health. It also performs **automatic recovery actions (auto-healing)** and sends detailed email reports using AWS SES on every run.

Designed to simulate real-world **Monitoring, Alerting, and Self-Healing systems**.

---

## 🧠 Key Features

✅ Real-time monitoring of:
- CPU usage  
- Memory usage  
- Disk usage (all partitions)  
- System uptime  
- Service status (systemctl-based)  

🔁 Auto-Healing Capabilities:
- Restart failed services automatically  
- Retry service recovery up to 3 times  
- Clean `/tmp` and `/var/tmp` when disk usage is high  

📧 Automated email reports using AWS SES  

⚙️ Configurable threshold-based monitoring  

⏱️ Scheduled execution using cron jobs  

🪶 Lightweight and agentless design  

---

## 🏗️ Architecture

EC2 (Linux Server)  
   ↓  
Python Script (monitor.py)  
   ↓  
Metrics Collection (psutil, subprocess)  
   ↓  
Threshold Evaluation  
   ↓  
Auto-Healing Actions  
   ↓  
Cron Job (Every 1 hour)  
   ↓  
Email Reports (AWS SES)  

---

## 🛠️ Tech Stack

**Language:** Python  

**Libraries:**
- psutil  
- boto3  
- subprocess  
- datetime  
- socket  
- os  

**Cloud Platform:** AWS (EC2, SES)  

**Operating System:** Linux  

**Scheduler:** Cron  

---

## 📂 Project Structure

```
ServerMonitoringTool/
│
├── CheckAndHeal.py    # Main monitoring + auto-healing script
├── requirements.txt   # Python dependencies
└── README.md          # Documentation
```

---

## ⚙️ Setup & Installation

### 1️⃣ Launch EC2 Instance
- Create a Linux instance on AWS EC2  
- Allow SSH (port 22) access  

### 2️⃣ Connect to EC2
```
ssh ec2-user@your-public-ip
```

### 3️⃣ Clone Repository
```
git clone https://github.com/rathaur-hr/ServerMonitoringTool.git
cd ServerMonitoringTool
```

### 4️⃣ Install Dependencies
```
pip3 install -r requirements.txt
```

---

## ⚙️ Configuration

```
CPU_LIMIT = 80
MEM_LIMIT = 85
DISK_LIMIT = 85

SERVICES = ["nginx", "sshd", "crond", "docker"]

SENDER = "your-email@gmail.com"
RECIPIENT = "receiver@email.com"
```

---

## ⏰ Automation (Cron Job)

Set up a cron job to run every one hour:

```
crontab -e
```

Add:

```
0 * * * * /usr/bin/python3 /path/to/monitor.py
```

---

## 📧 Email Reports

The system sends:

🚨 **Server Health Report (Every Run)**  

Example:

```
| CPU Usage           |  87%                 |
| Memory Usage        |  82%                 |
| Uptime              |  5 days              |
| Disk /              |  90%                 |
| Service nginx       | inactive             |
+---------------------+----------------------+

===== AUTO-HEALING ACTIONS =====
+----------+-----------+---------+---------------------+
| TARGET   | ACTION    | RESULT  | DETAILS             |
+----------+-----------+---------+---------------------+
| nginx    | RESTART   | SUCCESS | Attempt 1           |
| /        | DISK CLEAN| SUCCESS | /tmp cleaned        |
+----------+-----------+---------+---------------------+
```
## 🧠 Learning Outcomes

- Real-world server monitoring concepts  
- Auto-healing infrastructure design  
- AWS EC2 deployment and management  
- AWS SES email integration  
- Cron job automation  
- Python system-level scripting  

---


## 👨‍💻 Author

**Harshit Rathaur**  
