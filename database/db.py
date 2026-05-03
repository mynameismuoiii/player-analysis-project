import sqlite3
import re

class FootballDB:
    def __init__(self, db_path='football_data.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def clean_value(self, val_str):
        """
        Chuẩn hóa: 'N/a' -> 0, '€50M' -> 50000000.0, '€500k' -> 500000.0
        """
        if not val_str or val_str.lower() == "n/a":
            return 0.0
        
        # Xóa ký hiệu tiền tệ và khoảng trắng
        clean_str = re.sub(r'[€$£,]', '', val_str).strip().lower()
        
        try:
            if 'm' in clean_str:
                return float(clean_str.replace('m', '')) * 1_000_000
            elif 'k' in clean_str:
                return float(clean_str.replace('k', '')) * 1_000
            return float(clean_str)
        except ValueError:
            return 0.0

    def upsert_player(self, data):
        """
        Thêm mới hoặc cập nhật thông tin cầu thủ và chỉ số.
        Data format: {'name': 'Messi', 'market_value': '€50M', 'goals': 'N/a', ...}
        """
        cursor = self.conn.cursor()
        
        # 1. Xử lý bảng Players (Dùng name + club làm key để update nếu tồn tại)
        cursor.execute('''
            INSERT INTO players (name, nationality, position, club)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(player_id) DO UPDATE SET club=excluded.club
        ''', (data['name'], data.get('nat', ''), data.get('pos', ''), data.get('club', '')))
        
        player_id = cursor.lastrowid if cursor.lastrowid else self.get_player_id(data['name'])

        # 2. Chuẩn hóa và chèn Stats
        goals = self.clean_value(str(data.get('goals', 0))) # Tái sử dụng hàm clean cho số
        cursor.execute('''
            INSERT INTO stats (player_id, goals, assists)
            VALUES (?, ?, ?)
        ''', (player_id, int(goals), int(self.clean_value(str(data.get('assists', 0))))))

        # 3. Chuẩn hóa và chèn Market Value
        mkt_val = self.clean_value(data.get('market_value', '0'))
        cursor.execute('''
            INSERT INTO values_history (player_id, market_value)
            VALUES (?, ?)
        ''', (player_id, mkt_val))

        self.conn.commit()

    def get_player_id(self, name):
        res = self.conn.execute('SELECT player_id FROM players WHERE name = ?', (name,)).fetchone()
        return res['player_id'] if res else None

    def close(self):
        self.conn.close()