# Scan Your Device

`Scan Your Device` is a Python tool that displays detailed information about the system, including hardware, CPU, memory, GPU, disk usage, and more. It is useful for users who might not be familiar with their system's hardware and specifications.

## Features

- Platform Information (OS, Architecture, Hostname, IP, MAC Address, Processor)
- CPU Information (Physical/Logical Cores, Frequency, Brand)
- Memory Information (Total, Used, Available RAM)
- Disk Information (Total, Used, Free Space)
- Boot Time
- Network Interfaces
- GPU Information (Load, Memory, Temperature)
- CPU Load Percentage
- Top 5 Memory-Consuming Processes
- Battery Information (if available)
- Temperature Sensors (for Linux)
  
## Requirements

Install the required Python packages before running the tool:

```bash
pip install psutil py-cpuinfo gputil rich
```
or
```bash
pip install -r requirements.txt
```
## Usage

To run the tool, simply execute the Python script:

```bash
python main.py
```

The script will scan and display system information using the [Rich](https://rich.readthedocs.io/en/stable/) library for a visually appealing output in the terminal.

### Sample Output

```
System Information Overview
----------------------------

Platform: Linux
Architecture: x86_64
Processor: Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz
...
```

## Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please submit a pull request or open an issue.

- **Fork the Repository**: Create a personal copy of the repository on GitHub.
- **Make Changes**: Implement your changes and test them locally.
- **Submit a Pull Request**: Describe your changes and submit a pull request for review.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Awiones

