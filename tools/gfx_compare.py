"""그래픽 전/후 비교: python gfx_compare.py 새arc 출력.png 텍스처명[:x0,y0,x1,y1] ... [--scale N]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import subs
from PIL import Image, ImageDraw
new, out = sys.argv[1], sys.argv[2]; args = [a for a in sys.argv[3:] if not a.startswith('--')]
scale = int(next((a.split('=')[1] for a in sys.argv if a.startswith('--scale=')), 1))
OLD = 'work/orig/texture.arc'
def toim(a):
    im = Image.fromarray(a, 'RGBA'); bg = Image.new('RGBA', im.size, (40, 44, 110, 255)); bg.alpha_composite(im); return bg.convert('RGB')
rows = []
for spec in args:
    name, _, box = spec.partition(':')
    o = toim(subs.load_tex(OLD, name)[0]); n = toim(subs.load_tex(new, name)[0])
    if box:
        b = tuple(int(v) for v in box.split(',')); o = o.crop(b); n = n.crop(b)
    o = o.resize((o.width * scale, o.height * scale), Image.NEAREST); n = n.resize((n.width * scale, n.height * scale), Image.NEAREST)
    rows.append((name, o, n))
W = max(r[1].width for r in rows) * 2 + 12; H = sum(r[1].height + 16 for r in rows) + 14
img = Image.new('RGB', (W, H), (0, 0, 0)); d = ImageDraw.Draw(img)
d.text((2, 1), 'BEFORE', fill=(255, 128, 128)); d.text((W // 2 + 4, 1), 'AFTER', fill=(128, 255, 128)); y = 14
for name, o, n in rows:
    d.text((2, y), name, fill=(255, 255, 0)); y += 14
    img.paste(o, (0, y)); img.paste(n, (W // 2 + 6, y)); y += o.height + 2
img.save(out)
