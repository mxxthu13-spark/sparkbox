/**
 * 使用 uni-app Canvas 2D API 绘制想法卡片
 * 支持多种模板风格
 */

const CARD_WIDTH = 750
const CARD_HEIGHT = 1000

const TEMPLATES = {
  minimal: {
    bg: '#ffffff',
    textColor: '#1a1a1a',
    subTextColor: '#6b7280',
    accentColor: '#6366f1',
    borderColor: '#e5e7eb',
  },
  night: {
    bg: '#1a1a2e',
    textColor: '#e8e8ff',
    subTextColor: '#9ca3af',
    accentColor: '#818cf8',
    borderColor: '#374151',
  },
  forest: {
    bg: '#1a3a2a',
    textColor: '#c8f0d8',
    subTextColor: '#86efac',
    accentColor: '#34d399',
    borderColor: '#166534',
  },
  warm: {
    bg: '#fff7ed',
    textColor: '#7c2d12',
    subTextColor: '#9a3412',
    accentColor: '#ea580c',
    borderColor: '#fed7aa',
  },
  note: {
    bg: '#fefce8',
    textColor: '#713f12',
    subTextColor: '#92400e',
    accentColor: '#d97706',
    borderColor: '#fde68a',
  },
}

/**
 * 自动换行文字绘制
 */
function drawWrappedText(ctx, text, x, y, maxWidth, lineHeight, maxLines = 0) {
  const chars = text.split('')
  let line = ''
  let lineCount = 0
  const lines = []

  for (let i = 0; i < chars.length; i++) {
    const testLine = line + chars[i]
    const { width } = ctx.measureText(testLine)
    if (width > maxWidth && line.length > 0) {
      lines.push(line)
      line = chars[i]
      lineCount++
      if (maxLines > 0 && lineCount >= maxLines) {
        lines[lines.length - 1] += '...'
        break
      }
    } else {
      line = testLine
    }
  }
  if (line) lines.push(line)

  lines.forEach((l, i) => {
    ctx.fillText(l, x, y + i * lineHeight)
  })
  return lines.length
}

/**
 * 生成卡片 - 返回 canvas 的 base64 图片数据
 */
export async function generateCard({ canvasId, content, templateId = 'minimal', date, author, quote }) {
  return new Promise((resolve, reject) => {
    const template = TEMPLATES[templateId] || TEMPLATES.minimal

    const query = uni.createSelectorQuery()
    query
      .select(`#${canvasId}`)
      .fields({ node: true, size: true })
      .exec((res) => {
        if (!res[0]?.node) {
          reject(new Error('Canvas 节点未找到'))
          return
        }
        const canvas = res[0].node
        const ctx = canvas.getContext('2d')
        const dpr = uni.getSystemInfoSync().pixelRatio || 2
        canvas.width = CARD_WIDTH * dpr
        canvas.height = CARD_HEIGHT * dpr
        ctx.scale(dpr, dpr)

        // 背景
        ctx.fillStyle = template.bg
        ctx.fillRect(0, 0, CARD_WIDTH, CARD_HEIGHT)

        // 顶部装饰条
        ctx.fillStyle = template.accentColor
        ctx.fillRect(0, 0, CARD_WIDTH, 8)

        // Logo & 品牌
        ctx.fillStyle = template.accentColor
        ctx.font = 'bold 28rpx PingFang SC, sans-serif'
        ctx.fillText('⚡ 闪念盒子', 60, 80)

        // 分隔线
        ctx.strokeStyle = template.borderColor
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.moveTo(60, 100)
        ctx.lineTo(CARD_WIDTH - 60, 100)
        ctx.stroke()

        // 主文字
        ctx.fillStyle = template.textColor
        ctx.font = '500 38rpx PingFang SC, sans-serif'
        const textLines = drawWrappedText(ctx, content, 60, 160, CARD_WIDTH - 120, 64, 12)

        // 引号装饰
        ctx.fillStyle = template.accentColor
        ctx.globalAlpha = 0.15
        ctx.font = 'bold 200rpx Georgia'
        ctx.fillText('"', 40, 180)
        ctx.globalAlpha = 1

        // AI 金句
        if (quote) {
          const quoteY = 160 + textLines * 64 + 60
          ctx.fillStyle = template.accentColor
          ctx.globalAlpha = 0.1
          ctx.fillRect(60, quoteY - 30, CARD_WIDTH - 120, textLines * 52 + 60)
          ctx.globalAlpha = 1
          ctx.fillStyle = template.accentColor
          ctx.font = 'italic 500 30rpx PingFang SC'
          ctx.fillText('✦', 80, quoteY + 12)
          ctx.fillStyle = template.subTextColor
          drawWrappedText(ctx, quote, 120, quoteY, CARD_WIDTH - 180, 52, 3)
        }

        // 底部信息
        const bottomY = CARD_HEIGHT - 100
        ctx.strokeStyle = template.borderColor
        ctx.lineWidth = 1
        ctx.beginPath()
        ctx.moveTo(60, bottomY - 20)
        ctx.lineTo(CARD_WIDTH - 60, bottomY - 20)
        ctx.stroke()

        ctx.fillStyle = template.subTextColor
        ctx.font = '24rpx PingFang SC, sans-serif'
        if (date) ctx.fillText(date, 60, bottomY + 20)
        if (author) {
          const authorWidth = ctx.measureText(author).width
          ctx.fillText(author, CARD_WIDTH - 60 - authorWidth, bottomY + 20)
        }

        // 导出图片
        uni.canvasToTempFilePath(
          {
            canvas,
            fileType: 'jpg',
            quality: 0.95,
            success(res) {
              resolve(res.tempFilePath)
            },
            fail(err) {
              reject(err)
            },
          },
          null
        )
      })
  })
}
