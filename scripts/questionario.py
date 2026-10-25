"""Traduz o questionario de dificuldade (subscr/subsel.dat, TPL em 0x0, imagem 0,
CMPR 512x448): apaga as letras escuras do papel e escreve o texto em portugues.

Uso: python -I scripts/questionario.py <subsel.dat entrada> <subsel.dat saida> [previa.png]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tpl import listar, decodificar_cmpr
from cmpr import regravar

F = r'C:\Windows\Fonts'
AREA = (128, 110, 400, 334)            # area do texto antigo no papel
# (x, y da linha de base, texto, fonte, tamanho)
LINHAS = [
    (135, 123, 'PERGUNTA', 'timesbd.ttf', 12),
    (139, 140, 'Qual frase melhor descreve a sua', 'times.ttf', 17),
    (139, 160, 'opinião sobre jogos?', 'times.ttf', 17),
    (130, 194, 'I . ALPINISMO - além das dificuldades', 'times.ttf', 16),
    (148, 214, 'vem a sensação de conquista.', 'times.ttf', 16),
    (130, 254, 'II . CAMINHADA - dá para chegar', 'times.ttf', 16),
    (148, 274, 'ao destino com tranquilidade.', 'times.ttf', 16),
    (198, 324, 'OK  •  •  •  Botão A', 'times.ttf', 16),
]

def main(entrada, saida, previa=None):
    dados = bytearray(open(entrada, 'rb').read())
    w, h, fmt, off = listar(dados, 0)[0]
    assert (w, h, fmt) == (512, 448, 14)
    px = decodificar_cmpr(dados, w, h, off)
    img = Image.new('RGB', (w, h)); img.putdata([p[:3] for p in px])
    x0, y0, x1, y1 = AREA
    lum = lambda p: (p[0] * 3 + p[1] * 6 + p[2]) // 10
    # cor do papel em cada linha = mediana dos pixels claros
    mask = Image.new('L', (w, h), 0); dm = ImageDraw.Draw(mask)
    for y in range(y0, y1):
        lin = sorted(lum(px[y * w + x]) for x in range(x0, x1))
        papel = lin[len(lin) * 2 // 3]
        for x in range(x0, x1):
            if lum(px[y * w + x]) < papel - 22:
                dm.point((x, y), 255)
    mask = mask.filter(ImageFilter.MaxFilter(3))   # pega tambem a borda das letras
    # preenche as letras com o papel em volta (borrao so dentro da mascara)
    papel_img = img.filter(ImageFilter.MedianFilter(9))
    for _ in range(3):
        papel_img = Image.composite(papel_img.filter(ImageFilter.MedianFilter(9)), img, mask)
    img = Image.composite(papel_img, img, mask)
    d = ImageDraw.Draw(img)
    for x, y, texto, fonte, tam in LINHAS:
        f = ImageFont.truetype(os.path.join(F, fonte), tam)
        d.text((x, y), texto, font=f, fill=(28, 26, 24), anchor='ls')
    novo = list(img.get_flattened_data()) if hasattr(img, 'get_flattened_data') else list(img.getdata())
    n = regravar(dados, off, w, h, [p[:3] for p in px], novo)
    open(saida, 'wb').write(dados)
    print(f'questionario: {n} blocos regravados')
    if previa:
        img.save(previa)

if __name__ == '__main__':
    main(*sys.argv[1:4])
