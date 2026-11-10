# Shared CYD LAN Server

Small, reusable Flask server for CYD-to-Windows communication. It keeps the
last 100 short messages in memory and exposes a dependency-light JSON API.
Use it for the Pocket OS messenger or as the base for another CYD app.

## Run

```bash
python -m pip install -r requirements.txt
python server.py --port 5000
```

Options: `--host` (default `127.0.0.1`), `--port` (default `5000`), `--debug`.
Environment equivalents: `CYD_SERVER_HOST`, `CYD_SERVER_PORT`,
`CYD_SERVER_TOKEN`, `CYD_MAX_MESSAGES`.

The server binds to localhost by default. To allow a CYD on the LAN, configure
a long random token and bind to all interfaces. For PowerShell:

```powershell
$env:CYD_SERVER_TOKEN = "replace-with-a-long-random-secret"
$env:CYD_SERVER_HOST = "0.0.0.0"
python server.py --port 5000
```

Non-loopback binds are refused unless `CYD_SERVER_TOKEN` is set to at least 16 characters. The CYD must
send an Authorization header using the Bearer scheme and configured token for
requests to `/message`, `/messages`, and `/messages/clear`; store the token in
the device's private configuration. The `/`, `/ping`, and `/health` liveness
and status endpoints remain unauthenticated. Use a unique token and do not
expose this development server directly to the internet; the API does not
provide TLS.

## Endpoints

| Method | Path | Body / query | Result |
|---|---|---|---|
| GET | `/` | ? | `CYD LAN SERVER OK` |
| GET | `/ping` | ? | `pong` |
| GET | `/health` | ? | JSON status and message count |
| POST | `/message` | `{"message":"...", "source":"CYD"}` | 201 + stored item |
| GET | `/messages` | `?limit=50` | newest-first JSON list |
| POST | `/messages/clear` | ? | clears the in-memory queue |

Validation: JSON object required (415 for non-JSON), request bodies are limited
to 4096 bytes (413 otherwise), and `message` must be a non-empty string of at
most 240 characters (400 otherwise). `source` is trimmed to 32 characters.
`CYD_MAX_MESSAGES` must be between 1 and 10000. Timestamps are local ISO-8601
with offset.

## curl examples

```bash
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/message \
     -H "Content-Type: application/json" \
     -d '{"message":"hello from the PC","source":"PC"}'
curl "http://127.0.0.1:5000/messages?limit=5"
```

For a token-protected LAN server, include the Authorization header with the
Bearer scheme and configured token on each message endpoint request.

## Persistence and security

Messages are held in RAM only and disappear when the server stops. Message
read/write/clear endpoints support bearer-token authentication; LAN binding
requires it. TLS and rate limiting are not provided, so use only on a trusted
LAN and do not port-forward the server. Keep localhost binding if only the
server machine should reach it.
