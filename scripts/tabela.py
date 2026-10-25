"""Tabela de caracteres do RE Remake GC NTSC-U.
Cada caractere ocupa 2 bytes (16 bits, big-endian). O codigo e 0x80 + a posicao
da letra na imagem da fonte (etc/core.dat, textura em 0x24EC60, 32 letras por linha).
Codigos que nao estao aqui sao codigos de controle e aparecem como {XXXX}."""

LINHAS_FONTE = [
    # 0x80-0x9F
    ' ▶▼0123456789:%&+-/=,.•…()!?“”~㎝',
    # 0xA0-0xBF
    '—<>[]①②ABCDEFGHIJKLMNOPQRSTUVWXY',
    # 0xC0-0xDF
    'Zabcdefghijklmnopqrstuvwxyzâêîôû',
    # 0xE0-0xFF
    'ÂÊÎÔÛàèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝäëïöü',
    # 0x100-0x11F
    'ÿÄËÏÖÜŸãõÃÕñÑåÅçÇøØþÞšŠßÐƒµðæœÆŒ',
    # 0x120-0x126
    '°¡¿\'™;#',
]

TABELA = {}
for n, linha in enumerate(LINHAS_FONTE):
    for i, c in enumerate(linha):
        if c != '\0':
            TABELA[0x80 + n * 32 + i] = c

FIM = 0x0001        # fim da mensagem
QUEBRA = 0x0006     # quebra de linha
