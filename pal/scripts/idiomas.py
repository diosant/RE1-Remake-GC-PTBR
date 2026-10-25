"""Descobre o idioma e o tipo (texto normal ou legenda) de cada bloco de um .txt do PAL."""
import re
PALAVRAS = {
    'en': {'the', 'is', 'you', 'it', 'a', 'of', 'to', 'and', "it's", 'i', 'there', 'this', 'what'},
    'de': {'der', 'die', 'das', 'ist', 'und', 'ich', 'nicht', 'ein', 'eine', 'sie', 'du', 'es', 'mit'},
    'fr': {'le', 'la', 'les', 'est', 'et', 'je', 'vous', 'un', 'une', 'pas', 'de', 'il', 'ce', 'tu'},
    'es': {'el', 'la', 'es', 'y', 'que', 'un', 'una', 'no', 'de', 'está', 'los', 'hay', 'lo', 'me'},
    'it': {'il', 'è', 'e', 'che', 'un', 'una', 'non', 'di', 'la', 'sono', 'questo', 'hai', 'mi', 'ci'},
}

def idioma(msgs):
    texto = ' '.join(re.sub(r'\{[0-9A-F]{4}\}|\{NOFIM\}', ' ', m) for m in msgs).lower()
    if '¿' in texto or '¡' in texto: return 'es'
    pal = re.findall(r"[a-zà-ÿ']+", texto)
    if not pal: return '--'
    pontos = {l: sum(1 for p in pal if p in ws) for l, ws in PALAVRAS.items()}
    return max(pontos, key=pontos.get) if max(pontos.values()) else '--'

def legenda(msgs):
    com_pausa = sum(1 for m in msgs if '{0008}' in m)
    return com_pausa >= len(msgs) * 0.6

def classificar(blocos):
    """blocos: {(bloco, pos): {msg: texto}} -> lista [(chave, idioma, eh_legenda)] em ordem."""
    ks = sorted(blocos, key=lambda k: k[1])
    return [(k, idioma(list(blocos[k].values())), legenda(list(blocos[k].values()))) for k in ks]
