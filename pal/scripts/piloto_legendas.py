"""Teste de legendas no disco PAL: troca o ESPANHOL por portugues em poucas cenas.

- main.dol, bloco 3 (espanhol): legendas do video de abertura.
- st1/r106 (saguao) e st1/r105 (sala de jantar):
    bloco 7 = legendas em espanhol -> portugues (traducao abaixo)
    bloco 3 = textos normais em espanhol -> traducao ja feita no disco US
      (procura o texto ingles do bloco 0 no dicionario ingles->portugues do US).

Confere que cada legenda nova tem exatamente os mesmos codigos de controle
(pausas, tempos) da original; so o texto e as quebras de linha mudam.

Uso: python -I pal/scripts/piloto_legendas.py
Gera pal/textos/ptbr/disco1 e pal/textos/ptbr/disco1_sys (nao mexe em textos/).
"""
import os, re, sys
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'scripts'))
from inserir_textos import ler_txt

EN_PAL = os.path.join(RAIZ, 'pal', 'textos', 'en_pal')
SAIDA = os.path.join(RAIZ, 'pal', 'textos', 'ptbr')
CAB = re.compile(r'(### bloco (\d+) \(0x([0-9A-F]+)\) mensagem (\d+)\n)')

ABERTURA = {  # main.dol, bloco 3
 152: "{0000}{0002}{0000}Julho de 1998, floresta de{0006}Raccoon ",
 153: "{0000}{0002}{0000}A equipe Alpha está{0006}sobrevoando a floresta {000E}{0007}{0013}{0009}{0002}{FFFF}Û{0008}{000C}{NOFIM}",
 228: "{0008}{003A}{0007}a noroeste de Raccoon City. ",
 154: "{0000}{0002}{0000}Estamos procurando o{0006}helicóptero dos nossos {000E}{0007}{0013}{0009}{0002}{FFFF}à{0008}{000F}{NOFIM}",
 229: "{0008}{004B}{0007}colegas da equipe Bravo,{0006}com quem perdemos {000E}{0007}{0013}{0009}{0002}{FFFF}è{0008}{000F}{NOFIM}",
 230: "{0008}{004B}{0007}contato. ",
 155: "{0000}{0002}{0000}Recentemente houve vários{0006}casos de assassinato em {000E}{0007}{0013}{0009}{0002}{FFFF}ì{0008}{000C}{NOFIM}",
 231: "{0008}{003A}{0007}Raccoon City. ",
 156: "{0000}{0002}{0000}Recebemos relatos estranhos{0006}de famílias {000E}{0007}{0013}{0009}{0002}{FFFF}ò{0008}{000A}{NOFIM}",
 232: "{0008}{0032}{0007}atacadas por grupos de até{0006}10 pessoas. {000E}{0007}{0013}{0009}{0002}{FFFF}ù{0008}{000A}{NOFIM}",
 233: "{0008}{0032}{0007}Pelo visto, as vítimas{0006}tinham marcas {000E}{0007}{0013}{0009}{0002}{FFFF}À{0008}{000A}{NOFIM}",
 234: "{0008}{0032}{0007}de mordidas. ",
 157: "{0000}{0002}{0000}A equipe Bravo foi enviada{0006}para investigar os casos... ",
 158: "{0000}{0002}{0000}mas perdemos o contato. ",
 159: "{0000}{0002}{0000}Olhe, Chris! ",
 160: "{0000}{0002}{0000}O helicóptero da equipe{0006}Bravo estava abandonado. ",
 161: "{0000}{0002}{0000}Não havia ninguém dentro, só{0006}o corpo do Kevin. ",
 162: "{0000}{0002}{0000}Continuamos procurando{0006}os outros membros. ",
 163: "{0000}{0002}{0000}Mas tudo virou um{0006}pesadelo. ",
 164: "{0000}{0002}{0000}Brad! ",
 165: "{0000}{0002}{0000}Aonde diabos ele vai? ",
 166: "{0000}{0002}{0000}Por aqui, Chris! ",
 167: "{0000}{0002}{0000}Droga! ",
 168: "{0000}{0002}{0000}Vamos para aquela mansão! ",
}

SAGUAO = {  # st1/r106, bloco 7 (so o texto; os codigos vem da original)
 0: "Todos estão bem? ", 2: "Barry? Cadê o Barry? ", 3: "Ele está... ", 5: "Não... ",
 6: "O que foi isso? ", 7: "Vou dar uma olhada. ",
 8: "Certo. Eu e a Jill ficamos{0006}aqui cobrindo a área. ",
 9: "Chris... ", 10: "Tome cuidado. ", 11: "Pode deixar. ",
 12: "Aquele tiro... Chris, conto{0006}com você para investigar|isso. ",
 13: "Pode deixar, Wesker. ", 14: "Wesker? Jill? ",
 15: "Para onde foi todo{0006}mundo? ", 16: "Que lugar é este? ",
 17: "Com certeza não é uma casa{0006}qualquer.|Isso é óbvio. ",
 18: "Ei, Wesker, cadê o{0006}Chris? ", 19: "Jill, não! ",
 20: "Você não pode voltar lá fora. ", 21: "Mas temos que encontrar... ",
 22: "O que foi isso? ", 23: "Chris? ", 24: "Não... ", 25: "Jill, vá investigar. ",
 26: "Eu vou com ela. ", 27: "O Chris é um grande amigo meu. ",
 28: "Eu fico vigiando{0006}esta área. ", 29: "Fiquem alertas! ", 31: "Wesker! ",
 32: "Jill, me ajude a procurá-lo. ",
 33: "Mas não vamos nos afastar{0006}muito do saguão. ", 34: "Boa ideia. ",
 35: "Barry. ", 36: "Teve sorte, Jill? ", 37: "Não. ",
 38: "O que está acontecendo aqui? ", 39: "Não entendo nada. ", 40: "Nem eu. ",
 41: "O Chris, e agora o Wesker. ", 42: "Não dá para fazer muita coisa. ",
 43: "É melhor procurarmos{0006}separados. ",
 44: "Vou dar outra olhada na sala{0006}de jantar. ",
 45: "Certo, eu tento a{0006}outra porta. ", 46: "Esta mansão é enorme. ",
 47: "Deve ser fácil se perder aqui.{0006}|Vamos começar pelo térreo. ",
 48: "Ah! Quase me esqueço. ", 49: "Tome, uma gazua. ",
 50: "Com certeza vai ser útil. ",
 52: "Obrigada. Posso precisar{0006}dela. ",
 53: "Ei, se acontecer algo, o saguão{0006}será o ponto de encontro. |9",
 54: "o saguão será o ponto de{0006}encontro. ", 55: "Tudo bem? ", 56: "Claro. ",
 57: "Barry. ", 58: "Alguma boa notícia? ", 59: "Fora eu continuar vivo ",
 60: "Este lugar também não parece{0006}muito seguro. ",
 61: "Temos que pensar em como{0006}sair daqui. ",
 62: "Deve haver uma porta dos{0006}fundos em algum lugar. ",
 63: "Então vamos nos separar de{0006}novo. ",
 64: "Espere um pouco! Olhe o{0006}que eu encontrei. ", 65: "O quê? ",
 66: "Granadas ácidas. ",
 67: "Com certeza essas coisas vão{0006}|sair correndo apavoradas agora. ",
 68: "Para você. ", 69: "Espero que não precise{0006}usar. ", 70: "E você? ",
 71: "Não se preocupe. Até agora{0006}ela nunca me deixou na mão. ",
 72: "Bom, então eu fico com elas. ", 73: "Até mais. ", 74: "Tchau. ",
 75: "Até mais. ", 76: "Tchau. ",
 77: "Só restamos três membros{0006}do S.T.A.R.S. ",
 78: "O capitão Wesker, a Jill e eu. ",
 79: "Não sabemos onde está o{0006}Barry... ",
 80: "Só restamos três membros{0006}do S.T.A.R.S. ",
 81: "O capitão Wesker, o Barry e eu.{0006}",
 82: "Não sabemos onde está o{0006}Chris... ",
 83: "Aquele tiro. Jill, conto com você{0006}para investigar. ",
 84: "Pode deixar, Wesker. ", 85: "Ah, Jill! ", 86: "Entendo... ",
 87: "Certo, vão vocês dois. ", 88: "Claro. ",
 89: "nesta “casa de loucos”? Não. ",
}

JANTAR = {  # st1/r105, bloco 7
 0: "A sala de jantar... ", 1: "Acho que você devia dar uma{0006}olhada nisto. ",
 2: "O que é? ", 3: "Sangue... ", 4: "Jill, ",
 5: "veja se encontra mais alguma{0006}coisa por aí. Eu fico |analisando isto. ",
 6: "Tomara que não seja do{0006}Chris. ", 7: "Barry... ", 8: "Barry! ",
 9: "O que foi? ", 10: "Cuidado! É um monstro. ", 11: "Deixa que eu cuido dele ",
 12: "Que diabos é essa coisa? ",
 13: "Achei o Kenneth... essa coisa{0006}acabou com ele... ",
 14: "Vamos avisar o Wesker. ", 15: "Já está amarelando? ",
 16: "Isso não é do seu feitio. ", 17: "Quem está aí? ", 18: "Você! Pare! ",
 19: "Não chegue perto dele, Jill! Ele{0006}está louco! ",
 20: "Mas que diabos...! ",
 21: "É melhor avisarmos o{0006}Wesker sobre isso. ",
}

CODIGO = re.compile(r'\{[0-9A-F]{4}\}|\{NOFIM\}')

def codigos(t):
    return [c for c in CODIGO.findall(t) if c != '{0006}']

def encaixar(orig, texto):
    """Poe o texto portugues entre os codigos da legenda original.
    Na original, os trechos de texto ficam entre codigos que nao sao {0006};
    em 'texto', os trechos sao separados por '|'."""
    partes = re.split(r'((?:\{(?!0006)[0-9A-F]{4}\}|\{NOFIM\})+)', orig)
    # partes: texto, codigos, texto, codigos, ... (textos nos indices pares)
    idx_txt = [i for i in range(0, len(partes), 2) if partes[i].replace('{0006}', '').strip()]
    novos = texto.split('|')
    if len(novos) != len(idx_txt):
        raise SystemExit(f'ERRO: trechos diferentes: {orig!r} x {texto!r}')
    for i, n in zip(idx_txt, novos):
        partes[i] = n
    return ''.join(partes)

def escrever(rel_en, rel_pt, trocas):
    """trocas: {bloco: {msg: texto_novo}}. Reescreve o .txt mantendo o resto igual."""
    texto = open(os.path.join(EN_PAL, rel_en), encoding='utf-8').read()
    partes = CAB.split(texto)
    out = [partes[0]]
    for k in range(1, len(partes), 5):
        cab, b, _, m, corpo = partes[k:k + 5]
        b, m = int(b), int(m)
        novo = trocas.get(b, {}).get(m)
        if novo is not None:
            orig = corpo.rstrip('\n').replace('\n', '')
            if b != 3 and codigos(orig) != codigos(novo):   # bloco 3 = textos normais (caixas podem mudar)
                raise SystemExit(f'ERRO {rel_en} bloco {b} msg {m}: codigos mudaram\n {orig}\n {novo}')
            corpo = novo.replace('{0006}', '{0006}\n') + '\n' + ('\n' if corpo.endswith('\n\n') else '')
        out += [cab, corpo]
    dst = os.path.join(SAIDA, rel_pt)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write(''.join(out))
    print('gravado:', os.path.relpath(dst, RAIZ))

def dicionario_us():
    """Ingles -> portugues a partir da traducao ja feita do disco 1 US."""
    d = {}
    en_ref = os.path.join(RAIZ, 'textos', 'en', 'disco1'); pt_ref = os.path.join(RAIZ, 'textos', 'ptbr', 'disco1')
    for dp, _, fs in os.walk(en_ref):
        for f in fs:
            if not f.endswith('.txt'): continue
            rel = os.path.relpath(os.path.join(dp, f), en_ref)
            en = ler_txt(os.path.join(dp, f)); pt = ler_txt(os.path.join(pt_ref, rel))
            for k, msgs in en.items():
                for i, t in msgs.items():
                    if pt[k][i] != t: d.setdefault(t, pt[k][i])
    return d

def sala(rel, legendas, dic):
    blocos = ler_txt(os.path.join(EN_PAL, rel))
    chaves = sorted(blocos, key=lambda k: k[1])
    ingles, espanhol, leg_es = blocos[chaves[0]], blocos[chaves[3]], blocos[chaves[7]]
    trocas = {3: {}, 7: {}}
    if len(ingles) == len(espanhol):
        for i, t in ingles.items():
            if t in dic: trocas[3][i] = dic[t]
        print(f'  {rel}: {len(trocas[3])} de {len(ingles)} textos normais vieram da traducao US')
    for i, t in legendas.items():
        trocas[7][i] = '{0000}' + encaixar(leg_es[i][len('{0000}'):], t)
    escrever(rel, rel, trocas)

def main():
    dic = dicionario_us()
    sala(os.path.join('disco1', 'st1', 'r106.dat.txt'), SAGUAO, dic)
    sala(os.path.join('disco1', 'st1', 'r105.dat.txt'), JANTAR, dic)
    escrever(os.path.join('disco1_sys', 'main.dol.txt'), os.path.join('disco1_sys', 'main.dol.txt'), {3: ABERTURA})

if __name__ == '__main__':
    main()
