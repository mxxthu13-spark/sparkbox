"""
测试脚本：验证回顾功能
"""
import sqlite3
from datetime import datetime

db_path = 'd:/Cursor/sparkbox/backend/sparkbox.db'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("检查 reviews 表结构")
    print("=" * 60)
    cursor.execute("PRAGMA table_info(reviews)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]}: {col[2]}")
    
    print("\n" + "=" * 60)
    print("最新的3条回顾记录")
    print("=" * 60)
    cursor.execute("""
        SELECT id, title, thought_count, category_ids, theme, review_mode, 
               period_start, period_end, created_at
        FROM reviews 
        ORDER BY created_at DESC 
        LIMIT 3
    """)
    
    reviews = cursor.fetchall()
    for i, r in enumerate(reviews, 1):
        print(f"\n回顾 {i}:")
        print(f"  ID: {r[0]}")
        print(f"  标题: {r[1]}")
        print(f"  想法数: {r[2]}")
        print(f"  分类IDs: {r[3]}")
        print(f"  主题: {r[4]}")
        print(f"  模式: {r[5]}")
        print(f"  时间: {r[6]} ~ {r[7]}")
        print(f"  创建时间: {r[8]}")
    
    print("\n" + "=" * 60)
    print("检查想法记录")
    print("=" * 60)
    cursor.execute("""
        SELECT COUNT(*) as total,
               COUNT(DISTINCT category_id) as categories
        FROM thoughts 
        WHERE is_deleted = 0
    """)
    stats = cursor.fetchone()
    print(f"  总想法数: {stats[0]}")
    print(f"  分类数: {stats[1]}")
    
    print("\n" + "=" * 60)
    print("按分类统计")
    print("=" * 60)
    cursor.execute("""
        SELECT c.name, c.id, COUNT(t.id) as count
        FROM categories c
        LEFT JOIN thoughts t ON c.id = t.category_id AND t.is_deleted = 0
        GROUP BY c.id, c.name
        ORDER BY count DESC
    """)
    for cat in cursor.fetchall():
        print(f"  {cat[0]}: {cat[2]} 条 (ID: {cat[1]})")
    
    conn.close()
    
except Exception as e:
    print(f"\n错误: {e}")
