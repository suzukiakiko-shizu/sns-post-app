import sqlite3
import os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("db/posts.db")
c = conn.cursor()

# 古いテーブルを削除（なければスキップ）
c.execute("DROP TABLE IF EXISTS post_images")
c.execute("DROP TABLE IF EXISTS posts")

# 新しい posts テーブル
c.execute("""
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body TEXT NOT NULL,
    hashtags TEXT,
    post_date TEXT,
    created_at TEXT,
    status TEXT DEFAULT '未承認',
    thumbnail BLOB
)
""")

# 新しい post_images テーブル
c.execute("""
CREATE TABLE post_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    image BLOB,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
)
""")

conn.commit()
conn.close()

print("✅ テーブルを初期化しました！")
