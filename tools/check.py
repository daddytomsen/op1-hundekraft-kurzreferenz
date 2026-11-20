# Aufruf: python3 -I check.py <id> [<id> ...]   prüft de/<id>.html gegen src/<id>.html
import sys,re,os,collections
W=os.path.dirname(os.path.abspath(__file__))
def skel(t):
    tags=[re.sub(r'\salt="[^"]*"','',x) for x in re.findall(r'<[^>]+>',t)]
    ph=collections.Counter(re.findall(r'\[\[[^\]]+\]\]',t))
    return tags,ph
ok=True
for i in sys.argv[1:]:
    a=open(W+'/src/%s.html'%i,encoding='utf-8').read()
    p=W+'/de/%s.html'%i
    if not os.path.exists(p): print(i,'FEHLT'); ok=False; continue
    b=open(p,encoding='utf-8').read()
    ta,pa=skel(a); tb,pb=skel(b)
    if ta!=tb:
        ok=False
        n=next((k for k,(x,y) in enumerate(zip(ta,tb)) if x!=y),min(len(ta),len(tb)))
        print(i,'TAGS weichen ab bei Tag Nr.',n,'| src:',ta[n-1:n+2],'| de:',tb[n-1:n+2],'| Anzahl',len(ta),len(tb))
    elif pa!=pb:
        ok=False; print(i,'PLATZHALTER weichen ab:',dict((pa-pb)+(pb-pa)))
    elif re.search(r'alt="[^"]*"[^>]*"',' '.join(re.findall(r'<img[^>]*>',b))): ok=False; print(i,'Anführungszeichen im alt-Text')
    else:
        ta_=len(re.sub(r'<[^>]+>','',a)); tb_=len(re.sub(r'<[^>]+>','',b))
        print(i,'ok','(Textlänge %d → %d)'%(ta_,tb_), 'WARNUNG: auffällig kurz' if tb_<0.8*ta_ else '')
sys.exit(0 if ok else 1)
