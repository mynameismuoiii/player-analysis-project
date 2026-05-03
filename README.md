# Player Analysis Project (EPL 2024-2025)

## 📌 Mô tả

Project này thu thập, xử lý và phân tích dữ liệu cầu thủ giải Ngoại hạng Anh mùa 2024–2025.

Bao gồm:

- Crawl dữ liệu thống kê cầu thủ từ FBref
- Crawl giá chuyển nhượng từ FootballTransfers
- Lưu dữ liệu vào SQLite
- Xây dựng Flask REST API tra cứu cầu thủ
- Xây dựng CLI dùng requests để gọi API
- Phân tích dữ liệu và clustering: K-means, PCA

---

## 🧑‍🤝‍🧑 Thành viên

- Trang: Database + Model dữ liệu
- Hương: FBref crawler
- Thảo: FootballTransfers crawler
- Ngọc: API + CLI + Analysis

---

## 📁 Cấu trúc project

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
│   ├── fbref/
│   │   ├── __init__.py
│   │   ├── crawl_fbref.py
│   │   ├── parser.py
│   │   ├── selectors.py
│   │   └── cleaning.py
│   │
│   └── footballtransfers/
│       ├── crawl_values.py
│       ├── matcher.py
│       ├── retry.py
│       └── helpers.py
│
├── api/
│   ├── app.py
│   ├── routes.py
│   └── services.py
│
├── cli/
│   └── lookup.py
│
└── analysis/
    ├── stats_summary.py
    ├── valuation.py
    ├── kmeans_cluster.py
    ├── pca_visualization.py
    └── plot_utils.py
```

---

# ⚙️ Cài đặt

## 1. Clone project

```bash
git clone <repo-url>
cd player-analysis-project
```

---

## 2. Tạo môi trường ảo

```bash
python -m venv venv
```

---

## 3. Cài thư viện

### PowerShell

```bash
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu muốn activate venv:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### CMD

```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## 4. Kiểm tra cài đặt

```bash
.\venv\Scripts\python.exe -c "import pandas, requests, bs4, flask; print('OK')"
```

Nếu hiện:

```txt
OK
```

là cài đặt thành công.

---

# ▶️ Chạy project từ đầu

## Bước 1: Khởi tạo database

```bash
.\venv\Scripts\python.exe -m database.init_db
```

Kết quả mong muốn:

```txt
Database initialized successfully.
```

---

## Bước 2: Chuẩn bị HTML cache FBref

Do FBref có cơ chế Cloudflare/rate-limit, nhóm lưu HTML của trang FBref về local cache rồi parse bằng Python.

Mở link:

```txt
https://fbref.com/en/comps/9/2024-2025/stats/players/2024-2025-Premier-League-Stats
```

Trang đúng phải có tiêu đề:

```txt
Player Standard Stats 2024-2025 Premier League
```

Khi bảng cầu thủ đã hiện đầy đủ, bấm:

```txt
Ctrl + S
```

Lưu file vào:

```txt
data/raw/fbref_player_stats.html
```

Lưu ý: nên bật hiển thị đuôi file trong File Explorer:

```txt
View -> Show -> File name extensions
```

để chắc chắn file có tên đúng là:

```txt
fbref_player_stats.html
```

---

## Bước 3: Crawl dữ liệu FBref

```bash
.\venv\Scripts\python.exe -m crawlers.fbref.crawl_fbref
```

Kết quả mong muốn:

```txt
Đang đọc HTML cache local...
Đang parse bảng FBref...
Đang cleaning dữ liệu...
Số cầu thủ sau khi lọc > 90 phút: ...
Đang lưu SQLite...
DONE
```

Sau khi chạy xong sẽ tạo database:

```txt
data/player_analysis.db
```

và bảng SQLite:

```txt
fbref_player_stats
```

---

## Bước 4: Kiểm tra dữ liệu FBref

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM fbref_player_stats').fetchone()); print(conn.execute('SELECT player, squad FROM fbref_player_stats LIMIT 5').fetchall()); conn.close()"
```

Nếu hiện số dòng và danh sách cầu thủ là dữ liệu FBref đã lưu thành công.

---

## Bước 5: Crawl giá chuyển nhượng FootballTransfers

```bash
.\venv\Scripts\python.exe -m crawlers.footballtransfers.crawl_values
```

Sau khi chạy xong sẽ tạo bảng:

```txt
player_values
```

---

## Bước 6: Kiểm tra dữ liệu giá chuyển nhượng

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM player_values').fetchone()); print(conn.execute('SELECT player, team, market_value_text FROM player_values LIMIT 5').fetchall()); conn.close()"
```

Nếu hiện dữ liệu là phần crawl giá đã chạy thành công.

---

# 🌐 Chạy Flask API

Mở terminal mới và chạy:

```bash
.\venv\Scripts\python.exe -m api.app
```

Kết quả mong muốn:

```txt
Running on http://127.0.0.1:5000
```

Giữ terminal này chạy.

---

# 🔎 Test API bằng trình duyệt

Tra cứu theo tên cầu thủ:

```txt
http://127.0.0.1:5000/api/player?name=Saka
```

Tra cứu theo câu lạc bộ:

```txt
http://127.0.0.1:5000/api/club?club=Arsenal
```

---

# 💻 Chạy CLI

Mở terminal thứ hai.

## Tra theo tên cầu thủ

```bash
.\venv\Scripts\python.exe -m cli.lookup --name Saka
```

## Tra theo câu lạc bộ

```bash
.\venv\Scripts\python.exe -m cli.lookup --club Arsenal
```

Kết quả sẽ:

- In dữ liệu ra màn hình
- Xuất CSV vào thư mục `data/processed/`

Ví dụ:

```txt
data/processed/player_saka.csv
data/processed/club_arsenal.csv
```

---

# 🔄 Chạy lại project từ đầu

Nếu muốn test lại toàn bộ project:

## Xóa database cũ

```bash
del data\player_analysis.db
```

## Chạy lại

```bash
.\venv\Scripts\python.exe -m database.init_db
.\venv\Scripts\python.exe -m crawlers.fbref.crawl_fbref
.\venv\Scripts\python.exe -m crawlers.footballtransfers.crawl_values
```

Sau đó chạy API:

```bash
.\venv\Scripts\python.exe -m api.app
```

Mở terminal khác để test CLI:

```bash
.\venv\Scripts\python.exe -m cli.lookup --club Arsenal
```

---

# 📊 Phân tích dữ liệu

Thư mục `analysis/` chứa:

- Thống kê mean / median / std theo đội
- Định giá cầu thủ
- K-means clustering
- PCA visualization
- Scatter plot 2D / 3D

Ví dụ chạy:

```bash
.\venv\Scripts\python.exe -m analysis.stats_summary
```

Kết quả phân tích sẽ được lưu vào:

```txt
data/processed/
```

---

# 🧪 Một số lệnh kiểm tra nhanh

## Kiểm tra các bảng trong SQLite

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()); conn.close()"
```

## Xem 5 cầu thủ đầu tiên

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT player, squad FROM fbref_player_stats LIMIT 5').fetchall()); conn.close()"
```

## Đếm số cầu thủ theo câu lạc bộ

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT squad, COUNT(*) FROM fbref_player_stats GROUP BY squad LIMIT 10').fetchall()); conn.close()"
```

---