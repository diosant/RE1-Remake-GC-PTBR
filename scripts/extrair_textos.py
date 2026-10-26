"""Extrai os blocos de mensagens do RE Remake GC para arquivos .txt.

Formato de bloco descoberto (big-endian):
  u32 ???  | u32 quantidade N | N x u32 deslocamento (relativo ao inicio do bloco)
Cada mensagem vai do seu deslocamento ate o inicio da proxima (em ordem de
posicao) e termina em 0x0001. O codigo 0x0001 tambem aparece no meio, como
parametro de comandos, entao nao da para usar so ele como fim.

Uso: python -I scripts/extrair_textos.py <pasta_extraida> <pasta_saida>
"""
import os, struct, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabela import TABELA, FIM, QUEBRA

NAO_FIM = {0x0000, 0x0009, 0x000B}   # comandos que levam 0x0001 como parametro

def ler_msg(d, pos, ate=None):
    """Le os codigos de uma mensagem. Se 'ate' for dado, le ate essa posicao;
    senao, para no primeiro 0x0001 que nao seja parametro de comando."""
    codes = []
    while pos + 2 <= len(d):
        if ate is not None and pos >= ate:
            break
        v = struct.unpack_from('>H', d, pos)[0]
        codes.append(v); pos += 2
        if ate is None and v == FIM and (len(codes) <= 2 or codes[-2] not in NAO_FIM):
            break
        if len(codes) > 30000:
            return None
    return codes

def ler_msgs(d, pos, offs):
    """Le todas as mensagens de um bloco usando os limites entre deslocamentos."""
    ordem = sorted(set(offs))
    prox = {a: b for a, b in zip(ordem, ordem[1:])}
    return [ler_msg(d, pos + o, pos + prox[o] if o in prox else None) for o in offs]

def legivel(codes):
    # conta so letras comuns (A-Z, a-z, espaco), para evitar falsos positivos em dados binarios
    letras = sum(1 for c in codes if 0xA7 <= c <= 0xDA or c == 0x80)
    return letras >= max(3, len(codes) * 0.5)

def para_texto(codes):
    out = []
    sem_fim = not codes or codes[-1] != FIM
    if not sem_fim:
        codes = codes[:-1]
    for c in codes:
        if c in TABELA: out.append(TABELA[c])
        elif c == QUEBRA: out.append('{0006}\n')
        else: out.append('{%04X}' % c)
    if sem_fim: out.append('{NOFIM}')   # mensagem sem 0x0001 no final (nao mexer)
    return ''.join(out)

def achar_blocos(d):
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
                if None not in msgs and len(bons) >= max(1, n // 2):
                    blocos.append((pos, offs, msgs))
                    pos = (pos + max(offs) + 2 + 3) // 4 * 4   # continua alinhado em 4
                    continue
        pos += 4
    return blocos

def main(raiz, saida):
    resumo = []
    for dp, _, fs in os.walk(raiz):
        for f in sorted(fs):
            p = os.path.join(dp, f)
            d = open(p, 'rb').read()
            blocos = achar_blocos(d)
            if not blocos: continue
            rel = os.path.relpath(p, raiz)
            dst = os.path.join(saida, rel + '.txt')
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            total = 0
            with open(dst, 'w', encoding='utf-8') as out:
                out.write(f'# Arquivo: {rel}\n')
                for bi, (bpos, offs, msgs) in enumerate(blocos):
                    for mi, m in enumerate(msgs):
                        out.write(f'\n### bloco {bi} (0x{bpos:X}) mensagem {mi}\n')
                        out.write(para_texto(m or []) + '\n')
                        total += 1
            resumo.append((rel, len(blocos), total))
    for r in resumo: print(f'{r[2]:5d} mensagens em {r[1]} bloco(s): {r[0]}')
    print('TOTAL', sum(r[2] for r in resumo), 'mensagens em', len(resumo), 'arquivos')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
