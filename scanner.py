
import argparse
import json
import os
import threading

from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from mcstatus import JavaServer


# ==========================================
# Defaults
# ==========================================

DEFAULT_CONFIG = "servers.json"
DEFAULT_THREADS = 10
DEFAULT_TIMEOUT = 3
DEFAULT_OUTPUT_DIR = "results"

lock = threading.Lock()
results = []


# ==========================================
# Argument parsing
# ==========================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Minecraft Java Server Inventory Scanner"
    )

    parser.add_argument(
        "--config",
        default=DEFAULT_CONFIG,
        help="Path to JSON server configuration"
    )

    parser.add_argument(
        "--output-file",
        default=None,
        help="Custom JSON output path"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=DEFAULT_THREADS,
        help="Maximum concurrent workers"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Minecraft status request timeout in seconds"
    )

    return parser.parse_args()


# ==========================================
# Configuration
# ==========================================

def load_config(config_path):
    if not os.path.isfile(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)

    servers = config.get("servers")

    if not isinstance(servers, list):
        raise ValueError("'servers' must be a JSON array")

    validated = []

    for entry in servers:
        if not isinstance(entry, dict):
            raise ValueError("Each server must be a JSON object")

        ip = entry.get("ip")
        port = entry.get("port", 25565)

        if not isinstance(ip, str) or not ip.strip():
            raise ValueError("Every server needs a valid IP or hostname")

        if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
            raise ValueError(f"Invalid port for {ip}: {port}")

        validated.append((ip.strip(), port))

    return validated


# ==========================================
# Output handling
# ==========================================

def initialize_output(output_file):
    directory = os.path.dirname(os.path.abspath(output_file))
    os.makedirs(directory, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump([], file)


def save_results(output_file):
    temp_file = output_file + ".tmp"

    with lock:
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4, ensure_ascii=False)

        os.replace(temp_file, output_file)


# ==========================================
# Minecraft server status
# ==========================================

def scan_server(ip, port, timeout, output_file):

    try:
        server = JavaServer(
            ip,
            port,
            timeout=timeout
        )

        status = server.status()

        forge_data = getattr(status, "forge_data", None)

        server_info = {
            "ip": ip,
            "port": port,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),

            "status": {
                "description": str(status.description),

                "players": {
                    "online": status.players.online,
                    "max": status.players.max,

                    "sample": [
                        {
                            "name": player.name,
                            "id": str(player.id)
                        }
                        for player in (status.players.sample or [])
                    ]
                },

                "version": {
                    "name": status.version.name,
                    "protocol": status.version.protocol
                },

                "is_modded": forge_data is not None,

                "secure_chat": getattr(
                    status,
                    "enforces_secure_chat",
                    None
                )
            }
        }

        with lock:
            results.append(server_info)

            print(
                f"\n[+] Minecraft server found: {ip}:{port}"
            )

            print(
                f"    Version: {status.version.name}"
            )

            print(
                f"    Players: "
                f"{status.players.online}/{status.players.max}"
            )

            print(
                f"    Modded: {server_info['status']['is_modded']}"
            )

            # Snapshot and write while holding the lock.
            # This prevents concurrent file writes.
            temp_file = output_file + ".tmp"

            with open(temp_file, "w", encoding="utf-8") as file:
                json.dump(
                    results,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            os.replace(temp_file, output_file)

        return server_info

    except Exception as error:
        print(f"[-] {ip}:{port} - {error}")
        return None


# ==========================================
# Main
# ==========================================

def main():

    global results

    args = parse_arguments()

    if args.threads < 1:
        raise ValueError("--threads must be at least 1")

    if args.timeout <= 0:
        raise ValueError("--timeout must be greater than 0")

    servers = load_config(args.config)

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d-%H%M%S")

    output_file = args.output_file or os.path.join(
        DEFAULT_OUTPUT_DIR,
        f"{timestamp}-servers.json"
    )

    results = []

    initialize_output(output_file)

    print("=" * 45)
    print(" Minecraft Java Server Inventory")
    print("=" * 45)

    print(f"Targets: {len(servers)}")
    print(f"Threads: {args.threads}")
    print(f"Timeout: {args.timeout}s")
    print(f"Output: {output_file}")

    completed = 0

    with ThreadPoolExecutor(
        max_workers=args.threads
    ) as executor:

        futures = {
            executor.submit(
                scan_server,
                ip,
                port,
                args.timeout,
                output_file
            ): (ip, port)

            for ip, port in servers
        }

        for future in as_completed(futures):
            future.result()
            completed += 1

            print(
                f"\nProgress: {completed}/{len(servers)}"
            )

    save_results(output_file)

    print("\n" + "=" * 45)
    print("Scan complete!")
    print(f"Targets checked: {completed}")
    print(f"Servers found: {len(results)}")
    print(f"Results saved: {output_file}")
    print("=" * 45)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as error:
        print(f"\n[!] Configuration error: {error}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
        raise SystemExit(130)
