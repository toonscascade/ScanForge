#!/usr/bin/env python3

import socket
import sys
import time
from datetime import datetime
import threading
from queue import Queue
import argparse
from colorama import init, Fore, Style
from tqdm import tqdm
import os
import ipaddress

# Initialize colorama
init()

def show_banner():
    """Print a fancy banner for the tool."""
    banner = f"""
{Fore.CYAN}╔════════════════════════════════════════════════════════════╗
║                                                                ║
║  {Fore.GREEN}█████ {Fore.GREEN}█████ {Fore.GREEN}█████ {Fore.GREEN}█   █ {Fore.BLUE}█████ {Fore.BLUE}█████ {Fore.GREEN}█████ {Fore.GREEN}█████ {Fore.GREEN}█████{Fore.CYAN}  ║
║  {Fore.GREEN}█     {Fore.GREEN}█     {Fore.GREEN}█   █ {Fore.GREEN}██  █ {Fore.BLUE}█     {Fore.BLUE}█   █ {Fore.GREEN}█   █ {Fore.GREEN}█     {Fore.GREEN}█    {Fore.CYAN}  ║
║  {Fore.GREEN}█████ {Fore.GREEN}█     {Fore.GREEN}█████ {Fore.GREEN}█ █ █ {Fore.BLUE}█████ {Fore.BLUE}█   █ {Fore.GREEN}█████ {Fore.GREEN}█ ███ {Fore.GREEN}█████{Fore.CYAN}  ║
║  {Fore.GREEN}    █ {Fore.GREEN}█     {Fore.GREEN}█   █ {Fore.GREEN}█  ██ {Fore.BLUE}█     {Fore.BLUE}█   █ {Fore.GREEN}█  █  {Fore.GREEN}█   █ {Fore.GREEN}█    {Fore.CYAN}  ║
║  {Fore.GREEN}█████ {Fore.GREEN}█████ {Fore.GREEN}█   █ {Fore.GREEN}█   █ {Fore.BLUE}█     {Fore.BLUE}█████ {Fore.GREEN}█   █ {Fore.GREEN}█████ {Fore.GREEN}█████{Fore.CYAN}  ║
║                                                                ║
║  {Fore.YELLOW}Port Scanner for Ethical Hackers and Network Engineers{Fore.CYAN}     ║
║  {Fore.YELLOW}Version 1.0.0{Fore.CYAN}                                           ║
║  {Fore.MAGENTA}Made by toonscascade{Fore.CYAN}                                    ║
╚════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def ip_range_to_list(ip1, ip2):
    """Convert IP range to list of IPs."""
    try:
        start = ipaddress.IPv4Address(ip1)
        end = ipaddress.IPv4Address(ip2)
        return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start), int(end) + 1)]
    except ValueError as e:
        print(f"{Fore.RED}[!] Error: Invalid IP range - {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

class PortScanner:
    def __init__(self, host, port_start=1, port_end=1024, timeout=1, num_threads=100):
        self.host = host
        self.port_start = port_start
        self.port_end = port_end
        self.timeout = timeout
        self.num_threads = num_threads
        self.q = Queue()
        self.open_ports = []
        self.lock = threading.Lock()
        self.total = port_end - port_start + 1
        self.done = 0
        self.bar = None

    def port_service(self, port):
        """Get service name for a given port."""
        try:
            return socket.getservbyport(port)
        except:
            return "unknown"

    def check_port(self, port):
        """Scan a single port and return its status."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            res = s.connect_ex((self.host, port))
            if res == 0:
                service = self.port_service(port)
                with self.lock:
                    self.open_ports.append((port, service))
                    if self.bar:
                        self.bar.write(f"{Fore.GREEN}[+] {self.host} - Port {port} is open - {service}{Style.RESET_ALL}")
            s.close()
        except socket.error:
            pass
        finally:
            with self.lock:
                self.done += 1
                if self.bar:
                    self.bar.update(1)

    def thread_worker(self):
        """Worker thread function."""
        while True:
            port = self.q.get()
            if port is None:
                break
            self.check_port(port)
            self.q.task_done()

    def run(self):
        """Start the port scanning process."""
        print(f"\n{Fore.CYAN}[*] Let's scan some ports!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {self.host}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Port range: {self.port_start}-{self.port_end}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Threads: {self.num_threads}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Timeout: {self.timeout}s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")

        # Create progress bar
        self.bar = tqdm(
            total=self.total,
            desc=f"{Fore.CYAN}Scanning{Style.RESET_ALL}",
            unit="ports",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )

        # Create and start worker threads
        threads = []
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.thread_worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # Add ports to queue
        for port in range(self.port_start, self.port_end + 1):
            self.q.put(port)

        # Wait for all ports to be scanned
        self.q.join()

        # Stop worker threads
        for _ in range(self.num_threads):
            self.q.put(None)
        for t in threads:
            t.join()

        # Close progress bar
        if self.bar:
            self.bar.close()

        # Print scan summary
        print(f"\n{Fore.CYAN}[*] Done at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Ports scanned: {self.total}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Open ports: {len(self.open_ports)}{Style.RESET_ALL}")
        
        if self.open_ports:
            print(f"\n{Fore.CYAN}[*] Here's what we found:{Style.RESET_ALL}")
            for port, service in sorted(self.open_ports):
                print(f"{Fore.GREEN}[+] {self.host} - Port {port}: {service}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[!] No open ports found in that range{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}[*] All done!{Style.RESET_ALL}")

def main():
    # Clear screen and print banner
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()

    parser = argparse.ArgumentParser(
        description='ScanForge - A Python-based port scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.YELLOW}Examples:{Style.RESET_ALL}
  Basic scan:              python portscanner.py example.com
  IP range scan:          python portscanner.py 192.168.1.1-192.168.1.10
  Custom port range:       python portscanner.py example.com -p 1-1000
  Custom timeout:          python portscanner.py example.com -t 2
  Custom thread count:     python portscanner.py example.com -n 200

{Fore.YELLOW}Note:{Style.RESET_ALL} Always ensure you have permission before scanning any system.
"""
    )
    parser.add_argument('target', help='Target IP address, domain name, or IP range (e.g., 192.168.1.1-192.168.1.10)')
    parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1024)', default='1-1024')
    parser.add_argument('-t', '--timeout', type=float, help='Connection timeout in seconds', default=1)
    parser.add_argument('-n', '--threads', type=int, help='Number of threads', default=100)
    
    args = parser.parse_args()

    try:
        # Check if target is an IP range
        if '-' in args.target:
            ip1, ip2 = args.target.split('-')
            targets = ip_range_to_list(ip1, ip2)
        else:
            # Resolve domain name to IP if needed
            print(f"{Fore.CYAN}[*] Resolving target...{Style.RESET_ALL}")
            ip = socket.gethostbyname(args.target)
            print(f"{Fore.GREEN}[+] Target resolved to: {ip}{Style.RESET_ALL}")
            targets = [ip]
        
        # Parse port range
        port_start, port_end = map(int, args.ports.split('-'))
        
        # Scan each target
        for tgt in targets:
            scanner = PortScanner(
                host=tgt,
                port_start=port_start,
                port_end=port_end,
                timeout=args.timeout,
                num_threads=args.threads
            )
            scanner.run()

    except socket.gaierror:
        print(f"\n{Fore.RED}[!] Error: Could not resolve hostname{Style.RESET_ALL}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Scan interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
