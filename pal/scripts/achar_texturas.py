"""Para cada textura traduzida no US (listas scripts/imagens/*.py e as dos outros scripts),
acha a mesma textura (ingles) no PAL e lista as texturas do mesmo tamanho no mesmo arquivo PAL."""
import sys, os, struct, hashlib, runpy
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from tpl import listar_com_paleta, BPP

def tpls(d):
    out = []; i = d.find(b'\x00\x20\xaf\x30')
    while i != -1:
        try:
            for k, (w, h, f, o, p) in enumerate(listar_com_paleta(d, i)):
                if 0 < w <= 2048 and 0 < h <= 2048 and o + w * h * BPP.get(f, 8) // 8 <= len(d):
                    out.append((i, k, w, h, f, o))
        except Exception:
            pass
        i = d.find(b'\x00\x20\xaf\x30', i + 4)
    return out

def dados_img(d, w, h, f, o):
    return d[o:o + (w + 7) // 8 * 8 * ((h + 7) // 8 * 8) * BPP.get(f, 8) // 8]

if __name__ == '__main__':
    us_arq, pal_arq = sys.argv[1:3]
    du = open(us_arq, 'rb').read(); dp = open(pal_arq, 'rb').read()
    tp = tpls(dp)
    hp = {hashlib.md5(dados_img(dp, w, h, f, o)).hexdigest(): (b, k) for b, k, w, h, f, o in tp}
    for b, k, w, h, f, o in tpls(du):
        m = hp.get(hashlib.md5(dados_img(du, w, h, f, o)).hexdigest())
        mesmos = [(hex(b2), k2) for b2, k2, w2, h2, f2, o2 in tp if (w2, h2, f2) == (w, h, f)]
        print(f'US 0x{b:X}#{k} {w}x{h} f{f} -> PAL igual: {(hex(m[0]), m[1]) if m else None}; mesmo tamanho no PAL: {mesmos[:12]}')
