"""Core logic for alexa-tts (unofficial Alexa web API via alexapy)."""
import asyncio
import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "alexa-tts"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _load_config():
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {}


def _save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def login_interactive(email, password, url_base="https://www.amazon.com", port=8099):
    """Run the proxy login. User must open the printed URL in a browser."""
    async def main():
        from alexapy.alexalogin import AlexaLogin
        from alexapy.alexaproxy import AlexaProxy

        outdir = str(CONFIG_DIR)
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        login = AlexaLogin(
            url=url_base,
            email=email,
            password=password,
            outputpath=lambda name: os.path.join(outdir, name),
            oauth_login=True,
        )
        proxy = AlexaProxy(login, f"http://localhost:{port}")
        print(f"Open http://localhost:{port} in your browser and complete Amazon login.")
        await proxy.run()
        cfg = _load_config()
        cfg["email"] = email
        cfg["logged_in"] = True
        _save_config(cfg)
        print("Login complete. Session saved.")

    asyncio.run(main())


def list_devices():
    cfg = _load_config()
    if not cfg.get("logged_in"):
        raise RuntimeError("Not logged in. Run: alexa-tts --login")
    return ["(device listing requires a live session; see README)"]


def speak(text, device=None, **kwargs):
    raise NotImplementedError(
        "alexa-tts speak requires a live AlexaLogin session; "
        "see README for the login flow."
    )
