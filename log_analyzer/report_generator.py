import gzip
import os
import re
from collections import namedtuple
from datetime import datetime
from typing import Generator, Optional, Tuple

import structlog


LogFile = namedtuple("LogFile", ["path", "date", "extension"])


def find_latest_log(log_dir: str) -> LogFile:
    """Find the latest log file in the given directory."""
    if not os.path.exists(log_dir):
        raise FileNotFoundError(f"Log directory '{log_dir}' does not exist.")

    latest_log = None
    log_pattern = re.compile(r"nginx-access-ui\.log-(\d{8})(?:\.gz)?$")

    for file_name in os.listdir(log_dir):
        match = log_pattern.match(file_name)
        if not match:
            continue

        log_date_str = match.group(1)
        log_date = datetime.strptime(log_date_str, "%Y%m%d")
        log_path = os.path.join(log_dir, file_name)
        extension = "gz" if file_name.endswith(".gz") else ""

        if latest_log is None or log_date > latest_log.date:
            latest_log = LogFile(path=log_path, date=log_date, extension=extension)

    if latest_log is None:
        raise FileNotFoundError("No valid log files found in the directory.")

    return latest_log


def parse_log(
    log_file: LogFile,
) -> Generator[Tuple[Optional[str], Optional[float]], None, None]:
    log_pattern = re.compile(
        r'"(?:(?P<method>GET|POST|PUT|DELETE)\s+'
        r'(?P<url>\S+)\s+HTTP/\d\.\d|0)"'
        r".*?(?P<request_time>\d+\.\d+)$"
    )

    opener = gzip.open if log_file.extension == "gz" else open

    with opener(log_file.path, "rt", encoding="utf-8") as file:
        for line in file:
            match = log_pattern.search(line)

            if match:
                url = match.group("url")
                request_time = float(match.group("request_time"))
                yield url, request_time
                continue

            logger = structlog.get_logger()
            logger.error(
                "Failed to parse log line",
                line=line,
            )
            yield None, None
