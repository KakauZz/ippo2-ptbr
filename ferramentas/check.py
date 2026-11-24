"""Valida a traducao de um bloco: python3 check.py NN  (ex.: 03)"""
import json, re, sys, unicodedata

MAXLEN = 46

def norm(t):
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return t.replace('…', '...').replace('“', '"').replace('”', '"').replace('’', "'").replace('‘', "'")

def tokens(t):
    return re.findall(r'_tc|_w|_mf\[[^\]]*\]|\{K\d+\}', t)

def problems(jp, pt):
    p = []
    if not pt or not pt.strip():
        return ['vazio']
    if tokens(jp) != tokens(pt):
        p.append('codigos diferentes: jp=%s pt=%s' % (tokens(jp), tokens(pt)))
    n = norm(pt)
    if re.search(r'[぀-ヿ一-鿿！-～]', n):
        p.append('sobrou japones/full-width')
    try:
        n.encode('shift_jis')
    except UnicodeEncodeError as e:
        p.append('caractere invalido: %r' % n[e.start:e.end])
    for page in n.split('_tc'):
        lines = [l for l in page.strip('\n').split('\n')]
        if len(lines) > 4 and len(lines) > len(jp.split('\n')):
            p.append('pagina com %d linhas' % len(lines))
        for l in lines:
            vis = re.sub(r'_w|_mf\[[^\]]*\]|\{K\d+\}', '', l)
            if len(vis) > MAXLEN:
                p.append('linha com %d caracteres: %r' % (len(vis), vis))
    return p

if __name__ == '__main__':
    k = sys.argv[1]
    src = {e['id']: e['jp'] for e in json.load(open('/home/claude/ippo/chunks/c%s.json' % k, encoding='utf-8'))}
    try:
        out = json.load(open('/home/claude/ippo/out/c%s.json' % k, encoding='utf-8'))
    except FileNotFoundError:
        out = {}
    out = {int(a): b for a, b in out.items()}
    bad = 0
    for i, jp in src.items():
        if i not in out:
            print('FALTA', i); bad += 1; continue
        pr = problems(jp, out[i])
        if pr:
            bad += 1
            print(i, '; '.join(pr))
    print('total', len(src), 'feitos', len(out), 'com problema', bad)
