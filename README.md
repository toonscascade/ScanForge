# ScanForge

ScanForge is a Python-based port scanner.

## Legal Disclaimer and Educational Use

**Important:** This tool is intended for **educational purposes only**.

*   **Legal Warnings:** Unauthorized scanning of networks or systems is illegal and unethical in many jurisdictions. You are solely responsible for ensuring that you have explicit permission to scan any target.
*   **Fair Use:** This tool should only be used in compliance with all applicable laws and regulations, and with the express consent of the system owner.

By using this tool, you acknowledge and agree to these terms. The developers are not responsible for any misuse or damage caused by this tool.

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