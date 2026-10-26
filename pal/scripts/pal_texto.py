"""Extrai/insere textos do disco PAL usando os scripts do projeto (scripts/),
mas com uma busca de blocos um pouco mais tolerante: alguns blocos de legenda
do PAL tem muitas falas vazias (so pausa) e o extrator original os ignorava.

Uso:
  python -I pal/scripts/pal_texto.py extrair <pasta_extraida> <pasta_saida>
  python -I pal/scripts/pal_texto.py inserir <pasta_extraida> <pasta_textos> <pasta_saida>
(mesmos argumentos de scripts/extrair_textos.py e scripts/inserir_textos.py)
"""
import os, struct, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
import extrair_textos, inserir_textos
from extrair_textos import ler_msgs, legivel

def achar_blocos_pal(d):
    blocos = []
    pos = 0
    fim = len(d) - 12
    while pos < fim:
        n = struct.unpack_from('>I', d, pos + 4)[0]
        if 1 <= n <= 2000 and struct.unpack_from('>I', d, pos + 8)[0] == 8 + 4 * n:
            offs = struct.unpack_from('>%dI' % n, d, pos + 8) if pos + 8 + 4*n <= len(d) else None
            if offs and all(pos + o < len(d) for o in offs):
                msgs = ler_msgs(d, pos, offs)
                bons = [m for m in msgs if m and legivel(m)]
                # mensagem so de pausa: {0000}{0008}{xxxx}{0001}
                pausas = [m for m in msgs if m and len(m) == 4 and m[0] == 0 and m[1] == 8 and m[3] == 1]
                if None not in msgs and len(bons) >= 1 and len(bons) + len(pausas) >= max(1, (n + 1) // 2):
                    blocos.append((pos, offs, msgs))
                    pos = (pos + max(offs) + 2 + 3) // 4 * 4
                    continue
        pos += 4
    return blocos

ALINHAMENTO = 0x20

def abrir_espaco_pal(dados, bpos, bloco, rel):
    """O bloco novo e maior que o original.
    1) Se couber ate o inicio do proximo bloco (sobra de alinhamento), grava ali.
    2) Nas salas, a secao de texto comeca com uma tabela de 5 deslocamentos (EN DE FR ES IT).
       Se o bloco espanhol (portugues) couber no espaco do espanhol + italiano, grava ali e
       faz o italiano apontar para o mesmo bloco (o arquivo nao muda de tamanho; o disco 2
       quase nao tem espaco livre). Nesse caso, o italiano daquela sala tambem fica em portugues.
    3) Senao, aumenta a secao e empurra o resto do arquivo, corrigindo a tabela, o cabecalho
       (16 ponteiros em 0x00) e a lista em 0x40."""
    sala = os.path.basename(rel).startswith('r')
    inicios = sorted(p for p, _, _ in achar_blocos_pal(bytes(dados)))
    lista = inserir_textos.ler_secoes(dados, rel)[1] if sala else []
    def proximo(pos):
        depois = [p for p in inicios if p > pos] + [v for v in lista if v > pos]
        return min(depois) if depois else len(dados)
    prox = proximo(bpos)
    if bpos + len(bloco) <= prox:
        novo = bytearray(dados)
        novo[bpos:prox] = bloco + b'\0' * (prox - bpos - len(bloco))
        print(f'  {rel}: bloco usou a sobra ate o proximo bloco')
        return novo
    if not sala:
        raise SystemExit(f'ERRO: {rel}: texto grande demais ({len(bloco)} > {prox - bpos}); encurte o texto.')
    cab = list(struct.unpack_from('>16I', dados, 0))
    secao = max(v for v in lista if v <= bpos)
    tabela = list(struct.unpack_from('>5I', dados, secao))
    if tabela[0] != 0x14 or secao + max(tabela) > len(dados):
        raise SystemExit(f'ERRO: {rel}: secao de texto em 0x{secao:X} sem a tabela de idiomas esperada')
    if secao + tabela[3] == bpos and secao + tabela[4] == prox:
        fim_it = proximo(prox)
        if bpos + len(bloco) <= fim_it:
            novo = bytearray(dados)
            novo[bpos:fim_it] = bloco + b'\0' * (fim_it - bpos - len(bloco))
            tabela[4] = tabela[3]
            struct.pack_into('>5I', novo, secao, *tabela)
            print(f'  {rel}: bloco usou o espaco do italiano (italiano aponta para o portugues)')
            return novo
    delta = (len(bloco) - (prox - bpos) + ALINHAMENTO - 1) // ALINHAMENTO * ALINHAMENTO
    resultado = bytearray(dados[:bpos]) + bloco + b'\0' * (prox - bpos + delta - len(bloco)) + dados[prox:]
    tabela = [t + delta if secao + t > bpos else t for t in tabela]
    cab = [v + delta if v > bpos else v for v in cab]
    lista = [v + delta if v > bpos else v for v in lista]
    struct.pack_into('>5I', resultado, secao, *tabela)
    struct.pack_into('>16I', resultado, 0, *cab)
    struct.pack_into('>%dI' % len(lista), resultado, 0x40, *lista)
    print(f'  {rel}: bloco aumentado em {delta} bytes')
    return resultado

extrair_textos.achar_blocos = achar_blocos_pal
inserir_textos.achar_blocos = achar_blocos_pal
inserir_textos.abrir_espaco = abrir_espaco_pal

def subscr_pal(novo, bpos, bloco, dol):
    # no PAL nao sabemos aumentar o subscr.dat (a correcao do main.dol e so do US): so usa a sobra
    return abrir_espaco_pal(novo, bpos, bloco, 'subscr/subscr.dat'), dol, 0
inserir_textos.abrir_espaco_subscr = subscr_pal

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'extrair':
        extrair_textos.main(*sys.argv[2:4])
    elif cmd == 'inserir':
        inserir_textos.main(*sys.argv[2:6])
    else:
        raise SystemExit(__doc__)
