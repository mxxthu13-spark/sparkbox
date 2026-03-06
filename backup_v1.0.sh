#!/bin/bash

echo "========================================"
echo "SparkBox v1.0 备份工具"
echo "========================================"
echo ""

BACKUP_DIR="sparkbox_v1.0_backup_$(date +%Y%m%d_%H%M%S)"

echo "创建备份目录: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

echo ""
echo "[1/8] 备份后端代码..."
cp -r backend "$BACKUP_DIR/"
echo "✓ 后端代码备份完成"

echo ""
echo "[2/8] 备份前端代码..."
cp -r frontend "$BACKUP_DIR/"
echo "✓ 前端代码备份完成"

echo ""
echo "[3/8] 备份文档..."
cp -r docs "$BACKUP_DIR/"
echo "✓ 文档备份完成"

echo ""
echo "[4/8] 备份根目录文件..."
cp README.md "$BACKUP_DIR/" 2>/dev/null
cp FINAL_COMPLETE.md "$BACKUP_DIR/" 2>/dev/null
cp COMPLETE.md "$BACKUP_DIR/" 2>/dev/null
echo "✓ 根目录文件备份完成"

echo ""
echo "[5/8] 备份数据库..."
if [ -f backend/sparkbox.db ]; then
    cp backend/sparkbox.db "$BACKUP_DIR/"
    echo "✓ 数据库备份完成"
else
    echo "⚠ 未找到数据库文件"
fi

echo ""
echo "[6/8] 清理临时文件..."
rm -rf "$BACKUP_DIR/backend/venv"
rm -rf "$BACKUP_DIR/backend/__pycache__"
find "$BACKUP_DIR/backend" -name "*.pyc" -delete
find "$BACKUP_DIR/backend" -name "__pycache__" -type d -delete
rm -rf "$BACKUP_DIR/frontend/node_modules"
rm -rf "$BACKUP_DIR/frontend/dist"
echo "✓ 临时文件清理完成"

echo ""
echo "[7/8] 创建版本信息..."
cat > "$BACKUP_DIR/VERSION.txt" << EOF
SparkBox v1.0 备份

备份时间: $(date)
备份内容:
- 后端代码 (backend/)
- 前端代码 (frontend/)
- 文档 (docs/)
- 数据库 (sparkbox.db)
- README.md

恢复说明:
1. 解压备份文件
2. 安装后端依赖: cd backend && pip install -r requirements.txt
3. 安装前端依赖: cd frontend && npm install
4. 配置 .env 文件
5. 启动服务

注意事项:
- 请妥善保管 .env 文件中的密钥
- 数据库文件包含所有用户数据
- 定期备份以防数据丢失
EOF
echo "✓ 版本信息创建完成"

echo ""
echo "[8/8] 压缩备份文件..."
tar -czf "$BACKUP_DIR.tar.gz" "$BACKUP_DIR"
if [ -f "$BACKUP_DIR.tar.gz" ]; then
    echo "✓ 备份文件压缩完成"
    rm -rf "$BACKUP_DIR"
    echo ""
    echo "========================================"
    echo "备份完成！"
    echo "========================================"
    echo ""
    echo "备份文件: $BACKUP_DIR.tar.gz"
    echo "文件大小: $(du -h "$BACKUP_DIR.tar.gz" | cut -f1)"
    echo ""
else
    echo "✗ 压缩失败，保留未压缩的备份目录"
    echo "备份目录: $BACKUP_DIR"
fi

echo "备份完成！"
