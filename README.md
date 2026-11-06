# CYD Local Flask Server

Small LAN companion server for CYD apps. It provides the legacy Spotify-compatible routes and `/message` plus `/messages` endpoints for short PC messages. It requires Flask 2.0 or newer for the `@app.get` and `@app.post` route decorators.

## Run

```text
py -m pip install -r requirements.txt
py server.py
```

The server listens on `0.0.0.0:5000` so a CYD on the same LAN can reach it. Keep the network trusted; there is no authentication and messages are held only in memory.

## Verification

Python syntax and Flask route smoke tests were run during review. Spotify routes are compatibility stubs: they log requests and return placeholder now-playing data; they do not control Spotify.

