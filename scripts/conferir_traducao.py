"""Confere a traducao antes de reinserir.

Para cada mensagem, compara o original (en) com a traducao (ptbr):
  - os codigos de controle (tudo entre chaves, menos quebra de linha {0006}
    e troca de caixa {0005}{0007}) precisam ser os mesmos e na mesma ordem;
  - nenhuma linha pode passar da maior linha do original naquele bloco + 3 letras
    (a fonte e proporcional; no teste, linhas de 35 letras couberam na caixa das salas);
  - todos os caracteres precisam existir na fonte do jogo.

Uso: python -I scripts/conferir_traducao.py <pasta_en> <pasta_ptbr>
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabela import TABELA
from inserir_textos import ler_txt

LINHA = {'0006', '0005', '0007'}
CARACTERES = set(TABELA.values())
TAG = re.compile(r'\{([0-9A-F]{4}|NOFIM)\}')

def codigos(t):
    return [c for c in TAG.findall(t) if c not in LINHA]

def linhas(t):
    return [len(TAG.sub('', l)) for l in re.split(r'\{0006\}|\{0005\}\{0007\}', t)]

def main(pasta_en, pasta_pt):
    problemas = 0
    for dp, _, fs in os.walk(pasta_en):
        for f in fs:
            if not f.endswith('.txt'): continue
            rel = os.path.relpath(os.path.join(dp, f), pasta_en)
            en = ler_txt(os.path.join(dp, f))
            pt = ler_txt(os.path.join(pasta_pt, rel))
            for chave, msgs in en.items():
                # limite por bloco (itens e documentos tem larguras diferentes)
                maior = max((max(linhas(t)) for t in msgs.values()), default=0) + 3
                for i, t_en in msgs.items():
                    t_pt = pt.get(chave, {}).get(i)
                    onde = f'{rel} msg {i}'
                    if t_pt is None:
                        print(f'FALTA: {onde}'); problemas += 1; continue
                    # nomes de local da tela de save: os codigos acompanham cada letra
                    letra_a_letra = '{000B}{0000}{0020}' in t_en
                    if codigos(t_en) != codigos(t_pt) and not letra_a_letra:
                        print(f'CODIGOS DIFERENTES: {onde}\n   en: {t_en}\n   pt: {t_pt}'); problemas += 1
                    if t_pt != t_en and max(linhas(t_pt)) > maior:
                        print(f'LINHA LONGA ({max(linhas(t_pt))} > {maior}): {onde}\n   pt: {t_pt}'); problemas += 1
                    ruins = {c for c in TAG.sub('', t_pt) if c not in CARACTERES}
                    if ruins:
                        print(f'CARACTERE FORA DA FONTE {ruins}: {onde}'); problemas += 1
    print('problemas encontrados:', problemas)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
