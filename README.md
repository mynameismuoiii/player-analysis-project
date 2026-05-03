# Player Analysis Project (EPL 2024-2025)

## 📌 Mô tả

Project này thu thập, xử lý và phân tích dữ liệu cầu thủ giải Ngoại hạng Anh mùa 2024–2025.

Bao gồm:

- Crawl dữ liệu thống kê cầu thủ từ FBref
- Crawl giá chuyển nhượng từ FootballTransfers
- Lưu dữ liệu vào SQLite
- Xây dựng Flask REST API tra cứu cầu thủ
- Xây dựng CLI dùng requests để gọi API
- Phân tích dữ liệu và clustering (K-means, PCA)

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
│   ├── processed/
│   └── player_analysis.db
│
├── database/
│   ├── schema.sql
│   ├── init_db.py
│   ├── db.py
│   └── helpers.py
│
├── crawlers/
│   ├── fbref/
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

### PowerShell (khuyên dùng)

Do PowerShell có thể chặn activate script nên cài trực tiếp bằng Python trong venv:

```bash
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### CMD

```cmd
venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## 4. Kiểm tra cài đặt

```bash
.\venv\Scripts\python.exe -c "import pandas, requests, bs4, flask, soccerdata; print('OK')"
```

Nếu hiện:

```txt
OK
```

thì cài đặt thành công.

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

## Bước 2: Crawl dữ liệu FBref

```bash
.\venv\Scripts\python.exe -m crawlers.fbref.crawl_fbref
```

Sau khi chạy xong sẽ tạo:

```txt
data/player_analysis.db
data/processed/fbref_player_stats.csv
```

và bảng SQLite:

```txt
fbref_player_stats
```

---

## Bước 3: Kiểm tra dữ liệu FBref

```bash
.\venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM fbref_player_stats').fetchone()); print(conn.execute('SELECT player, team FROM fbref_player_stats LIMIT 5').fetchall()); conn.close()"
```

Nếu hiện số dòng và danh sách cầu thủ là dữ liệu FBref đã lưu thành công.

---

## Bước 4: Crawl giá chuyển nhượng FootballTransfers

```bash
.\venv\Scripts\python.exe -m crawlers.footballtransfers.crawl_values
```

Sau khi chạy xong sẽ tạo bảng:

```txt
player_values
```

---

## Bước 5: Kiểm tra dữ liệu giá chuyển nhượng

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
- Xuất CSV vào thư mục:

```txt
data/processed/
```

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

## Chạy lại toàn bộ

```bash
.\venv\Scripts\python.exe -m database.init_db

.\venv\Scripts\python.exe -m crawlers.fbref.crawl_fbref

.\venv\Scripts\python.exe -m crawlers.footballtransfers.crawl_values

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


