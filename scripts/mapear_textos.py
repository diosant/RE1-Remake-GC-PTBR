"""Procura em todos os arquivos trechos que parecem texto na tabela do jogo."""
import sys, os, struct
sys.path.insert(0, os.path.dirname(__file__))
from tabela import TABELA
root = sys.argv[1]
for dp, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(dp, f)
        d = open(p, 'rb').read()
        total = 0; amostra = None
        for off in (0, 1):
            n = (len(d) - off) // 2
            vals = struct.unpack_from(f'>{n}H', d, off)
            run = 0; start = 0
            for i, v in enumerate(vals):
                if v in TABELA:
                    if run == 0: start = i
                    run += 1
                else:
                    if run >= 12:
                        total += 1
                        if amostra is None:
                            amostra = (off + start*2, ''.join(TABELA[x] for x in vals[start:start+run])[:60])
                    run = 0
        if total:
            print(f'{total:6d}  {p}  0x{amostra[0]:X}: {amostra[1]}')
