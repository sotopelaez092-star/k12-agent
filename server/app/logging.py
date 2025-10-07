import logging
import sys

def setup_logging(level: str = "INFO"):
    root = logging.getLogger()
    root.setLevel(getattr(logging,level.upper(),logging.INFO))
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = JsonFormatter()
        handler.setFormatter(formatter)
        root.addHandler(handler)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        import json, time
        ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created))
        base = {
            "timestamp": ts,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for key in ("method","path","rid","status","duration_ms"):
            if hasattr(record, key):
                base[key] = getattr(record, key)
        return json.dumps(base, ensure_ascii=False)
