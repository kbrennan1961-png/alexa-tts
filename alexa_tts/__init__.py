"""alexa-tts: Text-to-speech announcements on Amazon Echo devices (unofficial)."""
from .core import login_interactive, list_devices, speak
__all__ = ["login_interactive", "list_devices", "speak"]
__version__ = "0.1.0"
