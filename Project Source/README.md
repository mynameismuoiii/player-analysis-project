# ⚽ Player Analysis Project - EPL 2024/2025

## 📌 Giới thiệu

Project thu thập, xử lý và tra cứu dữ liệu cầu thủ giải Ngoại hạng Anh mùa 2024/2025.

Project bao gồm:

- Crawl dữ liệu thống kê cầu thủ từ FBref  
- Crawl giá trị chuyển nhượng từ FootballTransfers  
- Lưu dữ liệu vào SQLite  
- Xây dựng Flask REST API  
- Xây dựng CLI dùng requests  
- Export dữ liệu ra CSV để phân tích  
- Phân tích dữ liệu (KMeans, PCA)  

---

## 👥 Thành viên

| Thành viên | Công việc |
|---|---|
| Trang | Database + SQLite |
| Hương | FBref crawler |
| Thảo | FootballTransfers crawler |
| Ngọc | API + CLI + Analysis |

---

## 📁 Cấu trúc project

```
PLAYER-ANALYSIS-PROJECT/
│
├── Project Source/
│   ├── data/
│   │   ├── raw/
│   │   │   └── fbref_player_stats.html
│   │   ├── processed/
│   │   └── player_analysis.db
│   │
│   ├── database/
│   │   ├── schema.sql
│   │   ├── init_db.py
│   │   ├── db.py
│   │   └── helpers.py
│   │
│   ├── crawlers/
│   │   ├── fbref/
│   │   └── footballtransfers/
│   │
│   ├── api/
│   ├── cli/
│   └── analysis/
│
├── Project Report/      # File báo cáo (PDF)
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## ⚠️ Lưu ý quan trọng

> Tất cả các lệnh phải chạy trong thư mục `Project Source`

---

## ⚙️ Yêu cầu hệ thống

- Python 3.10+  
- Google Chrome  
- Windows PowerShell hoặc CMD  

---

## 📦 Cài đặt project

### 1. Clone project

```bash
git clone <repo-url>
cd PLAYER-ANALYSIS-PROJECT
```

---

## 🐍 Tạo môi trường ảo

### PowerShell

```bash
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### CMD

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

---

## 📥 Cài thư viện

```bash
pip install -r requirements.txt
```

---

## 📄 requirements.txt

```txt
flask
pandas
requests
beautifulsoup4
lxml
selenium
webdriver-manager
scikit-learn
matplotlib
numpy
```

---

## 🗄️ Khởi tạo database

```bash
cd "Project Source"
python -m database.init_db
```

---

## 🌐 Crawl dữ liệu FBref

### Bước 1: Tải HTML

Mở link:

```
https://fbref.com/en/comps/9/2024-2025/stats/players/2024-2025-Premier-League-Stats
```

Sau đó:

- Nhấn **Ctrl + S**
- Lưu vào:

```
Project Source/data/raw/fbref_player_stats.html
```

---

### ⚠️ Lưu ý

- Bật hiển thị đuôi file trong Windows  
- File phải đúng tên: `fbref_player_stats.html`

---

### ▶️ Chạy crawler

```bash
cd "Project Source"
python -m crawlers.fbref.crawl_fbref
```

Kết quả:

```
data/player_analysis.db
data/processed/fbref_player_stats.csv
```

---

## 🔍 Kiểm tra dữ liệu

```bash
python -c "import sqlite3; conn=sqlite3.connect('data/player_analysis.db'); print(conn.execute('SELECT COUNT(*) FROM fbref_player_stats').fetchone()); conn.close()"
```

---

## 💰 Crawl FootballTransfers

```bash
python -m crawlers.footballtransfers.crawl_values
```

Kết quả:

```
data/processed/player_values.csv
```

---

## 🌐 Chạy Flask API

```bash
python -m api.app
```

Truy cập:

```
http://127.0.0.1:5000
```

---

## 🔎 Test API

```
http://127.0.0.1:5000/api/player?name=Saka
http://127.0.0.1:5000/api/club?club=Arsenal
```

---

## 💻 CLI

Mở terminal mới:

```bash
cd "Project Source"
python -m cli.lookup --name Saka
```

---

## 📊 Phân tích dữ liệu (Analysis)

### 📈 stats_summary.py

```bash
python -m analysis.stats_summary
```

Output:

```
data/processed/mean_stats.csv
data/processed/median_stats.csv
data/processed/std_stats.csv
```

---

### 💸 valuation.py

```bash
python -m analysis.valuation
```

Output:

```
data/processed/valuation.csv
```

---

### 🔵 kmeans_cluster.py

```bash
python -m analysis.kmeans_cluster
```

Output:

```
data/processed/elbow.png
data/processed/kmeans_clusters.csv
```

---

### 🗺️ pca_visualization.py

```bash
python -m analysis.pca_visualization
```

Output:

```
data/processed/pca_2d.png
data/processed/pca_3d.png
```

---

### 🔄 Chạy toàn bộ analysis

```bash
python -m analysis.stats_summary
python -m analysis.valuation
python -m analysis.kmeans_cluster
python -m analysis.pca_visualization
```

---

## 📌 Ghi chú

- Phải có file HTML trước khi crawl  
- Chạy FBref trước FootballTransfers  
- Chạy API trước CLI  
- PCA phụ thuộc KMeans  

---

## 🔄 Chạy lại toàn bộ project

```bash
cd "Project Source"

python -m database.init_db
python -m crawlers.fbref.crawl_fbref
python -m crawlers.footballtransfers.crawl_values
python -m api.app
```