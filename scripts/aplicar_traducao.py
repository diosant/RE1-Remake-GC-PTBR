"""Aplica um dicionario de traducao (scripts/traducoes/*.py) sobre o .txt em ingles
e grava o .txt em portugues. Mensagens que nao estao no dicionario ficam iguais.
Chaves do dicionario: numero (bloco 0) ou (bloco, numero) para os outros blocos.

Uso: python -I scripts/aplicar_traducao.py <traducao.py> <txt_en> <txt_ptbr>
"""
import re, sys, runpy

def main(trad, en, pt):
    T = runpy.run_path(trad)['T']
    texto = open(en, encoding='utf-8').read()
    partes = re.split(r'(### bloco \d+ \(0x[0-9A-F]+\) mensagem \d+\n)', texto)
    out = [partes[0]]
    for k in range(1, len(partes), 2):
        cab, corpo = partes[k], partes[k + 1]
        i = int(re.search(r'mensagem (\d+)', cab).group(1))
        b = int(re.search(r'bloco (\d+)', cab).group(1))
        chave = i if b == 0 else (b, i)
        out.append(cab)
        if chave in T:
            # quebra a linha depois de cada {0006} para ficar legivel no .txt
            out.append(T[chave].replace('{0006}', '{0006}\n') + '\n\n')
        else:
            out.append(corpo)
    open(pt, 'w', encoding='utf-8').write(''.join(out).rstrip('\n') + '\n')

if __name__ == '__main__':
    main(*sys.argv[1:4])
