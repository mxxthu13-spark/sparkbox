/**
 * H5 Canvas 卡片图片生成工具
 * 生成 750x1000px 的精美卡片并返回 dataURL
 */

const TEMPLATES = {
  minimal: { bg: '#ffffff', text: '#1a1a1a', accent: '#6366f1', subtext: '#9ca3af' },
  night:   { bg: '#1a1a2e', text: '#e8e8ff', accent: '#818cf8', subtext: '#6b7280' },
  forest:  { bg: '#1a3a2a', text: '#c8f0d8', accent: '#34d399', subtext: '#6b7280' },
  warm:    { bg: '#fff7ed', text: '#7c2d12', accent: '#ea580c', subtext: '#9ca3af' },
  note:    { bg: '#fefce8', text: '#713f12', accent: '#d97706', subtext: '#9ca3af' },
}

/**
 * 自动换行文字绘制
 */
function drawWrappedText(ctx, text, x, y, maxWidth, lineHeight) {
  const chars = text.split('')
  let line = ''
  let curY = y
  const lines = []

  for (let i = 0; i < chars.length; i++) {
    const testLine = line + chars[i]
    if (chars[i] === '\n') {
      lines.push(line)
      line = ''
      continue
    }
    const metrics = ctx.measureText(testLine)
    if (metrics.width > maxWidth && line !== '') {
      lines.push(line)
      line = chars[i]
    } else {
      line = testLine
    }
  }
  lines.push(line)

  lines.forEach((l) => {
    ctx.fillText(l, x, curY)
    curY += lineHeight
  })

  return curY
}

/**
 * 生成卡片图片，返回 dataURL
 */
export async function generateCard({ content, templateId = 'minimal', date = '', author = '闪念盒子', quote = '' }) {
  const W = 750
  const H = 1000
  const tpl = TEMPLATES[templateId] || TEMPLATES.minimal

  const canvas = document.createElement('canvas')
  canvas.width = W
  canvas.height = H
  const ctx = canvas.getContext('2d')

  // 背景
  ctx.fillStyle = tpl.bg
  ctx.fillRect(0, 0, W, H)

  // 顶部装饰条
  ctx.fillStyle = tpl.accent
  ctx.beginPath()
  ctx.roundRect(60, 72, 80, 8, 4)
  ctx.fill()

  // 品牌名
  ctx.fillStyle = tpl.accent
  ctx.font = 'bold 28px -apple-system, "PingFang SC", sans-serif'
  ctx.fillText('⚡ 闪念盒子', 60, 136)

  // 分割线
  ctx.strokeStyle = tpl.text
  ctx.globalAlpha = 0.12
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(60, 168)
  ctx.lineTo(W - 60, 168)
  ctx.stroke()
  ctx.globalAlpha = 1

  // 正文
  ctx.fillStyle = tpl.text
  ctx.font = '400 38px -apple-system, "PingFang SC", sans-serif'
  const textEndY = drawWrappedText(ctx, content, 60, 228, W - 120, 64)

  // AI 金句
  if (quote) {
    const quoteY = Math.max(textEndY + 40, 600)
    // 金句背景
    ctx.fillStyle = tpl.accent
    ctx.globalAlpha = 0.1
    ctx.beginPath()
    ctx.roundRect(60, quoteY - 20, W - 120, 120, 12)
    ctx.fill()
    ctx.globalAlpha = 1

    // 金句文字
    ctx.fillStyle = tpl.accent
    ctx.font = 'italic 500 32px -apple-system, "PingFang SC", sans-serif'
    ctx.fillText('✦  ' + quote, 80, quoteY + 28)
  }

  // 底部分割线
  ctx.strokeStyle = tpl.text
  ctx.globalAlpha = 0.1
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(60, H - 120)
  ctx.lineTo(W - 60, H - 120)
  ctx.stroke()
  ctx.globalAlpha = 1

  // 日期
  ctx.fillStyle = tpl.subtext
  ctx.font = '300 24px -apple-system, "PingFang SC", sans-serif'
  ctx.fillText(date, 60, H - 72)

  // 右下角品牌
  ctx.fillStyle = tpl.subtext
  ctx.textAlign = 'right'
  ctx.font = '300 24px -apple-system, "PingFang SC", sans-serif'
  ctx.fillText(author, W - 60, H - 72)
  ctx.textAlign = 'left'

  return canvas.toDataURL('image/png')
}

/**
 * 下载卡片图片到本地
 */
export function downloadCard(dataURL, filename = 'sparkbox-card.png') {
  const a = document.createElement('a')
  a.href = dataURL
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
