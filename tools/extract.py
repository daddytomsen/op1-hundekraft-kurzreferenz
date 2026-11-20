import sys,re,json,os,collections
S=sys.argv[1]; app=open(sys.argv[2],encoding='utf-8').read()
m=open(S+'/manual/manual.html',encoding='utf-8').read()
main=m[m.find('<main'):m.find('</main>')]
ids=re.findall(r'\b(?:S|F|add|[A-Z]{1,2})\(\s*(?:"(?:synth|drum|fx|play|tape|sys)",)?"([a-z0-9_-]+)"',app)[2:]
want=[i for i in ids if i!='open']+['notation']
def balanced(s,start):
    d=0
    for x in re.finditer(r'<(/?)div\b[^>]*>',s[start:]):
        d+= -1 if x.group(1) else 1
        if d==0: return s[start:start+x.end()]
    raise Exception('unbalanced')
frag={}
for x in re.finditer(r'<div class="sub"[^>]*>',main):
    f=balanced(main,x.start()); h=re.search(r'<h3[^>]*id="([^"]+)"',f)
    if h and h.group(1) in want: frag[h.group(1)]=f
assert set(frag)==set(want),set(want)-set(frag)
imgs={}; srcs=set()
def shrink(f):
    def r(mm):
        tag=mm.group(0); src=re.search(r'src="([^"?]+)',tag).group(1); srcs.add(src)
        cls=re.search(r'class="([^"]+)"',tag); cls=cls.group(1) if cls else ''
        name=os.path.basename(src)[:-4]
        if cls=='okey': return '[[%s]]'%name
        if cls=='knobcap': return '[[cap:%s]]'%name
        if cls=='knobmini': return '[[mini:%s]]'%name
        n=len(imgs); imgs[n]=tag
        alt=re.search(r'alt="([^"]*)"',tag)
        return '<img n="%d" alt="%s">'%(n,alt.group(1) if alt else '')
    f=re.sub(r'<img\b[^>]*>',r,f)
    f=f.replace('<span class="okey okey-text" title="Shift">Shift</span>','[[Shift]]')
    return f
out={k:shrink(frag[k]) for k in want}
left=collections.Counter(re.findall(r'<span class="okey okey-text"[^>]*>[^<]*</span>',''.join(out.values())))
print('other text keys',left.most_common(12))
os.makedirs(S+'/work/src',exist_ok=True)
for k,v in out.items(): open(S+'/work/src/%s.html'%k,'w',encoding='utf-8').write(v)
json.dump(imgs,open(S+'/work/imgs.json','w'))
open(S+'/work/srcs.txt','w').write('\n'.join(sorted(srcs)))
sizes=[(k,len(out[k])) for k in want]; print('total',sum(s for _,s in sizes),'orig',sum(len(frag[k]) for k in want),'imgs',len(srcs))
# batches ~55k
b=[];cur=[];n=0
for k,s in sizes:
    if n+s>52000 and cur: b.append(cur);cur=[];n=0
    cur.append(k);n+=s
b.append(cur); json.dump(b,open(S+'/work/batches.json','w'))
for i,x in enumerate(b): print(i,sum(len(out[k]) for k in x),x)
print(out['wavetable'][:1500])
