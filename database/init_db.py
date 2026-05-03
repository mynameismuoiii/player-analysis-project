import sqlite3

def init_db():
    conn = sqlite3.connect('football_data.db')
    cursor = conn.cursor()

    # Bảng thông tin cầu thủ
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            nationality TEXT,
            position TEXT,
            club TEXT
        )
    ''')

    # Bảng chỉ số (Stats)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            matches_played INTEGER DEFAULT 0,
            goals INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            FOREIGN KEY (player_id) REFERENCES players (player_id)
        )
    ''')

    # Bảng giá trị chuyển nhượng (Values)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS values_history (
            value_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            market_value REAL,
            currency TEXT DEFAULT 'EUR',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (player_id) REFERENCES players (player_id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "_main_":
    init_db()