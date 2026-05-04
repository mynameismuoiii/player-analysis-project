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
| Trang | Database + API |
| Hương | FBref crawler + CLI |
| Thảo | FootballTransfers crawler |
| Ngọc | Analysis |

---

## 📁 Cấu trúc project

```txt
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

Tất cả các lệnh chạy chương trình cần được thực hiện trong thư mục `Project Source`.

```bash
cd "Project Source"
```

Nếu chạy lệnh ở sai thư mục, chương trình có thể không tìm thấy database, file HTML hoặc các module Python.

---

## ⚙️ Yêu cầu hệ thống

- Python 3.10+
- Google Chrome
- Windows PowerShell hoặc CMD
- Kết nối Internet khi crawl dữ liệu FootballTransfers

---

## 📦 Cài đặt project

### 1. Clone project

```bash
git clone <repo-url>
cd PLAYER-ANALYSIS-PROJECT
```

---

## 🐍 Tạo môi trường ảo

Trước tiên, di chuyển vào thư mục source:

```bash
cd "Project Source"
```

### PowerShell

```powershell
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

Cài toàn bộ thư viện trong `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

Kiểm tra thư viện đã cài thành công:

```bash
python -c "import pandas, bs4, selenium, flask, requests; print('OK')"
```

Nếu terminal in ra `OK` nghĩa là môi trường đã cài đúng thư viện.

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

## 🧩 Lưu ý khi VSCode báo lỗi thư viện

Nếu VSCode báo đỏ các thư viện như `pandas`, `bs4`, `selenium` nhưng chương trình vẫn chạy được trong terminal, nguyên nhân thường là VSCode đang chọn sai Python interpreter.

Cách xử lý:

1. Nhấn `Ctrl + Shift + P`
2. Chọn `Python: Select Interpreter`
3. Chọn Python trong môi trường ảo của project:

```txt
Project Source/venv/Scripts/python.exe
```

Sau đó reload lại VSCode nếu cần:

```txt
Ctrl + Shift + P
Developer: Reload Window
```

Lỗi import màu đỏ trong VSCode là lỗi phân tích môi trường của editor, không phải lỗi chương trình nếu chạy terminal vẫn thành công.

---

## 🗄️ Khởi tạo database

```bash
python -m database.init_db
```

Kết quả:

```txt
data/player_analysis.db
```

---

## 🌐 Crawl dữ liệu FBref

### Bước 1: Tải HTML

Mở link:

```txt
https://fbref.com/en/comps/9/2024-2025/stats/players/2024-2025-Premier-League-Stats
```

Sau đó:

- Nhấn **Ctrl + S**
- Lưu vào:

```txt
Project Source/data/raw/fbref_player_stats.html
```

---

### ⚠️ Lưu ý

- Bật hiển thị đuôi file trong Windows
- File phải đúng tên: `fbref_player_stats.html`

Do FBref có thể chặn crawl trực tiếp bằng `requests` hoặc `selenium`, gặp CAPTCHA hoặc rate-limit, project sử dụng cách lưu trước file HTML và đọc từ local. Cách này giúp chương trình chạy ổn định hơn khi demo và không phụ thuộc vào mạng.

---

### ▶️ Chạy crawler

```bash
python -m crawlers.fbref.crawl_fbref
```

Kết quả:

```txt
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

Chạy sau khi đã crawl dữ liệu FBref:

```bash
python -m crawlers.footballtransfers.crawl_values
```

Kết quả:

```txt
data/processed/player_values.csv
```

Nếu không tìm thấy giá trị chuyển nhượng của cầu thủ, chương trình sẽ lưu là:

```txt
N/a
```

---

## 🌐 Chạy Flask API

```bash
python -m api.app
```

Truy cập:

```txt
http://127.0.0.1:5000
```

---

## 🔎 Test API

Tra cứu cầu thủ theo tên:

```txt
http://127.0.0.1:5000/api/player?name=Saka
```

Tra cứu cầu thủ theo câu lạc bộ:

```txt
http://127.0.0.1:5000/api/club?club=Arsenal
```

Các endpoint chính:

| Endpoint | Chức năng |
|---|---|
| `GET /` | Kiểm tra API và xem ví dụ sử dụng |
| `GET /api/player?name=Saka` | Tra cứu cầu thủ theo tên |
| `GET /api/club?club=Arsenal` | Tra cứu cầu thủ theo câu lạc bộ |

---

## 💻 CLI

CLI dùng thư viện `requests` để gọi Flask API, vì vậy cần chạy API trước.

### Bước 1: Chạy API

```bash
python -m api.app
```

### Bước 2: Mở terminal mới

```bash
cd "Project Source"
```

Tra cứu theo tên cầu thủ:

```bash
python -m cli.lookup --name "Saka"
```

Tra cứu theo câu lạc bộ:

```bash
python -m cli.lookup --club "Arsenal"
```

Kết quả sẽ được in ra terminal và xuất ra CSV trong thư mục:

```txt
data/processed/
```

Ví dụ file đầu ra:

| Truy vấn | File CSV |
|---|---|
| `--name "Saka"` | `data/processed/player_saka.csv` |
| `--club "Arsenal"` | `data/processed/club_arsenal.csv` |

---

## 📊 Phân tích dữ liệu (Analysis)

### 📈 stats_summary.py

```bash
python -m analysis.stats_summary
```

Output:

```txt
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

```txt
data/processed/valuation.csv
```

---

### 🔵 kmeans_cluster.py

```bash
python -m analysis.kmeans_cluster
```

Output:

```txt
data/processed/elbow.png
data/processed/kmeans_clusters.csv
```

---

### 🗺️ pca_visualization.py

```bash
python -m analysis.pca_visualization
```

Output:

```txt
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

- Phải có file HTML trước khi crawl FBref
- Chạy FBref trước FootballTransfers
- Chạy API trước CLI
- PCA phụ thuộc KMeans
- Nếu VSCode báo lỗi import thư viện nhưng terminal vẫn chạy được, hãy chọn lại Python interpreter trong VSCode

---

## 🔄 Chạy lại toàn bộ project

Thực hiện lần lượt các lệnh sau trong thư mục `Project Source`:

```bash
python -m database.init_db
python -m crawlers.fbref.crawl_fbref
python -m crawlers.footballtransfers.crawl_values
python -m api.app
```

Sau khi API chạy, mở terminal mới để chạy CLI:

```bash
cd "Project Source"
python -m cli.lookup --name "Saka"
python -m cli.lookup --club "Arsenal"
```

---

## 📤 Kết quả đầu ra chính

| Chức năng | Kết quả |
|---|---|
| Database | `data/player_analysis.db` |
| FBref CSV | `data/processed/fbref_player_stats.csv` |
| FootballTransfers CSV | `data/processed/player_values.csv` |
| CLI export | `data/processed/player_*.csv`, `data/processed/club_*.csv` |
| Analysis CSV | `data/processed/*.csv` |
| Analysis images | `data/processed/*.png` |

---

## ✅ Kết luận

Project đã hoàn thành các yêu cầu chính của bài tập lớn, bao gồm thu thập dữ liệu cầu thủ, lưu trữ vào SQLite, xây dựng REST API, viết chương trình CLI sử dụng `requests`, xuất dữ liệu ra CSV và thực hiện phân tích dữ liệu bằng các phương pháp thống kê, KMeans và PCA.