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

# Initialize colorama
init()

def print_banner():
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

class ScanForge:
    def __init__(self, target, start_port=1, end_port=1024, timeout=1, threads=100):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.timeout = timeout
        self.threads = threads
        self.port_queue = Queue()
        self.open_ports = []
        self.lock = threading.Lock()
        self.total_ports = end_port - start_port + 1
        self.scanned_ports = 0
        self.progress_bar = None

    def get_service_name(self, port):
        """Get service name for a given port."""
        try:
            service = socket.getservbyport(port)
            return service
        except:
            return "unknown"

    def scan_port(self, port):
        """Scan a single port and return its status."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((self.target, port))
            if result == 0:
                service = self.get_service_name(port)
                with self.lock:
                    self.open_ports.append((port, service))
                    if self.progress_bar:
                        self.progress_bar.write(f"{Fore.GREEN}[+] Port {port} is open - {service}{Style.RESET_ALL}")
            sock.close()
        except socket.error:
            pass
        finally:
            with self.lock:
                self.scanned_ports += 1
                if self.progress_bar:
                    self.progress_bar.update(1)

    def worker(self):
        """Worker thread function."""
        while True:
            port = self.port_queue.get()
            if port is None:
                break
            self.scan_port(port)
            self.port_queue.task_done()

    def start_scan(self):
        """Start the port scanning process."""
        print(f"\n{Fore.CYAN}[*] Starting ScanForge port scanner{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Target: {self.target}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Port range: {self.start_port}-{self.end_port}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Threads: {self.threads}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Timeout: {self.timeout}s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}\n")

        # Create progress bar
        self.progress_bar = tqdm(
            total=self.total_ports,
            desc=f"{Fore.CYAN}Scanning ports{Style.RESET_ALL}",
            unit="ports",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
        )

        # Create and start worker threads
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            threads.append(t)

        # Add ports to queue
        for port in range(self.start_port, self.end_port + 1):
            self.port_queue.put(port)

        # Wait for all ports to be scanned
        self.port_queue.join()

        # Stop worker threads
        for _ in range(self.threads):
            self.port_queue.put(None)
        for t in threads:
            t.join()

        # Close progress bar
        if self.progress_bar:
            self.progress_bar.close()

        # Print scan summary
        print(f"\n{Fore.CYAN}[*] Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Total ports scanned: {self.total_ports}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Open ports found: {len(self.open_ports)}{Style.RESET_ALL}")
        
        if self.open_ports:
            print(f"\n{Fore.CYAN}[*] Open ports and services:{Style.RESET_ALL}")
            for port, service in sorted(self.open_ports):
                print(f"{Fore.GREEN}[+] Port {port}: {service}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}[!] No open ports found in the specified range{Style.RESET_ALL}")

        print(f"\n{Fore.CYAN}[*] Scan completed successfully!{Style.RESET_ALL}")

def main():
    # Clear screen and print banner
    os.system('cls' if os.name == 'nt' else 'clear')
    print_banner()

    parser = argparse.ArgumentParser(
        description='ScanForge - A Python-based port scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Fore.YELLOW}Examples:{Style.RESET_ALL}
  Basic scan:              python portscanner.py example.com
  Custom port range:       python portscanner.py example.com -p 1-1000
  Custom timeout:          python portscanner.py example.com -t 2
  Custom thread count:     python portscanner.py example.com -n 200

{Fore.YELLOW}Note:{Style.RESET_ALL} Always ensure you have permission before scanning any system.
"""
    )
    parser.add_argument('target', help='Target IP address or domain name')
    parser.add_argument('-p', '--ports', help='Port range (e.g., 1-1024)', default='1-1024')
    parser.add_argument('-t', '--timeout', type=float, help='Connection timeout in seconds', default=1)
    parser.add_argument('-n', '--threads', type=int, help='Number of threads', default=100)
    
    args = parser.parse_args()

    try:
        # Resolve domain name to IP if needed
        print(f"{Fore.CYAN}[*] Resolving target...{Style.RESET_ALL}")
        target_ip = socket.gethostbyname(args.target)
        print(f"{Fore.GREEN}[+] Target resolved to: {target_ip}{Style.RESET_ALL}")
        
        # Parse port range
        start_port, end_port = map(int, args.ports.split('-'))
        
        # Create and start scanner
        scanner = ScanForge(
            target=target_ip,
            start_port=start_port,
            end_port=end_port,
            timeout=args.timeout,
            threads=args.threads
        )
        scanner.start_scan()

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
