"""
修复旧的回顾记录，确保所有字段都存在
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.config import settings

# 创建数据库连接
engine = create_engine(settings.DATABASE_URL.replace('+aiosqlite', ''))
SessionLocal = sessionmaker(bind=engine)

def fix_reviews():
    db = SessionLocal()
    try:
        # 检查 reviews 表结构
        result = db.execute(text("PRAGMA table_info(reviews)"))
        columns = {row[1] for row in result}
        
        print("当前 reviews 表的字段:")
        for col in sorted(columns):
            print(f"  - {col}")
        
        # 检查是否缺少新字段
        required_fields = ['category_ids', 'theme', 'review_mode', 'ai_content']
        missing_fields = [f for f in required_fields if f not in columns]
        
        if missing_fields:
            print(f"\n缺少字段: {missing_fields}")
            print("正在添加缺少的字段...")
            
            if 'category_ids' not in columns:
                db.execute(text("ALTER TABLE reviews ADD COLUMN category_ids TEXT DEFAULT '[]'"))
                print("  ✓ 添加 category_ids 字段")
            
            if 'theme' not in columns:
                db.execute(text("ALTER TABLE reviews ADD COLUMN theme VARCHAR(200)"))
                print("  ✓ 添加 theme 字段")
            
            if 'review_mode' not in columns:
                db.execute(text("ALTER TABLE reviews ADD COLUMN review_mode VARCHAR(20)"))
                print("  ✓ 添加 review_mode 字段")
            
            if 'ai_content' not in columns:
                db.execute(text("ALTER TABLE reviews ADD COLUMN ai_content TEXT"))
                print("  ✓ 添加 ai_content 字段")
            
            db.commit()
            print("\n字段添加完成！")
        else:
            print("\n所有必需字段都存在。")
        
        # 查询所有回顾记录
        result = db.execute(text("SELECT id, title, ai_content, ai_summary, ai_insights FROM reviews"))
        reviews = result.fetchall()
        
        print(f"\n找到 {len(reviews)} 条回顾记录")
        
        # 检查哪些记录缺少 ai_content
        empty_content_count = 0
        for review in reviews:
            review_id, title, ai_content, ai_summary, ai_insights = review
            if not ai_content:
                empty_content_count += 1
                print(f"\n记录 '{title}' (ID: {review_id[:8]}...) 缺少 ai_content")
                
                # 尝试从 ai_summary 或 ai_insights 恢复内容
                content = ai_summary or ai_insights or ""
                if content:
                    db.execute(
                        text("UPDATE reviews SET ai_content = :content WHERE id = :id"),
                        {"content": content, "id": review_id}
                    )
                    print(f"  ✓ 已从 {'ai_summary' if ai_summary else 'ai_insights'} 恢复内容")
        
        if empty_content_count > 0:
            db.commit()
            print(f"\n已修复 {empty_content_count} 条记录")
        else:
            print("\n所有记录都有 ai_content，无需修复")
        
        print("\n✅ 数据库检查和修复完成！")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("SparkBox 回顾记录修复工具")
    print("=" * 60)
    fix_reviews()
