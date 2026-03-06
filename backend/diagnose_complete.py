"""
完整的问题诊断和验证脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import sqlite3
from datetime import datetime

def check_database():
    print("=" * 60)
    print("SparkBox 数据库诊断工具")
    print("=" * 60)
    print()
    
    conn = sqlite3.connect('sparkbox.db')
    cursor = conn.cursor()
    
    # 1. 检查最新想法的时间
    print("[1] 检查最新想法的时间")
    cursor.execute("SELECT content, created_at FROM thoughts WHERE is_deleted = 0 ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"  内容: {row[0][:50]}...")
        print(f"  创建时间: {row[1]}")
        
        # 解析时间
        try:
            db_time = datetime.fromisoformat(row[1].replace(' ', 'T'))
            now = datetime.now()
            diff_hours = (now - db_time).total_seconds() / 3600
            print(f"  当前时间: {now}")
            print(f"  时间差: {diff_hours:.2f} 小时")
            if abs(diff_hours) < 1:
                print("  ✓ 时间正常")
            else:
                print(f"  ⚠ 时间差异较大: {diff_hours:.2f} 小时")
        except Exception as e:
            print(f"  ❌ 时间解析失败: {e}")
    else:
        print("  没有想法记录")
    print()
    
    # 2. 检查回顾记录
    print("[2] 检查回顾记录")
    cursor.execute("SELECT id, title, ai_content, category_ids, thought_count, thought_ids FROM reviews ORDER BY created_at DESC LIMIT 5")
    rows = cursor.fetchall()
    if rows:
        for i, row in enumerate(rows, 1):
            review_id, title, ai_content, category_ids, thought_count, thought_ids = row
            print(f"  [{i}] {title}")
            print(f"      ID: {review_id[:8]}...")
            print(f"      AI内容长度: {len(ai_content) if ai_content else 0} 字符")
            print(f"      分类IDs: {category_ids}")
            print(f"      想法数量: {thought_count}")
            print(f"      想法IDs: {thought_ids[:100]}..." if thought_ids and len(thought_ids) > 100 else f"      想法IDs: {thought_ids}")
            
            # 验证想法数量
            if thought_ids:
                import json
                try:
                    ids = json.loads(thought_ids)
                    actual_count = len(ids)
                    if actual_count == thought_count:
                        print(f"      ✓ 想法数量匹配")
                    else:
                        print(f"      ⚠ 想法数量不匹配: 记录{thought_count}, 实际{actual_count}")
                except:
                    print(f"      ❌ 想法IDs解析失败")
            
            if not ai_content:
                print(f"      ❌ 缺少AI内容")
            else:
                print(f"      ✓ 有AI内容")
            
            if not category_ids or category_ids == '[]':
                print(f"      ⚠ 没有分类信息")
            else:
                print(f"      ✓ 有分类信息")
            print()
    else:
        print("  没有回顾记录")
    print()
    
    # 3. 检查分类统计
    print("[3] 检查分类统计")
    cursor.execute("SELECT category_id, COUNT(*) FROM thoughts WHERE is_deleted = 0 GROUP BY category_id")
    rows = cursor.fetchall()
    if rows:
        for cat_id, count in rows:
            if cat_id:
                cursor.execute("SELECT name, icon FROM categories WHERE id = ?", (cat_id,))
                cat = cursor.fetchone()
                if cat:
                    print(f"  {cat[1]} {cat[0]}: {count} 条")
                else:
                    print(f"  未知分类 ({cat_id[:8]}...): {count} 条")
            else:
                print(f"  无分类: {count} 条")
    else:
        print("  没有想法记录")
    print()
    
    # 4. 检查表结构
    print("[4] 检查 reviews 表结构")
    cursor.execute("PRAGMA table_info(reviews)")
    columns = cursor.fetchall()
    required_fields = ['category_ids', 'theme', 'review_mode', 'ai_content']
    existing_fields = [col[1] for col in columns]
    
    for field in required_fields:
        if field in existing_fields:
            print(f"  ✓ {field}")
        else:
            print(f"  ❌ 缺少字段: {field}")
    print()
    
    conn.close()
    
    print("=" * 60)
    print("诊断完成")
    print("=" * 60)

if __name__ == "__main__":
    check_database()
