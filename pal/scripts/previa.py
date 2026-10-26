"""Salva previas PNG (reduzidas) de texturas TPL: previa.py <arquivo> <saida.png> <escala> base#idx ..."""
import sys, os
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from tpl import listar_com_paleta, decodificar, decodificar_cmpr, decodificar_indexada
from PIL import Image, ImageDraw
def imagem(d, base, idx):
    w, h, f, o, p = listar_com_paleta(d, base)[idx]
    px = decodificar_cmpr(d, w, h, o) if f == 14 else decodificar_indexada(d, w, h, f, o, p) if f in (8, 9) else decodificar(d, w, h, f, o)
    im = Image.new('RGBA', (w, h)); im.putdata(px)
    fundo = Image.new('RGBA', (w, h), (90, 0, 90, 255)); fundo.alpha_composite(im); return fundo.convert('RGB')
arq, saida, esc = sys.argv[1], sys.argv[2], float(sys.argv[3])
d = open(arq, 'rb').read()
ims = []
for a in sys.argv[4:]:
    b, i = a.split('#'); ims.append((a, imagem(d, int(b, 16), int(i))))
W = sum(int(im.width * esc) + 6 for _, im in ims); H = max(int(im.height * esc) for _, im in ims) + 14
out = Image.new('RGB', (W, H), (255, 255, 255)); x = 0; dr = ImageDraw.Draw(out)
for nome, im in ims:
    out.paste(im.resize((int(im.width * esc), int(im.height * esc))), (x, 14)); dr.text((x, 0), nome, fill=(0, 0, 0)); x += int(im.width * esc) + 6
out.save(saida)
