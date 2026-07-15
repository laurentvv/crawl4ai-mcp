import io
import os
import sys

os.environ["PYTHONIOENCODING"] = "utf-8"
try:
    # Force UTF-8 usage for stdout/stderr
    if sys.stdout.encoding != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if sys.stderr.encoding != "utf-8":
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
except AttributeError:
    pass
