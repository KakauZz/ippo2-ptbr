import re
W=37; MAXL=4
TOK=re.compile(r'(_w(?:\[[^\]]*\])?|_mf\[[^\]]*\])')
def vis(s): return len(TOK.sub('',s))
def wrap_page(p):
    lead=''
    m=re.match(r'^(\s*_mf\[[^\]]*\])',p)
    lines=[]
    for ln in p.strip('\n').split('\n'):
        if vis(ln)<=W: lines.append(ln); continue
        cur=''
        for w in ln.split(' '):
            cand=(cur+' '+w) if cur else w
            if cur and vis(cand)>W:
                lines.append(cur);cur=w
            else: cur=cand
        if cur: lines.append(cur)
    return [l for l in lines if l!='' ] or ([''] if p.strip('\n')=='' else [])
def rewrap(t):
    if '{K' in t or '<' in t or '//' in t: return t
    pages=re.split(r'\n?_tc\n?',t)
    out=[]
    for p in pages:
        L=wrap_page(p)
        if not L: out.append(p.strip('\n')); continue
        for i in range(0,len(L),MAXL): out.append('\n'.join(L[i:i+MAXL]))
    return '\n_tc\n'.join(out)
