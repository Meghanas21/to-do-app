"""
Centralized logging setup.

Every request, auth event, and error is logged with a consistent format so
that CORS/network problems can be diagnosed from server logs (e.g. "did the
request even arrive at the backend, or did it die at the browser preflight
stage?").
"""
import logging
import sys


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Quiet down noisy third-party loggers a bit
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


logger = logging.getLogger("todo_api")
