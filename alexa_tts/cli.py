#!/usr/bin/env python3
"""CLI for alexa-tts."""
import argparse
import getpass
import sys

from alexa_tts import login_interactive, list_devices


def main():
    p = argparse.ArgumentParser(description="TTS announcements on Amazon Echo (unofficial)")
    p.add_argument("text", nargs="*", help="text to announce")
    p.add_argument("--login", action="store_true", help="run Amazon login via browser proxy")
    p.add_argument("--list", action="store_true", help="list devices")
    p.add_argument("--email", default=None)
    p.add_argument("--password", default=None)
    p.add_argument("--port", type=int, default=8099)
    p.add_argument("--host", default=None, help="host/IP for the proxy (default: auto-detect LAN IP)")
    args = p.parse_args()

    if args.login:
        email = args.email or input("Amazon email: ")
        password = args.password or getpass.getpass("Amazon password: ")
        login_interactive(email, password, port=args.port, host=args.host)
        return

    if args.list:
        print("\n".join(list_devices()))
        return

    print("alexa-tts speak is not yet wired to a live session.")
    print("Run: alexa-tts --login  (then re-run with text)")
    sys.exit(1)


if __name__ == "__main__":
    main()
