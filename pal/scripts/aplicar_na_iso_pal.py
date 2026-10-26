"""Como scripts/aplicar_na_iso.py, mas para o PAL (disco quase cheio):
um arquivo que cresceu fica no mesmo lugar se couber na sobra antes do proximo
arquivo do disco; so vai para o fim da ISO se nao couber.

Uso: python -I pal/scripts/aplicar_na_iso_pal.py <iso_base> <pasta_alterados> <iso_saida>
A ISO base nunca e modificada.
"""
import os, shutil, struct, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from aplicar_na_iso import ler_fst, ALINHA_ISO

def main(base, alterados, saida):
    arquivos, entradas = ler_fst(base)
    inicios = sorted(o for o, _ in arquivos.values())
    tam_iso = os.path.getsize(base)
    livre = max(o + t for o, t in arquivos.values())
    livre = (livre + ALINHA_ISO - 1) // ALINHA_ISO * ALINHA_ISO
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
                    prox = min([i for i in inicios if i > off] + [tam_iso])
                    if off + len(dados) <= prox:
                        print(f'  {rel} cresceu ({tam} -> {len(dados)} bytes), coube no mesmo lugar')
                    else:
                        off = livre
                        livre = (off + len(dados) + ALINHA_ISO - 1) // ALINHA_ISO * ALINHA_ISO
                        if livre > tam_iso:
                            raise SystemExit('ERRO: acabou o espaco livre na ISO')
                        print(f'  {rel} cresceu ({tam} -> {len(dados)} bytes), movido para 0x{off:X}')
                iso.seek(off); iso.write(dados)
                if len(dados) != tam:
                    iso.seek(entradas[rel] + 4); iso.write(struct.pack('>II', off, len(dados)))
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
