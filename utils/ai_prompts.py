from utils.categories import TARGET_CATEGORIES, PURPOSE_CATEGORIES, FORMAT_CATEGORIES

# --- 投稿ネタから構成案を生成するプロンプト ---
def build_structure_prompt(topic: str) -> str:
    target_list = "\n".join([f"- {t}" for t in TARGET_CATEGORIES])
    purpose_list = "\n".join([f"- {p}" for p in PURPOSE_CATEGORIES])
    format_list  = "\n".join([f"- {f}" for f in FORMAT_CATEGORIES])

    prompt = f"""
あなたは、地域密着型の三菱ディーラーが発信するSNSマーケティングの専門家です。

前提として、このアカウントのメインフォロワーは「30〜50代の男性（地域在住・車に関心あり）」です。
ターゲット選定時はこの層に刺さる内容を優先してください。

以下の投稿ネタに対して、あらかじめ定義されたカテゴリ一覧から、最適なターゲット・目的・投稿形式を1つずつ選び、理由も添えて提案してください。

【投稿ネタ】：
{topic}

--- 想定ターゲットカテゴリ ---
{target_list}

--- 投稿の目的一覧 ---
{purpose_list}

--- 投稿形式一覧 ---
{format_list}

出力形式（箇条書き）：
1. 選ばれたターゲットとその理由
2. 選ばれた目的とその理由
3. 選ばれた投稿形式とその理由
4. 投稿の方向性（どんな切り口で伝えると刺さるか）
"""
    return prompt

# --- 選択カテゴリに基づいて構成案を再生成するプロンプト ---
def build_structure_prompt_from_selection(topic: str, target: str, purpose: str, format_type: str) -> str:
    return f"""
あなたは、地域密着型の三菱ディーラーが発信するSNSマーケティングの専門家です。

以下の投稿ネタに対して、指定されたカテゴリに基づいて投稿構成案を提案してください。

【投稿ネタ】：{topic}

【ターゲット】：{target}  
【目的】：{purpose}  
【投稿形式】：{format_type}  

出力形式（箇条書き）：
1. 投稿の方向性（どんな切り口で伝えると刺さるか）
2. 投稿で意識すべきトーン（例：親しみやすく、誠実に、など）
3. 想定される読者の反応やベネフィット（共感ポイント）

簡潔で現場で使いやすい形で提案してください。
"""

# --- 投稿本文・画像案・ハッシュタグなどを生成するプロンプト ---
def build_post_content_prompt(topic: str, target: str, purpose: str, format_type: str) -> str:
    return f"""
あなたは、地域密着型の三菱ディーラーが発信するSNS投稿の専門家です。

以下の条件に基づいて、SNS投稿に必要な要素をすべて出力してください。

【投稿ネタ】：{topic}  
【ターゲット】：{target}  
【目的】：{purpose}  
【投稿形式】：{format_type}  

出力形式：
1. 投稿本文（親しみやすく、絵文字を交えて）
2. サムネイル用キャッチコピー（短く印象的に）
3. Canvaで編集しやすい画像アイデアを1〜3案（構図や要素、配置なども含めて）
4. 人気・関連性のあるハッシュタグを5～10個

30〜50代の男性が興味を持ちやすいようなトーンでお願いします。
"""
