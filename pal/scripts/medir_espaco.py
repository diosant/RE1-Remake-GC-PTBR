"""Mostra, para cada arquivo, quanto o bloco portugues passa do espaco do bloco espanhol.
Uso: python -I pal/scripts/medir_espaco.py <pasta_extraida> <pasta_textos_pt>"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pal_texto
from inserir_textos import ler_txt, codificar, montar_bloco
raiz, pasta = sys.argv[1:3]
for dp, _, fs in os.walk(pasta):
    for f in sorted(fs):
        rel = os.path.relpath(os.path.join(dp, f), pasta)[:-4]
        d = open(os.path.join(raiz, rel), 'rb').read()
        t = ler_txt(os.path.join(dp, f))
        blocos = pal_texto.achar_blocos_pal(d)
        for bi, (bpos, offs, msgs) in enumerate(blocos):
            novas = [codificar(t[(bi, bpos)][i], rel) for i in range(len(offs))]
            fim = max(o + 2 * len(m) for o, m in zip(offs, msgs))
            prox = blocos[bi + 1][0] if bi + 1 < len(blocos) else None
            novo = len(montar_bloco(struct.unpack_from('>I', d, bpos)[0], offs, novas))
            if novo > fim:
                folga = (prox - bpos - novo) if prox else None
                print(f'{rel:22s} bloco {bi} usa {novo} / original {fim} (falta {novo-fim}); ate o proximo bloco: {prox - bpos if prox else "-"}')
