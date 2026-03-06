from abc import ABC, abstractmethod
from typing import Optional


class BaseAIService(ABC):
    @abstractmethod
    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        pass

    async def summarize_thoughts(self, thoughts: list[str]) -> dict:
        content = "\n".join([f"{i+1}. {t}" for i, t in enumerate(thoughts)])
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个善于提炼思想精华的助手。用户会给你一组个人想法，"
                    "请帮助提炼核心洞察。输出格式为 JSON，包含以下字段：\n"
                    '- "summary": 整体总结（2-3句话）\n'
                    '- "insights": 核心洞察列表（3-5条，每条15字以内）\n'
                    '- "keywords": 关键词列表（5-8个）\n'
                    '- "quote": 最有价值的一句金句（从原文中提炼或改写，20字以内）'
                ),
            },
            {
                "role": "user",
                "content": f"请分析以下 {len(thoughts)} 条想法：\n\n{content}",
            },
        ]
        result = await self.chat(messages, temperature=0.5)
        import json
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(result[start:end])
        except Exception:
            pass
        return {"summary": result, "insights": [], "keywords": [], "quote": ""}

    async def refine_thought(self, content: str, mode: str = "polish") -> str:
        mode_prompts = {
            "polish": "将以下想法改写得更加流畅、完整，保留原意但提升表达质量，输出改写后的内容：",
            "expand": "基于以下想法，生成一个完整的思考框架或文章大纲，包含3-5个要点：",
            "quote": "将以下想法提炼为一句精炼的金句（20字以内），直接输出金句，不需要解释：",
            "copywrite": "将以下想法改写为适合社交媒体分享的文案（100字以内），有感染力，直接输出：",
        }
        prompt = mode_prompts.get(mode, mode_prompts["polish"])
        messages = [
            {"role": "system", "content": "你是一个专业的文字润色和内容创作助手。"},
            {"role": "user", "content": f"{prompt}\n\n{content}"},
        ]
        return await self.chat(messages, temperature=0.8)

    async def generate_monthly_report(self, thoughts: list[dict], month: str) -> dict:
        content = "\n".join([
            f"[{t.get('created_at', '')}] [{t.get('category', '无分类')}] {t['content']}"
            for t in thoughts
        ])
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个善于做个人成长总结的助手。根据用户这段时间的想法记录，"
                    "生成一份有温度的月度总结报告。输出格式为 JSON：\n"
                    '- "title": 这个月的主题标题（10字以内）\n'
                    '- "summary": 综合总结（3-4句话，有温度，像朋友写给自己的信）\n'
                    '- "highlights": 亮点时刻列表（3条，从原始想法中选取或提炼）\n'
                    '- "growth": 成长洞察（这段时间你最大的变化或收获，2-3句话）\n'
                    '- "keywords": 高频关键词（5-8个）\n'
                    '- "mood": 整体情绪倾向（积极/平和/低落/充实 等）'
                ),
            },
            {
                "role": "user",
                "content": f"这是我 {month} 的 {len(thoughts)} 条想法记录：\n\n{content}",
            },
        ]
        result = await self.chat(messages, temperature=0.7)
        import json
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(result[start:end])
        except Exception:
            pass
        return {
            "title": f"{month}的思考",
            "summary": result,
            "highlights": [],
            "growth": "",
            "keywords": [],
            "mood": "平和",
        }

    async def generate_three_mode_review(self, thoughts: list[str], style: str = "summary") -> dict:
        """生成三种模式的回顾：摘要、洞察、灵魂"""
        content = "\n".join([f"{i+1}. {t}" for i, t in enumerate(thoughts)])
        
        system_prompt = """你是一位善于洞察人类内心的思想观察者。  
你的任务不是复述用户的笔记，而是从零散的记录中，看见用户的思想脉络、价值观和长期主题。

请遵循以下原则：

1. 不要逐条总结笔记内容
2. 不要复述用户写过的话
3. 重点寻找这些记录背后的：
   - 核心问题
   - 思想倾向
   - 价值观
   - 长期主题
4. 输出应该像一段温和而深刻的内在对话，而不是分析报告
5. 语言简洁但有洞察力
6. 让用户在读到时产生"原来我在想这个"的感觉
7. 写作语气像是在提醒用户，而不是在解释给用户听。避免使用"用户提到""你的笔记显示"等表达。
8. 如果这些记录之间存在共同的长期关注点，请指出这种重复出现的思想线索。
9. 每个模式的内容要简洁有力（150-200字），分2-3个自然段，每段之间用空行分隔。
10. 要像一个懂你的朋友，和你进行深入的灵魂对话。

请根据用户的笔记生成三个不同角度的总结，输出格式为 JSON：

{
  "summary": "【摘要模式】提炼出用户最近一段时间最核心的思考方向。150-200字，分2-3段，段落之间用\\n\\n分隔。",
  "insight": "【洞察模式】指出这些想法背后的思想结构或价值观。150-200字，分2-3段，段落之间用\\n\\n分隔。",
  "soul": "【灵魂模式】像一段人与自己对话的文字，帮助用户看见更深层的意义。150-200字，分2-3段，段落之间用\\n\\n分隔。",
  "theme": "【长期主题】用一句话概括这些记录可能指向的人生主题或长期思考方向（20-30字）"
}

每个总结要简洁有力，分段清晰，不要过长。要像一个懂你的朋友，和你进行深入的灵魂对话。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"请分析以下 {len(thoughts)} 条想法记录：\n\n{content}"},
        ]
        
        result = await self.chat(messages, temperature=0.7)
        
        import json
        try:
            start = result.find("{")
            end = result.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(result[start:end])
        except Exception:
            pass
        
        # 如果解析失败，返回默认结构
        return {
            "summary": result[:200] if len(result) > 200 else result,
            "insight": "暂无洞察",
            "soul": "暂无灵魂对话",
            "theme": "持续探索中",
        }
