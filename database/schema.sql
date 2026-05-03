CREATE TABLE IF NOT EXISTS player_values (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player TEXT NOT NULL,
    team TEXT,
    matched_name TEXT DEFAULT 'N/a',
    market_value_text TEXT DEFAULT 'N/a',
    market_value_eur REAL,
    source TEXT DEFAULT 'footballtransfers',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);