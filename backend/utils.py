# utils.py
import hmac, hashlib, os
from datetime import datetime, timezone
import pytz

from dotenv import load_dotenv

load_dotenv()
_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET").encode()
#verify the signature with serect key
def verify_signature(request):
    #Return True if X-Hub-Signature-256 matches the body.
    header_sig = request.headers.get("X-Hub-Signature-256", "")
    if not header_sig.startswith("sha256="):
        return False
    body = request.data
    mac = hmac.new(_SECRET, msg=body, digestmod=hashlib.sha256)
    return hmac.compare_digest("sha256=" + mac.hexdigest(), header_sig)


#time formating base on IST time
def format_time(dt: datetime | None = None) -> str:
    ist = pytz.timezone("Asia/Kolkata")
    if dt is None:
        dt = datetime.utcnow()
    dt_ist = dt.astimezone(ist)

    day = dt_ist.day
    suffix = "th" if 11 <= day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return dt_ist.strftime(f"{day}{suffix} %B %Y - %I:%M %p IST")