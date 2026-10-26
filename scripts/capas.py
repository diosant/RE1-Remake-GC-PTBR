"""Traduz o titulo e a data/subtitulo das capas dos documentos (subscr.dat).

Cada capa e uma imagem CMPR 512x448. Na faixa das linhas 284-300 ha o titulo
(a esquerda) e um subtitulo (a direita). O script apaga essa faixa onde ha texto
e escreve o texto em portugues com uma fonte de maquina de escrever.

Uso: python -I scripts/capas.py <subscr.dat de entrada> <subscr.dat de saida> [previa.png]
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
from tpl import listar, decodificar_cmpr
from cmpr import regravar

FONTE = r'C:\Windows\Fonts\cour.ttf'
Y0, Y1 = 284, 300          # faixa do texto
COR = (62, 62, 62)
FUNDO = (6, 4, 2)

CAPAS = {
    0x1DA540: ("Diário do Zelador", "9 de maio~19 de maio de 1998"),
    0x1F6580: ("Botânica.......", "dizem que têm poderes de cura."),
    0x2125C0: ("Testamento científico", "Minha querida Alma,"),
    0x22E600: ("Filme.....", "............prova"),
    0x24A640: ("RELATÓRIO DA PLANTA 42", "Cresce num ritmo espantoso."),
    0x266680: ("Experimento de química orgânica", "Tipos e características dos UMB"),
    0x2826C0: ("Chefe de Segurança", "ordens urgentes da sede da Umbrella"),
    0x29E700: ("PROTOCOLOS DE SEGURANÇA", "SUBSOLO 1 ~ 4"),
    0x2BA740: ("Carta de pesquisador", "Minha querida Ada,"),
    0x2D6780: ("FAX", "Exige-se ação imediata."),
    0x2F27C0: ("Testamento científico", "Minha querida Alma,"),
    0x30E800: ("Bilhete de suicídio", "Linda, eu não quero morrer"),
    0x32A840: ("Manual da S.T.A.R.S......", "controles e defesa de emergência"),
    0x346880: ("Foto de família e notas", "Minha querida Lisa,"),
    0x3628C0: ("Foto de família e notas", "Minha querida Lisa,"),
    0x37E900: ("Nota de observação", "Registros do espécime de amostra"),
    0x39A940: ("Diário de G. Trevor", "Como vim parar aqui?"),
    0x3B6980: ("Foto de família e notas", "Minha querida Lisa,"),
    0x3D29C0: ("Foto do Barry", "A família dele"),
    0x3EEA00: ("Livro da Maldição", "Com as quatro no lugar, o mal despertará"),
    0x40AA40: ("V-ACT", "Nota do pesquisador"),
    0x426A80: ("Descarte de cadáveres", "como os V-ACT."),
}

def e_texto(p):
    """Pixel do texto antigo: cinza (sem cor) e de brilho medio."""
    r, g, b = p[:3]
    return 22 < max(r, g, b) < 100 and max(r, g, b) - min(r, g, b) < 14

def limites(px, w):
    """Primeira e ultima coluna com texto antigo na faixa."""
    cols = [x for x in range(w) if sum(e_texto(px[y * w + x]) for y in range(Y0, Y1)) >= 1]
    return (cols[0], cols[-1] + 1) if cols else (20, 500)

def grupos_de_texto(px, w):
    """Trechos de colunas (x0, x1) com texto antigo, juntando letras proximas."""
    cols = [x for x in range(w) if sum(e_texto(px[y * w + x]) for y in range(Y0, Y1)) >= 1]
    grupos = []
    for x in cols:
        if grupos and x - grupos[-1][1] <= 10: grupos[-1][1] = x
        else: grupos.append([x, x])
    return grupos

# trechos (x0, x1) que nao devem ser apagados (fotos no meio da faixa)
PROTEGER = {0x3D29C0: (200, 370)}

def apagar(img, px, w, base=None):
    """Nos trechos com texto antigo, pinta a faixa inteira com o fundo escuro da coluna,
    menos os pixels coloridos/claros (pedacos de foto)."""
    for g0, g1 in grupos_de_texto(px, w):
        for x in range(max(0, g0 - 3), min(w, g1 + 4)):
            if base in PROTEGER and PROTEGER[base][0] <= x < PROTEGER[base][1]:
                continue
            coluna = [px[y * w + x][:3] for y in range(Y0 - 3, Y1 + 3)]
            fundo = min(coluna, key=sum)
            for y in range(Y0 - 1, Y1 + 1):
                r, g, b = px[y * w + x][:3]
                if max(r, g, b) < 110 and max(r, g, b) - min(r, g, b) < 30:
                    img.putpixel((x, y), fundo)

def desenhar(img, texto, x, alinhar, tamanho):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(FONTE, tamanho)
    larg = d.textlength(texto, font=f)
    if alinhar == 'dir': x -= larg
    d.text((x, Y0 + 1), texto, font=f, fill=COR)
    return larg

def main(entrada, saida, previa=None):
    dados = bytearray(open(entrada, 'rb').read())
    tiras = []
    for base, (titulo, sub) in CAPAS.items():
        w, h, fmt, off = listar(dados, base)[0]
        assert (w, h, fmt) == (512, 448, 14), hex(base)
        px = decodificar_cmpr(dados, w, h, off)
        esq, dir_ = limites(px, w)
        img = Image.new('RGB', (w, h)); img.putdata([p[:3] for p in px])
        d = ImageDraw.Draw(img)
        apagar(img, px, w, base)
        tam = 13
        while tam > 8:   # diminui a letra se titulo e subtitulo se encostarem
            f = ImageFont.truetype(FONTE, tam)
            if d.textlength(titulo, font=f) + d.textlength(sub, font=f) + 20 <= dir_ - esq: break
            tam -= 1
        desenhar(img, titulo, esq, 'esq', tam)
        desenhar(img, sub, dir_, 'dir', tam)
        novo = list(img.get_flattened_data()) if hasattr(img, 'get_flattened_data') else list(img.getdata())
        n = regravar(dados, off, w, h, [p[:3] for p in px], novo)
        print(f'capa 0x{base:X}: "{titulo}" / "{sub}" (letra {tam}, {n} blocos)')
        tiras.append(img.crop((0, 278, 512, 306)))
    open(saida, 'wb').write(dados)
    if previa:
        folha = Image.new('RGB', (512, 28 * len(tiras)))
        for i, t in enumerate(tiras): folha.paste(t, (0, 28 * i))
        folha.resize((1024, 56 * len(tiras))).point(lambda v: min(255, v * 3)).save(previa)

if __name__ == '__main__':
    main(*sys.argv[1:4])
