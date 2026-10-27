import json,pathlib,re
s='''圧巻でらした|akkan de rashita
世は実に易し|yo wa jitsu ni yasushi
安心し切った|anshin shikitta
深き喜び|fukaki yorokobi
戦うは|tatakau wa
なぎ倒すは|nagitaosu wa
か弱い己自身さ|kayowai onore jishin sa
胸はって|mune hatte
綺麗に散るのさ|kirei ni chiru no sa
ほんまよーやるわ|honma yoo yaru wa
めっちゃがんばっとるわ|metcha ganbattoru wa
わしかて|washi kate
負けんよーにな|maken yoo ni na
ひそかに|hisoka ni
何かと努めるわ|nanika to tsutomeru wa
なんも無くたって|nanmo nakutatte
いいや|ii ya
結果なんぞ|kekka nanzo
かったりーわ|kattarii wa
鼓動に任せて|kodou ni makasete
自由に踊って|jiyuu ni odotte
敵も味方も|teki mo mikata mo
ここにはねえから|koko ni wa nee kara
ほんまはねえから|honma wa nee kara
あの日のことは|ano hi no koto wa
忘れてね|wasurete ne
消えたいけど|kietai kedo
もう大丈夫|mou daijoubu
旅路は続く|tabiji wa tsuzuku
忘れるね|wasureru ne
みんなだって|minna datte
この宇宙が|kono uchuu ga
教室なら|kyoushitsu nara
隣同士|tonari doushi
学びは続く|manabi wa tsuzuku
果てしないと|hateshinai to
終わりがくると|owari ga kuru to
昨日までより|kinou made yori
優しくなれる|yasashiku nareru
気がした|ki ga shita
あーあ|aa a
僕らは|bokura wa
まだ先の長い|mada saki no nagai
旅の中で|tabi no naka de
中で|naka de
誰かを|dareka o
あるけど|aru kedo
いつの間にか|itsu no ma ni ka
この日さえも|kono hi sae mo
全てを|subete o
笑うだろう|warau darou
愛すだろう|aisu darou
お元気ですか|ogenki desu ka
この町は|kono machi wa
青春です|seishun desu
誰もがみな|dare mo ga mina
まだ見えない|mada mienai
旅路の先へ|tabiji no saki e
僕たちは|bokutachi wa
いつになれど|itsu ni naredo
少年です|shounen desu
心の奥底では|kokoro no okusoko de wa
永遠を|eien o
求めています|motomete imasu
ものが|mono ga
ここには|koko ni wa
無いけど|nai kedo
目にしてきた|me ni shite kita
手に触れてきた|te ni furete kita
全てに|subete ni
意味はあるから|imi wa aru kara
何かを|nanika o
これからまた|kore kara mata
色んな愛を|ironna ai o
あなたに|anata ni
返すだろう|kaesu darou
永遠なる|eien naru
光のなか|hikari no naka
午後も|gogo mo
日々も|hibi mo
終わりが来る|owari ga kuru
あの日の|ano hi no
きらめきも|kirameki mo
ときめきも|tokimeki mo
あれもこれも|are mo kore mo
置いてくる|oite kuru
それで良かったと|sore de yokatta to
これで良かったと|kore de yokatta to
健やかに|sukoyaka ni
日まで|hi made
明けてゆく空も|akete yuku sora mo
暮れてゆく空も|kurete yuku sora mo
超えてゆく|koete yuku
変わりゆくものは|kawari yuku mono wa
仕方がないねと|shikata ga nai ne to
手を放す|te o hanasu
軽くなる|karuku naru
満ちてゆく|michite yuku
手にした|te ni shita
瞬間に|shunkan ni
無くなる|naku naru
そんなものばかり|sonna mono bakari
追いかけては|oikakete wa
無駄にしてた|muda ni shiteta
という言葉|to iu kotoba
今なら|ima nara
本当の意味が|hontou no imi ga
分かるのかな|wakaru no kana
為に|tame ni
愛すのは|aisu no wa
カラカラな心に|karakara na kokoro ni
お恵みを|omegumi o
晴れてゆく空も|harete yuku sora mo
荒れてゆく空も|arete yuku sora mo
愛でてゆく|medete yuku
何もないけれど|nani mo nai keredo
差し出すよ|sashidasu yo
胸の光|mune no hikari
闇を照らし|yami o terashi
道を示す|michi o shimesu
生死を超えて|seishi o koete
共に|tomo ni
愛しか|ai shika
感じたくもない|kanjitaku mo nai
何の分け隔てもない|nan no wakehedate mo nai
かかってきなさい|kakatte kinasai
全て受け止めるから|subete uketomeru kara
一体何がほしいわけ|ittai nani ga hoshii wake
誰に|dare ni
勝ちたいわけ|kachitai wake
気づけんよね|kizuken yo ne
何もかも|nani mo kamo
持ってるのにね|motteru no ni ne
何でも|nan demo
好きに|suki ni
選びな|erabi na
あなたの心の中|anata no kokoro no naka
咲かせな|sakase na
えいっ|ei!
その閉じた心|sono tojita kokoro
こじ開けな|kojiake na
あっけーな|akkee na
何かの|nanika no
あれもこれもが|are mo kore mo ga
比べるものは|kuraberu mono wa
何もない|nani mo nai
勝ちや負けとか|kachi ya make toka
一切ない|issai nai
好きにしてください|suki ni shite kudasai
何も|nani mo
知ったこっちゃない|shitta kotcha nai
僕が|boku ga
激しく泣いたせいで|hageshiku naita sei de
君が|kimi ga
派手に笑ったせいで|hade ni waratta sei de
夏の暑さ|natsu no atsusa
身体を焦がして|karada o kogashite
冬の厳しさ|fuyu no kibishisa
骨身に沁みた|honemi ni shimita
真っ平らに|mattaira ni
真っ直ぐに|massugu ni
そこへ|soko e
行けたかな|iketa kana
っしゃ|ssha
遅くはねーから|osoku wa nee kara
生まれゆくもの|umare yuku mono
死にゆくもの|shini yuku mono
全てが|subete ga
同時の出来事|douji no dekigoto
みな抱きしめたら|mina dakishimetara
踊りなさいな|odori nasai na
さいな|sai na
苦しむことは|kurushimu koto wa
肩落とすこた|kata otosu kota
真っ白な心に|masshiro na kokoro ni
真実を|shinjitsu o
真っ黒なところは|makkuro na tokoro wa
真新しい風に|maatarashii kaze ni
好きだよ|suki da yo
好きだけど|suki da kedo
置いてかなきゃ|oite kanakya
知らんけど|shiran kedo
私たちもう|watashitachi mou
そんな頃よ|sonna koro yo
先に|saki ni
さよならするわ|sayonara suru wa
悪いのは|warui no wa
そうよ|sou yo
いつも私でいいの|itsumo watashi de ii no
先に進まなければ|saki ni susumanakereba
ゴールできぬ|gooru dekinu
ゲームなのよ|geemu na no yo
指切りげんまん|yubikiri genman
ホラでも吹いたら|hora demo fuitara
針でもなんでも|hari demo nan demo
飲ませていただき|nomasete itadaki
鏡よ鏡よ|kagami yo kagami yo
この世で1番|kono yo de ichiban
変わることのない|kawaru koto no nai
愛をくれるのは|ai o kureru no wa
あたしの最後は|atashi no saigo wa
あなたがいい|anata ga ii
あなたと|anata to
このまま|kono mama
おサラバするより|osaraba suru yori
死ぬのがいいわ|shinu no ga ii wa
三度の飯より|sando no meshi yori
あんたがええのよ|anta ga ee no yo
あんたと|anta to
おサラバするよか|osaraba suru yoka
それでも|sore demo
死んでも|shinde mo
治してみせます|naoshite misemasu
失って初めて|ushinatte hajimete
気がつくなんて|ki ga tsuku nante
そんなダサいこと|sonna dasai koto
もうしたないのよ|mou shitanai no yo
わたしの最後は|watashi no saigo wa
そんなダサいのは|sonna dasai no wa
もう要らないのよ|mou iranai no yo'''
M=dict(row.split('|') for row in s.splitlines())
for key in ['workin-hard','tabiji','michi-teyu-ku','matsuri','masshiro','shinunoga-e-wa']:
 p=pathlib.Path('work/analysis',key+'.json');d=json.loads(p.read_text());n=0
 for line,a in d['lines'].items():
  if not a['tk']:continue
  for t in a['tk']:
   if t['t'] in M:t['r']=M[t['t']];n+=1
  # Keep source punctuation in the full line and substitute token readings in order.
  pos=0;parts=[]
  for t in a['tk']:
   q=line.find(t['t'],pos)
   if q<0:raise Exception((line,t))
   parts.append(line[pos:q]);parts.append(t['r']);parts.append(' ');pos=q+len(t['t'])
  parts.append(line[pos:]);a['ro']=re.sub(r'\s+',' ',''.join(parts)).strip()
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2));print(key,n)
