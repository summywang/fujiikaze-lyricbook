import json,re
from pathlib import Path
rows=[x.split('\t') for x in Path('work/damn.tsv').read_text().splitlines()]
vocab=[x.split('\t') for x in Path('work/damn-vocab.tsv').read_text().splitlines()]
vocab.sort(key=lambda x:len(x[0]),reverse=True)
lines={}; unmatched=set()
for raw,zh,ro in rows:
    ro=ro.replace('mamottek u','mamotteku')
    tk=[]; pos=0
    if re.search('[ぁ-龯]',raw):
        while pos<len(raw):
            v=next((v for v in vocab if raw.startswith(v[0],pos)),None)
            if v:
                t,k,r,p,m=v;tk.append(dict(t=t,k=k,r=r,p=p,m=m));pos+=len(t)
            else:
                c=raw[pos]; pos+=1
                if re.search('[ぁ-龯]',c):unmatched.add(c)
                tk.append(dict(t=c,k='',r='',p='sym',m=''))
    lines[raw]=dict(v=2,ro=ro,zh=zh,tk=tk)
obj={'summary':'從對他人的迷戀與自責，逐漸轉向靠近、珍惜自己。前半的「あなた」與後半的「わたし」形成對照；最後的自我承諾，讓反覆的咒罵也帶出放下執著的可能。這是依歌詞語境的閱讀，並非唯一解釋。','notes':['てまう是てしまう的方言形式，帶有「不知不覺竟然……」的懊惱；すりゃ、なりゃ分別是すれば、なれば的縮約。','「青さ」可讀成青澀、不成熟；與「赤くなった」的色彩變化一起閱讀，保留詩意，不限定成單一情節。','don’t give a damn 是「不在乎」的慣用語；damn單獨使用則是較粗俗的感嘆。','末段 him 可理解為被照顧的自己；little father 的指涉不明，翻譯保留稱呼，避免當成已證實的宗教指涉。','原文保留你提供的拼寫。We’ll just dancing 屬非標準句法；標準表達可為 We’ll just dance 或 We’ll just be dancing。'],'lines':lines}
expected=set(x for x in Path('work/lyrics/damn.txt').read_text().splitlines() if x)
assert expected==set(lines),(expected-set(lines),set(lines)-expected)
Path('work/analysis/damn.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
print('damn:',len(lines),'unique lines; unmatched Japanese:',unmatched)
