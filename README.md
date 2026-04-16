## 🚀 Server Monitoring & Auto-Healing System (Python + AWS)

### 📌 Overview
A production-ready Python-based monitoring system that continuously tracks server health and automatically performs corrective actions when issues are detected.

This tool not only monitors system metrics but also **self-heals services and disk issues**, and sends detailed reports via **AWS SES email notifications**.

---

## 🔍 Features

### ✅ System Monitoring
- CPU Usage (real-time)
- Memory Utilization
- Disk Usage (all mounted partitions)
- Service Health Monitoring:
  - nginx
  - sshd
  - crond
  - docker
- System Uptime Tracking

---

### ⚠️ Intelligent Thresholds
| Metric | Threshold |
|-------|----------|
| CPU Usage | > 80% |
| Memory Usage | > 85% |
| Disk Usage | > 85% |

---

### 🔁 Auto-Healing Capabilities
- 🔄 Automatically restarts failed services using `systemctl`
- 🔁 Retries service restart up to **3 times**
- 🧹 Cleans `/tmp` and `/var/tmp` when disk usage is high
- 📊 Maintains structured action logs

---

### 📩 Email Reporting (AWS SES)
- Sends **detailed health reports every run**
- Includes:
  - System metrics table
  - Service status
  - Auto-healing actions performed
- Uses **AWS SES (Simple Email Service)** for reliable delivery

---

## 🛠️ Tech Stack

- **Python**
- **psutil**
- **AWS SES (boto3)**
- **Linux (systemctl, cron)**
- **Shell commands via subprocess**

---

## 📂 Project Structure

```
monitoring-auto-healing/
│
├── monitor.py        # Main script (monitor + heal + report)
└── README.md
```

---

## ⚙️ Configuration

Update these variables in your script:

```python
REGION = "ap-south-1"
SENDER = "your-email@gmail.com"
RECIPIENT = "recipient@email.com"

SERVICES = ["nginx", "sshd", "crond", "docker"]

CPU_LIMIT = 80
MEM_LIMIT = 85
DISK_LIMIT = 85
```

---

## ▶️ How It Works

1. Script collects system metrics using `psutil`
2. Checks all configured services via `systemctl`
3. If any issue detected:
   - Restarts service (with retries)
   - Cleans temp directories if disk is high
4. Builds:
   - 📊 Health Status Table
   - ⚙️ Auto-Healing Action Table
5. Sends full report via AWS SES

---

## 🧪 Sample Output (Email Report)

```
SERVER HEALTH REPORT
Server : ip-172-31-xx-xx
Time   : 2026-04-17 12:00:00

===== HEALTH STATUS =====
+---------------------+----------------------+
| CHECK               | VALUE                |
+---------------------+----------------------+
| CPU Usage           |  87%                 |
| Memory Usage        |  82%                 |
| Uptime              |   5 days             |
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

---

## ☁️ AWS SES Setup (Required)

1. Verify sender email in AWS SES  
2. Move SES out of sandbox (or verify recipient)  
3. Configure IAM permissions for SES  

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ⏰ Automation (Cron Job)

Run script every hour:

```bash
crontab -e
```

```
0 * * * * python3 /path/to/monitor.py
```

---

## 🔐 Permissions Required

- `systemctl` access (root or sudo)
- Permission to delete temp files (`/tmp`, `/var/tmp`)
- AWS IAM role/user with SES access

---

## 📌 Key Highlights (For Recruiters)

- Real-world **self-healing infrastructure simulation**
- Integration with **AWS SES for automated reporting**
- Handles **service failures + disk issues automatically**
- Uses **retry logic and structured reporting**
- Fully deployable on **Linux + AWS EC2**

---

# 📦 requirements.txt

```
psutil==5.9.8
boto3==1.34.0
botocore==1.34.0
```

## 👨‍💻 Author

**Harshit Rathaur**  
