from log_analyzer.main import main


def test_main_with_log_file(tmpdir, monkeypatch):
    # Конфиг, который должен использовать main()
    config = {
        "REPORT_SIZE": 10,
        "REPORT_DIR": str(tmpdir),
        "LOG_DIR": str(tmpdir),
    }

    # Подменяем функцию load_config внутри модуля main,
    # чтобы он не читал реальный config.json из корня проекта
    monkeypatch.setattr(
        "log_analyzer.main.load_config",
        lambda *_args, **_kwargs: config,
    )

    # Создаем валидный лог-файл в формате nginx (без .gz)
    log_file = tmpdir / "nginx-access-ui.log-20231001"
    log_line = (
        "1.2.3.4 - - [29/Jun/2023:12:00:00 +0300] "
        '"GET /api/test HTTP/1.1" 200 123 "-" "-" "-" "-" 0.123\n'
    )
    with open(log_file, "w", encoding="utf-8") as file:
        file.write(log_line)

    # Запускаем основную функцию
    main()

    # Проверяем, что отчет был создан в tmpdir
    report_files = [
        path for path in tmpdir.listdir() if path.basename.startswith("report-")
    ]
    assert len(report_files) > 0, "No report files were generated"
