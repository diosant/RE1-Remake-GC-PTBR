"""Telas do final e extras (etc/ending.dat): resultado, premios liberados, menu de extras."""
GA = 'GARA.TTF'
F = dict(m='foto', f=GA)
TIT = dict(F, s=26, cor=(214, 214, 205))
COR = (200, 200, 192)
CORPO = dict(F, s=21, esp=7, cor=COR)

ROUPA = "Você pegou a “Chave do armário”.\n\nUma roupa nova foi liberada.\nAgora você pode trocar de roupa\nna sala de figurinos."
INVIS_TIT = dict(TIT, r=(30, 8, 482, 88), t='AGORA TENTE SOBREVIVER\nAO INIMIGO INVISÍVEL', esp=9)
INVIS = dict(CORPO, r=(8, 312, 504, 402), t='O modo “Inimigo Invisível” foi liberado.\n\nIsso mesmo, você não vê os inimigos!')

def resultado(base):
    return {'arquivo': 'etc/ending.dat', 'base': base, 'itens': [
        dict(F, r=(30, 22, 290, 84), t='RESULTADO', s=62, cor=(225, 228, 240), limiar=12),
        dict(F, r=(24, 118, 200, 145), t='TEMPO DE JOGO', s=21, cor=(225, 228, 240), a='e'),
    ]}

TRABALHOS = [resultado(b) for b in (0x1C320, 0x38360, 0x543A0, 0x703E0, 0x8C420, 0xA8460)] + [
  {'arquivo': 'etc/ending.dat', 'base': 0xC44A0, 'itens': [
    dict(TIT, r=(40, 28, 472, 64), t='JILL GANHOU UMA ROUPA NOVA!'),
    dict(CORPO, r=(36, 284, 476, 412), t=ROUPA)]},
  {'arquivo': 'etc/ending.dat', 'base': 0xFC520, 'itens': [
    dict(TIT, r=(40, 28, 472, 64), t='CHRIS GANHOU UMA ROUPA NOVA!'),
    dict(CORPO, r=(36, 284, 476, 412), t=ROUPA)]},
  {'arquivo': 'etc/ending.dat', 'base': 0x1A46A0, 'itens': [
    dict(TIT, r=(40, 28, 472, 64), t='VOCÊ TEM TODAS AS ROUPAS!'),
    dict(CORPO, r=(36, 284, 476, 412), t=ROUPA)]},
  {'arquivo': 'etc/ending.dat', 'base': 0xE04E0, 'itens': [INVIS_TIT, INVIS]},
  {'arquivo': 'etc/ending.dat', 'base': 0x188660, 'itens': [INVIS_TIT, INVIS]},
  {'arquivo': 'etc/ending.dat', 'base': 0x118560, 'itens': [
    dict(TIT, r=(40, 28, 472, 64), t='CHRIS E JILL AGORA TÊM ISTO!'),
    dict(CORPO, r=(30, 332, 482, 366), t='Você ganhou a “Samurai Edge”, modelo do Barry.')]},
  {'arquivo': 'etc/ending.dat', 'base': 0x1345A0, 'itens': [
    dict(TIT, r=(40, 8, 472, 88), t='CHRIS E JILL AGORA TÊM\nUMA ARMA ESPECIAL!', esp=9),
    dict(CORPO, r=(30, 332, 482, 366), t='Você ganhou um “Lança-foguetes infinito”.')]},
  {'arquivo': 'etc/ending.dat', 'base': 0x1505E0, 'itens': [
    dict(TIT, r=(30, 8, 482, 88), t='AGORA VOCÊ PODE JOGAR O\nMODO SOBREVIVÊNCIA REAL!', esp=9),
    dict(CORPO, r=(6, 94, 506, 398), s=19, esp=6, t=(
        'O modo “Sobrevivência Real”\nfoi liberado.\n\n'
        'Neste modo os baús não são mais ligados.\nOs itens guardados num baú só podem\nser pegos naquele mesmo lugar.\n\n'
        'Além disso, a “mira” passa\na ser manual.\n\n'
        'Este é o recurso “protótipo” que existia\nantes mesmo do primeiro Resident Evil.'))]},
  {'arquivo': 'etc/ending.dat', 'base': 0x16C620, 'itens': [
    dict(TIT, r=(30, 8, 482, 88), t='UM ZUMBI PERIGOSO!?\n··· CUIDADO', esp=9),
    dict(F, r=(160, 172, 350, 202), t='! AVISO !', s=21, cor=(170, 40, 40), limiar=10),
    dict(CORPO, r=(14, 222, 498, 374), t=(
        'Há um zumbi especial à espreita em\nalgum lugar da mansão, equipado com\num grande estoque de granadas.\n\n'
        'Se você encontrar esse zumbi,\nsaia correndo de lá!'))]},
]

# carta do diretor (escrita a mao no papel)
INK = dict(m='claro', f='Inkfree.ttf', a='e', cor=(28, 32, 34), esp=14)
TRABALHOS += [
  {'arquivo': 'etc/ending.dat', 'base': 0x3160C0, 'itens': [
    dict(INK, r=(44, 56, 458, 382), s=21, rot=-4, t=(
      'Obrigado por dedicar o seu tempo para\njogar “biohazard” (Resident Evil)\naté o fim.\n'
      'Se você está lendo esta carta, eu o saúdo!\nVocê é um jogador realmente notável!\n'
      'Imagino que tenha vivido experiências\nbem memoráveis pelo caminho.'))]},
  {'arquivo': 'etc/ending.dat', 'base': 0x332100, 'itens': [
    dict(INK, r=(34, 50, 464, 396), s=21, rot=-3, t=(
      'A dor de ver a tela de “Game Over”\nvez após vez...\nO doce gosto da vitória quando você\n'
      'finalmente zera o jogo...\nA camaradagem que você dividiu\ncom o seu personagem...\n'
      'A emoção... e a sensação esmagadora\nde pavor.'))]},
  {'arquivo': 'etc/ending.dat', 'base': 0x34E140, 'itens': [
    dict(INK, r=(24, 44, 440, 396), s=21, rot=-4, t=(
      'Acreditamos que os jogos são mais do que\no produto de uma equipe.\nÉ preciso o apoio de jogadores\n'
      'dedicados como você para que um\njogo valha a pena.\nPor isso, ficamos muito felizes quando\n'
      'alguém aproveita um dos nossos jogos\ntão a fundo quanto você.')),
    dict(INK, r=(438, 348, 472, 390), t='')]},
  {'arquivo': 'etc/ending.dat', 'base': 0x36A180, 'itens': [
    dict(INK, r=(24, 40, 462, 272), s=21, rot=-3, t=(
      'Por isso, em nome de toda a equipe,\npermita-me agradecer e parabenizá-lo\npelo ótimo trabalho!\n\n'
      'Muito obrigado por jogar!')),
    dict(INK, r=(266, 352, 496, 398), s=19, rot=-3, t='Representante da equipe')]},
]

# menu de extras depois do final e "PRESS BUTTON"
AM = (215, 220, 150)          # amarelo-esverdeado das letras
BR = (120, 120, 40)           # aura
OV = dict(m='transp', f='GARABD.TTF', cor=AM, brilho=BR)
TRABALHOS += [
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 0, 'itens': [
    dict(F, r=(60, 40, 452, 128), t='Obrigado por jogar!!', f='GARABD.TTF', s=50, cor=(225, 230, 160), limiar=14),
    dict(F, r=(84, 155, 430, 200), t='Mensagem do nosso diretor', s=34, cor=(95, 95, 85), limiar=10),
    dict(F, r=(56, 276, 468, 320), t='Desenhos de roupas não usados', s=34, cor=(95, 95, 85), limiar=10),
    dict(F, r=(160, 376, 356, 410), t='Salvar e voltar ao título', s=21, cor=(95, 95, 85), limiar=10),
  ]},
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 1, 'itens': [
    dict(OV, r=(0, 0, 512, 96), t='Mensagem do nosso diretor', s=38)]},
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 2, 'itens': [
    dict(OV, r=(0, 0, 512, 96), t='Desenhos de roupas não usados', s=38)]},
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 3, 'itens': [
    dict(OV, r=(0, 0, 512, 48), t='Salvar e voltar ao título', s=24)]},
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 8, 'itens': [
    dict(OV, r=(0, 0, 136, 40), t='Voltar ao menu', s=19)]},
  {'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': 9, 'itens': [
    dict(OV, r=(0, 0, 136, 40), t='Voltar ao menu', s=19, cor=(150, 150, 110), brilho=(60, 60, 20))]},
  {'arquivo': 'etc/ending.dat', 'base': 0xE0, 'indice': 0, 'itens': [
    dict(m='transp', f='times.ttf', r=(0, 76, 160, 97), t='APERTE UM BOTÃO', s=18, a='e', cor=(235, 235, 235))]},
]
for i, txt, cor in ((4, 'Próx.', AM), (5, 'Próx.', (150, 150, 110)), (6, 'Volta', AM), (7, 'Volta', (150, 150, 110))):
    TRABALHOS.append({'arquivo': 'etc/ending.dat', 'base': 0x266AE0, 'indice': i, 'itens': [
        dict(OV, r=(0, 46, 54 if i < 6 else 52, 72), t=txt, s=17, cor=cor)]})
