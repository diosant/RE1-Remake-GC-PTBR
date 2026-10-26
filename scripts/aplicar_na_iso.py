"""Copia a ISO base e grava por cima os arquivos alterados (mesmo tamanho).

Uso: python -I scripts/aplicar_na_iso.py <iso_base> <pasta_alterados> <iso_saida>
A ISO base nunca e modificada; o resultado vai para <iso_saida>.
"""
import os, shutil, struct, sys

def ler_fst(iso):
    with open(iso, 'rb') as f:
        f.seek(0x424)
        fst_off, fst_size = struct.unpack('>II', f.read(8))
        f.seek(fst_off)
        fst = f.read(fst_size)
    total = struct.unpack_from('>I', fst, 8)[0]
    nomes = fst[total * 12:]
    def nome(i):
        o = struct.unpack_from('>I', fst, i * 12)[0] & 0xFFFFFF
        return nomes[o:nomes.index(b'\0', o)].decode('latin-1')
    arquivos = {}
    entradas = {}
    def andar(ini, fim, prefixo):
        i = ini
        while i < fim:
            tipo = fst[i * 12]
            a, b = struct.unpack_from('>II', fst, i * 12 + 4)
            if tipo == 1:
                andar(i + 1, b, prefixo + nome(i) + '/'); i = b
            else:
                arquivos[(prefixo + nome(i)).lower()] = (a, b)
                entradas[(prefixo + nome(i)).lower()] = fst_off + i * 12
                i += 1
    andar(1, total, '')
    return arquivos, entradas

ALINHA_ISO = 0x8000

def main(base, alterados, saida):
    arquivos, entradas = ler_fst(base)
    livre = max(o + t for o, t in arquivos.values())
    livre = (livre + ALINHA_ISO - 1) // ALINHA_ISO * ALINHA_ISO
    tam_iso = os.path.getsize(base)
    print('copiando a ISO base...')
    shutil.copyfile(base, saida)
    with open(saida, 'r+b') as iso:
        for dp, _, fs in os.walk(alterados):
            for f in fs:
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, alterados).replace(os.sep, '/').lower()
                off, tam = arquivos[rel]
                dados = open(p, 'rb').read()
                if len(dados) > tam:
                    # nao cabe no lugar: vai para o espaco livre no fim do disco
                    off = livre
                    livre = (off + len(dados) + ALINHA_ISO - 1) // ALINHA_ISO * ALINHA_ISO
                    if livre > tam_iso:
                        raise SystemExit('ERRO: acabou o espaco livre na ISO')
                    print(f'  {rel} cresceu ({tam} -> {len(dados)} bytes), movido para 0x{off:X}')
                iso.seek(off); iso.write(dados)
                if len(dados) != tam:
                    iso.seek(entradas[rel] + 4); iso.write(struct.pack('>II', off, len(dados)))
                print('gravado:', rel)
        # main.dol corrigido (quando o texto dos itens cresce)
        dol = os.path.join(os.path.dirname(os.path.abspath(alterados)), os.path.basename(os.path.abspath(alterados)) + '_sys', 'main.dol')
        if os.path.exists(dol):
            dados = open(dol, 'rb').read()
            iso.seek(0x420); dol_off = struct.unpack('>I', iso.read(4))[0]
            iso.seek(dol_off); velho = iso.read(len(dados))
            if len(velho) != len(dados):
                raise SystemExit('ERRO: main.dol com tamanho diferente')
            iso.seek(dol_off); iso.write(dados)
            print('gravado: sys/main.dol')
    print('ISO pronta:', saida)

if __name__ == '__main__':
    main(*sys.argv[1:4])
