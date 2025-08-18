# pyserver-starter

A simple Python utility to start an HTTP server on a free port, with improved port detection and graceful shutdown.

## Features
- Automatically finds a free port (starting from a default or user-specified port)
- Uses `psutil` for robust port detection if available, or falls back to parsing `ss` command output
- Serves files from a user-specified directory
- Graceful shutdown on user command or interruption
- Colored and timestamped logging for clarity

## Requirements
- Python 3.7+
- [colorama](https://pypi.org/project/colorama/)
- [psutil](https://pypi.org/project/psutil/) (optional, for better port detection)

Install dependencies:
```sh
pip install colorama psutil
```

## Usage

Run the improved server script:

```sh
python main.py [--port PORT] [--directory DIR]
```

- `--port PORT`: (Optional) Port to start searching from (default: 5000)
- `--directory DIR`: (Optional) Directory to serve (default: current directory)

Example:
```sh
python main.py --port 8080 --directory /path/to/serve
```

The script will:
- Find the first available port starting from the specified port
- Start a Python HTTP server in the background
- Wait for you to enter `q` to exit, then gracefully shut down the server

## License
MIT
