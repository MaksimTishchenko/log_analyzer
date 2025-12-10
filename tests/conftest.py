import os
import tempfile

import pytest


@pytest.fixture
def temp_log_file():
    """Создает временный файл логов nginx."""
    with tempfile.NamedTemporaryFile(
        mode="w+",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(
            '1.2.3.4 - - [29/Jun/2023:12:00:00 +0300] '
            '"GET /api/test HTTP/1.1" 200 123 "-" "-" "-" "-" 0.123\n'
        )
        tmp.write(
            '1.2.3.5 - - [29/Jun/2023:12:00:01 +0300] '
            '"POST /api/test2 HTTP/1.1" 200 456 "-" "-" "-" "-" 0.456\n'
        )
        file_name = tmp.name

    try:
        yield file_name
    finally:
        if os.path.exists(file_name):
            os.unlink(file_name)


@pytest.fixture
def temp_config_file(tmp_path):
    """Создает временный конфигурационный файл."""
    config_path = tmp_path / "config.json"
    config_path.write_text(
        '{"REPORT_SIZE": 10, '
        '"REPORT_DIR": "./reports", '
        '"LOG_DIR": "./logs"}',
        encoding="utf-8",
    )
    return str(config_path)
