import psutil

def run():
    print("\n🖥️ System\n")

    print(f"CPU: {psutil.cpu_percent(interval=1)}%")
    print(f"RAM: {psutil.virtual_memory().percent}%")
