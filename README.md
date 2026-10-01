# NetPulse

A lightweight, dependency-free Python CLI tool for quick network diagnostics.

## Features

- **Ping**: Check host reachability and latency.
- **HTTP Check**: Measure HTTP response status and latency.
- **Port Scanner**: Scan common or custom ports on a target host.
- **Network Info**: Retrieve local hostname and IP address.

## Installation

No external dependencies are required. Just ensure you have Python 3 installed.

```bash
git clone https://github.com/yourusername/netpulse.git
cd netpulse
```

## Usage

Run the script using Python:

```bash
# Get local network info
python main.py info

# Ping a host
python main.py ping google.com

# Check HTTP status
python main.py http github.com

# Scan specific ports
python main.py scan localhost --ports 22,80,443,8080
```