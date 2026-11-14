// 使い方: node render.js            … 写真/before.jpg と 写真/after.jpg を使って画像を作成
//         node render.js 名前       … 写真/名前_before.jpg と 写真/名前_after.jpg を使用（出力にも名前が付きます）
// 写真が無い場合は、写真の場所を示したサンプル画像を作成します。
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const dir = __dirname;
const name = process.argv[2] || '';
const prefix = name ? name + '_' : '';
const find = (k) => ['jpg', 'jpeg', 'png', 'JPG', 'JPEG', 'PNG']
  .map((e) => path.join(dir, '写真', `${prefix}${k}.${e}`)).find(fs.existsSync);

(async () => {
  const browser = await chromium.launch();
  const before = find('before'), after = find('after');
  const tag = (before && after) ? (name || '完成') : 'サンプル';
  for (const [format, h, label] of [['post', 1350, '投稿'], ['story', 1920, 'ストーリーズ']]) {
    const page = await browser.newPage({ viewport: { width: 1080, height: h } });
    const q = new URLSearchParams({ format });
    if (before) q.set('before', pathToFileURL(before).href);
    if (after) q.set('after', pathToFileURL(after).href);
    await page.goto(pathToFileURL(path.join(dir, 'template.html')).href + '?' + q);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForLoadState('networkidle');
    const out = path.join(dir, `パリジェンヌビフォーアフター_${label}_${tag}.png`);
    await page.screenshot({ path: out });
    console.log('作成:', out);
    await page.close();
  }
  await browser.close();
})();
