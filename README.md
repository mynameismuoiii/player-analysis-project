# Player Analysis Project - EPL 2024/2025

## 📌 Giới thiệu

Project thu thập, xử lý và tra cứu dữ liệu cầu thủ giải Ngoại hạng Anh mùa 2024/2025.

Project bao gồm:

- Crawl dữ liệu thống kê cầu thủ từ FBref
- Crawl giá trị chuyển nhượng từ FootballTransfers
- Lưu dữ liệu vào SQLite
- Xây dựng Flask REST API
- Xây dựng CLI dùng `requests`
- Export dữ liệu ra CSV để phân tích

---

# 👥 Thành viên

| Thành viên | Công việc |
|---|---|
| Trang | Database + SQLite |
| Hương | FBref crawler |
| Thảo | FootballTransfers crawler |
| Ngọc | API + CLI + Analysis |

---

# 📁 Cấu trúc project

```txt
player-analysis-project/
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── fbref_player_stats.html
│   ├── processed/
│   └── player_analysis.db
│
├── database/
│   ├── __init__.py
│   ├── schema.sql
│   ├── init_db.py
│   ├── db.py
│   └── helpers.py
│
├── crawlers/
│   ├── __init__.py
│   │
│   ├── fbref/
│   │   ├── __init__.py
│   │   ├── crawl_fbref.py
│   │   ├── parser.py
│   │   ├── selectors.py
│   │   └── cleaning.py
│   │
│   └── footballtransfers/
│       ├── __init__.py
│       ├── crawl_values.py
│       ├── matcher.py
│       ├── retry.py
│       └── helpers.py
│
├── api/
│   ├── __init__.py
│   ├── app.py
│   ├── routes.py
│   └── services.py
│
├── cli/
│   ├── __init__.py
│   └── lookup.py
│
└── analysis/
```

---

# ⚙️ Yêu cầu hệ thống

- Python 3.10+
- Google Chrome
- Windows PowerShell hoặc CMD

---

# 📦 Cài đặt project

## 1. Clone project

```bash
git clone <repo-url>
cd player-analysis-project
```

---

# 🐍 Tạo môi trường ảo

## PowerShell

```bash
python -m venv venv
```

Kích hoạt:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

---

## CMD

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

---

# 📥 Cài thư viện

```bash
pip install -r requirements.txt
```

Hoặc:

```bash
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

# 📄 requirements.txt

```txt
flask
pandas
requests
beautifulsoup4
lxml
selenium
webdriver-manager
```

---

# 🚫 .gitignore

```gitignore
# Python cache
__pycache__/
*.py[cod]

# Virtual environment
venv/
.venv/
env/

# IDE
.vscode/
.idea/

# Database
*.db
*.sqlite
*.sqlite3

# Data
data/raw/*.html
data/processed/*.csv
data/player_analysis.db

# Logs
*.log
logs/

# Selenium
.wdm/
.seleniumbase/

# Environment
.env
.env.*

# Jupyter
.ipynb_checkpoints/
```

---

# ✅ Kiểm tra cài đặt

```bash
python -c "import flask, pandas, requests, bs4, selenium; print('OK')"
```

Nếu hiện:

```txt
OK
```

là cài đặt thành công.

---

# 🗄️ Khởi tạo database

Chạy:

```bash
python -m database.init_db
```

Kết quả mong muốn:

```txt
Database initialized successfully.
```

Database sẽ được tạo tại:

```txt
data/player_analysis.db
```

---

# 🌐 Crawl dữ liệu FBref

## Bước 1: Tải HTML FBref

Mở link:

```txt
https://fbref.com/en/comps/9/2024-2025/stats/players/2024-2025-Premier-League-Stats
```

Trang đúng phải là:

```txt
Player Standard Stats 2024-2025 Premier League
```

Sau khi bảng hiện đầy đủ:

```txt
Ctrl + S
```

Lưu file vào:

```txt
data/raw/fbref_player_stats.html
```

---

## ⚠️ Lưu ý quan trọng

Cần bật hiển thị đuôi file trong Windows:

```txt
View -> Show -> File name extensions
```

Đảm bảo file đúng tên:

```txt
fbref_player_stats.html
```

Không được là:

```txt
fbref_player_stats.html.html
```

---

# ▶️ Chạy crawler FBref

```bash
python -m crawlers.fbref.crawl_fbref
```

Kết quả mong muốn:

```txt
Đang đọc HTML cache local...
Đang parse bảng FBref...
Đang cleaning dữ liệu...
Số cầu thủ sau khi lọc > 90 phút: ...
Đang lưu SQLite...
Đang export CSV...
DONE
```

Sau khi chạy xong sẽ tạo:

```txt
data/player_analysis.db
data/processed/fbref_player_stats.csv
```

Bảng SQLite:

```txt
fbref_player_stats
```

---

# 🔍 Kiểm tra dữ liệu FBref

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM fbref_player_stats').fetchone()); print(conn.execute('SELECT player, squad FROM fbref_player_stats LIMIT 5').fetchall()); conn.close()"
```

---

# 💰 Crawl giá chuyển nhượng FootballTransfers

Sau khi đã có bảng `fbref_player_stats`, chạy:

```bash
python -m crawlers.footballtransfers.crawl_values
```

Crawler sẽ:

- Đọc danh sách cầu thủ từ SQLite
- Tìm giá trị chuyển nhượng trên FootballTransfers
- Lưu dữ liệu vào SQLite
- Export CSV

Kết quả sau khi chạy:

```txt
data/processed/player_values.csv
```

Bảng SQLite:

```txt
player_values
```

---

# 🔍 Kiểm tra dữ liệu FootballTransfers

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM player_values').fetchone()); print(conn.execute('SELECT player, squad, market_value_text FROM player_values LIMIT 5').fetchall()); conn.close()"
```

---

# 🌐 Chạy Flask API

```bash
python -m api.app
```

Kết quả mong muốn:

```txt
Running on http://127.0.0.1:5000
```

Giữ terminal này chạy để API hoạt động.

---

# 🔎 Test API

## Home

```txt
http://127.0.0.1:5000/
```

---

## Tra cứu theo tên cầu thủ

```txt
http://127.0.0.1:5000/api/player?name=Saka
```

---

## Tra cứu theo câu lạc bộ

```txt
http://127.0.0.1:5000/api/club?club=Arsenal
```

---

# 💻 Chạy CLI

Mở terminal khác trong khi API vẫn đang chạy.

## Tra cứu theo tên cầu thủ

```bash
python -m cli.lookup --name Saka
```

---

## Tra cứu theo câu lạc bộ

```bash
python -m cli.lookup --club Arsenal
```

CLI sẽ:

- In dữ liệu ra terminal
- Xuất CSV vào `data/processed/`

Ví dụ:

```txt
data/processed/player_saka.csv
data/processed/club_arsenal.csv
```

---

# 🔄 Chạy lại project từ đầu

## Xóa database cũ

```bash
del data\player_analysis.db
```

---

## Chạy lại toàn bộ project

```bash
python -m database.init_db
python -m crawlers.fbref.crawl_fbref
python -m crawlers.footballtransfers.crawl_values
python -m api.app
```

Mở terminal khác để test CLI:

```bash
python -m cli.lookup --club Arsenal
```

---

# 🧪 Một số lệnh kiểm tra nhanh

## Kiểm tra các bảng SQLite

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()); conn.close()"
```

---

## Xem 5 cầu thủ đầu tiên

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT player, squad FROM fbref_player_stats LIMIT 5').fetchall()); conn.close()"
```

---

## Đếm số cầu thủ theo CLB

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT squad, COUNT(*) FROM fbref_player_stats GROUP BY squad LIMIT 10').fetchall()); conn.close()"
```

---

# 📌 Ghi chú

- Cần chạy `database.init_db` trước khi crawl dữ liệu.
- Cần có file `data/raw/fbref_player_stats.html` trước khi chạy FBref crawler.
- Cần chạy FBref crawler trước FootballTransfers crawler.
- Cần bật Flask API trước khi chạy CLI.
