"""Reinsere os textos (.txt) nos arquivos do jogo.

Le cada .txt da pasta de textos, codifica de volta para os codigos do jogo
e reconstroi o bloco de mensagens no mesmo lugar do arquivo original.
O bloco novo precisa caber no espaco do bloco original.

Uso: python -I scripts/inserir_textos.py <pasta_extraida> <pasta_textos> <pasta_saida> [pasta_imagens]
pasta_imagens (opcional): arquivos do jogo com imagens ja traduzidas; quando existe
um arquivo la, ele e usado no lugar do original.
Grava apenas os arquivos que mudaram em <pasta_saida> (mesma estrutura de pastas).
"""
import os, re, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tabela import TABELA, FIM
from extrair_textos import achar_blocos
from espaco_subscr import abrir_espaco_subscr

INVERSA = {v: k for k, v in TABELA.items()}
CAB = re.compile(r'^### bloco (\d+) \(0x([0-9A-F]+)\) mensagem (\d+)$')

def ler_txt(caminho):
    """Devolve {(bloco, pos): {msg: texto}}."""
    blocos = {}
    atual = None; linhas = []
    def fecha():
        if atual is not None:
            texto = '\n'.join(linhas)
            if texto.endswith('\n'): texto = texto[:-1]
            blocos.setdefault(atual[:2], {})[atual[2]] = texto.replace('\n', '')
    for linha in open(caminho, encoding='utf-8').read().split('\n'):
        m = CAB.match(linha)
        if m:
            fecha()
            atual = (int(m.group(1)), int(m.group(2), 16), int(m.group(3))); linhas = []
        elif atual is not None:
            linhas.append(linha)
    fecha()
    return blocos

def codificar(texto, onde):
    sem_fim = texto.endswith('{NOFIM}')
    if sem_fim:
        texto = texto[:-len('{NOFIM}')]
    codes = []
    i = 0
    while i < len(texto):
        if texto[i] == '{':
            j = texto.index('}', i)
            codes.append(int(texto[i+1:j], 16)); i = j + 1
        else:
            c = texto[i]
            if c not in INVERSA:
                raise SystemExit(f'ERRO: caractere {c!r} nao existe na tabela ({onde})')
            codes.append(INVERSA[c]); i += 1
    if not sem_fim:
        codes.append(FIM)
    return codes

def montar_bloco(cab_u32, offs_orig, msgs):
    """Monta o bloco mantendo a mesma ordem das mensagens na memoria.
    Mensagens que apontavam para o mesmo lugar continuam compartilhadas
    (vale o texto da primeira)."""
    n = len(msgs)
    base = 8 + 4 * n
    ordem = sorted(range(n), key=lambda i: offs_orig[i])
    corpo = b''
    offs = [0] * n
    novo_de = {}
    for i in ordem:
        if offs_orig[i] in novo_de:
            offs[i] = novo_de[offs_orig[i]]; continue
        offs[i] = novo_de[offs_orig[i]] = base + len(corpo)
        corpo += struct.pack('>%dH' % len(msgs[i]), *msgs[i])
    return struct.pack('>II', cab_u32, n) + struct.pack('>%dI' % n, *offs) + corpo

ALINHAMENTO = 0x20

def ler_secoes(dados, rel):
    """Cabecalho dos .dat de sala/core: 16 ponteiros em 0x00 e lista ordenada
    de inicios de secao em 0x40 (terminada em 0)."""
    cab = list(struct.unpack_from('>16I', dados, 0))
    lista = []
    p = 0x40
    while True:
        v = struct.unpack_from('>I', dados, p)[0]
        # a lista acaba no 0, ou quando aparece um valor fora de ordem/fora do arquivo
        if v == 0 or v >= len(dados) or (lista and v <= lista[-1]): break
        lista.append(v); p += 4
    return cab, lista

def abrir_espaco(dados, bpos, bloco, rel):
    """O texto nao cabe: aumenta a secao de texto no proprio lugar e empurra
    todas as secoes seguintes para frente, corrigindo cabecalho e lista.
    (Mover o texto para o fim do arquivo fez o jogo travar.)"""
    cab, lista = ler_secoes(dados, rel)
    if bpos not in cab or bpos not in lista or lista != sorted(lista):
        raise SystemExit(f'ERRO: {rel}: texto grande demais e nao sei abrir espaco neste tipo de arquivo ainda.')
    depois = [v for v in lista if v > bpos]
    prox = depois[0] if depois else len(dados)
    novo_tam = (len(bloco) + ALINHAMENTO - 1) // ALINHAMENTO * ALINHAMENTO
    delta = max(0, novo_tam - (prox - bpos))
    resultado = bytearray(dados[:bpos]) + bloco + b'\0' * (prox - bpos + delta - len(bloco)) + dados[prox:]
    cab = [v + delta if v > bpos else v for v in cab]
    lista = [v + delta if v > bpos else v for v in lista]
    struct.pack_into('>16I', resultado, 0, *cab)
    struct.pack_into('>%dI' % len(lista), resultado, 0x40, *lista)
    print(f'  {rel}: secao de texto aumentada em {delta} bytes')
    return resultado

def main(raiz, pasta_txt, saida, pasta_img=None):
    mudados = 0
    def original(rel):
        if pasta_img and os.path.exists(os.path.join(pasta_img, rel)):
            return open(os.path.join(pasta_img, rel), 'rb').read()
        return open(os.path.join(raiz, rel), 'rb').read()
    feitos = set()
    dol_antigo = os.path.join(os.path.dirname(os.path.abspath(saida)), os.path.basename(os.path.abspath(saida)) + '_sys', 'main.dol')
    if os.path.exists(dol_antigo):
        os.remove(dol_antigo)
    for dp, _, fs in os.walk(pasta_txt):
        for f in fs:
            if not f.endswith('.txt'): continue
            rel = os.path.relpath(os.path.join(dp, f), pasta_txt)[:-4]
            orig = original(rel); feitos.add(rel)
            # compara com o original de verdade, para gravar tambem mudancas so de imagem
            verdadeiro = open(os.path.join(raiz, rel), 'rb').read()
            novo = bytearray(orig)
            textos = ler_txt(os.path.join(dp, f))
            # de tras para frente: aumentar um bloco nao muda a posicao dos anteriores
            for bi, (bpos, offs, msgs) in reversed(list(enumerate(achar_blocos(orig)))):
                t = textos[(bi, bpos)]
                novas = [codificar(t[i], f'{rel} bloco {bi} msg {i}') for i in range(len(offs))]
                fim_orig = max(o + 2 * len(m) for o, m in zip(offs, msgs))
                cab = struct.unpack_from('>I', orig, bpos)[0]
                bloco = montar_bloco(cab, offs, novas)
                if len(bloco) <= fim_orig:
                    novo[bpos:bpos + fim_orig] = bloco + b'\0' * (fim_orig - len(bloco))
                elif rel.replace(os.sep, '/') == 'subscr/subscr.dat':
                    # usa o main.dol ja corrigido por outro bloco, se houver
                    fonte = dol_antigo if os.path.exists(dol_antigo) else os.path.join(raiz, '..', 'sys', 'main.dol')
                    novo, dol_novo, delta = abrir_espaco_subscr(novo, bpos, bloco, open(fonte, 'rb').read())
                    os.makedirs(os.path.dirname(dol_antigo), exist_ok=True)
                    open(dol_antigo, 'wb').write(dol_novo)
                    print(f'  {rel}: bloco {bi} aumentado em {delta} bytes (main.dol corrigido em {dol_antigo})')
                else:
                    novo = abrir_espaco(novo, bpos, bloco, rel)
            if bytes(novo) != verdadeiro:
                dst = os.path.join(saida, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                open(dst, 'wb').write(novo)
                print('alterado:', rel); mudados += 1
    if pasta_img:   # arquivos que so tem imagem traduzida
        for dp, _, fs in os.walk(pasta_img):
            for f in fs:
                rel = os.path.relpath(os.path.join(dp, f), pasta_img)
                if rel not in feitos:
                    dst = os.path.join(saida, rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    open(dst, 'wb').write(open(os.path.join(dp, f), 'rb').read())
                    print('alterado (imagem):', rel); mudados += 1
    print('arquivos alterados:', mudados)

if __name__ == '__main__':
    main(*sys.argv[1:5])
