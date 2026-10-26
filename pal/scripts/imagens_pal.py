"""Leva para o disco PAL as telas (texturas) que ja foram traduzidas no disco US.

No PAL cada tela existe uma vez por idioma (EN DE FR ES IT), com o mesmo desenho.
A textura traduzida do US (gerada por gerar_discoN.bat em build/imagens_discoN) e
copiada para o lugar da versao ESPANHOLA do PAL. As capas dos documentos so existem
uma vez (iguais para todos os idiomas). O menu do titulo do PAL tem outro tamanho
(256x22), entao e desenhado de novo aqui.

Uso: python -I pal/scripts/imagens_pal.py <N>
Le build/imagens_discoN (US traduzido) e pal/extraido/discoN; grava pal/build/imagens_discoN.
"""
import os, struct, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from PIL import Image, ImageDraw, ImageFont
from tpl import listar_com_paleta, decodificar, BPP, BLOCO
from titulo import gravar_rgba8, FONTE as FONTE_TITULO, TEXTOS as TEXTOS_TITULO

# (arquivo no PAL, base#indice no US traduzido) -> base#indice no PAL (versao espanhola)
COPIAS = {
    'subscr/subopt.dat': [((0x0, 0), (0x600C0, 0)),       # menu de opcoes
                          ((0x20040, 0), (0x160200, 0)),  # ajuste de brilho
                          ((0x60080, 0), (0x2A0340, 0)),  # configurar controle
                          ((0xA00C0, 0), (0x3E0480, 0))], # configurar audio
    'subscr/subscr.dat': [((0x0, 0), (0x653080, 0))],     # tela de status (botoes)
    'subscr/subsel.dat': [((0x0, 0), (0x74E80, 0)),       # questionario de dificuldade
                          ((0x0, 2), (0x74E80, 2)),       # carimbo APROVADO
                          ((0x26F80, 12), (0xC2D80, 24))],# SELECAO DE PERSONAGEM
}
# capas dos documentos: base no US -> base no PAL (uma so para todos os idiomas)
CAPAS = dict(zip(
    [0x1DA540, 0x1F6580, 0x2125C0, 0x22E600, 0x24A640, 0x266680, 0x2826C0, 0x29E700, 0x2BA740,
     0x2D6780, 0x2F27C0, 0x30E800, 0x32A840, 0x346880, 0x3628C0, 0x37E900, 0x39A940, 0x3B6980,
     0x3D29C0, 0x3EEA00, 0x40AA40, 0x426A80],
    [0x17B2A0, 0x1972E0, 0x1B3320, 0x1CF360, 0x1EB3A0, 0x2073E0, 0x223420, 0x23F460, 0x25B4A0,
     0x2774E0, 0x293520, 0x2AF560, 0x2CB5A0, 0x2E75E0, 0x303620, 0x31F660, 0x33B6A0, 0x3576E0,
     0x373720, 0x38F760, 0x3AB7A0, 0x3C77E0]))
TITULO_BASE, TITULO_ES = 0x73EA0, 27     # 45 imagens = 9 por idioma; espanhol = 27..35

def pixels(im):
    return im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata()

def tamanho(w, h, f):
    bw, bh = BLOCO[f]
    return (w + bw - 1) // bw * bw * ((h + bh - 1) // bh * bh) * BPP[f] // 8

def copiar(dst, db, di, src, sb, si, onde):
    w, h, f, o, p = listar_com_paleta(src, sb)[si]
    w2, h2, f2, o2, p2 = listar_com_paleta(dst, db)[di]
    if (w, h, f) != (w2, h2, f2):
        raise SystemExit(f'ERRO {onde}: tamanhos diferentes {w}x{h} f{f} x {w2}x{h2} f{f2}')
    n = tamanho(w, h, f)
    dst[o2:o2 + n] = src[o:o + n]
    if p and p2:
        if p[1] != p2[1]: raise SystemExit(f'ERRO {onde}: paletas diferentes')
        dst[p2[2]:p2[2] + 2 * p2[1]] = src[p[2]:p[2] + 2 * p[1]]

def copiar_centralizado(dst, db, di, src, sb, si):
    """Imagem RGBA8 do US num lugar mais largo do PAL: centraliza com transparencia."""
    w, h, f, o, p = listar_com_paleta(src, sb)[si]
    w2, h2, f2, o2, p2 = listar_com_paleta(dst, db)[di]
    assert f == f2 == 6 and h == h2 and w <= w2
    im = Image.new('RGBA', (w, h)); im.putdata(decodificar(src, w, h, 6, o))
    novo = Image.new('RGBA', (w2, h2), (0, 0, 0, 0)); novo.paste(im, ((w2 - w) // 2, 0))
    gravar_rgba8(dst, o2, w2, h2, list(pixels(novo)))

def titulo(dados):
    """Desenha o menu do titulo em portugues nas 9 imagens do espanhol (mesmo metodo do US)."""
    imgs = listar_com_paleta(dados, TITULO_BASE)
    for k, texto in enumerate(TEXTOS_TITULO):
        w, h, fmt, off, _ = imgs[TITULO_ES + k]
        assert fmt == 6
        px = decodificar(dados, w, h, fmt, off)
        ys = [i // w for i, p in enumerate(px) if p[3] > 60]
        y0, y1 = min(ys), max(ys) + 1
        alvo = y1 - y0; tam = alvo + 4
        while ImageFont.truetype(FONTE_TITULO, tam).getbbox('H')[3] - ImageFont.truetype(FONTE_TITULO, tam).getbbox('H')[1] > alvo and tam > 6:
            tam -= 1
        f = ImageFont.truetype(FONTE_TITULO, tam)
        larg = int(f.getlength(texto)) + 2
        mask = Image.new('L', (larg, h), 0)
        ImageDraw.Draw(mask).text((1, y1), texto, font=f, fill=255, anchor='ls')
        if larg > w - 4:
            mask = mask.resize((w - 4, h), Image.LANCZOS)
        final = Image.new('L', (w, h), 0); final.paste(mask, ((w - mask.size[0]) // 2, 0))
        gravar_rgba8(dados, off, w, h, [(255, 255, 255, a) for a in pixels(final)])

def tpls_em_ordem(d):
    out = []; i = d.find(b'\x00\x20\xaf\x30')
    while i != -1:
        try:
            for k, (w, h, f, o, p) in enumerate(listar_com_paleta(d, i)):
                if 0 < w <= 2048 and 0 < h <= 2048: out.append((i, k, w, h, f, o))
        except Exception:
            pass
        i = d.find(b'\x00\x20\xaf\x30', i + 4)
    return out

def main(n):
    us_trad = os.path.join(RAIZ, 'build', f'imagens_disco{n}')
    us_orig = os.path.join(RAIZ, 'extraido', f'disco{n}', 'files')
    pal = os.path.join(RAIZ, 'pal', 'extraido', f'disco{n}', 'files')
    saida = os.path.join(RAIZ, 'pal', 'build', f'imagens_disco{n}')
    def gravar(rel, dados):
        dst = os.path.join(saida, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(dados); print('gravado:', rel)
    def ler_us(rel):
        p = os.path.join(us_trad, rel)
        if not os.path.exists(p): raise SystemExit(f'ERRO: falta {p} (rode antes o gerar_disco{n}.bat do US)')
        return open(p, 'rb').read()
    # menus, status, selecao
    for rel, lista in COPIAS.items():
        src = ler_us(rel); dst = bytearray(open(os.path.join(pal, rel), 'rb').read())
        for (sb, si), (db, di) in lista:
            copiar(dst, db, di, src, sb, si, f'{rel} 0x{db:X}#{di}')
        if rel == 'subscr/subscr.dat':
            for sb, db in CAPAS.items():
                copiar(dst, db, 0, src, sb, 0, f'capa 0x{db:X}')
        gravar(rel, dst)
    # titulo
    dados = bytearray(open(os.path.join(pal, 'etc/title.dat'), 'rb').read())
    titulo(dados); gravar('etc/title.dat', dados)
    # telas do final: o espanhol usa etc/ending_spa.dat, com as texturas na mesma ordem do ending.dat
    orig = open(os.path.join(us_orig, 'etc/ending.dat'), 'rb').read(); src = ler_us('etc/ending.dat')
    dst = bytearray(open(os.path.join(pal, 'etc/ending_spa.dat'), 'rb').read())
    a, b = tpls_em_ordem(orig), tpls_em_ordem(bytes(dst))
    if len(a) != len(b): raise SystemExit('ERRO: ending_spa.dat com outra quantidade de texturas')
    mudou = 0
    for (sb, si, w, h, f, o), (db, di, w2, h2, f2, o2) in zip(a, b):
        t = tamanho(w, h, f)
        if orig[o:o + t] == src[o:o + t]: continue
        if (w, h, f) == (w2, h2, f2): copiar(dst, db, di, src, sb, si, f'ending 0x{db:X}#{di}')
        else: copiar_centralizado(dst, db, di, src, sb, si)
        mudou += 1
    print(f'final: {mudou} texturas traduzidas')
    gravar('etc/ending_spa.dat', dst)

if __name__ == '__main__':
    main(int(sys.argv[1]))
