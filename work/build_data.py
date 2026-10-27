import json,re
from pathlib import Path
root=Path('/Users/user/Documents/Codex/2026-10-28/new-chat')
html=(root/'outputs/kaze-site/dist/index.html').read_text()
keys=re.findall(r'key:"([a-z-]+)"',html)
data={};problems=[]; token_count=0
for key in keys:
    path=root/'work/analysis'/f'{key}.json'
    if not path.exists(): problems.append(f'{key}: missing analysis'); continue
    obj=json.loads(path.read_text())
    raw=(root/'work/lyrics'/f'{key}.txt').read_text().strip()
    uniq=list(dict.fromkeys(line.strip() for line in raw.splitlines() if line.strip()))
    missing=set(uniq)-set(obj['lines']);extra=set(obj['lines'])-set(uniq)
    if missing or extra:problems.append(f'{key}: {len(missing)} missing, {len(extra)} unexpected lines')
    for text in uniq:
        a=obj['lines'].get(text)
        if not a:continue
        if not a.get('zh'):problems.append(f'{key}: missing translation {text}')
        if re.search('[ぁ-ヿ㐀-鿿]',text) and not a.get('ro'): problems.append(f'{key}: missing romaji {text}')
        pos=0
        for t in a.get('tk',[]):
            token_count+=1
            at=text.find(t['t'],pos)
            if at<0:problems.append(f'{key}: misplaced token {t["t"]} in {text}')
            else:pos=at+len(t['t'])
            if t.get('p')!='sym' and not t.get('m'):problems.append(f'{key}: empty token meaning')
    data[key]={'v':1,'raw':raw,'uniq':uniq,'ann':[obj['lines'].get(t) for t in uniq],'summary':obj['summary'],'notes':obj['notes'],'updated':1793145600000}
if problems:
    print('\n'.join(problems));raise SystemExit(1)
out=root/'outputs/kaze-site/dist/data'
out.mkdir(exist_ok=True)
(out/'lyrics.js').write_text('const PUBLISHED = '+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n')
(out/'lyrics.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
report={'songs':len(data),'lines':sum(len(x['raw'].splitlines()) for x in data.values()),'unique_lines':sum(len(x['uniq']) for x in data.values()),'tokens':token_count}
(root/'work/validation.json').write_text(json.dumps(report,indent=2))
print(report)
