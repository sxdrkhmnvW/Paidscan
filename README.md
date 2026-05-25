# 🔍 PaidScan.Uz — Network Recon Toolkit

Универсальный инструмент для сетевой разведки, сканирования портов и быстрых OSINT-проверок.  
**Используйте только на собственных системах или при наличии разрешения.**

---

## Что нового

- CLI + интерактивное меню
- Поддержка `--target`, `--ports`, `--discover`, `--save-report`, `--timeout`, `--threads`
- Конфиг в `paidscan_config.json` или `~/.paidscan_config.json`
- Авто-отчёт, темы и алиасы
- `paramiko` как опциональная зависимость для SSH-брутфорса
- Контакты: Discord `cxpygen`, Telegram `sxdrkhmnvW`

---

## Установка

```bash
python3 -m pip install -r requirements.txt
```

Если не хотите устанавливать `paramiko`, запускайте тулзу без SSH-брутфорса.

---

## Быстрый старт

```bash
python3 test/test.py --help
```

```bash
# Сканировать стандартные порты на хосте
python3 test/test.py -t 192.168.1.1 --port-scan

# Сканировать конкретные порты
python3 test/test.py -t 192.168.1.1 --port-scan -p 22,80,443

# Сканировать подсеть на живые хосты
python3 test/test.py --discover 192.168.1.0/24

# Сканировать HTTPS-порт и сохранить отчёт
python3 test/test.py -t example.com --port-scan -p 443 --https --save-report html --output report.html

# Быстрая проверка HTTP-инфо
python3 test/test.py -t example.com --http-info --https

# Проверить пароль в HIBP
python3 test/test.py --check-pwned P@ssw0rd
```

---

## Основные флаги

| Флаг | Описание |
|------|----------|
| `-t / --target` | Host/IP/alias |
| `-p / --ports` | Порты или диапазоны, например `22,80,1-1024` |
| `--discover` | Поиск живых хостов в подсети |
| `--port-scan` | Запустить TCP-сканирование |
| `--http-info` | Получить HTTP заголовки и технологию сервера |
| `--ssl-check` | Проверить SSL сертификат |
| `--save-report` | Сохранить отчёт в `txt`, `json` или `html` |
| `--output` | Указать имя выходного файла |
| `--config` | Использовать конкретный конфиг-файл |
| `--theme` | Выбрать тему терминала |
| `--alias` | Добавить alias вида `name=target` |

---

## Файлы репозитория

- `test/test.py` — основной скрипт
- `README.md` — документация
- `requirements.txt` — опциональная зависимость `paramiko`
- `.gitignore` — файлы и каталоги, исключаемые из Git

---

## Контакты

- Discord: `cxpygen`
- Telegram: `sxdrkhmnvW`

---

## Важно

Используйте только для авторизованного тестирования собственных систем. Несанкционированное сканирование может нарушать закон.
