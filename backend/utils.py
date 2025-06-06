# utils.py
import hmac, hashlib, os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()
_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET").encode()

def verify_signature(request):
    """Return True if X-Hub-Signature-256 matches the body."""
    header_sig = request.headers.get("X-Hub-Signature-256", "")
    if not header_sig.startswith("sha256="):
        return False
    body = request.data
    mac = hmac.new(_SECRET, msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest("sha256=" + mac.hexdigest(), header_sig)

def format_time(dt: datetime | None = None) -> str:
    """`1st April 2021 - 9:30 PM UTC` format."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    return dt.strftime("%#d %B %Y - %#I:%M %p UTC")
