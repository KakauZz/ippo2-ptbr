import json,re,sys,collections,openpyxl,importlib.util,os
sys.path.insert(0,'/home/claude/ippo'); from rewrap import rewrap
sys.path.insert(0,'/home/claude/ippo'); import gvx2
spec=importlib.util.spec_from_file_location('c','/home/claude/ippo/check.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
D='/mnt/user-data/uploads/teste do jogo/data/'
ws=openpyxl.load_workbook('/mnt/user-data/uploads/teste do jogo/traducao/dialogos_para_traduzir.xlsx').active
rows={r[0]:r for r in ws.iter_rows(min_row=2,values_only=True)}
items={i['id']:i for i in json.load(open('items.json'))}
pt={}
for k in range(19):
  pt.update({int(a):b for a,b in json.load(open(f'out/c{k:02d}.json')).items()})
by=collections.defaultdict(list); usados=0; rejeit=0
for i,it in items.items():
  if i not in pt or C.problems(it['jp'],pt[i]): rejeit+= i in pt; continue
  orig=rows[i][4]
  ws_=iter(re.findall(r'_w(?:\[[^\]]*\])?',orig))
  t=rewrap(C.norm(pt[i]))
  t=re.sub(r'_w',lambda m:next(ws_),t)
  t=re.sub(r'\{K(\d+)\}',lambda m:it['keep'][int(m.group(1))],t)
  by[rows[i][1]].append((orig,t.encode('shift_jis'))); usados+=1
os.makedirs('saida/DATA',exist_ok=True)
falhas=[]
for f,pairs in by.items():
  d=open(D+f,'rb').read()
  nb,rep=gvx2.replace_all(d,pairs)
  falhas+=[(f,x) for x in rep.get('falhou',[])+rep['nao_achou']]
  open('saida/DATA/'+f.upper(),'wb').write(nb)
print(falhas);print('aplicados',usados,'de',len(items),'| rejeitados',rejeit,'| arquivos',len(by),'| falhas',len(falhas))
