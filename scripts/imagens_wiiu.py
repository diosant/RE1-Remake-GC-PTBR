"""Gera as imagens do titulo do Wii U (para o UWUVCI AIO), uma arte para cada imagem.
TV, GamePad e icone: recorta sem esticar (preenche e corta o que sobra).
Logo: encaixa inteiro, sem cortar, com fundo transparente.
  tv.png      1280x720  (bootTvTex, tela da TV ao abrir o jogo)
  gamepad.png  854x480  (bootDrcTex, tela do GamePad ao abrir o jogo)
  icone.png    128x128  (iconTex, icone no menu do Wii U)
  logo.png     170x42   (bootLogoTex, logo pequeno no canto da tela de abertura)

Uso: python -I scripts/imagens_wiiu.py <arte tv> <arte gamepad> <arte icone> <arte logo> <pasta saida>
"""
import sys, os
from PIL import Image

def recortar(arte, w, h, aparar=0):
    """Escala para cobrir w x h e corta o excesso pelo centro.
    aparar: pixels tirados de cada borda da arte antes (molduras e restos de selo)."""
    img = Image.open(arte).convert('RGB')
    img = img.crop((aparar, aparar, img.width - aparar, img.height - aparar))
    esc = max(w / img.width, h / img.height)
    nova = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    x, y = (nova.width - w) // 2, (nova.height - h) // 2
    return nova.crop((x, y, x + w, y + h))

def encaixar(arte, w, h, margem=2):
    """Corta as bordas transparentes e encaixa inteiro em w x h, centralizado."""
    img = Image.open(arte).convert('RGBA')
    img = img.crop(img.getchannel('A').getbbox())
    esc = min((w - 2 * margem) / img.width, (h - 2 * margem) / img.height)
    img = img.resize((round(img.width * esc), round(img.height * esc)), Image.LANCZOS)
    tela = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    tela.paste(img, ((w - img.width) // 2, (h - img.height) // 2), img)
    return tela

def main(tv, gamepad, icone, logo, saida):
    os.makedirs(saida, exist_ok=True)
    recortar(tv, 1280, 720).save(os.path.join(saida, 'tv.png'))
    recortar(gamepad, 854, 480, aparar=6).save(os.path.join(saida, 'gamepad.png'))
    recortar(icone, 128, 128, aparar=8).convert('RGBA').save(os.path.join(saida, 'icone.png'))
    encaixar(logo, 170, 42).save(os.path.join(saida, 'logo.png'))
    for n in ('tv.png', 'gamepad.png', 'icone.png', 'logo.png'):
        i = Image.open(os.path.join(saida, n))
        print(f'{n:12} {i.width}x{i.height} {i.mode}')

if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
