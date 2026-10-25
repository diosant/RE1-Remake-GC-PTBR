"""Abre espaco para os textos do subscr/subscr.dat (itens e documentos).

O subscr.dat nao tem cabecalho proprio: o main.dol guarda uma tabela com
(posicao, tamanho) de cada parte do arquivo, em 0x178AC0 (posicao no main.dol).
  - textos dos itens: fim da parte que comeca em 0x806A0 (termina em 0x10C620);
  - textos dos documentos: parte que comeca em 0x1CCD00 (termina em 0x1DA540).
Para aumentar um texto, aumentamos a parte dele, empurramos as partes seguintes e
corrigimos a tabela no main.dol. A parte dos itens tambem aparece numa constante
do codigo (lis/addi em 0x700A0 do main.dol = 0x10C620).
"""
import struct

TABELA_INI, TABELA_FIM = 0x178AC0, 0x178C38
CODIGO_LIS = 0x700A0   # lis r3,0x11 / addi r30,r3,-0x39E0  (= 0x10C620)
FIM_PARTE_ITENS = 0x10C620
ALINHAMENTO = 0x20

def ler_tabela(dol):
    return [struct.unpack_from('>II', dol, p) for p in range(TABELA_INI, TABELA_FIM, 8)]

def abrir_espaco_subscr(dados, bpos, bloco, dol):
    """Devolve (novo_subscr, novo_dol, delta). Use em ordem decrescente de bpos."""
    tabela = ler_tabela(dol)
    partes = [(o, t) for o, t in tabela if o <= bpos < o + t]
    if not partes:
        raise SystemExit(f'ERRO: subscr.dat: texto em 0x{bpos:X} fora das partes conhecidas')
    ini, tam = min(partes, key=lambda p: p[1])
    fim_parte = ini + tam
    novo_tam = (len(bloco) + ALINHAMENTO - 1) // ALINHAMENTO * ALINHAMENTO
    delta = max(0, novo_tam - (fim_parte - bpos))
    sub = bytearray(dados[:bpos]) + bloco + b'\x00' * (fim_parte - bpos + delta - len(bloco)) + dados[fim_parte:]
    dol = bytearray(dol)
    for p in range(TABELA_INI, TABELA_FIM, 8):
        off, t = struct.unpack_from('>II', dol, p)
        if off >= fim_parte:
            off += delta
        elif off <= bpos and off + t == fim_parte:   # a parte do texto (e blocos que a incluem)
            t += delta
        struct.pack_into('>II', dol, p, off, t)
    # constante no codigo que guarda o fim da parte dos itens
    alto, baixo = struct.unpack_from('>II', dol, CODIGO_LIS)
    assert alto >> 16 == 0x3C60 and baixo >> 16 == 0x3BC3, 'codigo do main.dol diferente do esperado'
    atual = ((alto & 0xFFFF) << 16) + ((baixo & 0xFFFF) - 0x10000 if baixo & 0x8000 else baixo & 0xFFFF)
    if fim_parte <= atual:
        v = atual + delta
        struct.pack_into('>II', dol, CODIGO_LIS, 0x3C600000 | ((v + 0x8000) >> 16), 0x3BC30000 | (v & 0xFFFF))
    return sub, bytes(dol), delta
