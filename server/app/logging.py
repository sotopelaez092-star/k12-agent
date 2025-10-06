import logging
import sys

def setup_logging(level: str = "INFO"):
    root = logging.getLogger()
    root.setLevel(getattr(logging,level.upper(),logging.INFO))
    if not root.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)
