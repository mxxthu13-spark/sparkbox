"""
一键诊断和修复所有问题
"""
import sqlite3
from datetime import datetime
import sys

def diagnose():
    print("=" * 60)
    print("开始诊断...")
    print("=" * 60)
    
    db_path = 'd:/Cursor/sparkbox/backend/sparkbox.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. 检查时间
        print("\n【1. 检查时间】")
        cursor.execute("SELECT created_at FROM thoughts ORDER BY created_at DESC LIMIT 1")
        latest = cursor.fetchone()
        if latest:
            db_time = datetime.fromisoformat(latest[0])
            now = datetime.now()
            diff_hours = (now - db_time).total_seconds() / 3600
            
            print(f"数据库最新时间: {latest[0]}")
            print(f"当前系统时间: {now}")
            print(f"时间差: {diff_hours:.1f} 小时")
            
            if abs(diff_hours) > 1:
                print("❌ 时间不正确！需要修复")
                return False
            else:
                print("✓ 时间正确")
        
        # 2. 检查记录数量
        print("\n【2. 检查记录数量】")
        cursor.execute("SELECT COUNT(*) FROM thoughts WHERE is_deleted = 0")
        count = cursor.fetchone()[0]
        print(f"总想法数: {count}")
        
        cursor.execute("SELECT COUNT(DISTINCT category_id) FROM thoughts WHERE is_deleted = 0 AND category_id IS NOT NULL")
        cat_count = cursor.fetchone()[0]
        print(f"使用的分类数: {cat_count}")
        
        # 3. 检查最新记录
        print("\n【3. 最新5条记录】")
        cursor.execute("""
            SELECT id, content, created_at, category_id 
            FROM thoughts 
            WHERE is_deleted = 0 
            ORDER BY created_at DESC 
            LIMIT 5
        """)
        rows = cursor.fetchall()
        for i, row in enumerate(rows, 1):
            content = row[1][:30] + '...' if len(row[1]) > 30 else row[1]
            print(f"{i}. {row[2]} | {content}")
        
        # 4. 检查分类
        print("\n【4. 分类统计】")
        cursor.execute("""
            SELECT c.name, COUNT(t.id) as count
            FROM categories c
            LEFT JOIN thoughts t ON c.id = t.category_id AND t.is_deleted = 0
            GROUP BY c.id, c.name
            ORDER BY count DESC
        """)
        cats = cursor.fetchall()
        for cat in cats[:5]:
            print(f"  {cat[0]}: {cat[1]} 条")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("诊断完成")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 诊断失败: {e}")
        return False

def fix_order():
    """确保前端按正确顺序显示"""
    print("\n提示：前端排序问题需要检查代码")
    print("应该使用: ORDER BY created_at DESC (最新在前)")

if __name__ == "__main__":
    success = diagnose()
    
    if success:
        print("\n✓ 数据库状态正常")
        print("\n接下来请确保：")
        print("1. 后端已重启")
        print("2. 前端已刷新")
        print("3. 清除浏览器缓存")
    else:
        print("\n需要修复，请运行: python fix_timezone.py")
