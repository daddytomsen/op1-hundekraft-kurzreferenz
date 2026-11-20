# Setzt die übersetzten Fragmente zu anleitung.js zusammen und kopiert die Bilder.
# Aufruf im Projektordner: python3 tools/build.py .
# Quelle je Abschnitt: tools/de/<id>.html (deutsch), tools/src/<id>.html (englisches Original, gekürzte Platzhalter-Form).
# Neue Bilder werden aus ../manual/ neben dem tools-Ordner erwartet; vorhandene bleiben unangetastet.
import sys,re,json,os,shutil,html
W=os.path.dirname(os.path.abspath(__file__)); S=os.path.dirname(W); OUT=sys.argv[1]
imgs=json.load(open(W+'/imgs.json'))
ids=[f[:-5] for f in sorted(os.listdir(W+'/src')) if f.endswith('.html')]
used=set(); HB={}; missing=[]
def key(name):
    used.add('manual/keys/%s.png'%name)
    return '<img class="okey" src="manual/keys/%s.png" alt="%s" title="%s">'%(name,name,name)
def restore(t):
    def ph(m):
        x=m.group(1)
        if x=='Shift': return '<span class="okey okey-text" title="Shift">Shift</span>'
        if x.startswith('cap:') or x.startswith('mini:'):
            kind,name=x.split(':'); used.add('manual/keys/%s.png'%name)
            return '<img class="knob%s" src="manual/keys/%s.png" alt="">'%('cap' if kind=='cap' else 'mini',name)
        return key(x)
    t=re.sub(r'\[\[([^\]]+)\]\]',ph,t)
    def im(m):
        o=imgs[m.group(1)]; src=re.search(r'src="([^"?]+)',o).group(1); used.add(src)
        wh=''.join(' %s="%s"'%(a,re.search(a+r'="(\d+)"',o).group(1)) for a in ('width','height') if re.search(a+r'="(\d+)"',o))
        return '<img src="%s"%s alt="%s" loading="lazy">'%(src,wh,m.group(2))
    t=re.sub(r'<img n="(\d+)" alt="([^"]*)">',im,t)
    # Spaltenüberschriften der Tabellen als data-label in die Zellen (Handy-Ansicht)
    def table(m):
        tb=m.group(0); ths=[re.sub(r'<[^>]+>','',x).strip() for x in re.findall(r'<th[^>]*>(.*?)</th>',tb,flags=re.S)]
        def row(r):
            n=[-1]
            def td(c):
                n[0]+=1; lab=ths[n[0]] if n[0]<len(ths) else ''
                return re.sub(r' data-label="[^"]*"','',c.group(0)[:-1])+(' data-label="%s">'%html.escape(html.unescape(lab),quote=True) if lab else '>')
            return re.sub(r'<td\b[^>]*>',td,r.group(0))
        return re.sub(r'<tr\b.*?</tr>',row,tb,flags=re.S)
    t=re.sub(r'<table\b.*?</table>',table,t,flags=re.S)
    t=re.sub(r'class="([^"]+)"',lambda m:'class="%s"'%' '.join('m-'+c for c in m.group(1).split()),t)
    t=re.sub(r' data-(feature|kind)="[^"]*"','',t)
    return t.strip()
for i in ids:
    p=W+'/de/%s.html'%i
    if not os.path.exists(p): missing.append(i); continue
    HB[i]=restore(open(p,encoding='utf-8').read())
left=[i for i,v in HB.items() if '[[' in v or re.search(r'<img n=',v)]
js='/* Deutsche Übersetzung der Handbuch-Abschnitte des hundekraft-Projekts (hundekraft/op1-workshop, GPL-3.0-or-later). Erzeugte Datei. */\nwindow.HB={\n'+',\n'.join(json.dumps(k)+':'+json.dumps(v,ensure_ascii=False) for k,v in HB.items())+'\n};\n'
open(OUT+'/anleitung.js','w',encoding='utf-8').write(js)
for s in sorted(used):
    d=OUT+'/'+s; os.makedirs(os.path.dirname(d),exist_ok=True)
    if not os.path.exists(d): shutil.copyfile(S+'/'+s,d)
print('Abschnitte',len(HB),'fehlend',missing,'Reste',left,'Bilder',len(used),'Bytes',len(js.encode()))
