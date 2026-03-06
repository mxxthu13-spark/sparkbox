"""
回退时间修复 - 将时间减去8小时
"""
import sqlite3
from datetime import datetime

def rollback_timezone():
    db_path = 'd:/Cursor/sparkbox/backend/sparkbox.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=" * 50)
        print("回退时间修复...")
        print("=" * 50)
        
        # 查看修复前的数据
        cursor.execute("SELECT created_at FROM thoughts ORDER BY created_at DESC LIMIT 1")
        latest = cursor.fetchone()
        if latest:
            print(f"\n最新记录时间（回退前）: {latest[0]}")
        
        print(f"当前系统时间: {datetime.now()}")
        
        # 回退 thoughts 表（减去8小时）
        print("\n正在回退 thoughts 表...")
        cursor.execute("""
            UPDATE thoughts 
            SET created_at = datetime(created_at, '-8 hours'),
                updated_at = datetime(updated_at, '-8 hours')
        """)
        
        # 回退其他表
        cursor.execute("""
            UPDATE reviews 
            SET created_at = datetime(created_at, '-8 hours')
        """)
        
        cursor.execute("""
            UPDATE cards 
            SET created_at = datetime(created_at, '-8 hours')
        """)
        
        cursor.execute("""
            UPDATE categories 
            SET created_at = datetime(created_at, '-8 hours')
        """)
        
        cursor.execute("""
            UPDATE users 
            SET created_at = datetime(created_at, '-8 hours')
        """)
        
        # 提交更改
        conn.commit()
        
        # 验证修复结果
        cursor.execute("SELECT created_at FROM thoughts ORDER BY created_at DESC LIMIT 1")
        latest_after = cursor.fetchone()
        if latest_after:
            print(f"\n最新记录时间（回退后）: {latest_after[0]}")
        
        print("\n" + "=" * 50)
        print("回退完成！")
        print("=" * 50)
        print("\n请重启后端服务")
        
        conn.close()
        
    except Exception as e:
        print(f"\n回退失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    print("\n此脚本将所有时间减去8小时")
    confirm = input("确认继续？(输入 yes 继续): ")
    if confirm.lower() == 'yes':
        rollback_timezone()
    else:
        print("已取消操作")
