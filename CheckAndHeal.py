import psutil
import subprocess
import boto3
import socket
from datetime import datetime
import time
import os

# ================= CONFIG =================

REGION = "ap-south-1"
SENDER = "harshit.rathaur23@gmail.com"
RECIPIENT = "harshit.rathaur@zohomail.in"

SERVICES = ["nginx", "sshd", "crond", "docker"]

CPU_LIMIT = 80
MEM_LIMIT = 85
DISK_LIMIT = 85
MAX_SERVICE_RETRIES = 3

TEMP_DIRS = ["/tmp", "/var/tmp"]
HOSTNAME = socket.gethostname()

# ================= EMAIL =================

def send_email(subject, body):
    ses = boto3.client("ses", region_name=REGION)
    ses.send_email(
        Source=SENDER,
        Destination={"ToAddresses": [RECIPIENT]},
        Message={
            "Subject": {"Data": subject},
            "Body": {"Text": {"Data": body}}
        }
    )

# ================= DATA COLLECTION =================

def cpu_usage():
    return psutil.cpu_percent(interval=1)

def memory_usage():
    return psutil.virtual_memory().percent

def uptime_days():
    return (datetime.now() -
            datetime.fromtimestamp(psutil.boot_time())).days

def disk_usage_all():
    data = {}
    for p in psutil.disk_partitions():
        try:
            data[p.mountpoint] = psutil.disk_usage(p.mountpoint).percent
        except:
            pass
    return data

def service_status(service):
    return subprocess.getoutput(f"systemctl is-active {service}")

# ================= AUTO HEALING =================

def heal_services(service_states):
    actions = []

    for svc, state in service_states.items():
        if state == "active":
            continue

        for attempt in range(1, MAX_SERVICE_RETRIES + 1):
            subprocess.run(f"systemctl restart {svc}", shell=True)
            time.sleep(2)
            if service_status(svc) == "active":
                service_states[svc] = "active"
                actions.append(f"{svc}|RESTART|SUCCESS|Attempt {attempt}")
                break
        else:
            actions.append(f"{svc}|RESTART|FAILED|All retries used")

    return actions

def clean_temp_if_disk_high(disks):
    actions = []
    for m, u in disks.items():
        if u > DISK_LIMIT:
            for d in TEMP_DIRS:
                if os.path.isdir(d):
                    subprocess.run(f"rm -rf {d}/*", shell=True)
                    actions.append(f"{m}|DISK CLEAN|SUCCESS|{d} cleaned")
    return actions

# ================= TABLE BUILDERS =================

def build_health_table(cpu, mem, up, disks, services):
    lines = []
    lines.append("+---------------------+----------------------+")
    lines.append("| CHECK               | VALUE                |")
    lines.append("+---------------------+----------------------+")
    lines.append(f"| CPU Usage           | {cpu:>5}%               |")
    lines.append(f"| Memory Usage        | {mem:>5}%               |")
    lines.append(f"| Uptime              | {up:>5} days          |")

    for d, v in disks.items():
        lines.append(f"| Disk {d:<13} | {v:>5}%               |")

    for s, st in services.items():
        lines.append(f"| Service {s:<10} | {st:<20} |")

    lines.append("+---------------------+----------------------+")
    return "\n".join(lines)

def build_action_table(actions):
    if not actions:
        return "No auto‑healing actions were required."

    lines = []
    lines.append("+----------+-----------+---------+---------------------+")
    lines.append("| TARGET   | ACTION    | RESULT  | DETAILS             |")
    lines.append("+----------+-----------+---------+---------------------+")
    for a in actions:
        t, ac, r, d = a.split("|")
        lines.append(
            f"| {t:<8} | {ac:<9} | {r:<7} | {d:<19} |"
        )
    lines.append("+----------+-----------+---------+---------------------+")
    return "\n".join(lines)

# ================= MAIN (COMPLETE & CORRECT) =================

def main():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. Collect metrics
    cpu = cpu_usage()
    mem = memory_usage()
    up = uptime_days()
    disks = disk_usage_all()

    services = {}
    for s in SERVICES:
        services[s] = service_status(s)

    # 2. Auto‑healing
    actions = []
    actions.extend(clean_temp_if_disk_high(disks))
    actions.extend(heal_services(services))

    # 3. Build reports
    health_table = build_health_table(cpu, mem, up, disks, services)
    action_table = build_action_table(actions)

    # 4. Send email ALWAYS
    body = (
        f"SERVER HEALTH REPORT\n"
        f"Server : {HOSTNAME}\n"
        f"Time   : {timestamp}\n\n"
        f"===== HEALTH STATUS =====\n"
        f"{health_table}\n\n"
        f"===== AUTO‑HEALING ACTIONS =====\n"
        f"{action_table}"
    )

    send_email(f"SERVER REPORT – {HOSTNAME}", body)

if __name__ == "__main__":
    main()