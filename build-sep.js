// 마스터(실사-즉답훈련.html) → 본인 분리본 재생성
const fs = require('fs');
let m = fs.readFileSync('실사-즉답훈련.html','utf8');
let h = m;
// 1) 타이틀/부제/역할버튼
h = h.replace('<title>현장실사 즉답 훈련</title>','<title>현장실사 즉답 훈련 — 본인</title>');
h = h.replace('인사혁신처</div>','인사혁신처 · <b>본인</b>용</div>');
h = h.replace('<button class="rolebtn" id="roleBtn">','<button class="rolebtn" id="roleBtn" style="display:none">');
// 2) 타 페르소나 덱 비우기
h = h.replace(/const DECK_COLA = \[[\s\S]*?\n\];/, 'const DECK_COLA = [];');
h = h.replace(/const DECK_COLB = \[[\s\S]*?\n\];/, 'const DECK_COLB = [];');
h = h.replace(/const DECK_BOSS = \[[\s\S]*?\n\];/, 'const DECK_BOSS = [];');
// 3) PERSONAS: self만
h = h.replace(/const PERSONAS = \[[\s\S]*?\n\];/,
  'const PERSONAS = [\n  {key:"self", name:"본인 (박성민)", deck:DECK_SELF, cats:CATS_SELF},\n];');
// 4) localStorage 키 -self 접미사
for(const k of ['silsa-drill-v1','silsa-memo-v1','silsa-add-v1','silsa-pts-v1','silsa-persona-v1']){
  h = h.split('"'+k+'"').join('"'+k+'-self"');
}
fs.writeFileSync('실사-즉답훈련-본인.html', h);

// 검증
function jsok(file){
  const s=fs.readFileSync(file,'utf8');
  const mm=s.match(/<script>([\s\S]*)<\/script>/);
  try{ new Function(mm[1]); return true; }catch(e){ console.log(file,'JS_ERR',e.message); return false; }
}
function deckSelf(file){
  const s=fs.readFileSync(file,'utf8');
  return s.match(/const DECK_SELF = (\[[\s\S]*?\n\]);/)[1];
}
console.log('본인 JS_OK:', jsok('실사-즉답훈련-본인.html'));
console.log('DECK_SELF 동일(마스터==본인):', deckSelf('실사-즉답훈련.html')===deckSelf('실사-즉답훈련-본인.html'));
console.log('본인 DECK_COLA/COLB/BOSS 비움:',
  /const DECK_COLA = \[\];/.test(h)&&/const DECK_COLB = \[\];/.test(h)&&/const DECK_BOSS = \[\];/.test(h));
console.log('본인 PERSONAS self만:', (h.match(/\{key:"self"|\{key:"colA"|\{key:"colB"|\{key:"boss"/g)||[]).join(','));
console.log('본인 LS -self:', /"silsa-drill-v1-self"/.test(h));
console.log('본인 ver:', (h.match(/class="ver">([^<]*)/)||[])[1]);
console.log('Q2-7 실증 백업 포함:', /2번컵 자세 가림/.test(h));
