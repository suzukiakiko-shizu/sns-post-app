import sqlite3

# DBファイルへのパス
db_path = "db/posts.db"

# DB接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# テーブルがなければ作成
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    category TEXT,
    purpose TEXT,
    target TEXT,
    tone TEXT,
    format TEXT,
    content TEXT,
    thumbnail_copy TEXT,
    image_ideas TEXT,
    hashtags TEXT,
    status TEXT DEFAULT '未承認',
    created_by TEXT,
    created_at TEXT,
    approved_at TEXT
)
""")

# テスト投稿を1件だけ追加（すでにあればスキップ）
cursor.execute("SELECT COUNT(*) FROM posts")
if cursor.fetchone()[0] == 0:
    cursor.execute("""
    INSERT INTO posts (
        title, category, purpose, target, tone, format,
        content, thumbnail_copy, image_ideas, hashtags,
        status, created_by, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "メロンクリームソーダ登場",
        "限定ドリンク",
        "来店促進・親近感UP",
        "常連さん／甘い物好きな方",
        "やさしく・スタッフの声",
        "フィード",
        "6月限定！懐かしのあの味が登場♪",
        "見た目だけじゃない、本気の味",
        "ドリンクの写真＋スタッフの一言",
        "#限定ドリンク #メロンソーダ #沼津三菱",
        "未承認",
        "スタッフA",
        "2025-04-15 12:00"
    ))

conn.commit()
conn.close()

print("✅ posts.db を初期化しました。")
