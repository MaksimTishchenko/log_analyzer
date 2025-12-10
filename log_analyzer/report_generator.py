import json
import os

from pathlib import Path
from statistics import median
from typing import Any, Dict, Iterable, List, Optional, Tuple


def collect_statistics(
    parsed_logs: Iterable[Tuple[Optional[str], Optional[float]]],
) -> Tuple[Dict[str, Dict[str, Any]], int, float, int]:
    """Aggregate statistics for each URL."""
    stats: Dict[str, List[float]] = {}
    parsing_errors = 0

    for url, request_time in parsed_logs:
        if url is None or request_time is None:
            parsing_errors += 1
            continue

        stats.setdefault(url, []).append(request_time)

    total_count = sum(len(times) for times in stats.values())
    total_time = sum(sum(times) for times in stats.values())

    result: Dict[str, Dict[str, Any]] = {}
    for url, times in stats.items():
        count = len(times)
        time_sum = sum(times)
        time_max = max(times)
        time_avg = time_sum / count if count else 0
        time_med = median(times)

        count_perc = (count / total_count * 100) if total_count else 0
        time_perc = (time_sum / total_time * 100) if total_time else 0

        result[url] = {
            "url": url,
            "count": count,
            "count_perc": count_perc,
            "time_sum": time_sum,
            "time_perc": time_perc,
            "time_avg": time_avg,
            "time_max": time_max,
            "time_med": time_med,
        }

    return result, total_count, total_time, parsing_errors



def is_report_exists(report_dir: os.PathLike[str], report_date: str) -> bool:
    """Check if report for given date already exists."""
    report_dir_path = Path(report_dir)
    report_path = report_dir_path / f"report-{report_date}.html"
    return report_path.exists()

def _render_report(table: List[Dict[str, Any]]) -> str:
    """Render HTML report using template if available."""
    template_path = Path("templates") / "report.html"
    table_json = json.dumps(table)

    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        return template.replace("$table_json", table_json)

    return f"""<html>
<head><title>Log report</title></head>
<body>
<script>
var table = {table_json};
</script>
</body>
</html>"""

def generate_report(
    stats: Dict[str, Dict[str, Any]],
    report_date: str,
    report_dir: os.PathLike[str],
    report_size: int,
) -> None:
    """Generate HTML report file."""
    report_dir_path = Path(report_dir)
    report_dir_path.mkdir(parents=True, exist_ok=True)

    table = sorted(
        stats.values(),
        key=lambda item: item["time_sum"],
        reverse=True,
    )[:report_size]

    report_html = _render_report(table)
    report_path = report_dir_path / f"report-{report_date}.html"
    report_path.write_text(report_html, encoding="utf-8")
