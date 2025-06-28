# ScanForge

ScanForge is a Python-based port scanner designed for network security professionals and ethical hackers.

## Legal Disclaimer and Educational Use

**Important:** This tool is intended for **educational purposes only**.

*   **Legal Warnings:** Unauthorized scanning of networks or systems is illegal and unethical in many jurisdictions. You are solely responsible for ensuring that you have explicit permission to scan any target.
*   **Fair Use:** This tool should only be used in compliance with all applicable laws and regulations, and with the express consent of the system owner.

By using this tool, you acknowledge and agree to these terms. The developers are not responsible for any misuse or damage caused by this tool.

## Features

- Scan single IP addresses or domain names
- Scan IP address ranges (e.g., 192.168.1.1-192.168.1.10)
- Customizable port ranges
- Multi-threaded scanning for faster results
- Service detection for open ports
- Progress bar with estimated completion time
- Colorful and informative output
- Support for both IPv4 addresses

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ScanForge.git
cd ScanForge
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

1. Scan a single IP address:
```bash
python portscanner.py 192.168.1.1
```

2. Scan a domain name:
```bash
python portscanner.py example.com
```

3. Scan an IP range:
```bash
python portscanner.py 192.168.1.1-192.168.1.10
```

### Advanced Options

1. Custom port range:
```bash
python portscanner.py example.com -p 1-1000
```

2. Custom timeout:
```bash
python portscanner.py example.com -t 2
```

3. Custom thread count:
```bash
python portscanner.py example.com -n 200
```

4. Combine options:
```bash
python portscanner.py 192.168.1.1-192.168.1.10 -p 1-1000 -t 1 -n 200
```

## Command Line Arguments

- `target`: Target IP address, domain name, or IP range (e.g., 192.168.1.1-192.168.1.10)
- `-p, --ports`: Port range to scan (default: 1-1024)
- `-t, --timeout`: Connection timeout in seconds (default: 1)
- `-n, --threads`: Number of threads to use (default: 100)

## Output Format

The scanner provides detailed output including:
- Target information
- Scan progress
- Open ports with service names
- Scan summary

Example output:
```
[*] Starting ScanForge port scanner
[*] Target: 192.168.1.1
[*] Port range: 1-1024
[*] Threads: 100
[*] Timeout: 1s
[*] Scan started at: 2024-03-14 10:00:00

[+] 192.168.1.1 - Port 80: http
[+] 192.168.1.1 - Port 443: https
[+] 192.168.1.1 - Port 22: ssh

[*] Scan completed at: 2024-03-14 10:00:05
[*] Total ports scanned: 1024
[*] Open ports found: 3
```

## Requirements

- Python 3.6 or higher
- colorama
- tqdm

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Made by toonscascade

## Acknowledgments

- Thanks to all contributors and users
- Inspired by various network security tools
- Built for educational purposes

## What is Port Scanning?

Port scanning is like checking which doors are open on a computer. Each port is like a door that different programs use to talk to each other. This tool helps you see which doors are open and what's behind them.

## What Can This Tool Do?

- Easy to use with simple commands
- Shows a progress bar so you know what's happening
- Tells you what programs are running on open ports
- Works with website names and IP addresses
- Lets you choose which ports to check

## How to Get Started

1. Download the Tool
   - Click the green "Code" button
   - Click "Download ZIP"
   - Put the folder somewhere on your computer

2. Install Python
   - Go to python.org
   - Download Python
   - Run the installer (check "Add Python to PATH")

3. Install Required Files
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Go to the ScanForge folder
   - Type this:
   ```
   pip install -r requirements.txt
   ```

4. Run Your First Scan
   ```
   python portscanner.py example.com
   ```

## How to Use It

### Basic Use
Just type this and press Enter:
```
python portscanner.py example.com
```

### Advanced Use
When you're ready to try more options:
```
python portscanner.py example.com -p 1-1000 -t 2 -n 200
```

### What the Options Mean
- target: The website or IP address to scan
- -p, --ports: Which ports to check (like 1-1000)
- -t, --timeout: How long to wait for a response (in seconds)
- -n, --threads: How many ports to check at once

## Important Safety Note

Please remember:
- Only scan computers you own or have permission to test
- Scanning without permission is not allowed
- This tool is for learning about networks

## Need Help?

If you're stuck, try these:
1. Make sure Python is installed correctly
2. Check that you're in the right folder
3. Try the basic command first
4. Read any error messages carefully

## Learning Resources

Here are some helpful websites to learn more:
- What is Port Scanning? (varonis.com/blog/port-scanning)
- Understanding Network Ports (cloudflare.com/learning/network-layer/what-is-a-computer-port)
- Python for Beginners (python.org/about/gettingstarted)

## Questions?

If you have questions or find something confusing:
- Open an issue on GitHub
- Ask in the discussions section
- Send me a message

Remember: Everyone starts somewhere! Don't be afraid to try things and learn.

Happy learning! 