ThunderScan

ThunderScan is a lightweight, multithreaded Minecraft Java Edition server inventory tool written in Python.

It checks configured Minecraft server endpoints and collects server information, including the Message of the Day (MOTD), player counts, Minecraft version, protocol, player samples, and modded-server information.

Features
Minecraft server detection: Retrieves Minecraft Java Edition server status information.
Multithreading: Performs concurrent server checks using Python's ThreadPoolExecutor.
Configurable targets: Loads server IP addresses and ports from a JSON configuration file.
Configurable timeouts: Allows customization of Minecraft status request timeouts.
Player information: Collects online player counts, maximum player capacity, and available player samples.
Version detection: Retrieves Minecraft version names and protocol numbers.
Modded server detection: Identifies available Forge server information.
Secure chat information: Collects secure chat enforcement information when available.
UTC timestamps: Records the time of each successful server response.
Incremental saving: Saves successful results during execution.
Custom output paths: Allows users to specify where results are stored.
Error handling: Handles individual server failures without terminating the entire process.
Requirements
Python 3.10 or newer
Minecraft Java Edition server endpoints
Permission to query the configured servers

Python dependencies are listed in requirements.txt.

Installation
1. Clone the repository
bash
git clone https://github.com/KalHal123/ThunderScan.git
cd ThunderScan

2. Create a virtual environment
bash
python -m venv venv

3. Activate the virtual environment

Linux / macOS

bash
source venv/bin/activate


Windows

powershell
venv\Scripts\activate

4. Install dependencies
bash
pip install -r requirements.txt

Configuration

ThunderScan uses a JSON configuration file to define which Minecraft server endpoints should be checked.

Copy the example configuration:

bash
cp servers.example.json servers.json


On Windows, you can also copy the file manually.

Configuration example
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

Configuration parameters
Parameter	Description	Default
ip	Server IP address or hostname	Required
port	Minecraft server port	25565

Only configure endpoints you own or have explicit authorization to query.

Usage
Basic execution

Run ThunderScan with the default configuration:

bash
python scanner.py

Specify a configuration file
bash
python scanner.py --config servers.json

Specify an output file
bash
python scanner.py --output-file results/servers.json

Configure worker threads
bash
python scanner.py --threads 10

Configure request timeout
bash
python scanner.py --timeout 3

Full command example
bash
python scanner.py \
    --config servers.json \
    --threads 10 \
    --timeout 3 \
    --output-file results/servers.json

Command-line arguments
Argument	Description	Default
--config	Path to the JSON configuration file	servers.json
--output-file	Custom JSON output path	Timestamped file in results/
--threads	Maximum number of concurrent workers	10
--timeout	Minecraft status request timeout in seconds	3

Display all available arguments:

bash
python scanner.py --help

Output

ThunderScan saves successful server responses in JSON format.

By default, output files are stored in the results/ directory with a timestamp in their filenames.

Example output
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


The example values are illustrative and do not represent a live server.

Collected information
Field	Description
ip	Server IP address or hostname
port	Server port
timestamp	UTC timestamp of the response
description	Server Message of the Day (MOTD)
players.online	Current number of online players
players.max	Maximum player capacity
players.sample	Available sample player information
version.name	Minecraft version name
version.protocol	Minecraft protocol number
is_modded	Whether Forge information is available
secure_chat	Secure chat enforcement information, if available
Project Structure
text
ThunderScan/
|
|-- scanner.py
|-- servers.example.json
|-- requirements.txt
|-- README.md
|-- LICENSE
|-- .gitignore
|
|-- results/
    |-- servers.json

File	Description
scanner.py	Main scanner application
servers.example.json	Example server configuration
requirements.txt	Python dependencies
README.md	Project documentation
LICENSE	MIT license
.gitignore	Git exclusion rules
results/	Generated scan results
Error Handling

ThunderScan handles individual server failures without terminating the entire execution.

Possible errors include:

Connection timeouts
Connection refused
Invalid Minecraft status responses
DNS resolution failures
Unreachable endpoints

Errors are displayed in the terminal. Servers that fail to respond successfully are excluded from the results.

Legal Notice

ThunderScan is intended for authorized Minecraft server inventory and administration.

Only query servers and infrastructure that you own or have explicit permission to assess.

Users are responsible for complying with applicable laws, network policies, and service terms.

The developers are not responsible for misuse of this software.

License

ThunderScan is distributed under the MIT License.

See the LICENSE file for details.

Contributing

Contributions, bug reports, and feature requests are welcome.

To contribute:

Fork the repository.
Create a feature branch.
Make your changes.
Commit your changes.
Push your branch.
Open a pull request.
Dependencies

ThunderScan uses mcstatus to communicate with Minecraft Java Edition servers.
