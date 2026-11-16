# Installation

Requires Python 3.9+ and a PC on the same trusted private LAN as the CYD.

## Windows (PowerShell)

```powershell
git clone https://github.com/okyanus-11/CYD_Local_Flask_Server.git
cd CYD_Local_Flask_Server
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
$env:CYD_API_TOKEN = "replace-with-a-long-random-secret"
python server.py --host 0.0.0.0 --port 5000
```

## Linux / macOS

```bash
git clone https://github.com/okyanus-11/CYD_Local_Flask_Server.git
cd CYD_Local_Flask_Server
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
export CYD_API_TOKEN="replace-with-a-long-random-secret"
python server.py --host 0.0.0.0 --port 5000
```

Configure the same token and the PC's current LAN IPv4 address in the CYD client. LAN binding requires a token and requests use bearer authentication. Traffic is plain HTTP: use a trusted private network only, never port-forward the service, and never commit the token. Use `--host 127.0.0.1` for local-only access.
