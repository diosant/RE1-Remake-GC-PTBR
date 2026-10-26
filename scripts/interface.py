"""Traduz os textos desenhados na textura da tela de status (subscr.dat, TPL em 0x0,
imagem CMPR 1024x1024): botoes, avisos de saude, nomes das abas etc.

Cada item: (x0, y0, x1, y1) da area do texto antigo, texto novo, tipo, fonte, tamanho.
  tipo 'botao'  -> fundo opaco: apaga as letras claras e escreve por cima
  tipo 'transp' -> fundo transparente: limpa a area e escreve so as letras

Uso: python -I scripts/interface.py <subscr.dat entrada> <subscr.dat saida> [previa.png]
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from tpl import listar, decodificar_cmpr
from cmpr import regravar

F = r'C:\Windows\Fonts'
SERIF = os.path.join(F, 'georgia.ttf')
SERIF_B = os.path.join(F, 'georgiab.ttf')
TIMES = os.path.join(F, 'times.ttf')
COUR = os.path.join(F, 'cour.ttf')
COUR_B = os.path.join(F, 'courbd.ttf')

ITENS = [
    # botoes do menu principal
    ((760, 252, 850, 272), 'equipar', 'botao', SERIF, 19),
    ((864, 252, 946, 272), 'usar', 'botao', SERIF, 19),
    ((760, 285, 850, 305), 'combinar', 'botao', SERIF, 18),
    ((864, 285, 950, 305), 'examinar', 'botao', SERIF, 18),
    # rotulos ao lado dos botoes (primeiro limpa a coluna inteira)
    ((956, 244, 1022, 310), '', 'transp', SERIF, 13),
    ((958, 247, 1012, 261), 'SAIR', 'transp', SERIF, 13),
    ((958, 261, 1012, 276), 'ARQS', 'transp', SERIF, 13),
    ((958, 278, 1012, 292), 'CHAVE', 'transp', SERIF, 12),
    ((958, 292, 1012, 307), 'MAPA', 'transp', SERIF, 13),
    # sim / nao
    ((730, 452, 802, 474), 'SIM', 'botao', SERIF, 17),
    ((828, 452, 884, 474), 'NÃO', 'botao', SERIF, 17),
    # tela de itens
    ((30, 331, 118, 350), 'R - aproximar', 'botao', SERIF, 13),
    ((30, 363, 118, 383), 'L - afastar', 'botao', SERIF, 13),
    ((16, 387, 92, 411), '', 'transp', SERIF, 11),
    ((18, 390, 90, 406), 'EQUIPADA', 'transp', SERIF, 11),
    ((216, 337, 370, 353), 'ITENS DE DEFESA', 'botao', SERIF, 13),
    ((206, 365, 364, 378), 'ARMA', 'botao', SERIF, 11),
    ((166, 391, 256, 409), 'A - examinar', 'botao', SERIF, 13),
    ((286, 391, 376, 409), 'Y - examinar', 'botao', SERIF, 13),
    # estado de saude (placas claras com letra colorida)
    ((788, 473, 862, 486), 'BEM', 'placa', SERIF_B, 11),
    ((788, 489, 862, 502), 'CUIDADO', 'placa', SERIF_B, 11),
    ((788, 505, 862, 518), 'CUIDADO', 'placa', SERIF_B, 11),
    ((788, 521, 862, 534), 'VENENO', 'placa', SERIF_B, 11),
    ((788, 537, 862, 550), 'PÂNICO', 'placa', SERIF_B, 11),
    ((788, 553, 862, 566), 'PERIGO', 'placa', SERIF_B, 11),
    # personagens
    ((534, 543, 626, 558), 'Equipe Alpha', 'botao', COUR, 14),
    ((534, 559, 626, 574), 'Equipe Bravo', 'botao', COUR, 14),
    ((362, 576, 658, 592), '', 'botao', COUR, 13),
    ((364, 577, 498, 591), 'Posição:Ponta', 'botao', COUR, 13),
    ((500, 577, 656, 591), 'Posição:Retaguarda', 'botao', COUR, 13),
    # listas de itens e bau
    ((814, 599, 990, 615), 'Itens da Rebecca', 'transp', COUR_B, 16),
    ((814, 615, 990, 630), 'Itens do Chris', 'transp', COUR_B, 16),
    ((814, 630, 990, 646), 'Itens da Jill', 'transp', COUR_B, 16),
    ((814, 647, 930, 663), 'BAÚ DE ITENS', 'transp', COUR_B, 16),
    ((656, 673, 782, 692), '', 'transp', COUR_B, 14),
    ((656, 674, 782, 691), 'LISTA DE ITENS', 'transp', COUR_B, 14),
    ((96, 601, 150, 619), '', 'transp', COUR, 14),
    ((96, 602, 150, 618), 'arq. -', 'transp', COUR, 14),
]

def claro(p, limiar):
    return len(p) < 4 or p[3] >= 128 and sum(p[:3]) > limiar * 3

def aplicar(img, px, w, item, previa):
    (x0, y0, x1, y1), texto, tipo, fonte, tam = item
    # cor do texto = pixel mais claro da area original
    cor = max((px[y * w + x] for y in range(y0, y1) for x in range(x0, x1) if px[y * w + x][3] >= 128),
              key=lambda p: sum(p[:3]))[:3]
    if tipo == 'placa':
        # fundo claro, letra colorida: acha as letras (destoam da mediana da linha)
        def dist(a, b): return sum(abs(x - y) for x, y in zip(a[:3], b[:3]))
        def croma(p): return max(p[:3]) - min(p[:3])
        letras = set(); melhor = None
        for y in range(y0, y1):
            lin = sorted((px[y * w + x] for x in range(x0, x1)), key=lambda p: sum(p[:3]))
            med = lin[len(lin) // 2]
            for x in range(x0, x1):
                p = px[y * w + x]
                if dist(p, med) > 70:
                    letras.add((x, y))
                    if melhor is None or croma(p) > croma(melhor): melhor = p
        # apaga puxando a cor do vizinho mais proximo (na mesma linha) que nao e letra
        for (x, y) in letras:
            for k in range(1, x1 - x0):
                for xx in (x - k, x + k):
                    if x0 <= xx < x1 and (xx, y) not in letras:
                        img.putpixel((x, y), px[y * w + xx]); break
                else:
                    continue
                break
        cor = melhor[:3] if melhor else cor
    elif tipo == 'botao':
        for x in range(x0, x1):
            col = [px[y * w + x] for y in range(y0, y1)]
            escuro = min(col, key=lambda p: sum(p[:3]))
            for y in range(y0, y1):
                if sum(px[y * w + x][:3]) > sum(escuro[:3]) + 40:
                    img.putpixel((x, y), escuro)
    else:
        for x in range(x0, x1):
            for y in range(y0, y1):
                img.putpixel((x, y), (0, 0, 0, 0))
    if not texto:
        return
    # escreve o texto centralizado (botao) ou alinhado a esquerda (transp)
    f = ImageFont.truetype(fonte, tam)
    camada = Image.new('L', img.size, 0)
    d = ImageDraw.Draw(camada)
    bb = d.textbbox((0, 0), texto, font=f)
    larg, alt = bb[2] - bb[0], bb[3] - bb[1]
    while larg > x1 - x0 and tam > 8:   # aperta se nao couber
        tam -= 1; f = ImageFont.truetype(fonte, tam)
        bb = d.textbbox((0, 0), texto, font=f); larg, alt = bb[2] - bb[0], bb[3] - bb[1]
    x = x0 + (x1 - x0 - larg) // 2 - bb[0] if tipo in ('botao', 'placa') else x0 - bb[0]
    y = y0 + (y1 - y0 - alt) // 2 - bb[1]
    d.text((x, y), texto, font=f, fill=255)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            a = camada.getpixel((xx, yy))
            if not a: continue
            if tipo == 'transp':
                if a >= 128: img.putpixel((xx, yy), cor + (255,))
            else:
                fundo = img.getpixel((xx, yy))
                img.putpixel((xx, yy), tuple((c * a + f_ * (255 - a)) // 255 for c, f_ in zip(cor, fundo[:3])) + (255,))
    previa.append(img.crop((x0 - 4, y0 - 4, x1 + 4, y1 + 4)))

def main(entrada, saida, previa_png=None):
    dados = bytearray(open(entrada, 'rb').read())
    w, h, fmt, off = listar(dados, 0)[0]
    assert (w, h, fmt) == (1024, 1024, 14)
    px = decodificar_cmpr(dados, w, h, off)
    img = Image.new('RGBA', (w, h)); img.putdata(px)
    previa = []
    for item in ITENS:
        aplicar(img, px, w, item, previa)
    novo = list(img.get_flattened_data()) if hasattr(img, 'get_flattened_data') else list(img.getdata())
    n = regravar(dados, off, w, h, px, novo)
    open(saida, 'wb').write(dados)
    print(f'interface: {len(ITENS)} textos, {n} blocos regravados')
    if previa_png:
        alt = sum(p.size[1] for p in previa); larg = max(p.size[0] for p in previa)
        folha = Image.new('RGBA', (larg, alt), (40, 40, 40, 255)); y = 0
        for p in previa:
            fundo = Image.new('RGBA', p.size, (40, 40, 40, 255)); fundo.alpha_composite(p)
            folha.paste(fundo, (0, y)); y += p.size[1]
        folha.resize((larg * 3, alt * 3), Image.NEAREST).save(previa_png)

if __name__ == '__main__':
    main(*sys.argv[1:4])
