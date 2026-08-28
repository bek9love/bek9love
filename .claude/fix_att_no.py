import zipfile, re, os
SRC='/home/user/bek9love/현장실사-증빙자료-본문(별책쪽번호반영).hwpx'
z=zipfile.ZipFile(SRC); x=z.read('Contents/section0.xml').decode('utf-8')
parts=re.split(r'(<hp:p\b.*?</hp:p>)', x, flags=re.S)
pidx=[i for i,p in enumerate(parts) if p.startswith('<hp:p')]
def T(p):
    s=''.join(re.findall(r'<hp:t[^>]*>(.*?)</hp:t>', p, re.S))
    return re.sub(r'<[^>]+>','',s).replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').strip()
names={'특허 대장':1,'기술이전 대장':2,'사업화 실적 대장':4,'홍보 실적 대장':4,'현장 기술지원(컨설팅) 대장':3}
start={}
for k,i in enumerate(pidx):
    t=T(parts[i])
    if t in names and t not in start: start[t]=k
order=sorted((start[n], names[n]) for n in start)
def group_for(k):
    g=None
    for s,gg in order:
        if k>=s: g=gg
    return g
cnt={}
for k,i in enumerate(pidx):
    p=parts[i]
    if '붙임' not in p: continue
    g=group_for(k)
    if not g: continue
    def sub(m):
        cnt[g]=cnt.get(g,0)+1
        return f'붙임 {g}-{m.group(1)}'
    parts[i]=re.sub(r'붙임\s*(\d+)(?=\s*\()', sub, p)
x2=''.join(parts)
OUT='/home/user/bek9love/현장실사-증빙자료-본문(최종).hwpx'
tmp=OUT+'.tmp'; zin=zipfile.ZipFile(SRC); zo=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d=zin.read(it.filename)
    if it.filename=='Contents/section0.xml': d=x2.encode('utf-8')
    if it.filename=='mimetype': zo.writestr(zipfile.ZipInfo('mimetype'), d, zipfile.ZIP_STORED)
    else: zo.writestr(it, d)
zo.close(); zin.close(); os.replace(tmp,OUT)
print('그룹별 변환', cnt, '→', OUT)
