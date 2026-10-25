"""Busca relativa: acha uma palavra mesmo com codificacao desconhecida,
comparando as diferencas entre as letras (8 e 16 bits)."""
import sys, os, struct

def diffs(word):
    return [ord(b) - ord(a) for a, b in zip(word, word[1:])]

def search(data, word, width, endian):
    d = diffs(word)
    n = len(word)
    fmt = {1: 'B', 2: endian + 'H'}[width]
    hits = []
    for off in range(width):
        cnt = (len(data) - off) // width
        vals = struct.unpack_from(f'{endian}{cnt}{fmt[-1]}', data, off)
        for i in range(cnt - n + 1):
            ok = True
            for j in range(n - 1):
                if vals[i + j + 1] - vals[i + j] != d[j]:
                    ok = False; break
            if ok:
                hits.append((off + i * width, vals[i]))
    return hits

root, words = sys.argv[1], sys.argv[2:]
for dp, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(dp, f)
        if os.path.getsize(p) > 20_000_000: continue
        data = open(p, 'rb').read()
        for w in words:
            for width, en in ((1, '>'), (2, '>'), (2, '<')):
                h = search(data, w, width, en)
                if h:
                    print(f'{p} | {w} | {width*8}bit{en} | {len(h)} hits | primeiro off=0x{h[0][0]:X} valor_1a_letra=0x{h[0][1]:X}')
