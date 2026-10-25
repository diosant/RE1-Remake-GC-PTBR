"""Reaproveita traducoes ja feitas: monta a pasta ptbr de outro disco trocando cada
mensagem em ingles que tenha traducao identica em uma pasta ja traduzida.

Uso: python -I scripts/reaproveitar_traducao.py <en_ref> <ptbr_ref> <en_novo> <ptbr_novo>
Ex.: textos/en/disco1 textos/ptbr/disco1 textos/en/disco2 textos/ptbr/disco2
Mensagens sem traducao conhecida ficam em ingles e sao listadas no final.
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inserir_textos import ler_txt

CAB = re.compile(r'(### bloco (\d+) \(0x([0-9A-F]+)\) mensagem (\d+)\n)')

def main(en_ref, pt_ref, en_novo, pt_novo):
    # dicionario ingles -> portugues, por arquivo e global
    glob = {}
    por_arq = {}
    for dp, _, fs in os.walk(en_ref):
        for f in fs:
            if not f.endswith('.txt'): continue
            rel = os.path.relpath(os.path.join(dp, f), en_ref)
            en = ler_txt(os.path.join(dp, f)); pt = ler_txt(os.path.join(pt_ref, rel))
            d = {}
            for k, msgs in en.items():
                for i, t in msgs.items():
                    tp = pt[k][i]
                    if tp != t:
                        d.setdefault(t, tp); glob.setdefault(t, tp)
            por_arq[rel] = d
    faltam = 0; total = 0
    for dp, _, fs in os.walk(en_novo):
        for f in fs:
            if not f.endswith('.txt'): continue
            rel = os.path.relpath(os.path.join(dp, f), en_novo)
            texto = open(os.path.join(dp, f), encoding='utf-8').read()
            partes = CAB.split(texto)
            # partes: [inicio, cab, bloco, pos, msg, corpo, cab, ...]
            out = [partes[0]]
            msgs = ler_txt(os.path.join(dp, f))
            for k in range(1, len(partes), 5):
                cab, b, p, i, corpo = partes[k:k + 5]
                t = msgs[(int(b), int(p, 16))][int(i)]
                tr = por_arq.get(rel, {}).get(t) or glob.get(t)
                out.append(cab)
                total += 1
                if tr is not None:
                    out.append(tr.replace('{0006}', '{0006}\n') + '\n\n')
                else:
                    out.append(corpo)
                    if re.sub(r'\{[^}]*\}', '', t).strip():
                        faltam += 1
                        print(f'SEM TRADUCAO: {rel} msg {i}: {t[:70]}')
            dst = os.path.join(pt_novo, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'w', encoding='utf-8').write(''.join(out).rstrip('\n') + '\n')
    print(f'{total} mensagens; {faltam} com texto ainda sem traducao')

if __name__ == '__main__':
    main(*sys.argv[1:5])
