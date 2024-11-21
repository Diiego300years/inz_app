import subprocess

import psutil


def get_active_samba_users():
    """Catch active samba users """
    try:
        result = subprocess.run("smbstatus -b | awk 'NR>1 && !/^-/{print $2, $3, $4}'",
                                shell=True, capture_output=True, text=True)
        users = []
        for line in result.stdout.splitlines():
            users.append(line.strip())

        return users[2:]
    except Exception as e:
        print(f"Error fetching Samba users: {e}")
        return []


# smbstatus -b
def get_cpu_usage():
    """Get current CPU usage percentage."""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)  # Jednosekundowy interwał dla bardziej precyzyjnego odczytu
        return cpu_usage
    except Exception as e:
        print(f"Error fetching CPU usage: {e}")
        return None

def get_memory_usage():
    """Get current RAM usage information."""
    try:
        memory_info = psutil.virtual_memory()
        ram_usage = {
            "total": memory_info.total,
            "used": memory_info.used,
            "free": memory_info.available,
            "percent": memory_info.percent
        }
        return ram_usage
    except Exception as e:
        print(f"Error fetching memory usage: {e}")
        return None

def get_swap_usage():
    """Get current swap memory usage information."""
    try:
        swap_info = psutil.swap_memory()
        swap_usage = {
            "total": swap_info.total,
            "used": swap_info.used,
            "free": swap_info.free,
            "percent": swap_info.percent
        }
        return swap_usage
    except Exception as e:
        print(f"Error fetching swap usage: {e}")
        return None
