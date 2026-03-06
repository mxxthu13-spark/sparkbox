import sys

file_path = 'd:/Cursor/sparkbox/frontend/src/pages/settings/index.vue'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("'simple'", "'summary'")
content = content.replace('简洁', '摘要模式')
content = content.replace("'detailed'", "'insight'")
content = content.replace('详细', '洞察模式')
content = content.replace("'poetic'", "'soul'")
content = content.replace('诗意', '灵魂模式')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('替换完成')
