# Shared CYD LAN Server

Small, reusable Flask server for CYD ↔ Windows communication. It keeps the
last 100 short messages in memory and exposes a dependency-light JSON API.
Use it for the Pocket OS messenger or as the base for another CYD app.

## Run

```bash
python -m pip install -r requirements.txt
python server.py --port 5000
```

Options: `--host` (default `0.0.0.0`), `--port` (default `5000`), `--debug`.
Environment equivalents: `CYD_SERVER_HOST`, `CYD_SERVER_PORT`,
`CYD_MAX_MESSAGES`.

Find the PC's IPv4 address with `ipconfig` and put it in the firmware
`config.h`. The server has no authentication — keep it on a trusted LAN and
never expose it to the internet.

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
curl http://127.0.0.1:5000/health
curl -X POST http://127.0.0.1:5000/message \
     -H "Content-Type: application/json" \
     -d '{"message":"hello from the PC","source":"PC"}'
curl "http://127.0.0.1:5000/messages?limit=5"
```

## Persistence and security

Messages are held in RAM only and disappear when the server stops. There is no
authentication, no TLS and no rate limiting; it is a trusted-LAN utility.
Bind to `127.0.0.1` instead of `0.0.0.0` if only the local machine should reach
it.
