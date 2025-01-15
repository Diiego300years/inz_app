import psutil

def get_system_usage():
    try:
        # Pobranie ogólnego użycia CPU (procent).
        cpu_usage = psutil.cpu_percent(interval=0.1)

        # Pobranie informacji o pamięci systemowej
        memory_info = psutil.virtual_memory()
        memory_usage = {
            "percent": memory_info.percent
        }

        # Pobranie informacji o głównej partycji dyskowej (/).
        disk_info = psutil.disk_usage('/')
        disk_usage = {
            "percent": disk_info.percent
        }

        # Przygotowanie odpowiedzi o dysku.
        response = {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage
        }

        return response
    except Exception as e:
        print(f"Błąd podczas pobierania danych systemowych: {e}")
        error_response = {
            "cpu_usage": None,
            "memory_usage": {},
            "disk_usage": {}
        }
        return error_response

def get_top_resource_hungry_processes(top_n=5):
    try:
        processes = []

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                proc_info = proc.info
                proc_info['cpu_percent'] = proc.cpu_percent(interval=0.1)  # Pobranie użycia CPU
                proc_info['memory_usage_gb'] = round(proc_info['memory_info'].rss / (1024 ** 3), 2)  # Pamięć w GB
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Ignore for processes which can't be used
                continue

        response = {}
        for p in processes:
            response['name'] = p['name']
            response['cpu_percent'] = p['cpu_percent']
            response['memory_usage_gb'] = p['memory_usage_gb']

        return response
    except Exception as e:
        print(f"Błąd podczas pobierania danych procesów: {e}")
        return {
            "top_cpu_processes": [],
            "top_memory_processes": []
        }

def by_cpu(process):
    return(process['cpu_percent'])
