"""
数据库迁移脚本：为 reviews 表添加新字段
运行此脚本以更新现有数据库
"""
import sqlite3
import json

def migrate_database():
    db_path = 'sparkbox.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("开始数据库迁移...")
        
        # 检查字段是否已存在
        cursor.execute("PRAGMA table_info(reviews)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # 添加 category_ids 字段
        if 'category_ids' not in columns:
            print("添加 category_ids 字段...")
            cursor.execute("ALTER TABLE reviews ADD COLUMN category_ids TEXT DEFAULT '[]'")
            print("✓ category_ids 字段已添加")
        else:
            print("✓ category_ids 字段已存在")
        
        # 添加 theme 字段
        if 'theme' not in columns:
            print("添加 theme 字段...")
            cursor.execute("ALTER TABLE reviews ADD COLUMN theme TEXT")
            print("✓ theme 字段已添加")
        else:
            print("✓ theme 字段已存在")
        
        # 添加 review_mode 字段
        if 'review_mode' not in columns:
            print("添加 review_mode 字段...")
            cursor.execute("ALTER TABLE reviews ADD COLUMN review_mode TEXT")
            print("✓ review_mode 字段已添加")
        else:
            print("✓ review_mode 字段已存在")
        
        # 添加 ai_content 字段
        if 'ai_content' not in columns:
            print("添加 ai_content 字段...")
            cursor.execute("ALTER TABLE reviews ADD COLUMN ai_content TEXT")
            print("✓ ai_content 字段已添加")
        else:
            print("✓ ai_content 字段已存在")
        
        # 提交更改
        conn.commit()
        print("\n数据库迁移完成！")
        
        # 显示更新后的表结构
        cursor.execute("PRAGMA table_info(reviews)")
        print("\n当前 reviews 表结构：")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("SparkBox 数据库迁移工具")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    if success:
        print("\n✓ 迁移成功！可以重启后端服务了。")
    else:
        print("\n✗ 迁移失败，请检查错误信息。")
