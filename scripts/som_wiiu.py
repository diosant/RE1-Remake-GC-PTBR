"""Corta um trecho de um WAV (16 bits) para virar o som de abertura do Wii U (bootsound).
O Wii U toca so os primeiros 6 segundos; aplica fade de entrada e de saida para nao "estalar".

Uso: python -I scripts/som_wiiu.py <entrada.wav> <saida.wav> <inicio s> [duracao s] [fade_entrada s] [fade_saida s]
     padrao: duracao 6, fade_entrada 0.3, fade_saida 0.8
"""
import sys, wave, struct

def main(entrada, saida, inicio, duracao=6.0, fade_in=0.3, fade_out=0.8):
    w = wave.open(entrada)
    sr, ch = w.getframerate(), w.getnchannels()
    assert w.getsampwidth() == 2, 'precisa ser WAV de 16 bits'
    w.setpos(int(inicio * sr))
    n = min(int(duracao * sr), w.getnframes() - int(inicio * sr))
    s = list(struct.unpack('<%dh' % (n * ch), w.readframes(n)))
    fi, fo = int(fade_in * sr), int(fade_out * sr)
    for i in range(n):
        g = 1.0
        if i < fi: g = i / fi
        if i >= n - fo: g = min(g, (n - 1 - i) / fo)
        for c in range(ch):
            s[i * ch + c] = int(s[i * ch + c] * g)
    o = wave.open(saida, 'wb')
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr)
    o.writeframes(struct.pack('<%dh' % len(s), *s))
    o.close()
    print(f'{saida}: {n / sr:.2f} s, {sr} Hz, {ch} canais')

if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    main(a[0], a[1], *map(float, a[2:]))
