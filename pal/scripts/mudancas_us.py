"""Lista as texturas que o tradutor do US alterou (build/imagens_discoN x extraido/discoN)
e onde a mesma textura original (ingles) esta no PAL."""
import sys, os, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from achar_texturas import tpls, dados_img
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
n = sys.argv[1]
img = os.path.join(RAIZ, 'build', f'imagens_disco{n}')
for dp, _, fs in os.walk(img):
    for f in fs:
        rel = os.path.relpath(os.path.join(dp, f), img)
        orig = open(os.path.join(RAIZ, 'extraido', f'disco{n}', 'files', rel), 'rb').read()
        trad = open(os.path.join(dp, f), 'rb').read()
        pal = os.path.join(RAIZ, 'pal', 'extraido', f'disco{n}', 'files', rel)
        dp_ = open(pal, 'rb').read() if os.path.exists(pal) else b''
        hp = {}
        for b, k, w, h, fm, o in tpls(dp_):
            hp.setdefault(hashlib.md5(dados_img(dp_, w, h, fm, o)).hexdigest(), (hex(b), k))
        for b, k, w, h, fm, o in tpls(orig):
            a = dados_img(orig, w, h, fm, o); t = dados_img(trad, w, h, fm, o)
            if a != t:
                print(rel, f'0x{b:X}#{k}', f'{w}x{h} f{fm}', 'PAL EN:', hp.get(hashlib.md5(a).hexdigest()))
