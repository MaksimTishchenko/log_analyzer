import logging
from pathlib import Path

from log_analyzer.config import load_config
from log_analyzer.log_parser import find_latest_log, parse_log
from log_analyzer.report_generator import (
    collect_statistics,
    generate_report,
    is_report_exists,
)
from log_analyzer.utils import setup_logging


def main() -> None:
    """Entry point for log analyzer."""
    config = load_config("config.json")

    setup_logging(level=logging.INFO)
    logging.info("Starting log analyzer...")

    try:
        latest_log = find_latest_log(config["LOG_DIR"])
        logging.info("Latest log file found: %s", latest_log.path)
    except FileNotFoundError as error:
        logging.error(error)
        return

    report_date = latest_log.date.strftime("%Y.%m.%d")
    if is_report_exists(config["REPORT_DIR"], report_date):
        logging.info("Report already exists, skipping processing")
        return

    parsed_logs = list(parse_log(latest_log))
    (
        stats,
        total_count,
        total_time,
        parsing_errors,
    ) = collect_statistics(parsed_logs)

    logging.info(
        "Parsing statistics: total=%s, errors=%s, time=%.3f",
        total_count,
        parsing_errors,
        total_time,
    )

    report_path = Path(config["REPORT_DIR"])
    generate_report(stats, report_date, report_path, config["REPORT_SIZE"])


if __name__ == "__main__":
    main()
