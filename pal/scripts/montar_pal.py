"""Monta os textos em portugues do disco PAL, no lugar do ESPANHOL.

Textos normais (salas, itens, documentos, sistema): pega o texto ingles do PAL,
procura no dicionario ingles->portugues da traducao US (textos/en x textos/ptbr)
ou em pal/scripts/traducoes/extras.py, e grava no bloco espanhol.
Legendas das cenas: vem de pal/scripts/traducoes/legendas_discoN.py.

Uso: python -I pal/scripts/montar_pal.py <N>
Le pal/textos/en_pal/discoN(_sys), grava pal/textos/ptbr/discoN(_sys).
Lista no fim o que ficou em espanhol.
"""
import os, re, sys, importlib, difflib
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'scripts')); sys.path.insert(0, AQUI)
from inserir_textos import ler_txt

CAB = re.compile(r'(### bloco (\d+) \(0x([0-9A-F]+)\) mensagem (\d+)\n)')
CODIGO = re.compile(r'\{[0-9A-F]{4}\}|\{NOFIM\}|(?<=\{0008\})[^{](?=\{|$)|(?<=\{FFFF\})[^{](?=\{|$)')

# subscr.dat: itens EN, docs EN, itens DE FR ES IT, docs DE FR ES IT
ESPECIAIS = {'subscr/subscr.dat': ([(0, 4), (1, 8)], None),
             'st1/r119.dat': ([(0, 3)], 7),   # legenda espanhola dividida em 2 pedacos
             'main.dol': ([(0, 3)], None)}    # quantidades diferentes por idioma (legendas dos videos)

def mapear(blocos):
    """Os blocos vem em grupos (mesma quantidade de mensagens) na ordem EN DE FR ES IT.
    Grupo de 5 = textos normais (ou legendas com o ingles vazio); grupo de 4 = legendas DE FR ES IT.
    Devolve ([(bloco_en, bloco_es)], bloco_legenda_es), contando os blocos em ordem no arquivo."""
    ks = sorted(blocos, key=lambda k: k[1])
    grupos = []
    for j, k in enumerate(ks):
        if grupos and len(blocos[ks[grupos[-1][0]]]) == len(blocos[k]) and len(grupos[-1]) < 5:
            grupos[-1].append(j)
        else:
            grupos.append([j])
    normais, leg = [], None
    for g in grupos:
        if len(g) == 5 and not normais:
            normais = [(g[0], g[3])]
        elif len(g) == 5 and leg is None:
            leg = g[3]
        elif len(g) == 4 and leg is None:
            leg = g[2]
        else:
            return None, None
    return normais, leg

def codigos(t):
    return [c for c in CODIGO.findall(t) if c != '{0006}']

def encaixar(orig, texto, onde):
    """Poe o texto novo entre os codigos da legenda original; trechos separados por '|'.
    Os codigos (tempos, pausas) ficam exatamente como na original; {0006} pode mudar."""
    # um caractere logo depois de {0008}/{FFFF} e seguido de codigo e parametro (ex.: {0008}9), nao texto
    partes = re.split(r'((?:\{(?!0006)[0-9A-F]{4}\}|\{NOFIM\}|(?<=\{0008\})[^{](?=\{|$)|(?<=\{FFFF\})[^{](?=\{|$))+)', orig)
    idx = [i for i in range(0, len(partes), 2) if partes[i].replace('{0006}', '').strip()]
    novos = texto.split('|')
    if len(novos) != len(idx):
        raise SystemExit(f'ERRO {onde}: a original tem {len(idx)} trecho(s) de texto, a traducao tem {len(novos)}\n  {orig}\n  {texto}')
    for i, n in zip(idx, novos):
        partes[i] = n
    return ''.join(partes)

def normal(t):
    """So as letras e numeros, para achar textos iguais com quebras/espacos diferentes."""
    return re.sub(r'[^0-9A-Za-z]', '', re.sub(r'\{[0-9A-F]{4}\}|\{NOFIM\}', '', t)).lower()

def dicionario():
    d = {}; iguais = set()
    for n in (1, 2):
        en_ref = os.path.join(RAIZ, 'textos', 'en', f'disco{n}'); pt_ref = os.path.join(RAIZ, 'textos', 'ptbr', f'disco{n}')
        for dp, _, fs in os.walk(en_ref):
            for f in fs:
                if not f.endswith('.txt'): continue
                rel = os.path.relpath(os.path.join(dp, f), en_ref)
                if not os.path.exists(os.path.join(pt_ref, rel)): continue
                en = ler_txt(os.path.join(dp, f)); pt = ler_txt(os.path.join(pt_ref, rel))
                for k, msgs in en.items():
                    for i, t in msgs.items():
                        if k in pt and i in pt[k] and pt[k][i] != t: d.setdefault(t, pt[k][i])
                        elif k in pt and i in pt[k]: iguais.add(t)   # o US manteve igual de proposito
    try:
        d.update(importlib.import_module('traducoes.extras').D)
    except ModuleNotFoundError:
        pass
    for t, p in list(d.items()):
        if len(normal(t)) >= 8: d.setdefault(('~', normal(t)), p)
    for t in iguais:
        d.setdefault(t, t)
    return d

def escrever(src, dst, trocas):
    texto = open(src, encoding='utf-8').read()
    partes = CAB.split(texto)
    out = [partes[0]]
    for k in range(1, len(partes), 5):
        cab, b, _, m, corpo = partes[k:k + 5]
        novo = trocas.get((int(b), int(m)))
        if novo is not None:
            corpo = novo.replace('{0006}', '{0006}\n') + '\n' + ('\n' if corpo.endswith('\n\n') else '')
        out += [cab, corpo]
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(''.join(out))

def us_mesma_posicao(n, rel, nbloco):
    """Blocos do US (ingles, portugues) do mesmo arquivo, em ordem: para textos com pequenas
    diferencas de redacao entre US e PAL (ex.: documentos), usa a mensagem na mesma posicao."""
    en = os.path.join(RAIZ, 'textos', 'en', f'disco{n}', rel + '.txt')
    pt = os.path.join(RAIZ, 'textos', 'ptbr', f'disco{n}', rel + '.txt')
    if not (os.path.exists(en) and os.path.exists(pt)): return None
    e, p = ler_txt(en), ler_txt(pt)
    ks = sorted(e, key=lambda k: k[1])
    if nbloco >= len(ks): return None
    return e[ks[nbloco]], p[ks[nbloco]]

def parecido(a, b):
    return difflib.SequenceMatcher(None, normal(a), normal(b)).ratio()

def legendas_por_texto(n):
    """Legenda espanhola original -> traducao, usando os discos anteriores (o disco 2 repete
    muitas cenas do disco 1)."""
    por_es = {}
    for m in range(1, n):
        try:
            leg = importlib.import_module(f'traducoes.legendas_disco{m}').D
        except ModuleNotFoundError:
            continue
        for chave, t in leg.items():
            sufixo = '_sys' if chave[0] == 'main.dol' else ''
            src = os.path.join(RAIZ, 'pal', 'textos', 'en_pal2', f'disco{m}{sufixo}', chave[0] + '.txt')
            blocos = ler_txt(src); ks = sorted(blocos, key=lambda k: k[1])
            bs = chave[1] if len(chave) == 3 else (ESPECIAIS.get(chave[0]) or mapear(blocos))[1]
            por_es.setdefault(blocos[ks[bs]][chave[-1]], t)
    return por_es

def tem_texto(t):
    return bool(re.sub(r'\{[0-9A-F]{4}\}|\{NOFIM\}', '', t).strip())

def main(n):
    dic = dicionario()
    por_es = legendas_por_texto(n)
    try:
        leg = importlib.import_module(f'traducoes.legendas_disco{n}').D
    except ModuleNotFoundError:
        leg = {}
    faltam = []; usadas = set(); total_norm = 0; total_leg = 0
    for sufixo in ('', '_sys'):
        base = os.path.join(RAIZ, 'pal', 'textos', 'en_pal2', f'disco{n}{sufixo}')
        for dp, _, fs in os.walk(base):
            for f in sorted(fs):
                src = os.path.join(dp, f)
                rel = os.path.relpath(src, base).replace(os.sep, '/')[:-4]
                blocos = ler_txt(src); ks = sorted(blocos, key=lambda k: k[1])
                normais, b_leg = ESPECIAIS.get(rel) or mapear(blocos)
                if normais is None:
                    print(f'AVISO {rel}: {len(ks)} blocos, formato desconhecido, ficou como esta'); continue
                trocas = {}
                mesma = {be: us_mesma_posicao(n, rel, be if rel.startswith('subscr') else 0) for be, _ in normais}
                for be, bs in normais:
                    en, es = blocos[ks[be]], blocos[ks[bs]]
                    for i, t in es.items():
                        e = en.get(i)
                        if e is None or not e.replace('{0000}', '').strip():
                            continue   # sem ingles: e legenda (tratada abaixo) ou vazio
                        if e in dic:
                            trocas[(bs, i)] = dic[e]; total_norm += 1
                        elif ('~', normal(e)) in dic:
                            trocas[(bs, i)] = dic[('~', normal(e))]; total_norm += 1
                        elif mesma[be] and i in mesma[be][0] and parecido(e, mesma[be][0][i]) >= 0.85:
                            trocas[(bs, i)] = mesma[be][1][i]; total_norm += 1
                        elif (rel, bs, i) in leg:
                            pass
                        else:
                            faltam.append((rel, bs, i, e))
                if rel == 'main.dol':
                    from traducoes.extras import MENU_INGLES
                    for i, t in blocos[ks[0]].items():
                        if t == MENU_INGLES[0]: trocas[(0, i)] = MENU_INGLES[1]
                # legendas: chave (rel, bloco, msg) ou (rel, msg) para o bloco de legenda padrao
                for chave, t in leg.items():
                    if chave[0] != rel: continue
                    bs, i = (chave[1], chave[2]) if len(chave) == 3 else (b_leg, chave[1])
                    orig = blocos[ks[bs]][i]
                    trocas[(bs, i)] = encaixar(orig, t, f'{rel} bloco {bs} msg {i}'); total_leg += 1
                    usadas.add(chave)
                # legendas sem traducao propria: reaproveita a de outro disco (mesmo texto espanhol)
                alvos = []
                if b_leg is not None:
                    alvos += [(b_leg, i, t) for i, t in blocos[ks[b_leg]].items()]
                if rel == 'main.dol':
                    alvos += [(3, i, t) for i, t in blocos[ks[3]].items() if not tem_texto(blocos[ks[0]].get(i, ''))]
                for bs, i, t in alvos:
                    if (bs, i) in trocas or not tem_texto(t): continue
                    if t in por_es:
                        trocas[(bs, i)] = encaixar(t, por_es[t], f'{rel} bloco {bs} msg {i}'); total_leg += 1
                    else:
                        faltam.append((rel, bs, i, t))
                dst = os.path.join(RAIZ, 'pal', 'textos', 'ptbr', f'disco{n}{sufixo}', os.path.relpath(src, base))
                escrever(src, dst, trocas)
    sobra = set(leg) - usadas
    if sobra: print('AVISO: legendas sem arquivo:', sorted(sobra)[:5])
    print(f'textos normais traduzidos: {total_norm}; legendas: {total_leg}; sem traducao (ficaram em espanhol): {len(faltam)}')
    with open(os.path.join(RAIZ, 'pal', 'textos', f'faltam_disco{n}.txt'), 'w', encoding='utf-8') as out:
        for rel, bs, i, e in faltam:
            out.write(f'{rel}\t{bs}\t{i}\t{e}\n')

if __name__ == '__main__':
    main(int(sys.argv[1]))
