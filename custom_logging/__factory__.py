import structlog
import os
import dotenv


def setup_logger() -> None:
    """Configure logger according to the environment."""

    log_levels = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
        "CRITICAL": 50,
    }

    dotenv.load_dotenv()
    log_env = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = log_levels.get(log_env, 20)

    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            structlog.processors.KeyValueRenderer(key_order=["event", "level"]),
        ],
    )


def get_logger() -> structlog.BoundLogger:
    """Return a logger instance configured according to the environment."""

    setup_logger()
    return structlog.get_logger()
