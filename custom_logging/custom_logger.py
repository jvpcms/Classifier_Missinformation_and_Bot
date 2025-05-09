from datetime import datetime

from config.envconfig import Config, get_config


class CustomLogger:

    name: str
    logging_level: int = 0

    def __init__(self, name, envconfig: Config) -> None:
        self.name = name
        self.logging_level = envconfig.envs.logging_level

    def __log(self, message: str, level: str) -> None:
        """Log a message"""

        print(
            f"[{level} - {datetime.now().isoformat()}] {self.name}: {message}"
        )

    def debug(self, message: str) -> None:
        """Log a debug message"""
        if self.logging_level >= 5:
            self.__log(message, "DEBUG")

    def info(self, message: str) -> None:
        """Log an info message"""
        if self.logging_level >= 4:
            self.__log(message, "INFO")

    def warning(self, message: str) -> None:
        """Log a warning message"""
        if self.logging_level >= 3:
            self.__log(message, "WARNING")

    def error(self, message: str) -> None:
        """Log an error message"""
        if self.logging_level >= 2:
            self.__log(message, "ERROR")

    def critical(self, message: str) -> None:
        """Log a critical message"""
        if self.logging_level >= 1:
            self.__log(message, "CRITICAL")


def get_logger(name: str) -> CustomLogger:
    """Get a logger instance"""
    envconfig = get_config()
    return CustomLogger(name, envconfig)
