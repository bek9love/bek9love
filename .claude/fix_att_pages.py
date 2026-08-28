import zipfile, re, os
SRC="/root/.claude/uploads/63dc2bb3-3b21-5a25-bf5b-eae5fa6926fc/4c6c0a71-260727___________v3.hwpx"
OUT="/home/user/bek9love/현장실사-증빙자료-본문(별책쪽번호반영).hwpx"

z=zipfile.ZipFile(SRC)
x=z.read('Contents/section0.xml').decode('utf-8')
parts=re.split(r'(<hp:p\b.*?</hp:p>)', x, flags=re.S)
pidx=[i for i,p in enumerate(parts) if p.startswith('<hp:p')]

def text_of(p):
    s=''.join(re.findall(r'<hp:t[^>]*>(.*?)</hp:t>', p, re.S))
    return re.sub(r'<[^>]+>','',s).replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').strip()

# 대장 구획 시작 문단(순번) 찾기
names=['특허 대장','기술이전 대장','사업화 실적 대장','홍보 실적 대장','현장 기술지원(컨설팅) 대장']
start={}
for k,i in enumerate(pidx):
    t=text_of(parts[i])
    if t in names and t not in start: start[t]=k
print('구획 시작 문단', start)

# 별책 기준 오프셋
#  특허     : 별책 붙임1 간지 p.1  → 원본 p.2~23   (변동 없음)
#  기술이전 : 별책 붙임2 간지 p.24 → 원본 p.25~58  (+23)
#  보급     : 별책 붙임4 간지 p.95 → 원본 p.96~99  (+93)
#  컨설팅   : 별책 붙임3 간지 p.59 → 원본 p.60~94  (+57)
SEG=[('특허 대장',0), ('기술이전 대장',23), ('사업화 실적 대장',93), ('홍보 실적 대장',93), ('현장 기술지원(컨설팅) 대장',57)]
order=[(start[n],n,off) for n,off in SEG if n in start]
order.sort()
def offset_for(k):
    cur=0
    for s,n,off in order:
        if k>=s: cur=off
    return cur

log={}
for k,i in enumerate(pidx):
    p=parts[i]
    if '(p.' not in p: continue
    off=offset_for(k)
    def sub(m):
        old=int(m.group(1)); new=old+off
        log.setdefault(off,[]).append((old,new))
        return f'(p.{new})'
    parts[i]=re.sub(r'\(p\.(\d+)\)', sub, p)

x2=''.join(parts)
tmp=OUT+'.tmp'
zin=zipfile.ZipFile(SRC); zo=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
for it in zin.infolist():
    d=zin.read(it.filename)
    if it.filename=='Contents/section0.xml': d=x2.encode('utf-8')
    if it.filename=='mimetype': zo.writestr(zipfile.ZipInfo('mimetype'), d, zipfile.ZIP_STORED)
    else: zo.writestr(it, d)
zo.close(); zin.close(); os.replace(tmp, OUT)

for off in sorted(log):
    v=log[off]
    print(f'오프셋 +{off:2d} : {len(v)}건  {v[0][0]}→{v[0][1]} … {v[-1][0]}→{v[-1][1]}')
print('WROTE', OUT, round(os.path.getsize(OUT)/1024/1024,2),'MB')
