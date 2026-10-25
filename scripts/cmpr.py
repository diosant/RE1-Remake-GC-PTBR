"""Codificador CMPR (formato de textura do GameCube, parecido com DXT1).

So recodifica os sub-blocos 4x4 que mudaram; o resto da imagem fica
byte a byte igual ao original (sem perda de qualidade).
"""
import struct

def _565(c):
    r, g, b = c[:3]
    return ((r * 31 + 127) // 255) << 11 | ((g * 63 + 127) // 255) << 5 | ((b * 31 + 127) // 255)

def _de565(v):
    return ((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31)

def _codificar_sub(pixels):
    """pixels: 16 tuplas RGBA. Devolve 8 bytes. Com pixels transparentes usa o modo
    de 3 cores + transparente (cor 0 <= cor 1)."""
    transp = [len(p) > 3 and p[3] < 128 for p in pixels]
    opacos = [p[:3] for p, t in zip(pixels, transp) if not t]
    if not opacos:
        return struct.pack('>HHI', 0, 0xFFFF, 0xFFFFFFFF)   # tudo transparente
    lum = [p[0] * 3 + p[1] * 6 + p[2] for p in opacos]
    a = opacos[lum.index(max(lum))]; b = opacos[lum.index(min(lum))]
    c0, c1 = _565(a), _565(b)
    if any(transp):
        if c0 > c1:
            c0, c1 = c1, c0
        p0, p1 = _de565(c0), _de565(c1)
        pal = [p0, p1, tuple((x + y) // 2 for x, y in zip(p0, p1))]
    else:
        if c0 == c1:
            return struct.pack('>HHI', c0, c1, 0)
        if c0 < c1:
            c0, c1 = c1, c0
        p0, p1 = _de565(c0), _de565(c1)
        pal = [p0, p1, tuple((2 * x + y) // 3 for x, y in zip(p0, p1)), tuple((x + 2 * y) // 3 for x, y in zip(p0, p1))]
    bits = 0
    for j, p in enumerate(pixels):
        if transp[j]:
            k = 3
        else:
            k = min(range(len(pal)), key=lambda i: sum((p[t] - pal[i][t]) ** 2 for t in range(3)))
        bits |= k << (30 - 2 * j)
    return struct.pack('>HHI', c0, c1, bits)

def regravar(dados, off, w, h, antes, depois):
    """Grava em 'dados' (bytearray) os sub-blocos onde 'depois' difere de 'antes'.
    antes/depois: listas de tuplas (r,g,b[,a]) com w*h pixels."""
    pos = off; mudou = 0
    for by in range(0, h, 8):
        for bx in range(0, w, 8):
            for sb in range(4):
                sx, sy = bx + (sb % 2) * 4, by + (sb // 2) * 4
                idx = [(sy + j // 4) * w + sx + j % 4 for j in range(16)]
                if any(tuple(antes[i]) != tuple(depois[i]) for i in idx):
                    dados[pos:pos + 8] = _codificar_sub([depois[i] for i in idx]); mudou += 1
                pos += 8
    return mudou
