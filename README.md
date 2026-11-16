# Shared CYD LAN Server

Small, reusable Flask server for CYD ↔ Windows communication. It keeps the
last 100 short messages in memory and exposes a dependency-light JSON API.
Use it for the Pocket OS messenger or as the base for another CYD app.

## Run

```bash
python -m pip install -r requirements.txt
# PowerShell: $env:CYD_API_TOKEN = "a-long-random-secret"
# Bash: export CYD_API_TOKEN="a-long-random-secret"
python server.py --host 0.0.0.0 --port 5000
```

Options: `--host` (default `0.0.0.0`), `--port` (default `5000`).
Environment variables: `CYD_SERVER_HOST`, `CYD_SERVER_PORT`,
`CYD_MAX_MESSAGES`, and `CYD_API_TOKEN`.

**A long random `CYD_API_TOKEN` is mandatory for LAN binding.** Every endpoint
requires `Authorization: Bearer <token>`. Without a token, the server refuses
to start on a non-loopback address and tokenless requests are restricted to
loopback. Debug mode is also restricted to loopback. Find the PC's IPv4 address
with `ipconfig` and configure the same token in the CYD client. Do not commit
the token to Git.

## Endpoints

| Method | Path | Body / query | Result |
|---|---|---|---|
| GET | `/` | — | `CYD LAN SERVER OK` |
| GET | `/ping` | — | `pong` |
| GET | `/health` | — | JSON status and message count |
| POST | `/message` | `{"message":"...", "source":"CYD"}` | 201 + stored item |
| GET | `/messages` | `?limit=50` | newest-first JSON list |
| POST | `/messages/clear` | — | clears the in-memory queue |

Validation: JSON object required (415 for non-JSON), `message` must be a
non-empty string of at most 240 characters (400 otherwise). `source` is
trimmed to 32 characters. Timestamps are local ISO-8601 with offset.

## curl examples

```bash
curl http://127.0.0.1:5000/health -H "Authorization: Bearer $CYD_API_TOKEN"
curl -X POST http://127.0.0.1:5000/message \
     -H "Authorization: Bearer $CYD_API_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"message":"hello from the PC","source":"PC"}'
curl "http://127.0.0.1:5000/messages?limit=5" \
     -H "Authorization: Bearer $CYD_API_TOKEN"
```

## Persistence and security

Messages are held in RAM only and disappear when the server stops. The API
uses bearer-token authentication for LAN clients; traffic is still plain HTTP,
so use it only on a trusted private network and never port-forward it. There is
no rate limiting. Bind to `127.0.0.1` if only the local machine should reach
the service.

## Installation

Requires Python 3.9+. Install dependencies with `pip install -r requirements.txt`, set a long random `CYD_API_TOKEN`, and start `python server.py --host 0.0.0.0 --port 5000`. Configure the same token and the PC's current LAN IP in the CYD client. LAN traffic is plain HTTP, so use a trusted private network only. See the [full installation guide](INSTALLATION.md).
