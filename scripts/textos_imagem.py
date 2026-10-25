"""Ferramenta geral para trocar textos desenhados em texturas TPL (CMPR ou RGBA8).

As listas de trocas ficam em scripts/imagens/*.py. Cada arquivo define TRABALHOS:
  [{'arquivo': 'subscr/subopt.dat', 'base': 0x0, 'indice': 0, 'itens': [ ... ]}, ...]
Cada item e um dict:
  r      (x0, y0, x1, y1)  area do texto antigo (onde apaga e escreve)
  t      texto novo ('' = so apagar). Use '\\n' para varias linhas.
  m      modo de apagar: 'escuro' (letra clara em fundo escuro), 'claro' (letra escura
         em fundo claro, ex. papel), 'transp' (fundo transparente), 'placa' (letra
         colorida em placa clara)
  f, s   fonte (arquivo em C:\\Windows\\Fonts) e tamanho
  a      alinhamento: 'c' (centro, padrao), 'e' (esquerda), 'd' (direita)
  cor    cor da letra (padrao: a mais clara/escura da area original)
  borda  cor do contorno da letra (opcional)
  esp    espaco extra entre linhas

Uso: python -I scripts/textos_imagem.py <pasta_extraida_files> <pasta_saida> <lista.py> [pasta_previas]
O arquivo de saida e lido de <pasta_saida> se ja existir (assim varias listas se somam).
"""
import sys, os, runpy, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from tpl import listar_com_paleta, decodificar, decodificar_cmpr
from cmpr import regravar

FONTES = r'C:\Windows\Fonts'

def lum(p): return (p[0] * 3 + p[1] * 6 + p[2]) // 10

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

def apagar(img, px, w, item):
    x0, y0, x1, y1 = item['r']; m = item.get('m', 'escuro')
    opacos = [px[y * w + x] for y in range(y0, y1) for x in range(x0, x1) if px[y * w + x][3] >= 128]
    if m == 'claro':
        cor = min(opacos, key=lum)[:3] if opacos else (0, 0, 0)
    else:
        cor = max(opacos, key=lum)[:3] if opacos else (255, 255, 255)
    if m == 'transp':
        for y in range(y0, y1):
            for x in range(x0, x1): img.putpixel((x, y), (0, 0, 0, 0))
    elif m == 'escuro':
        for x in range(x0, x1):
            col = [px[y * w + x] for y in range(y0, y1)]
            fundo = min(col, key=lum)
            for y in range(y0, y1):
                p = px[y * w + x]
                dif = sum(abs(a - b) for a, b in zip(p[:3], fundo[:3]))
                if lum(p) > lum(fundo) + item.get('limiar', 10) or dif > 40:
                    img.putpixel((x, y), fundo[:3] + (p[3],))
    elif m == 'foto':
        # letra clara sobre foto: compara com a mediana da vizinhanca
        rgb = img.convert('RGB')
        viz = rgb.filter(ImageFilter.MedianFilter(item.get('viz', 15)))
        mask = Image.new('L', img.size, 0); dm = ImageDraw.Draw(mask)
        lim = item.get('limiar', 18)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if lum(px[y * w + x]) > lum(viz.getpixel((x, y))) + lim:
                    dm.point((x, y), 255)
        mask = mask.filter(ImageFilter.MaxFilter(5))
        caixa = Image.new('L', img.size, 0); ImageDraw.Draw(caixa).rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
        mask = Image.composite(mask, Image.new('L', img.size, 0), caixa)
        cheio = rgb
        for _ in range(5):
            cheio = Image.composite(cheio.filter(ImageFilter.MedianFilter(11)), rgb, mask)
        alfa = img.getchannel('A')
        img.paste(Image.composite(cheio, rgb, mask).convert('RGBA'), (0, 0))
        img.putalpha(alfa)
    elif m in ('claro', 'placa'):
        mask = Image.new('L', img.size, 0); dm = ImageDraw.Draw(mask)
        for y in range(y0, y1):
            lin = sorted((px[y * w + x] for x in range(x0, x1)), key=lum)
            ref = lin[len(lin) * 2 // 3]
            for x in range(x0, x1):
                p = px[y * w + x]
                dif = sum(abs(a - b) for a, b in zip(p[:3], ref[:3]))
                if (m == 'claro' and lum(p) < lum(ref) - 22) or (m == 'placa' and dif > 70):
                    dm.point((x, y), 255)
        mask = mask.filter(ImageFilter.MaxFilter(3))
        caixa = Image.new('L', img.size, 0); ImageDraw.Draw(caixa).rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
        mask = Image.composite(mask, Image.new('L', img.size, 0), caixa)
        rgb = img.convert('RGB'); cheio = rgb
        for _ in range(4):
            cheio = Image.composite(cheio.filter(ImageFilter.MedianFilter(9)), rgb, mask)
        alfa = img.getchannel('A')
        img.paste(Image.composite(cheio, rgb, mask).convert('RGBA'), (0, 0))
        img.putalpha(alfa)
        if m == 'placa':
            def croma(p): return max(p[:3]) - min(p[:3])
            cor = max(opacos, key=croma)[:3]
    return cor

def escrever(img, item, cor):
    x0, y0, x1, y1 = item['r']; texto = item.get('t', '')
    if not texto: return
    cor = tuple(item.get('cor', cor)); borda = item.get('borda')
    fonte = os.path.join(FONTES, item.get('f', 'georgia.ttf')); tam = item.get('s', 14)
    linhas = texto.split('\n'); esp = item.get('esp', 0)
    f = ImageFont.truetype(fonte, tam)
    sw = 1 if borda else 0
    def medir(f):
        # altura pela caixa real das letras (sem a folga da fonte)
        larg = max(f.getlength(l) for l in linhas) + 2 * sw
        bb = [f.getbbox(l) for l in linhas if l]
        asc = -min(b[1] for b in bb) + f.getmetrics()[0] if bb else f.getmetrics()[0]
        topo = min(b[1] for b in bb) if bb else 0
        fundo = max(b[3] for b in bb) if bb else tam
        return larg, fundo - topo, 0
    larg, asc, desc = medir(f)
    alt_linha = asc + desc + esp
    alt = alt_linha * len(linhas) - esp
    while alt > (y1 - y0) + 2 + item.get('folga', 0) and tam > 7:   # diminui se nao couber na altura
        tam -= 1; f = ImageFont.truetype(fonte, tam); larg, asc, desc = medir(f)
        alt_linha = asc + desc + esp; alt = alt_linha * len(linhas) - esp
    W, H = int(larg) + 4, int(alt) + 4
    camada = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(camada)
    a = item.get('a', 'c')
    for i, l in enumerate(linhas):
        lw = f.getlength(l)
        x = {'c': (W - lw) / 2, 'e': 2 + sw, 'd': W - lw - 2 - sw}[a]
        topo = min(f.getbbox(t)[1] for t in linhas if t)
        d.text((x, 2 - topo + i * alt_linha), l, font=f, fill=cor + (255,),
               stroke_width=sw, stroke_fill=(tuple(borda) + (255,)) if borda else None)
    if item.get('rot'):   # texto inclinado (ex.: letra a mao)
        camada = camada.rotate(item['rot'], resample=Image.BICUBIC, expand=True)
        W, H = camada.size
    if W > x1 - x0:   # aperta na horizontal se nao couber
        camada = camada.resize((x1 - x0, H), Image.LANCZOS); W = x1 - x0
    px_x = {'c': x0 + (x1 - x0 - W) // 2, 'e': x0, 'd': x1 - W}[a]
    px_y = y0 + (y1 - y0 - H) // 2
    if item.get('m') == 'transp':
        # transparencia de 1 bit no CMPR: so pixels bem opacos
        al = camada.getchannel('A').point(lambda v: 255 if v >= 110 else 0)
        camada.putalpha(al)
        img.alpha_composite(camada, (px_x, px_y))
    else:
        alfa = img.getchannel('A')
        img.alpha_composite(camada, (px_x, px_y))
        img.putalpha(alfa)

def processar(dados, trabalho, previas, nome):
    base, idx = trabalho['base'], trabalho.get('indice', 0)
    w, h, fmt, off, pal = listar_com_paleta(dados, base)[idx]
    if fmt == 14: px = decodificar_cmpr(dados, w, h, off)
    elif fmt == 6: px = decodificar(dados, w, h, fmt, off)
    else: raise SystemExit(f'formato {fmt} ainda nao suportado')
    img = Image.new('RGBA', (w, h)); img.putdata(px)
    for item in trabalho['itens']:
        cor = apagar(img, px, w, item)
        escrever(img, item, cor)
    novo = list(img.get_flattened_data()) if hasattr(img, 'get_flattened_data') else list(img.getdata())
    if fmt == 14:
        n = regravar(dados, off, w, h, px, novo)
    else:
        gravar_rgba8(dados, off, w, h, novo); n = -1
    if previas:
        fundo = Image.new('RGBA', img.size, (90, 0, 90, 255)); fundo.alpha_composite(img)
        fundo.convert('RGB').save(os.path.join(previas, f'{nome}_{base:06X}_{idx}.png'))
    return n

def main(raiz, saida, lista, previas=None):
    trabalhos = runpy.run_path(lista)['TRABALHOS']
    if previas: os.makedirs(previas, exist_ok=True)
    por_arquivo = {}
    for t in trabalhos: por_arquivo.setdefault(t['arquivo'], []).append(t)
    for arq, ts in por_arquivo.items():
        dst = os.path.join(saida, arq)
        fonte = dst if os.path.exists(dst) else os.path.join(raiz, arq)
        dados = bytearray(open(fonte, 'rb').read())
        for t in ts:
            n = processar(dados, t, previas, os.path.basename(arq).split('.')[0])
            print(f'{arq} 0x{t["base"]:X}#{t.get("indice", 0)}: {len(t["itens"])} textos ({n} blocos)')
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(dados)

if __name__ == '__main__':
    main(*sys.argv[1:5])
