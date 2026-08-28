import fitz, json, io, os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))
R='/home/user/bek9love/'
A4=(595.28,841.89); W,H=A4
nums=json.load(open('stamp_nums.json'))

# 1) 기존 별책의 붙임 본문(간지 제외) 위에 새 스탬프 덧씌우기
old=fitz.open(R+'현장실사-증빙자료-붙임(별책).pdf')   # 표지2 + 99p
# 별책 구성: idx2=간지1, 3~24=특허22, 25=간지2, 26~59=기술이전34, 60=간지3, 61~95=컨설팅35, 96=간지4, 97~100=보급4
SEG={1:(3,24),2:(26,59),3:(61,95)}
for g,(a,b) in SEG.items():
    lst=nums[str(g)]
    assert len(lst)==b-a+1, (g,len(lst),b-a+1)
    for k,idx in enumerate(range(a,b+1)):
        p=old[idx]
        p.draw_rect(fitz.Rect(30,15,120,38), color=None, fill=(1,1,1), overlay=True)
        p.insert_text((38,32), f'붙임 {g}-{lst[k]}', fontname='korea-s', fontsize=11, color=(0,0,0))
old.save('old_restamped.pdf', garbage=3, deflate=True)
print('특허·기술이전·컨설팅 스탬프 갱신 완료')

# 2) 보급 4쪽은 새로 렌더한 것으로 교체 (bogeup.pdf 3~6p = 붙임 4-1~4-4)
src=PdfReader('old_restamped.pdf'); bg=PdfReader('bogeup.pdf')
w=PdfWriter()
for i,p in enumerate(src.pages):
    if 96 <= i <= 99:      # 보급 붙임 4쪽 (0-idx 96~99)
        np=bg.pages[i-96+2]
        # 쪽번호 새로 부여 (별책 p.96~99)
        b=io.BytesIO(); c=canvas.Canvas(b,pagesize=A4)
        c.setFillColorRGB(1,1,1); c.rect(W/2-42,12,84,22,stroke=0,fill=1)
        c.setFillColorRGB(0,0,0); c.setFont('HYSMyeongJo-Medium',10)
        c.drawCentredString(W/2,19,f"- {i-1} -"); c.save(); b.seek(0)
        np.merge_page(PdfReader(b).pages[0])
        w.add_page(np)
    else:
        w.add_page(p)
with open(R+'현장실사-증빙자료-붙임(별책).pdf','wb') as f: w.write(f)
print('별책 저장', len(src.pages),'쪽 →', round(os.path.getsize(R+'현장실사-증빙자료-붙임(별책).pdf')/1024/1024,1),'MB')
