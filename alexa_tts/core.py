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


def login_interactive(email, password, url_base="https://www.amazon.com", port=8099, host=None, timeout=600):
    """Run the proxy login. User must open the printed URL in a browser."""
    if host is None:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            host = s.getsockname()[0]
        except Exception:
            host = "127.0.0.1"
        finally:
            s.close()
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
        proxy = AlexaProxy(login, f"http://{host}:{port}")
        # Wrap the success test to set a flag when it triggers.
        _orig_test = proxy.test_amazon_url
        async def _patched_test(resp, data, query):
            result = await _orig_test(resp, data, query)
            if result:
                login._proxy_success = True
            return result
        proxy.test_amazon_url = _patched_test
        await proxy.start_proxy(host="0.0.0.0")
        print(f"Open http://{host}:{port} in your browser and complete Amazon login.")
        print("Waiting for login to complete (up to 10 min)...")
        deadline = asyncio.get_event_loop().time() + timeout
        last_url = None
        while asyncio.get_event_loop().time() < deadline:
            if getattr(login, "_proxy_success", False) or getattr(login, "access_token", None) or getattr(login, "authorization_code", None):
                break
            try:
                lr = getattr(proxy, "last_resp", None)
                if lr is not None:
                    u = str(getattr(lr, "url", ""))
                    if u and u != last_url:
                        print(f"  last URL: {u}")
                        last_url = u
            except Exception:
                pass
            await asyncio.sleep(2)
        await login.save_cookiefile()
        await proxy.stop_proxy()
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
