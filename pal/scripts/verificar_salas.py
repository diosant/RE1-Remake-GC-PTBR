"""Confere as salas alteradas do PAL: em cada secao de texto (tabela de 5 idiomas no inicio),
o bloco espanhol (4o da tabela) tem exatamente o texto portugues do .txt, e o italiano
aponta para um bloco valido (o proprio italiano ou o portugues).
Uso: python -I pal/scripts/verificar_salas.py <pasta_alterados> <pasta_textos_pt>"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pal_texto
from inserir_textos import ler_txt, ler_secoes
from extrair_textos import ler_msgs, para_texto

def bloco_em(d, pos):
    n = struct.unpack_from('>I', d, pos + 4)[0]
    offs = struct.unpack_from('>%dI' % n, d, pos + 8)
    return [para_texto(m).replace('\n', '') for m in ler_msgs(d, pos, offs)]

alt, pasta = sys.argv[1:3]
erros = 0; secoes = 0
for dp, _, fs in os.walk(alt):
    for f in fs:
        if not f.startswith('r'): continue
        rel = os.path.relpath(os.path.join(dp, f), alt)
        d = open(os.path.join(dp, f), 'rb').read()
        textos = ler_txt(os.path.join(pasta, rel + '.txt'))
        pt = [list(textos[k].values()) for k in sorted(textos, key=lambda k: k[1])]
        _, lista = ler_secoes(d, rel)
        for sec in lista:
            if sec + 20 > len(d) or struct.unpack_from('>I', d, sec)[0] != 0x14: continue
            tab = struct.unpack_from('>5I', d, sec)
            if max(tab) > 0x100000 or any(sec + t + 8 > len(d) for t in tab): continue
            secoes += 1
            es = bloco_em(d, sec + tab[3])
            if es not in pt:
                print('ESPANHOL/PORTUGUES DIFERENTE', rel, hex(sec)); erros += 1
            if tab[4] != tab[3]:
                try: bloco_em(d, sec + tab[4])
                except Exception: print('ITALIANO QUEBRADO', rel, hex(sec)); erros += 1
print('secoes conferidas:', secoes, 'erros:', erros)
