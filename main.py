import argparse
import logging
import subprocess as subp
import sys

from colorama import Fore

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] - %(asctime)s - %(message)s",
)

try:
    import psutil
except ImportError:
    psutil = None
    if not sys.platform == "linux":
        logging.error(
            f"""{Fore.RED}ss command only works in Linux machines. Please install psutil using:
            {Fore.LIGHTCYAN_EX}pip install psutil colorama{Fore.WHITE}"""
        )
        sys.exit(1)


def get_used_ports() -> set[str]:
    """
    Returns a set of all used ports using psutil if available, otherwise falls back to parsing `ss` command output.
    """
    used_ports = set()

    if psutil:
        logging.info(f"{Fore.CYAN}Checking for used ports with psutil{Fore.WHITE}")
        for conn in psutil.net_connections():
            if conn.laddr and len(conn.laddr) > 1:
                used_ports.add(str(conn.laddr[1]))
            if conn.raddr and len(conn.raddr) > 1:
                used_ports.add(str(conn.raddr[1]))
    else:
        logging.info(f"{Fore.CYAN}Checking for used ports with ss command{Fore.WHITE}")
        process = subp.Popen(["ss", "-a"], stdout=subp.PIPE)
        output = process.communicate()
        socket_lines = output[0].decode().split("\n")

        for socket_line in socket_lines[1:]:
            split_line = [i for i in socket_line.split(" ") if i != ""]
            localPort = ""
            peerPort = ""
            if len(split_line) == 8:
                _, localPort = split_line[4], split_line[5]
                _, peerPort = split_line[6], split_line[7]
            elif len(split_line) == 6:
                _, localPort = split_line[4].rsplit(":", 1)
                if not ":" in split_line[5]:
                    peerPort = split_line[5]
                else:
                    _, peerPort = split_line[5].rsplit(":", 1)
            used_ports.add(peerPort)
            used_ports.add(localPort)

    return used_ports


def wait_for_exit_command():
    while True:
        try:
            command = input(f"\n{Fore.LIGHTBLUE_EX}Enter q to exit: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Fore.YELLOW}Exiting...{Fore.WHITE}")
            break
        if command.lower() == "q":
            break


def start_server(port: int, directory: str = "."):
    """start the server in the background"""
    try:
        server_process = subp.Popen(
            ["python3", "-m", "http.server", f"{port}", "--directory", directory],
            stdout=subp.PIPE,
            stderr=subp.PIPE,
        )
        logging.info(
            f"{Fore.CYAN}Server running at {Fore.YELLOW}http://0.0.0.0:{port}{Fore.WHITE} (directory being served: {directory})"
        )
        return server_process
    except Exception as e:
        logging.error(f"{Fore.RED}Failed to start server: {e}{Fore.WHITE}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Start a simple HTTP server on a free port."
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Default port to start searching from."
    )
    parser.add_argument(
        "--directory", type=str, default=".", help="Directory to serve."
    )
    args = parser.parse_args()

    used_ports = get_used_ports()
    free_port = args.port

    while True:
        if str(free_port) in used_ports:
            free_port += 1
        else:
            break
    logging.info(f"{Fore.GREEN}[Done] Free Port Found: {free_port}{Fore.WHITE}")

    server_process = start_server(free_port, args.directory)

    try:
        wait_for_exit_command()
    finally:
        if server_process:
            server_process.terminate()
            server_process.wait()
            logging.info(f"{Fore.YELLOW}Server stopped.{Fore.WHITE}")


if __name__ == "__main__":
    main()
