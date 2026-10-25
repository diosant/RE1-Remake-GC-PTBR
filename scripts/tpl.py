"""Le texturas TPL (formato de imagem do GameCube) e salva como PNG, sem bibliotecas externas."""
import struct, zlib

FORMATOS = {0: 'I4', 1: 'I8', 2: 'IA4', 3: 'IA8', 4: 'RGB565', 5: 'RGB5A3', 6: 'RGBA8', 8: 'C4', 9: 'C8', 14: 'CMPR'}
BLOCO = {0: (8, 8), 1: (8, 4), 2: (8, 4), 3: (4, 4), 4: (4, 4), 5: (4, 4), 6: (4, 4), 8: (8, 8), 9: (8, 4), 14: (8, 8)}
BPP = {0: 4, 1: 8, 2: 8, 3: 16, 4: 16, 5: 16, 6: 32, 8: 4, 9: 8, 14: 4}

def listar(d, base):
    """Lista as imagens de um TPL que comeca em 'base'."""
    n, tab = struct.unpack_from('>II', d, base + 4)
    imgs = []
    for i in range(n):
        ih, ph = struct.unpack_from('>II', d, base + tab + i * 8)
        h, w, fmt, off = struct.unpack_from('>HHII', d, base + ih)
        imgs.append((w, h, fmt, base + off))
    return imgs

def decodificar(d, w, h, fmt, off):
    """Devolve lista de pixels RGBA (so formatos de fonte/simples)."""
    bw, bh = BLOCO[fmt]
    px = [(0, 0, 0, 0)] * (w * h)
    pos = off
    for by in range(0, h, bh):
        for bx in range(0, w, bw):
            if fmt == 6:
                ar = d[pos:pos + 32]; gb = d[pos + 32:pos + 64]; pos += 64
                for i in range(16):
                    x, y = bx + i % 4, by + i // 4
                    if x < w and y < h:
                        px[y * w + x] = (ar[i*2+1], gb[i*2], gb[i*2+1], ar[i*2])
                continue
            for j in range(bh * bw):
                x, y = bx + j % bw, by + j // bw
                if fmt in (0, 8):   # I4 / C4 (C4 mostrado como tons de cinza do indice)
                    b = d[pos + j // 2]; v = (b >> 4) if j % 2 == 0 else (b & 15); v *= 17; c = (v, v, v, 255)
                elif fmt == 1:
                    v = d[pos + j]; c = (v, v, v, 255)
                elif fmt == 2:
                    b = d[pos + j]; a = (b >> 4) * 17; v = (b & 15) * 17; c = (v, v, v, a)
                elif fmt == 3:
                    a, v = d[pos + j*2], d[pos + j*2 + 1]; c = (v, v, v, a)
                elif fmt == 5:
                    v = struct.unpack_from('>H', d, pos + j*2)[0]
                    if v & 0x8000:
                        c = (((v >> 10) & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, (v & 31) * 255 // 31, 255)
                    else:
                        c = (((v >> 8) & 15) * 17, ((v >> 4) & 15) * 17, (v & 15) * 17, ((v >> 12) & 7) * 255 // 7)
                elif fmt == 4:
                    v = struct.unpack_from('>H', d, pos + j*2)[0]
                    c = ((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31, 255)
                else:
                    raise ValueError('formato nao suportado: %d' % fmt)
                if x < w and y < h:
                    px[y * w + x] = c
            pos += bw * bh * BPP[fmt] // 8
    return px

def salvar_png(caminho, w, h, px, fundo=(40, 40, 40)):
    linhas = b''
    for y in range(h):
        linhas += b'\0'
        for (r, g, b, a) in px[y*w:(y+1)*w]:
            linhas += bytes((r*a//255 + fundo[0]*(255-a)//255, g*a//255 + fundo[1]*(255-a)//255, b*a//255 + fundo[2]*(255-a)//255))
    def chunk(t, c): return struct.pack('>I', len(c)) + t + c + struct.pack('>I', zlib.crc32(t + c) & 0xffffffff)
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(linhas)) + chunk(b'IEND', b'')
    open(caminho, 'wb').write(png)

def _rgb565(v):
    return ((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31)

def decodificar_cmpr(d, w, h, off):
    """Formato CMPR (parecido com DXT1): blocos de 8x8 feitos de 4 sub-blocos 4x4."""
    px = [(0, 0, 0, 0)] * (w * h)
    pos = off
    for by in range(0, h, 8):
        for bx in range(0, w, 8):
            for sb in range(4):
                sx, sy = bx + (sb % 2) * 4, by + (sb // 2) * 4
                c0, c1 = struct.unpack_from('>HH', d, pos)
                bits = struct.unpack_from('>I', d, pos + 4)[0]
                pos += 8
                a, b = _rgb565(c0), _rgb565(c1)
                if c0 > c1:
                    cores = [a + (255,), b + (255,),
                             tuple((2 * x + y) // 3 for x, y in zip(a, b)) + (255,),
                             tuple((x + 2 * y) // 3 for x, y in zip(a, b)) + (255,)]
                else:
                    cores = [a + (255,), b + (255,),
                             tuple((x + y) // 2 for x, y in zip(a, b)) + (255,), (0, 0, 0, 0)]
                for j in range(16):
                    x, y = sx + j % 4, sy + j // 4
                    if x < w and y < h:
                        px[y * w + x] = cores[(bits >> (30 - 2 * j)) & 3]
    return px


def listar_com_paleta(d, base):
    """Como listar(), mas devolve tambem (formato, quantidade, posicao) da paleta."""
    n, tab = struct.unpack_from('>II', d, base + 4)
    imgs = []
    for i in range(n):
        ih, ph = struct.unpack_from('>II', d, base + tab + i * 8)
        h, w, fmt, off = struct.unpack_from('>HHII', d, base + ih)
        pal = None
        if ph:
            cnt, _, _, pfmt, poff = struct.unpack_from('>HBBII', d, base + ph)
            pal = (pfmt, cnt, base + poff)
        imgs.append((w, h, fmt, base + off, pal))
    return imgs

def cor_paleta(v, pfmt):
    if pfmt == 0:   # IA8
        a, i = v >> 8, v & 255; return (i, i, i, a)
    if pfmt == 1:   # RGB565
        return ((v >> 11) * 255 // 31, ((v >> 5) & 63) * 255 // 63, (v & 31) * 255 // 31, 255)
    if v & 0x8000:  # RGB5A3
        return (((v >> 10) & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, (v & 31) * 255 // 31, 255)
    return (((v >> 8) & 15) * 17, ((v >> 4) & 15) * 17, (v & 15) * 17, ((v >> 12) & 7) * 255 // 7)

def decodificar_indexada(d, w, h, fmt, off, pal):
    """C4 (fmt 8) ou C8 (fmt 9) usando a paleta."""
    pfmt, cnt, poff = pal
    cores = [cor_paleta(struct.unpack_from('>H', d, poff + 2 * i)[0], pfmt) for i in range(cnt)]
    bw, bh = (8, 8) if fmt == 8 else (8, 4)
    px = [(0, 0, 0, 0)] * (w * h); pos = off
    for by in range(0, h, bh):
        for bx in range(0, w, bw):
            for j in range(bw * bh):
                x, y = bx + j % bw, by + j // bw
                if fmt == 8:
                    b = d[pos + j // 2]; v = (b >> 4) if j % 2 == 0 else (b & 15)
                else:
                    v = d[pos + j]
                if x < w and y < h and v < len(cores): px[y * w + x] = cores[v]
            pos += bw * bh * (4 if fmt == 8 else 8) // 8
    return px
