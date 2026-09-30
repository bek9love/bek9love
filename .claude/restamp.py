import fitz, re, io, os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))

R='/home/user/bek9love/'
GRP=[('pat_nopage.pdf', 1, None, 1, '특허'),
     ('tt_nopage.pdf',  1, None, 2, '기술이전'),
     (R+'컨설팅대장(붙임포함).pdf', 2, None, 3, '컨설팅'),
     (R+'보급실적대장.pdf', 2, None, 4, '보급')]

STAMP=re.compile(r'^붙임\s*(\d+)$')

def restamp_page(page, g):
    """좌상단 '붙임 N' 스탬프 → '붙임 g-N'"""
    words=[w for w in page.get_text('words') if w[1]<48 and w[0]<140]
    # '붙임' + 숫자 조합 찾기
    idx=[i for i,w in enumerate(words) if w[4]=='붙임']
    done=None
    for i in idx:
        num=None
        if i+1<len(words) and words[i+1][4].isdigit(): num=words[i+1]
        if num is None: continue
        x0=min(words[i][0], num[0]); y0=min(words[i][1], num[1])
        x1=max(words[i][2], num[2]); y1=max(words[i][3], num[3])
        rect=fitz.Rect(x0-2, y0-2, x1+30, y1+2)
        page.draw_rect(rect, color=None, fill=(1,1,1), overlay=True)
        page.insert_text((x0, y1-2), f'붙임 {g}-{num[4]}',
                         fontname='china-s' if False else 'korea-s', fontsize=11, color=(0,0,0))
        done=int(num[4])
        break
    return done

out=fitz.open()
info=[]
for f, start, end, g, name in GRP:
    d=fitz.open(f)
    pages=range(start, len(d) if end is None else end)
    n=0
    for i in pages:
        p=d[i]
        r=restamp_page(p, g)
        if r: n+=1
    sub=fitz.open(); sub.insert_pdf(d, from_page=start, to_page=(len(d)-1 if end is None else end-1))
    out.insert_pdf(sub)
    info.append((name, g, len(list(pages)), n))
    print(f'{name}: {len(list(pages))}쪽 중 스탬프 갱신 {n}건')
out.save('att_restamped.pdf', garbage=3, deflate=True)
print('붙임 합계', out.page_count, '쪽 →', round(os.path.getsize('att_restamped.pdf')/1024/1024,1),'MB')
