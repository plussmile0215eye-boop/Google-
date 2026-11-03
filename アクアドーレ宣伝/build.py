# アクアドーレのポスター（通常版・秋冬版）のHTMLを作るスクリプト
# 使い方: python3 build.py → poster.html と poster_秋冬.html ができる
import pathlib

HERE = pathlib.Path(__file__).parent
QR = (HERE / "img/qr.svg").read_text()

THEMES = {
    "poster.html": dict(
        bg="linear-gradient(165deg,#fbe1e5 0%,#fdf0f1 34%,#eef6fc 66%,#dbedf9 100%)",
        a="#e3828f", a2="#cf7d8a", agrad="linear-gradient(135deg,#f4adb6,#e3828f)",
        b="#4f9fd1", b2="#79acd0", bsoft="#bfdff3", bgrad="linear-gradient(160deg,#95cff0,#5fa9dc)",
        line="#f1c6cb", hl="#fde3a7", text="#5c4a4a", sub="#8c7774",
        arch="linear-gradient(180deg,#d6ebf8,#eef6fc)",
        q="ねぇ、ちゃんと<br>飲めてる？", hook1="みんな、",
        en="Drink more water", snow=False,
    ),
    "poster_秋冬.html": dict(
        bg="linear-gradient(165deg,#efe1d4 0%,#f6ece3 40%,#f2e6db 70%,#e6d5c4 100%)",
        a="#c98b8f", a2="#b9787d", agrad="linear-gradient(135deg,#dcaaaa,#c98b8f)",
        b="#7f9bab", b2="#98aab4", bsoft="#cfd9df", bgrad="linear-gradient(160deg,#afc0cb,#7f97a6)",
        line="#e3c9c2", hl="#ecd5b0", text="#5c4a4a", sub="#8c7774",
        arch="linear-gradient(180deg,#dfe6ea,#f3ece6)",
        q="寒くなると<br>つい飲まなくなるよね？", hook1="冬こそ、",
        en="Warm up with water", snow=True,
    ),
}

SPARK = '<svg class="dec" style="left:{x}mm;top:{y}mm;width:{w}mm" viewBox="0 0 20 20"><path d="M10 0C11 7 13 9 20 10 13 11 11 13 10 20 9 13 7 11 0 10 7 9 9 7 10 0z" fill="{c}"/></svg>'
SNOW = '<svg class="dec" style="left:{x}mm;top:{y}mm;width:{w}mm" viewBox="-10 -10 20 20"><g stroke="{c}" stroke-width="1.4" stroke-linecap="round" fill="none"><path d="M0-9V9M-7.8-4.5 7.8 4.5M-7.8 4.5 7.8-4.5"/><path d="M-2.5-6.5 0-4 2.5-6.5M-2.5 6.5 0 4 2.5 6.5"/></g></svg>'

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:210mm;height:297mm}
body{font-variant-numeric:lining-nums;font-family:'Zen Maru Gothic',sans-serif;color:%(text)s;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.serif{font-family:'Cormorant Garamond',serif}
.page{width:210mm;height:297mm;background:%(bg)s;position:relative;overflow:hidden;padding:10mm 12mm 7mm;display:flex;flex-direction:column}
.page:before{content:"";position:absolute;inset:5mm;border:.35mm solid rgba(255,255,255,.9);border-radius:4mm;pointer-events:none}
.dec{position:absolute;z-index:0}
.top{margin-top:-2mm;display:flex;justify-content:space-between;align-items:baseline;font-family:'Cormorant Garamond',serif;color:%(b)s;font-size:11pt;letter-spacing:.32em;font-weight:600}
.top i{letter-spacing:.04em;font-weight:500;font-size:13pt;color:%(a)s}
.hero{display:flex;justify-content:space-between;align-items:flex-end;margin-top:2mm;position:relative;z-index:1}
.q{font-size:14pt;font-weight:700;color:%(b2)s;line-height:1.35}
.hook{font-size:33pt;font-weight:900;line-height:1.15;margin-top:2mm;white-space:nowrap;color:%(b)s}
.hook em{font-style:normal;color:%(a)s}
.en{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:17pt;color:%(a2)s;margin-top:1mm;font-weight:500}
.ph{width:62mm;height:54mm;position:relative;flex:none}
.arch{position:absolute;left:0;right:0;bottom:0;top:12mm;border-radius:31mm 32mm 3mm 3mm;background:%(arch)s}
.arch2{position:absolute;left:2.5mm;right:-2.5mm;bottom:-2.5mm;top:14.5mm;border-radius:31mm 32mm 3mm 3mm;border:.4mm solid %(a)s;opacity:.6}
.ph img{position:absolute;left:0;bottom:0;width:100%%;border-radius:0 0 3mm 3mm}
.ans{margin-top:3mm;text-align:center;position:relative;z-index:1}
.ans .a1{font-size:12.5pt;font-weight:700;color:%(sub)s;display:flex;align-items:center;justify-content:center;gap:3mm}
.ans .a1:before,.ans .a1:after{content:"";width:14mm;height:.35mm;background:%(a)s;opacity:.5}
.ans .a2{font-size:22pt;font-weight:900;color:%(a)s;line-height:1.3;margin-top:1mm}
.ans .a2 b{background:linear-gradient(transparent 62%%,%(hl)s 62%%);padding:0 1mm}
.name{text-align:center;margin-top:2mm;position:relative;z-index:1}
.name .tag{display:inline-block;font-size:10pt;font-weight:700;color:%(sub)s;border:.35mm solid %(bsoft)s;border-radius:10mm;padding:.6mm 4mm;background:rgba(255,255,255,.6)}
.name .ename{font-family:'Cormorant Garamond',serif;font-style:italic;font-size:14pt;color:%(b2)s;margin-top:.5mm;letter-spacing:.06em}
.name h1{font-size:36pt;font-weight:900;color:%(b)s;letter-spacing:.08em;line-height:1.05}
.name p{font-size:12.5pt;font-weight:700;margin-top:1.5mm}
.name p b{background:linear-gradient(transparent 60%%,%(hl)s 60%%)}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm;margin-top:4mm;position:relative;z-index:1}
.w{background:rgba(255,255,255,.78);border-radius:5mm;padding:2.5mm 2mm 2.5mm;text-align:center;box-shadow:0 .8mm 2.5mm rgba(120,90,90,.07)}
.w .t{font-size:9.5pt;font-weight:900;color:%(b2)s}
.w .b{font-family:'Cormorant Garamond',serif;font-weight:700;font-size:30pt;color:%(a)s;line-height:1}
.w .b small{font-family:'Zen Maru Gothic',sans-serif;font-size:13pt;font-weight:900}
.w .s{font-size:8.5pt;font-weight:700;color:%(sub)s;margin-top:1mm;line-height:1.35}
.free{margin-top:3.5mm;text-align:center;position:relative;z-index:1}
.free small{display:block;font-size:11.5pt;font-weight:900;color:%(a2)s}
.free strong{display:inline-block;font-size:23pt;font-weight:900;color:#fff;background:%(agrad)s;padding:1.3mm 12mm 1.8mm;border-radius:20mm;margin-top:1mm;letter-spacing:.06em;box-shadow:0 1.2mm 3mm rgba(201,120,130,.22)}
.hot{margin-top:2mm;font-size:13pt;font-weight:900}
.hot b{color:%(a2)s;font-size:16pt;background:linear-gradient(transparent 60%%,%(hl)s 60%%);padding:0 .5mm}
.hot span{color:%(b)s}
.u{font-size:10pt;font-weight:700;color:%(sub)s;margin-top:1mm}
.bottom{margin-top:auto;padding-top:3mm;display:flex;gap:4mm;position:relative;z-index:1}
.price{flex:1;background:rgba(255,255,255,.9);border-radius:5mm;padding:3mm 5mm;text-align:center;box-shadow:0 .8mm 2.5mm rgba(120,90,90,.08);display:flex;flex-direction:column;justify-content:center}
.price .l{font-size:11pt;font-weight:900;color:%(a2)s;letter-spacing:.1em}
.price .mo{margin-top:1mm;font-weight:900;font-size:13pt;line-height:1}
.price .mo b{font-family:'Cormorant Garamond',serif;font-weight:700;font-size:42pt;color:%(a)s;letter-spacing:.01em}
.price .mo .tx{font-size:11pt;color:%(sub)s}
.price .inc{font-size:12.5pt;font-weight:900;margin-top:1.5mm}
.price .row{display:flex;gap:2mm;justify-content:center;margin-top:2mm}
.price .row span{font-size:10pt;font-weight:900;border-radius:10mm;padding:1mm 3.5mm;background:%(hlsoft)s}
.qr{width:62mm;background:%(bgrad)s;border-radius:5mm;padding:3.5mm;text-align:center;color:#fff;display:flex;flex-direction:column;align-items:center}
.qr .h{font-weight:900;font-size:13pt;line-height:1.3}
.qr .c{width:34mm;height:34mm;margin-top:2mm;background:#fff;padding:2.2mm;border-radius:2.5mm}
.qr .c svg{display:block}
.qr .f{font-size:9.5pt;font-weight:900;margin-top:1.8mm}
.staff{text-align:center;font-size:11.5pt;font-weight:900;color:%(a2)s;margin-top:2mm;position:relative;z-index:1}
.note{font-size:7pt;color:%(sub)s;text-align:center;margin-top:1mm;font-weight:500;position:relative;z-index:1}
"""

BODY = """<div class="page">%(decor)s
<div class="top"><span>AQUADORE</span><i>for beauty &amp; health</i></div>
<div class="hero">
 <div><div class="q">%(q)s</div><div class="hook">%(hook1)s<br><em>水が足りてない！</em></div><div class="en">%(en)s ♡</div></div>
 <div class="ph"><div class="arch2"></div><div class="arch"></div><img src="img/up.png"></div>
</div>
<div class="ans"><div class="a1">だからこそ、このお水</div><div class="a2"><b>めっちゃおいしい</b>から<br>ついゴクゴク飲んじゃう！</div></div>
<div class="name"><span class="tag">水質にこだわったウォーターサーバー</span><div class="ename">Aquadore</div><h1>アクアドーレ</h1><p>タンクに<b>水道水を注ぐだけ</b>。重いボトルの注文も交換もナシ</p></div>
<div class="why">
 <div class="w"><div class="t">塩素・細菌の除去率</div><div class="b">99.9<small>%%</small></div><div class="s">PFAS・トリハロメタン<br>なども除去</div></div>
 <div class="w"><div class="t">浄水パワー</div><div class="b">2.5<small>台分</small></div><div class="s">一般的なサーバーと<br>比べて</div></div>
 <div class="w"><div class="t">好みで選べる水質</div><div class="b">4<small>種類</small></div><div class="s">水素×シリカ・水素<br>シリカ・バナジウム</div></div>
</div>
<div class="free"><small>1日27Lまで、飲んでも使ってもOK</small><strong>使い放題・飲み放題</strong>
 <div class="hot"><span>♨</span> お湯も出るから、<b>白湯</b>もすぐ飲める！</div>
 <div class="u">白湯に ／ 飲み水に ／ ご飯・お料理に ／ スキンケアに</div></div>
<div class="bottom">
 <div class="price"><div class="l">サーバーレンタル料</div>
  <div class="mo">月額 <b>3,980</b>円<span class="tx">（税抜）</span></div>
  <div class="inc">税込 4,378円</div>
  <div class="row"><span>1日あたり約133円（税抜）</span><span>年1回メンテナンス無料</span></div></div>
 <div class="qr"><div class="h">今日から<br>おいしい水生活！</div><div class="c">%(qr)s</div><div class="f">読み取ってお申し込み</div></div>
</div>
<div class="staff">気になったら、スタッフに気軽に声をかけてね</div>
<div class="note">※1日あたりの金額は税抜月額を30日で割った目安です。除去率・浄水能力はメーカー公表値です。</div>
</div>"""

for name, t in THEMES.items():
    t = dict(t, hlsoft=t["hl"] + "66")
    d = [SPARK.format(x=x, y=y, w=w, c=c) for x, y, w, c in
         [(120, 16, 5, t["hl"]), (113, 27, 3, t["bsoft"]), (8, 118, 3.5, t["line"]), (188, 128, 4, t["hl"])]]
    if t["snow"]:
        d += [SNOW.format(x=x, y=y, w=w, c=t["b2"]) for x, y, w in [(104, 12, 6), (12, 104, 5), (182, 112, 5.5), (190, 205, 4.5)]]
    html = ('<!doctype html><html lang="ja"><head><meta charset="utf-8">'
            '<link href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@500;700;900'
            '&family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500&display=swap" rel="stylesheet">'
            '<style>' + CSS % t + '</style></head><body>'
            + BODY % dict(t, decor="".join(d), qr=QR) + '</body></html>')
    (HERE / name).write_text(html)
    print("wrote", name)
