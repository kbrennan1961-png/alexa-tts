# alexa-tts

Text-to-speech announcements on Amazon Echo devices (unofficial).

Uses the unofficial Alexa web API via `alexapy`. Requires a one-time
Amazon login (browser, with 2FA) to capture a session.

## Install
```bash
pip install -r requirements.txt
```

## Login (one-time)
```bash
alexa-tts --login
# enter email + password; open the printed URL in a browser to complete login
```

## Status
Login scaffolding is provided. Wiring `speak()` to a live session and device
discovery is the next step (contributions welcome).

## License
MIT
