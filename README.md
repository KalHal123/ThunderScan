Minecraft Java Server Scanner

A lightweight Python-based Minecraft Java Edition server inventory tool. It checks configured Minecraft server endpoints and collects useful server information, including MOTD, player counts, version, protocol, player samples, and modded-server information.

Features
Minecraft Java Edition server status detection
Concurrent server checks using ThreadPoolExecutor
Configurable server targets
Configurable request timeout
Player count and player sample collection
Minecraft version and protocol detection
Modded server detection
Secure chat information when available
UTC timestamps
Incremental JSON result saving
Custom output file support
Individual error handling
Requirements
Python 3.10+
Minecraft Java Edition endpoints
Permission to query the configured servers
Installation

Clone the repository:

bash
git clone https://github.com/YOUR_USERNAME/minecraft-server-scanner.git
cd minecraft-server-scanner


Create a virtual environment:

bash
python -m venv venv


Activate it:

Linux / macOS

bash
source venv/bin/activate


Windows

powershell
venv\Scripts\activate


Install dependencies:

bash
pip install -r requirements.txt

Configuration

Edit servers.example.json or create your own servers.json.

Example:

json
{
    "servers": [
        {
            "ip": "127.0.0.1",
            "port": 25565
        },
        {
            "ip": "192.168.1.10",
            "port": 25565
        }
    ]
}


Only add endpoints you own or have explicit authorization to query.

Usage

Run with the default configuration:

bash
python scanner.py


Specify a custom configuration:

bash
python scanner.py --config servers.json


Specify a custom output file:

bash
python scanner.py --output-file results/servers.json


Configure concurrency and timeout:

bash
python scanner.py --threads 10 --timeout 3

Full example usage
bash
python scanner.py --config servers.json --threads 10 --timeout 3 --output-file results/servers.json

Example Output
json
[
    {
        "ip": "127.0.0.1",
        "port": 25565,
        "timestamp": "2026-11-17T22:00:00+00:00",
        "status": {
            "description": "A Minecraft Server",
            "players": {
                "online": 2,
                "max": 20,
                "sample": []
            },
            "version": {
                "name": "Paper 1.21",
                "protocol": 767
            },
            "is_modded": false,
            "secure_chat": null
        }
    }
]


The example values are illustrative.

Project Structure
text
minecraft-server-scanner/
├── scanner.py
├── README.md
├── requirements.txt
├── servers.example.json
├── .gitignore
├── LICENSE
└── results/

Output

Results are saved as JSON.

Each successful server response contains:

Field	Description
ip	Server IP address
port	Server port
timestamp	UTC timestamp
description	Server MOTD
players.online	Current players
players.max	Maximum players
players.sample	Sample player information
version.name	Minecraft server version
version.protocol	Protocol version
is_modded	Whether Forge data is available
secure_chat	Secure chat information, if available
Error Handling

Servers that cannot be reached or do not respond correctly are skipped. Errors are reported in the terminal.

Legal Notice

This project is intended for authorized Minecraft server inventory and administration.

Only query servers you own or have explicit permission to assess. You are responsible for complying with applicable laws, network policies, and service terms.

License

This project is licensed under the MIT License. See LICENSE for details.

Contributing

Contributions, bug reports, and feature requests are welcome.

Fork the repository.
Create a feature branch.
Commit your changes.
Open a pull request.

Built with Python and mcstatus.
