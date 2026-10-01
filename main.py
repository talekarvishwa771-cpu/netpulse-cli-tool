#!/usr/bin/env python3
import argparse
import platform
import socket
import subprocess
import sys
import time
import urllib.request

def ping_host(host, count=4):
    print(f"[*] Pinging {host}...")
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, str(count), host]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"[-] Ping failed:\n{e.output}")
    except Exception as e:
        print(f"[-] Error executing ping: {e}")

def check_http(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    print(f"[*] Checking HTTP status for {url}...")
    start = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NetPulse/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = (time.time() - start) * 1000
            print(f"[+] Status: {response.getcode()} OK")
            print(f"[+] Response Time: {latency:.2f} ms")
    except Exception as e:
        print(f"[-] HTTP request failed: {e}")

def scan_ports(host, ports_str):
    try:
        ports = [int(p.strip()) for p in ports_str.split(',')]
    except ValueError:
        print("[-] Invalid ports list. Use comma-separated integers (e.g., 80,443).")
        return

    print(f"[*] Scanning {host} on ports {ports}...")
    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[-] Could not resolve host: {host}")
        return

    print(f"[*] Target IP: {target_ip}")
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        result = s.connect_ex((target_ip, port))
        if result == 0:
            print(f"[+] Port {port}: OPEN")
        else:
            print(f"[-] Port {port}: CLOSED")
        s.close()

def show_info():
    print("[*] Gathering local network information...")
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unknown"
    print(f"[+] Hostname: {hostname}")
    print(f"[+] Local IP Address: {local_ip}")

def main():
    parser = argparse.ArgumentParser(description="NetPulse: A lightweight network diagnostic CLI tool.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ping command
    ping_parser = subparsers.add_parser("ping", help="Ping a host to check latency and reachability")
    ping_parser.add_argument("host", help="Target host or IP address")
    ping_parser.add_argument("-c", "--count", type=int, default=4, help="Number of ping requests to send")

    # HTTP command
    http_parser = subparsers.add_parser("http", help="Check HTTP status and latency of a URL")
    http_parser.add_argument("url", help="Target URL (e.g., google.com)")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan specific ports on a host")
    scan_parser.add_argument("host", help="Target host or IP address")
    scan_parser.add_argument("-p", "--ports", default="21,22,80,443,8080", help="Comma-separated list of ports to scan")

    # Info command
    subparsers.add_parser("info", help="Display local network information")

    args = parser.parse_args()

    if args.command == "ping":
        ping_host(args.host, args.count)
    elif args.command == "http":
        check_http(args.url)
    elif args.command == "scan":
        scan_ports(args.host, args.ports)
    elif args.command == "info":
        show_info()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()