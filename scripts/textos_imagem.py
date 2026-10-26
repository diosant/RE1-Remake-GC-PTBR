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
from tpl import listar_com_paleta, decodificar, decodificar_cmpr, decodificar_indexada, cor_paleta
from cmpr import regravar

FONTES = r'C:\Windows\Fonts'

def lum(p): return (p[0] * 3 + p[1] * 6 + p[2]) // 10

def preencher(img, mask, raio=4, passos=6):
    """Preenche os pixels marcados em 'mask' com a media dos vizinhos NAO marcados
    (convolucao normalizada), de fora para dentro. Evita manchas escuras."""
    import numpy as np
    rgb = np.asarray(img.convert('RGB'), dtype=np.float32)
    m = np.asarray(mask, dtype=np.float32) / 255.0
    valido = 1.0 - (m > 0.5)
    atual = rgb.copy()
    for _ in range(passos):
        num = Image.fromarray(np.uint8(np.clip(atual * valido[..., None], 0, 255)))
        den = Image.fromarray(np.uint8(valido * 255))
        nb = np.asarray(num.filter(ImageFilter.GaussianBlur(raio)), dtype=np.float32)
        db = np.asarray(den.filter(ImageFilter.GaussianBlur(raio)), dtype=np.float32)[..., None] / 255.0
        cheio = nb / np.maximum(db, 1e-3)
        novos = (valido < 0.5) & (db[..., 0] > 0.05)
        atual[novos] = cheio[novos]
        valido = np.maximum(valido, novos.astype(np.float32))
    out = Image.fromarray(np.uint8(np.clip(atual, 0, 255)))
    alfa = img.getchannel('A')
    res = Image.composite(out, img.convert('RGB'), mask).convert('RGBA'); res.putalpha(alfa)
    return res

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

def gravar_indexada(dados, w, h, fmt, off, pal, antes, depois):
    """C4/C8: troca cada pixel alterado pela cor mais parecida da paleta original."""
    pfmt, cnt, poff = pal
    cores = [cor_paleta(struct.unpack_from('>H', dados, poff + 2 * i)[0], pfmt) for i in range(cnt)]
    cache = {}
    def indice(p):
        if p not in cache:
            cache[p] = min(range(cnt), key=lambda i: sum((a - b) ** 2 for a, b in zip(p, cores[i])) * 1)
        return cache[p]
    bw, bh = (8, 8) if fmt == 8 else (8, 4)
    pos = off; mud = 0
    for by in range(0, h, bh):
        for bx in range(0, w, bw):
            for j in range(bw * bh):
                x, y = bx + j % bw, by + j // bw
                if x < w and y < h and tuple(antes[y * w + x]) != tuple(depois[y * w + x]):
                    k = indice(tuple(depois[y * w + x])); mud += 1
                    if fmt == 9:
                        dados[pos + j] = k
                    else:
                        b = dados[pos + j // 2]
                        dados[pos + j // 2] = (k << 4 | b & 15) if j % 2 == 0 else (b & 0xF0 | k)
            pos += bw * bh * (4 if fmt == 8 else 8) // 8
    return mud

def apagar(img, px, w, item):
    x0, y0, x1, y1 = item['r']; m = item.get('m', 'escuro')
    marcados = []   # pixels da letra antiga (para saber o espaco exato que ela ocupava)
    opacos = [px[y * w + x] for y in range(y0, y1) for x in range(x0, x1) if px[y * w + x][3] >= 128]
    if m == 'claro':
        cor = min(opacos, key=lum)[:3] if opacos else (0, 0, 0)
    else:
        cor = max(opacos, key=lum)[:3] if opacos else (255, 255, 255)
    if m == 'transp' and item.get('poli'):
        mask = Image.new('L', img.size, 0); ImageDraw.Draw(mask).polygon(item['poli'], fill=255)
        img.paste(Image.new('RGBA', img.size, (0, 0, 0, 0)), (0, 0), mask)
    elif m == 'transp':
        for y in range(y0, y1):
            for x in range(x0, x1):
                if px[y * w + x][3] >= 128: marcados.append((x, y))
                img.putpixel((x, y), (0, 0, 0, 0))
    elif m == 'escuro':
        for x in range(x0, x1):
            col = [px[y * w + x] for y in range(y0, y1)]
            fundo = tuple(item['fundo']) + (255,) if item.get('fundo') else min(col, key=lum)
            for y in range(y0, y1):
                p = px[y * w + x]
                dif = sum(abs(a - b) for a, b in zip(p[:3], fundo[:3]))
                if lum(p) > lum(fundo) + item.get('limiar', 10) or dif > 40:
                    img.putpixel((x, y), fundo[:3] + (p[3],))
                    if lum(p) > lum(fundo) + 40: marcados.append((x, y))
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
        viz = img.convert('RGB').filter(ImageFilter.MedianFilter(item.get('viz', 13)))
        for y in range(y0, y1):
            lin = sorted((px[y * w + x] for x in range(x0, x1)), key=lum)
            ref_linha = lin[len(lin) * 2 // 3]
            for x in range(x0, x1):
                p = px[y * w + x]
                if m == 'claro':
                    # letra escura: bem mais escura que o papel em volta
                    ref = viz.getpixel((x, y))
                    ref = ref if lum(ref) > lum(ref_linha) - 40 else ref_linha
                    marca = lum(p) < lum(ref) - item.get('limiar', 24)
                else:
                    marca = sum(abs(a - b) for a, b in zip(p[:3], ref_linha[:3])) > 70
                if marca:
                    dm.point((x, y), 255)
        mask = mask.filter(ImageFilter.MaxFilter(item.get('dil', 3)))
        caixa = Image.new('L', img.size, 0); ImageDraw.Draw(caixa).rectangle((x0, y0, x1 - 1, y1 - 1), fill=255)
        mask = Image.composite(mask, Image.new('L', img.size, 0), caixa)
        img.paste(preencher(img, mask), (0, 0))
        if m == 'placa':
            def croma(p): return max(p[:3]) - min(p[:3])
            cor = max(opacos, key=croma)[:3]
    caixa_antiga = None
    if marcados:
        xs = [a for a, b in marcados]; ys = [b for a, b in marcados]
        caixa_antiga = (min(xs), min(ys), max(xs) + 1, max(ys) + 1)
    return cor, caixa_antiga

def escrever(img, item, cor, caixa_antiga=None):
    x0, y0, x1, y1 = item['r']; texto = item.get('t', '')
    if not texto: return
    # Muitos textos sao recortes fixos da imagem (cada palavra e um 'sprite'): o texto
    # novo precisa ficar inteiro dentro do espaco exato da palavra antiga, senao sai
    # cortado no jogo. Acentos contam na altura.
    padrao = item.get('m', 'escuro') in ('transp', 'escuro', 'placa')
    if item.get('caber', padrao) and caixa_antiga and '\n' not in texto:
        bx0, by0, bx1, by1 = caixa_antiga
        # altura: a da palavra antiga (com uma folguinha para acentos); largura: a area toda
        f_ = item.get('folga_v', 2)
        y0, y1 = by0 - f_ // 2, by1 + (f_ - f_ // 2)
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
    while alt > (y1 - y0) + item.get('folga', 0) and tam > 6:   # diminui se nao couber na altura
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
    px_y = y0 + (y1 - y0 - (H - 4)) // 2 - 2
    if item.get('brilho'):   # aura em volta da letra (como nos menus do final)
        aura = Image.new('RGBA', camada.size, tuple(item['brilho']) + (0,))
        al = camada.getchannel('A').filter(ImageFilter.GaussianBlur(3)).point(lambda v: min(255, v * 2))
        aura.putalpha(al)
        aura.alpha_composite(camada); camada = aura
    if item.get('m') == 'transp' and not item.get('_rgba'):
        # transparencia de 1 bit no CMPR: so pixels bem opacos
        al = camada.getchannel('A').point(lambda v: 255 if v >= 110 else 0)
        camada.putalpha(al)
        img.alpha_composite(camada, (px_x, px_y))
    elif item.get('m') == 'transp':
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
    elif fmt in (8, 9): px = decodificar_indexada(dados, w, h, fmt, off, pal)
    else: raise SystemExit(f'formato {fmt} ainda nao suportado')
    img = Image.new('RGBA', (w, h)); img.putdata(px)
    itens = [dict(item, _rgba=(fmt in (6, 8, 9))) for item in trabalho['itens']]
    # primeiro apaga tudo, depois escreve (assim um texto novo nao e apagado pelo vizinho)
    feitos = [apagar(img, px, w, item) for item in itens]
    for item, (cor, caixa) in zip(itens, feitos):
        escrever(img, item, cor, caixa)
    novo = list(img.get_flattened_data()) if hasattr(img, 'get_flattened_data') else list(img.getdata())
    if fmt == 14:
        n = regravar(dados, off, w, h, px, novo)
    elif fmt in (8, 9):
        n = gravar_indexada(dados, w, h, fmt, off, pal, px, novo)
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
