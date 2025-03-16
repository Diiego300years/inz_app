import subprocess
import psutil


def get_active_samba_users():
    """Pozyskanie aktywnych członków sAMBA """
    try:
        users = []
        swap_group = []
        result_second = subprocess.run(
            "smbstatus -b | awk 'NR>1 && !/^-/{print $2}'",  # Pobierz kolumnę z nazwą grupy
            shell=True, capture_output=True, text=True
        )

        user_group = get_user_group(result_second)
        result = subprocess.run("smbstatus -b | awk 'NR>1 && !/^-/{print $2, $3, $4}'",
                                shell=True, capture_output=True, text=True)

        for line in result.stdout.splitlines():
            users.append(line.strip())

        swap_group = users[2:]

        for i in range(len(swap_group)):
            ans = swap_group[i].split(' ')
            ans[1] = user_group[i]
            swap_group[i] = ' '.join(ans)

        data_to_send = swap_group
        return data_to_send
    except Exception as e:
        print(f"Error fetching Samba users: {e}")
        return []

def get_samba_server_usage():
    try:
        samba_processes = []
        cpu_usage = []
        memory_usage = []

        # Iteracja po procesach związanych z Sambą
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
            if 'smb' in proc.info['name']:
                samba_processes.append(proc.info['name'])
                cpu_usage.append(proc.cpu_percent(interval=0.1))  # Pobranie CPU z krótkim interwałem
                memory_usage.append(round(proc.memory_info().rss / (1024 ** 3), 2))  # Pamięć w GB

        # Przygotowanie odpowiedzi
        response = {
            "processes": samba_processes,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }
        return response
    except Exception as e:
        print(f"Błąd podczas pobierania danych Samby: {e}")
        return {
            "cpu_usage": [],
            "memory_usage": [],
            "processes": []
        }


def get_user_group(data):
    if data.returncode == 0:
        ans = []

        for i in data.stdout.strip().split('\n')[2:]:
            print(i, "dumny?")
            command = subprocess.run(f"id -nG {i}", shell=True, capture_output=True, text=True)
            print("dziala?", command.stdout.strip().split(' '), type(command.stdout.strip()))
            result = command.stdout.strip().split(' ')
            ans.append(result[1])

        return ans
    else:
        print("Błąd:", data.stderr)
