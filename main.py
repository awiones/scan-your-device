import psutil
import platform
import uuid
import socket
from datetime import datetime
import cpuinfo  # Install via `pip install py-cpuinfo`
import GPUtil   # Install via `pip install gputil`
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich import box
from time import sleep

# Initialize console for Rich output
console = Console()

def get_system_info():
    info = {}

    # Using rich's status bar to show progress during each section
    with console.status("[bold green]Scanning Platform Information...") as status:
        sleep(1)  # Simulate a delay to show the status
        info["platform"] = platform.system()
        info["platform_release"] = platform.release()
        info["platform_version"] = platform.version()
        info["architecture"] = platform.machine()
        info["hostname"] = socket.gethostname()
        info["ip_address"] = socket.gethostbyname(socket.gethostname())
        info["mac_address"] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        info["processor"] = platform.processor()

    with console.status("[bold green]Scanning CPU Information...") as status:
        sleep(1)  # Simulate a delay to show the status
        info["cpu_cores"] = psutil.cpu_count(logical=False)
        info["logical_cores"] = psutil.cpu_count(logical=True)
        info["cpu_freq"] = psutil.cpu_freq().current
        info["cpu_info"] = cpuinfo.get_cpu_info()["brand_raw"]

    with console.status("[bold green]Scanning Memory Information...") as status:
        sleep(1)
        virtual_memory = psutil.virtual_memory()
        info["total_ram"] = virtual_memory.total
        info["used_ram"] = virtual_memory.used
        info["available_ram"] = virtual_memory.available
        info["ram_usage_percent"] = virtual_memory.percent

    with console.status("[bold green]Scanning Disk Information...") as status:
        sleep(1)
        disk_info = psutil.disk_usage('/')
        info["total_disk"] = disk_info.total
        info["used_disk"] = disk_info.used
        info["free_disk"] = disk_info.free
        info["disk_usage_percent"] = disk_info.percent

    with console.status("[bold green]Scanning Boot Time...") as status:
        sleep(1)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        info["boot_time"] = bt.strftime("%Y-%m-%d %H:%M:%S")

    with console.status("[bold green]Scanning Network Interfaces...") as status:
        sleep(1)
        info["network_interfaces"] = psutil.net_if_addrs()

    with console.status("[bold green]Scanning GPU Information...") as status:
        sleep(1)
        gpus = GPUtil.getGPUs()
        gpu_list = []
        for gpu in gpus:
            gpu_info = {
                "name": gpu.name,
                "load": gpu.load * 100,
                "free_memory": gpu.memoryFree,
                "used_memory": gpu.memoryUsed,
                "total_memory": gpu.memoryTotal,
                "temperature": gpu.temperature,
                "uuid": gpu.uuid
            }
            gpu_list.append(gpu_info)
        info["gpus"] = gpu_list

    # New Feature: CPU Load
    with console.status("[bold green]Scanning CPU Load...") as status:
        sleep(1)
        info["cpu_percent"] = psutil.cpu_percent(interval=1)

    # New Feature: Top 5 Memory-Consuming Processes
    with console.status("[bold green]Scanning Top Processes...") as status:
        sleep(1)
        processes = [(p.info['name'], p.info['memory_percent']) for p in psutil.process_iter(['name', 'memory_percent'])]
        info["top_processes"] = sorted(processes, key=lambda p: p[1], reverse=True)[:5]

    # New Feature: Battery Information
    with console.status("[bold green]Scanning Battery Information...") as status:
        sleep(1)
        battery = psutil.sensors_battery()
        info["battery"] = battery.percent if battery else None

    # New Feature: Temperature Sensors (if available and supported)
    if platform.system().lower() == "linux":  # Only check temperatures on Linux
        with console.status("[bold green]Scanning Temperature Sensors...") as status:
            try:
                sleep(1)
                temperatures = psutil.sensors_temperatures()
                info["temperatures"] = temperatures if temperatures else None
            except AttributeError:
                info["temperatures"] = None
    else:
        info["temperatures"] = None

    return info

def display_info(info):
    # Create a header with rich formatting
    console.rule("[bold blue]System Information Overview[/bold blue]")

    # Platform Information
    platform_table = Table(title="Platform Information", box=box.SIMPLE, style="cyan")
    platform_table.add_column("Property", style="bold magenta", justify="left")
    platform_table.add_column("Value", style="bold green")

    platform_table.add_row("Platform", info["platform"])
    platform_table.add_row("Platform Release", info["platform_release"])
    platform_table.add_row("Platform Version", info["platform_version"])
    platform_table.add_row("Architecture", info["architecture"])
    platform_table.add_row("Hostname", info["hostname"])
    platform_table.add_row("IP Address", info["ip_address"])
    platform_table.add_row("MAC Address", info["mac_address"])
    platform_table.add_row("Processor", info["processor"])
    platform_table.add_row("Physical CPU Cores", str(info["cpu_cores"]))
    platform_table.add_row("Logical CPU Cores", str(info["logical_cores"]))
    platform_table.add_row("CPU Frequency (MHz)", f"{info['cpu_freq']:.2f}")
    platform_table.add_row("CPU Info", info["cpu_info"])

    console.print(platform_table)

    # Memory Information
    memory_table = Table(title="Memory Information", box=box.SIMPLE, style="cyan")
    memory_table.add_column("Property", style="bold magenta", justify="left")
    memory_table.add_column("Value", style="bold green")

    memory_table.add_row("Total RAM", f"{info['total_ram'] // (1024 ** 3)} GB")
    memory_table.add_row("Used RAM", f"{info['used_ram'] // (1024 ** 3)} GB")
    memory_table.add_row("Available RAM", f"{info['available_ram'] // (1024 ** 3)} GB")
    
    # Add progress bar for RAM usage
    with Progress() as progress:
        ram_task = progress.add_task("[green]RAM Usage", total=100)
        progress.update(ram_task, completed=info['ram_usage_percent'])
    
    memory_table.add_row("RAM Usage (%)", f"{info['ram_usage_percent']}%")
    console.print(memory_table)

    # Disk Information
    disk_table = Table(title="Disk Information", box=box.SIMPLE, style="cyan")
    disk_table.add_column("Property", style="bold magenta", justify="left")
    disk_table.add_column("Value", style="bold green")

    disk_table.add_row("Total Disk Space", f"{info['total_disk'] // (1024 ** 3)} GB")
    disk_table.add_row("Used Disk Space", f"{info['used_disk'] // (1024 ** 3)} GB")
    disk_table.add_row("Free Disk Space", f"{info['free_disk'] // (1024 ** 3)} GB")

    # Add progress bar for Disk usage
    with Progress() as progress:
        disk_task = progress.add_task("[green]Disk Usage", total=100)
        progress.update(disk_task, completed=info['disk_usage_percent'])
    
    disk_table.add_row("Disk Usage (%)", f"{info['disk_usage_percent']}%")
    console.print(disk_table)

    # CPU Load Information
    cpu_load_panel = Panel(f"[bold green]CPU Load: {info['cpu_percent']}%[/bold green]", expand=False)
    console.print(cpu_load_panel)

    # Top 5 Memory Consuming Processes
    process_table = Table(title="Top 5 Processes by Memory Usage", box=box.SIMPLE, style="cyan")
    process_table.add_column("Process", style="bold magenta", justify="left")
    process_table.add_column("Memory Usage (%)", style="bold green")

    for process_name, memory_usage in info["top_processes"]:
        process_table.add_row(process_name, f"{memory_usage:.2f}%")
    console.print(process_table)

    # Battery Information (if available)
    if info["battery"] is not None:
        battery_panel = Panel(f"[bold yellow]Battery: {info['battery']}%[/bold yellow]", expand=False)
        console.print(battery_panel)
    else:
        console.print("[bold yellow]No battery information available.[/bold yellow]")

    # Temperature Sensors (if available and supported)
    if info["temperatures"]:
        console.rule("[bold blue]Temperature Sensors[/bold blue]")
        temp_table = Table(title="Temperature Sensors", box=box.SIMPLE, style="cyan")
        temp_table.add_column("Sensor", style="bold magenta", justify="left")
        temp_table.add_column("Temperature (°C)", style="bold green")

        for sensor, readings in info["temperatures"].items():
            for reading in readings:
                temp_table.add_row(sensor, f"{reading.current} °C")
        console.print(temp_table)
    else:
        console.print("[bold yellow]No temperature sensor information available.[/bold yellow]")

    # GPU Information (if any)
    if info["gpus"]:
        console.rule("[bold blue]GPU Information[/bold blue]")
        gpu_table = Table(title="GPU Information", box=box.SIMPLE, style="cyan")
        gpu_table.add_column("GPU Name", style="bold magenta", justify="left")
        gpu_table.add_column("Load (%)", style="bold green")
        gpu_table.add_column("Free Memory (MB)", style="bold green")
        gpu_table.add_column("Used Memory (MB)", style="bold green")
        gpu_table.add_column("Total Memory (MB)", style="bold green")
        gpu_table.add_column("Temperature (C)", style="bold green")

        for gpu in info["gpus"]:
            gpu_table.add_row(
                gpu['name'], 
                f"{gpu['load']}%", 
                f"{gpu['free_memory']} MB", 
                f"{gpu['used_memory']} MB", 
                f"{gpu['total_memory']} MB", 
                f"{gpu['temperature']} C"
            )
        console.print(gpu_table)
    else:
        console.print("[bold yellow]No GPUs found.[/bold yellow]")

if __name__ == "__main__":
    system_info = get_system_info()
    display_info(system_info)
