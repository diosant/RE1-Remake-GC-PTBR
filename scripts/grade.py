"""Gera uma imagem ampliada com grade de coordenadas, para achar a posicao dos textos.
Uso: python -I scripts/grade.py <arquivo> <base_tpl_hex> <indice> <x0> <y0> <x1> <y1> <escala> <saida.png>
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from tpl import listar_com_paleta, decodificar, decodificar_cmpr, decodificar_indexada

def carregar(dados, base, idx):
    w, h, fmt, off, pal = listar_com_paleta(dados, base)[idx]
    if fmt == 14: px = decodificar_cmpr(dados, w, h, off)
    elif fmt in (8, 9): px = decodificar_indexada(dados, w, h, fmt, off, pal)
    else: px = decodificar(dados, w, h, fmt, off)
    im = Image.new('RGBA', (w, h)); im.putdata(px)
    return im, (w, h, fmt, off, pal), px

def main(arq, base, idx, x0, y0, x1, y1, esc, saida):
    dados = open(arq, 'rb').read()
    im, _, _ = carregar(dados, int(base, 16), int(idx))
    x0, y0, x1, y1, esc = map(int, (x0, y0, x1, y1, esc))
    fundo = Image.new('RGBA', im.size, (90, 0, 90, 255)); fundo.alpha_composite(im)
    c = fundo.crop((x0, y0, x1, y1)).resize(((x1 - x0) * esc, (y1 - y0) * esc), Image.NEAREST).convert('RGB')
    d = ImageDraw.Draw(c)
    for x in range(x0 - x0 % 10, x1, 10):
        X = (x - x0) * esc
        d.line([(X, 0), (X, 6 if x % 50 else 14)], fill=(255, 0, 0))
        if x % 50 == 0: d.text((X + 2, 2), str(x), fill=(255, 255, 0))
    for y in range(y0 - y0 % 10, y1, 10):
        Y = (y - y0) * esc
        d.line([(0, Y), (6 if y % 50 else 14, Y)], fill=(255, 0, 0))
        if y % 50 == 0: d.text((16, Y - 5), str(y), fill=(0, 255, 255))
    c.save(saida)

if __name__ == '__main__':
    main(*sys.argv[1:10])
