"""Coloca as legendas em portugues (feitas para o disco PAL) no disco AMERICANO.

Descoberta: o disco US ja tem o sistema de legendas. Cada sala com cena tem uma secao
de legendas (ponteiro 12 do cabecalho da sala) com a mesma quantidade de falas do PAL,
mas todas vazias ({0000}). As legendas dos videos ficam vazias no etc/core.dat
(mensagens 151-180, que no PAL sao as 152-181 do main.dol).
Este script preenche essas falas vazias com as legendas portuguesas (com os codigos
de tempo do PAL) e gera arquivos para gravar por cima da ISO americana traduzida.

Uso: python -I pal/scripts/legendas_us.py <N>
Le: build/alterados_discoN (traducao US) ou extraido/discoN (original), e
    pal/textos/ptbr/discoN(_sys) (legendas em portugues).
Grava: pal/build/us_legendas_discoN/<arquivo>
"""
import os, re, struct, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'scripts')); sys.path.insert(0, AQUI)
from inserir_textos import ler_txt, codificar, montar_bloco, ler_secoes, abrir_espaco
from extrair_textos import ler_msgs, achar_blocos
from montar_pal import mapear, ESPECIAIS

# videos: mensagem do main.dol PAL -> pedacos que continuam a fala (ficam juntos no US)
PEDACOS = {153: [228], 154: [229, 230], 155: [231], 156: [232, 233, 234]}

def vazia(m):
    """Fala sem texto: so codigos (inicio, fim, pausas de tempo {0008}{xxxx})."""
    i = 0
    while i < len(m):
        if m[i] == 0x0008: i += 2; continue      # pausa + duracao
        if m[i] > 0x80: return False             # letra (0x80 = espaco)
        i += 1
    return True

def juntar(textos):
    """Junta pedacos de uma fala: tira o {NOFIM} dos que continuam no proximo."""
    return ''.join(t[:-len('{NOFIM}')] if t.endswith('{NOFIM}') else t for t in textos)

def base_us(n, rel):
    for p in (os.path.join(RAIZ, 'build', f'alterados_disco{n}', rel), os.path.join(RAIZ, 'extraido', f'disco{n}', 'files', rel)):
        if os.path.exists(p): return open(p, 'rb').read(), p
    return None, None

def salas(n, saida):
    feitas = 0
    base_pt = os.path.join(RAIZ, 'pal', 'textos', 'ptbr', f'disco{n}')
    base_en = os.path.join(RAIZ, 'pal', 'textos', 'en_pal2', f'disco{n}')
    for dp, _, fs in os.walk(base_pt):
        for f in sorted(fs):
            rel = os.path.relpath(os.path.join(dp, f), base_pt).replace(os.sep, '/')[:-4]
            if not rel.startswith('st'): continue
            blocos_en = ler_txt(os.path.join(base_en, rel + '.txt'))
            _, b_leg = ESPECIAIS.get(rel) or mapear(blocos_en)
            if b_leg is None: continue
            pt = ler_txt(os.path.join(dp, f)); ks = sorted(pt, key=lambda k: k[1])
            legendas = [pt[ks[b_leg]][i] for i in sorted(pt[ks[b_leg]])]
            dados, origem = base_us(n, rel)
            if dados is None: print(f'AVISO {rel}: nao existe no US'); continue
            cab, lista = ler_secoes(dados, rel)
            sec = cab[12]
            if not sec: print(f'AVISO {rel}: sala US sem secao de legendas'); continue
            cnt = struct.unpack_from('>I', dados, sec + 4)[0]
            offs = struct.unpack_from('>%dI' % cnt, dados, sec + 8)
            msgs = ler_msgs(dados, sec, offs)
            if len(legendas) < cnt:
                print(f'AVISO {rel}: US tem {cnt} falas e o PAL {len(legendas)}'); continue
            novas = [codificar(legendas[i], f'{rel} fala {i}') for i in range(cnt)]
            for i, m in enumerate(msgs):
                # falas com texto no US (perguntas, pensamentos): conferir que e a mesma fala no PAL
                if not vazia(m) and ((0x12 in m) != (0x12 in novas[i])):
                    print(f'AVISO {rel} fala {i}: pergunta sim/nao diferente entre US e PAL; mantive a do US')
                    novas[i] = list(m)
            bloco = montar_bloco(struct.unpack_from('>I', dados, sec)[0], offs, novas)
            fim = max(o + 2 * len(m) for o, m in zip(offs, msgs))
            novo = bytearray(dados)
            if len(bloco) <= fim:
                novo[sec:sec + fim] = bloco + b'\0' * (fim - len(bloco))
            else:
                novo = abrir_espaco(novo, sec, bloco, rel)
            dst = os.path.join(saida, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(novo); feitas += 1
    print(f'salas com legenda: {feitas}')

def videos(n, saida):
    rel = 'etc/core.dat'
    dados, _ = base_us(n, rel)
    pt = ler_txt(os.path.join(RAIZ, 'pal', 'textos', 'ptbr', f'disco{n}_sys', 'main.dol.txt'))
    es = pt[sorted(pt, key=lambda k: k[1])[3]]
    bpos, offs, msgs = achar_blocos(dados)[0]
    novas = list(msgs)
    for i_pal in range(152, 182):
        i_us = i_pal - 1
        if not vazia(msgs[i_us]):
            raise SystemExit(f'ERRO: core.dat mensagem {i_us} nao esta vazia (esperava legenda de video)')
        texto = juntar([es[i_pal]] + [es[j] for j in PEDACOS.get(i_pal, [])])
        novas[i_us] = codificar(texto, f'video {i_pal}')
    bloco = montar_bloco(struct.unpack_from('>I', dados, bpos)[0], offs, novas)
    fim = max(o + 2 * len(m) for o, m in zip(offs, msgs))
    novo = bytearray(dados)
    if len(bloco) <= fim:
        novo[bpos:bpos + fim] = bloco + b'\0' * (fim - len(bloco))
    else:
        novo = abrir_espaco(novo, bpos, bloco, rel)
    dst = os.path.join(saida, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'wb').write(novo); print('legendas dos videos: 30 falas no core.dat')

if __name__ == '__main__':
    n = int(sys.argv[1])
    saida = os.path.join(RAIZ, 'pal', 'build', f'us_legendas_disco{n}')
    if os.path.exists(saida):
        import shutil; shutil.rmtree(saida)
    salas(n, saida)
    videos(n, saida)
