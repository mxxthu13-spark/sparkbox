"""
修复数据库中的时间问题
将所有 UTC 时间转换为中国时间（+8小时）
"""
import sqlite3
from datetime import datetime

def fix_timezone():
    db_path = 'd:/Cursor/sparkbox/backend/sparkbox.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 备份提示
        print("=" * 50)
        print("开始修复时间...")
        print("=" * 50)
        
        # 查看修复前的数据
        cursor.execute("SELECT COUNT(*) FROM thoughts")
        thought_count = cursor.fetchone()[0]
        print(f"\n找到 {thought_count} 条想法记录")
        
        cursor.execute("SELECT created_at FROM thoughts ORDER BY created_at DESC LIMIT 1")
        latest = cursor.fetchone()
        if latest:
            print(f"最新记录时间（修复前）: {latest[0]}")
        
        # 修复 thoughts 表
        print("\n正在修复 thoughts 表...")
        cursor.execute("""
            UPDATE thoughts 
            SET created_at = datetime(created_at, '+8 hours'),
                updated_at = datetime(updated_at, '+8 hours')
        """)
        
        # 修复 reviews 表
        cursor.execute("SELECT COUNT(*) FROM reviews")
        review_count = cursor.fetchone()[0]
        if review_count > 0:
            print(f"正在修复 reviews 表（{review_count} 条记录）...")
            cursor.execute("""
                UPDATE reviews 
                SET created_at = datetime(created_at, '+8 hours')
            """)
        
        # 修复 cards 表
        cursor.execute("SELECT COUNT(*) FROM cards")
        card_count = cursor.fetchone()[0]
        if card_count > 0:
            print(f"正在修复 cards 表（{card_count} 条记录）...")
            cursor.execute("""
                UPDATE cards 
                SET created_at = datetime(created_at, '+8 hours')
            """)
        
        # 修复 categories 表
        cursor.execute("SELECT COUNT(*) FROM categories")
        category_count = cursor.fetchone()[0]
        if category_count > 0:
            print(f"正在修复 categories 表（{category_count} 条记录）...")
            cursor.execute("""
                UPDATE categories 
                SET created_at = datetime(created_at, '+8 hours')
            """)
        
        # 修复 users 表
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            print(f"正在修复 users 表（{user_count} 条记录）...")
            cursor.execute("""
                UPDATE users 
                SET created_at = datetime(created_at, '+8 hours')
            """)
        
        # 提交更改
        conn.commit()
        
        # 验证修复结果
        cursor.execute("SELECT created_at FROM thoughts ORDER BY created_at DESC LIMIT 1")
        latest_after = cursor.fetchone()
        if latest_after:
            print(f"\n最新记录时间（修复后）: {latest_after[0]}")
        
        print("\n" + "=" * 50)
        print("✓ 时间修复完成！")
        print("=" * 50)
        print(f"\n当前系统时间: {datetime.now()}")
        print("\n请重启后端服务以使更改生效。")
        
        conn.close()
        
    except Exception as e:
        print(f"\n✗ 修复失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("\n⚠️  警告：此脚本将修改数据库中的所有时间数据")
    print("建议先备份数据库文件：sparkbox.db\n")
    
    confirm = input("确认继续？(输入 yes 继续): ")
    if confirm.lower() == 'yes':
        fix_timezone()
    else:
        print("已取消操作")
