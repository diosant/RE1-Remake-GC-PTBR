"""Traduz o menu da tela de titulo (etc/title.dat, TPL em 0x76700, 9 imagens RGBA8 170x22).
Letra branca com transparencia; desenhamos o texto novo como mascara de transparencia.

Uso: python -I scripts/titulo.py <title.dat entrada> <title.dat saida> [previa.png]
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from tpl import listar, decodificar

BASE = 0x76700
FONTE = r'C:\Windows\Fonts\GARA.TTF'
TEXTOS = ['CARREGAR JOGO', 'NOVO JOGO', 'OPÇÕES', 'FÁCIL', 'NORMAL', 'DIFÍCIL',
          'DE NOVO....', 'SOBREVIVÊNCIA REAL', 'INIMIGO INVISÍVEL']

def gravar_rgba8(dados, off, w, h, px):
    pos = off
    for by in range(0, h, 4):
        for bx in range(0, w, 4):
            ar = bytearray(32); gb = bytearray(32)
            for i in range(16):
                x, y = bx + i % 4, by + i // 4
                r, g, b, a = px[y * w + x] if x < w and y < h else (0, 0, 0, 0)
                ar[2 * i], ar[2 * i + 1] = a, r
                gb[2 * i], gb[2 * i + 1] = g, b
            dados[pos:pos + 32] = ar; dados[pos + 32:pos + 64] = gb; pos += 64

def main(entrada, saida, previa=None):
    dados = bytearray(open(entrada, 'rb').read())
    imgs = listar(dados, BASE)
    folha = []
    for (w, h, fmt, off), texto in zip(imgs, TEXTOS):
        assert fmt == 6
        px = decodificar(dados, w, h, fmt, off)
        ys = [i // w for i, p in enumerate(px) if p[3] > 60]
        y0, y1 = min(ys), max(ys) + 1          # altura das letras do original
        alvo = y1 - y0
        # tamanho pela altura das maiusculas sem acento; acentos sobem acima da linha
        tam = alvo + 4
        while ImageFont.truetype(FONTE, tam).getbbox('H')[3] - ImageFont.truetype(FONTE, tam).getbbox('H')[1] > alvo and tam > 6:
            tam -= 1
        f = ImageFont.truetype(FONTE, tam)
        larg = int(f.getlength(texto)) + 2
        mask = Image.new('L', (larg, h), 0)
        ImageDraw.Draw(mask).text((1, y1), texto, font=f, fill=255, anchor='ls')
        if larg > w - 4:   # aperta na horizontal (letra condensada, como a original)
            mask = mask.resize((w - 4, h), Image.LANCZOS)
        final = Image.new('L', (w, h), 0)
        final.paste(mask, ((w - mask.size[0]) // 2, 0))
        novo = [(255, 255, 255, a) for a in (final.get_flattened_data() if hasattr(final, 'get_flattened_data') else final.getdata())]
        gravar_rgba8(dados, off, w, h, novo)
        print(f'titulo: "{texto}"')
        img = Image.new('RGBA', (w, h)); img.putdata(novo); folha.append(img)
    open(saida, 'wb').write(dados)
    if previa:
        sh = Image.new('RGBA', (170, 24 * len(folha)), (30, 30, 30, 255))
        for i, im in enumerate(folha): sh.alpha_composite(im, (0, 24 * i))
        sh.resize((340, 48 * len(folha))).save(previa)

if __name__ == '__main__':
    main(*sys.argv[1:4])
