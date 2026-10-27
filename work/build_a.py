import json,pathlib,re
ROOT=pathlib.Path('work')
def write(key,summary,notes,rows):
    out={}
    for row in rows.strip().split('\n'):
        cells=row.split('|'); raw,zh,ro=cells[:3]; tokens=[]
        for token in cells[3].split(';') if len(cells)>3 and cells[3] else []:
            t,k,r,p,m=token.split('~');tokens.append(dict(t=t,k=k,r=r,p=p,m=m))
        out[raw]=dict(v=2,ro=ro,zh=zh,tk=tokens)
    source=list(dict.fromkeys(x for x in (ROOT/'lyrics'/f'{key}.txt').read_text().splitlines() if x.strip()))
    assert set(source)==set(out),(key,set(source)-set(out),set(out)-set(source))
    for raw,line in out.items():
        at=0
        for t in line['tk']:
            pos=raw.find(t['t'],at);assert pos>=0,(raw,t);at=pos+len(t['t'])
    (ROOT/'analysis'/f'{key}.json').write_text(json.dumps(dict(summary=summary,notes=notes,lines=out),ensure_ascii=False,indent=2))
write('garden','以四季與庭園比喻生命中的相遇、失去與付出；可以讀成在變動中照顧內心，也學著放手。',['「咲いては枯れ」「失くしては」的「ては」表反覆發生。','「身を任せる」是順著流動、不強行控制；「だけ」在淚與愛的段落可讀成「有多少，就……多少」。','「果てるまで」省略了終結的主體，可理解為直到生命或這段旅程的盡頭。'],r'''
鳥は春を告げて|鳥兒宣告春天到來，|tori wa haru o tsugete|鳥~とり~tori~noun~鳥；は~は~wa~particle~提出主題；春~はる~haru~noun~春天；を~を~o~particle~標示受詞；告げて~つげて~tsugete~verb~告知、宣告（て形）
私は恋をして|而我墜入愛河，|watashi wa koi o shite|私~わたし~watashi~pronoun~我；は~は~wa~particle~主題；恋をして~こいをして~koi o shite~phrase~戀愛、墜入愛河
素敵な温度だけ|只讓那美好的溫度，|suteki na ondo dake|素敵な~すてきな~suteki na~na~美好的；温度~おんど~ondo~noun~溫度；だけ~だけ~dake~particle~只有
触れさせて この肌で|讓我用這肌膚感受吧。|furesasete kono hada de|触れさせて~ふれさせて~furesasete~verb~讓我觸碰（使役的請求）；この~この~kono~other~這個；肌~はだ~hada~noun~肌膚；で~で~de~particle~以、用
雲は夏を帯びて|雲染上了夏日氣息，|kumo wa natsu o obite|雲~くも~kumo~noun~雲；は~は~wa~particle~主題；夏を帯びて~なつをおびて~natsu o obite~phrase~帶著夏日氣息
私は目を閉じて|而我閉上雙眼，|watashi wa me o tojite|私~わたし~watashi~pronoun~我；は~は~wa~particle~主題；目を閉じて~めをとじて~me o tojite~phrase~閉上眼睛
綺麗な時間だけ|只追逐那些美麗的時光，|kirei na jikan dake|綺麗な~きれいな~kirei na~na~美麗的；時間~じかん~jikan~noun~時間、時光；だけ~だけ~dake~particle~只有
追いかけて 尽きるまで|追尋下去，直到耗盡。|oikakete tsukiru made|追いかけて~おいかけて~oikakete~verb~追逐；尽きるまで~つきるまで~tsukiru made~phrase~直到耗盡、終結
花は咲いては枯れ|花朵開了又謝，|hana wa saite wa kare|花~はな~hana~noun~花；は~は~wa~particle~主題；咲いては枯れ~さいてはかれ~saite wa kare~phrase~一次次盛開又枯萎
あなたに心奪われ|我的心被你奪走，|anata ni kokoro ubaware|あなたに~あなたに~anata ni~phrase~被你（被動句的施事）；心奪われ~こころうばわれ~kokoro ubaware~phrase~被奪走心、深深著迷
それでも守り続けたくて|即使如此，仍想一直守護，|sore demo mamoritsuzuketakute|それでも~それでも~sore demo~conj~即使如此；守り続けたくて~まもりつづけたくて~mamoritsuzuketakute~verb~想持續守護
私のガーデン 果てるまで|我的庭園，直到盡頭。|watashi no gaaden hateru made|私の~わたしの~watashi no~phrase~我的；ガーデン~がーでん~gaaden~noun~庭園（garden）；果てるまで~はてるまで~hateru made~phrase~直到終結
人は出会い別れ|人們相遇又別離，|hito wa deai wakare|人~ひと~hito~noun~人；は~は~wa~particle~主題；出会い~であい~deai~verb~相遇；別れ~わかれ~wakare~verb~別離
失くしてはまた手に入れ|失去了，又再次得到，|nakushite wa mata te ni ire|失くしては~なくしては~nakushite wa~phrase~失去後又（反覆）；また~また~mata~adv~再次；手に入れ~てにいれ~te ni ire~phrase~得到、取得
夜が秋を呼んで|夜晚喚來秋天，|yoru ga aki o yonde|夜~よる~yoru~noun~夜晚；が~が~ga~particle~主語；秋を呼んで~あきをよんで~aki o yonde~phrase~喚來秋天
私は旅に出て|而我踏上旅途，|watashi wa tabi ni dete|私~わたし~watashi~pronoun~我；は~は~wa~particle~主題；旅に出て~たびにでて~tabi ni dete~phrase~出發旅行
素敵な出会いだけ|只盼望美好的相遇，|suteki na deai dake|素敵な~すてきな~suteki na~na~美好的；出会い~であい~deai~noun~相遇；だけ~だけ~dake~particle~只有
待っていて その日まで|等待著，直到那天。|matte ite sono hi made|待っていて~まっていて~matte ite~verb~持續等待；その日まで~そのひまで~sono hi made~phrase~直到那一天
だから冬よおいで|所以，冬天啊，來吧，|dakara fuyu yo oide|だから~だから~dakara~conj~所以；冬よ~ふゆよ~fuyu yo~phrase~冬天啊（呼喚）；おいで~おいで~oide~verb~來吧
私を抱きしめて|緊緊抱住我，|watashi o dakishimete|私を~わたしを~watashi o~phrase~把我；抱きしめて~だきしめて~dakishimete~verb~緊緊抱住
その手の温もりで|用你手中的溫暖，|sono te no nukumori de|その手の~そのての~sono te no~phrase~那隻手的；温もり~ぬくもり~nukumori~noun~溫暖、暖意；で~で~de~particle~用、憑藉
生きさせて 溶けるまで|讓我活下去，直到融化。|ikisasete tokeru made|生きさせて~いきさせて~ikisasete~verb~讓我活著；溶けるまで~とけるまで~tokeru made~phrase~直到融化
季節に身を置いて|將自己置身於季節裡，|kisetsu ni mi o oite|季節に~きせつに~kisetsu ni~phrase~在季節裡；身を置いて~みをおいて~mi o oite~phrase~置身於
流れに身を任せ|讓自己順著流動，|nagare ni mi o makase|流れに~ながれに~nagare ni~phrase~順著流動、趨勢；身を任せ~みをまかせ~mi o makase~phrase~將自身交付、順其自然
なるようになるだけ|事情只會成為它會成為的樣子，|naru you ni naru dake|なるようになる~なるようになる~naru you ni naru~phrase~船到橋頭自然直、順其自然發展；だけ~だけ~dake~particle~只是
受け入れて そのままで|接受吧，就保持這樣。|ukeirete sono mama de|受け入れて~うけいれて~ukeirete~verb~接受；そのままで~そのままで~sono mama de~phrase~就照原樣
流した涙だけ|流過多少眼淚，|nagashita namida dake|流した~ながした~nagashita~verb~流下的；涙~なみだ~namida~noun~眼淚；だけ~だけ~dake~particle~有多少就有多少
ふりまいた愛だけ|散播過多少愛，|furimaita ai dake|ふりまいた~ふりまいた~furimaita~verb~散播的；愛~あい~ai~noun~愛；だけ~だけ~dake~particle~有多少就有多少
豊かになる庭で|庭園便因此愈加豐盛，|yutaka ni naru niwa de|豊かになる~ゆたかになる~yutaka ni naru~phrase~變得豐盛；庭で~にわで~niwa de~phrase~在庭園裡
掴んだ手 解き放て 空の果て|鬆開緊握的手吧，放向天空的盡頭。|tsukanda te tokihanate sora no hate|掴んだ手~つかんだて~tsukanda te~phrase~握住的手；解き放て~ときはなて~tokihanate~verb~解放吧、放開吧（命令形）；空の果て~そらのはて~sora no hate~phrase~天空的盡頭
ガーデン 果てるまで|這座庭園，直到盡頭。|gaaden hateru made|ガーデン~がーでん~gaaden~noun~庭園；果てるまで~はてるまで~hateru made~phrase~直到終結
'''.replace('；',';'))
write('hana','花的盛衰與內在的花相互映照；歌詞可讀成接納外在變化，並尋找自身不易消逝的價值。',['「誰を生きようかな」把「生きる」與「誰を」相接，是有意留白的詩性說法，可理解為要活成誰、以何種自我活著。','「内なる」是較書面的「內在的」；「咲かせる」是「咲く」的使役形，意為讓花綻放。','「誰もが一人／全ては一つ」並置個體的孤獨與整體的連結，翻譯保留這個張力。'],r'''
枯れていく|正漸漸枯萎，|karete iku|枯れていく~かれていく~karete iku~verb~逐漸枯萎（ていく表變化延續）
今この瞬間も|就在此時此刻，也，|ima kono shunkan mo|今~いま~ima~noun~現在；この瞬間~このしゅんかん~kono shunkan~phrase~這個瞬間；も~も~mo~particle~也
咲いている|正盛開著。|saite iru|咲いている~さいている~saite iru~verb~正在盛開
全ては溶けていく|一切都逐漸消融。|subete wa tokete iku|全て~すべて~subete~noun~一切；は~は~wa~particle~主題；溶けていく~とけていく~tokete iku~verb~逐漸融化、消融
何が出来るのだろうか|我究竟能做些什麼呢？|nani ga dekiru no darou ka|何が~なにが~nani ga~phrase~什麼（主語）；出来る~できる~dekiru~verb~能做到；のだろうか~のだろうか~no darou ka~phrase~究竟……呢（自問）
誰を生きようかな|我該活成誰的模樣呢？|dare o ikiyou kana|誰を~だれを~dare o~phrase~誰（此處是詩性受詞）；生きようかな~いきようかな~ikiyou kana~phrase~要怎麼活呢（意志形加自問）
みんな儚い|每個人都如此短暫，|minna hakanai|みんな~みんな~minna~noun~大家、一切；儚い~はかない~hakanai~adj~短暫無常、易逝
みんな尊い|每個人都如此珍貴。|minna toutoi|みんな~みんな~minna~noun~大家、一切；尊い~とうとい~toutoi~adj~珍貴、值得尊重
しわしわに萎れた花束 小わきに抱えて|將皺縮枯萎的花束夾抱在臂彎，|shiwashiwa ni shioreta hanataba kowaki ni kakaete|しわしわに~しわしわに~shiwashiwa ni~adv~皺巴巴地；萎れた~しおれた~shioreta~verb~枯萎的；花束~はなたば~hanataba~noun~花束；小わきに抱えて~こわきにかかえて~kowaki ni kakaete~phrase~夾抱在腋下、臂彎
永遠に変わらぬ輝き 探してた|一直尋找永遠不變的光輝。|eien ni kawaranu kagayaki sagashiteta|永遠に~えいえんに~eien ni~adv~永遠地；変わらぬ~かわらぬ~kawaranu~verb~不改變的（ぬ是否定）；輝き~かがやき~kagayaki~noun~光輝；探してた~さがしてた~sagashiteta~verb~一直在尋找（探していた的口語）
僕らを信じてみた|我試著相信我們，|bokura o shinjite mita|僕らを~ぼくらを~bokura o~phrase~我們（受詞）；信じてみた~しんじてみた~shinjite mita~verb~試著相信了
僕らを感じてた|也一直感受著我們。|bokura o kanjiteta|僕らを~ぼくらを~bokura o~phrase~我們（受詞）；感じてた~かんじてた~kanjiteta~verb~一直感受著
咲かせにいくよ 内なる花を|我要去讓內心的花綻放。|sakase ni iku yo uchi naru hana o|咲かせにいくよ~さかせにいくよ~sakase ni iku yo~phrase~要去使它綻放喔；内なる~うちなる~uchi naru~phrase~內在的；花を~はなを~hana o~phrase~花（倒裝受詞）
さりげなく|不著痕跡地，|sarigenaku|さりげなく~さりげなく~sarigenaku~adv~自然地、不著痕跡地
思いを込めてみる|試著注入心意。|omoi o komete miru|思いを込めてみる~おもいをこめてみる~omoi o komete miru~phrase~試著傾注心意
やむを得ず|在不得已之下，|yamu o ezu|やむを得ず~やむをえず~yamu o ezu~phrase~不得已、無可奈何
祈りを込めていく|將祈願一點點傾注其中。|inori o komete iku|祈り~いのり~inori~noun~祈禱、祈願；を込めていく~をこめていく~o komete iku~phrase~持續注入、傾注
いつまで迷うんだろうか|我還要迷惘到什麼時候呢？|itsu made mayou n darou ka|いつまで~いつまで~itsu made~adv~直到何時；迷う~まよう~mayou~verb~迷惘；んだろうか~んだろうか~n darou ka~phrase~究竟……呢
いつかは分かるよな|總有一天會明白的吧。|itsuka wa wakaru yo na|いつかは~いつかは~itsuka wa~phrase~總有一天；分かるよな~わかるよな~wakaru yo na~phrase~會懂的吧（自我確認）
誰もが一人|每個人都是獨自一人，|dare mo ga hitori|誰もが~だれもが~dare mo ga~phrase~每一個人都；一人~ひとり~hitori~noun~一個人、獨自
全ては一つ ay|而一切又是一體，ay。|subete wa hitotsu ay|全ては~すべては~subete wa~phrase~一切（主題）；一つ~ひとつ~hitotsu~noun~一個、一體；ay~ay~ay~interj~和聲
色々な姿や形に惑わされるけど|雖然會被種種姿態與形貌迷惑，|iroiro na sugata ya katachi ni madowasareru kedo|色々な~いろいろな~iroiro na~na~各式各樣的；姿や形に~すがたやかたちに~sugata ya katachi ni~phrase~被姿態、形狀等；惑わされるけど~まどわされるけど~madowasareru kedo~phrase~雖然被迷惑
いつの日か 全てがかわいく思えるさ|總有一天，會覺得一切都很可愛的。|itsu no hi ka subete ga kawaiku omoeru sa|いつの日か~いつのひか~itsu no hi ka~phrase~總有一天；全てが~すべてが~subete ga~phrase~一切都；かわいく思えるさ~かわいくおもえるさ~kawaiku omoeru sa~phrase~會覺得可愛的啊
わたしは何になろうか|我想成為什麼呢？|watashi wa nani ni narou ka|わたしは~わたしは~watashi wa~phrase~我（主題）；何になろうか~なにになろうか~nani ni narou ka~phrase~要成為什麼呢
どんな色がいいかな|什麼樣的顏色才好呢？|donna iro ga ii kana|どんな色~どんないろ~donna iro~phrase~什麼樣的顏色；がいいかな~がいいかな~ga ii kana~phrase~比較好呢（自問）
探しにいくよ 内なる花を|我要去尋找內心的花。|sagashi ni iku yo uchi naru hana o|探しにいくよ~さがしにいくよ~sagashi ni iku yo~phrase~要去尋找喔；内なる~うちなる~uchi naru~phrase~內在的；花を~はなを~hana o~phrase~花（倒裝受詞）
My flower's here, my flower's here|我的花就在這裡，我的花就在這裡。||
'''.replace('；',';'))
write('kirari','在混亂與流動的人生裡，選擇與「你」同行，也讓新日子與笨拙的過往一同發光。這裡的「你」保留為可開放理解的對象。',['「さらり」偏向輕盈俐落、毫不費力；「きらり」是光芒一閃；「ほろり」可描寫落淚；「ゆらり」描寫輕輕搖晃。','「二人は一人きり」「明け行く夕日」「今夜も昼下がり」刻意並置不尋常的時間與人數意象，翻譯保留矛盾，不改成一般敘述。','「最後にゃ」是「最後には」的縮約；「連れてって」是「連れていって」的口語。'],r'''
荒れ狂う季節の中を二人は一人きり さらり|在狂亂的季節裡，兩人如獨自一人般，輕盈前行。|arekuruu kisetsu no naka o futari wa hitorikiri sarari|荒れ狂う~あれくるう~arekuruu~verb~狂暴翻騰的；季節の中を~きせつのなかを~kisetsu no naka o~phrase~穿越季節之中；二人は一人きり~ふたりはひとりきり~futari wa hitorikiri~phrase~兩人卻像獨自一人（詩性並置）；さらり~さらり~sarari~adv~輕盈、俐落地
明け行く夕日の中を今夜も昼下がり さらり|在漸漸破曉的夕陽中，今夜也是午後，輕輕掠過。|akeyuku yuuhi no naka o kon'ya mo hirusagari sarari|明け行く~あけゆく~akeyuku~verb~逐漸破曉；夕日の中を~ゆうひのなかを~yuuhi no naka o~phrase~在夕陽之中穿行；今夜も昼下がり~こんやもひるさがり~kon'ya mo hirusagari~phrase~今夜也是午後（詩性時間並置）；さらり~さらり~sarari~adv~輕盈地
どれほど朽ち果てようと最後にゃ笑いたい|無論朽敗到何種地步，最後還是想笑著。|dore hodo kuchihateyou to saigo nya waraitai|どれほど~どれほど~dore hodo~adv~無論多麼；朽ち果てようと~くちはてようと~kuchihateyou to~phrase~即使徹底朽敗；最後にゃ~さいごにゃ~saigo nya~phrase~最後（最後には的口語）；笑いたい~わらいたい~waraitai~verb~想要笑
何のために戦おうとも動機は愛がいい ah|無論為何而戰，我希望動機是愛，啊。|nan no tame ni tatakaou tomo douki wa ai ga ii ah|何のために~なんのために~nan no tame ni~phrase~為了什麼；戦おうとも~たたかおうとも~tatakaou tomo~phrase~無論怎樣戰鬥；動機は~どうきは~douki wa~phrase~動機（主題）；愛がいい~あいがいい~ai ga ii~phrase~是愛就好；ah~ah~ah~interj~啊
新しい日々は探さずとも常に ここに (ここに)|新的日子不必尋找，始終就在這裡（在這裡）。|atarashii hibi wa sagasazu tomo tsune ni koko ni (koko ni)|新しい日々は~あたらしいひびは~atarashii hibi wa~phrase~新的每一天；探さずとも~さがさずとも~sagasazu tomo~phrase~即使不尋找；常に~つねに~tsune ni~adv~始終；ここに~ここに~koko ni~phrase~在這裡；ここに~ここに~koko ni~phrase~在這裡
色々見てきたけれどこの瞳は永遠に きらり|雖然見過了許多，這雙眼眸仍會永遠閃耀。|iroiro mite kita keredo kono hitomi wa eien ni kirari|色々見てきたけれど~いろいろみてきたけれど~iroiro mite kita keredo~phrase~雖然一路看過許多；この瞳は~このひとみは~kono hitomi wa~phrase~這雙眼眸；永遠に~えいえんに~eien ni~adv~永遠；きらり~きらり~kirari~adv~閃閃發光、一閃
あれほど生きてきたけど全ては夢みたい|活過了這麼多，一切卻彷彿一場夢。|are hodo ikite kita kedo subete wa yume mitai|あれほど生きてきたけど~あれほどいきてきたけど~are hodo ikite kita kedo~phrase~雖然一路活過那麼多；全ては~すべては~subete wa~phrase~一切；夢みたい~ゆめみたい~yume mitai~phrase~像夢一樣
あれもこれも魅力的でも私は君がいい ah|這也迷人、那也迷人，但我選擇你，啊。|are mo kore mo miryokuteki demo watashi wa kimi ga ii ah|あれもこれも~あれもこれも~are mo kore mo~phrase~這個那個都；魅力的でも~みりょくてきでも~miryokuteki demo~phrase~即使很有魅力；私は君がいい~わたしはきみがいい~watashi wa kimi ga ii~phrase~我覺得你最好、我選擇你；ah~ah~ah~interj~啊
どこにいたの 探してたよ|你在哪裡呀？我一直在找你。|doko ni ita no sagashiteta yo|どこにいたの~どこにいたの~doko ni ita no~phrase~你之前在哪裡；探してたよ~さがしてたよ~sagashiteta yo~phrase~一直在找喔
連れてって 連れてって|帶我走，帶我走。|tsuretette tsuretette|連れてって~つれてって~tsuretette~verb~帶我走（連れていって縮約）；連れてって~つれてって~tsuretette~verb~帶我走
何もかも 捨ててくよ|我會拋下一切跟你走。|nani mo kamo suteteku yo|何もかも~なにもかも~nani mo kamo~phrase~一切；捨ててくよ~すててくよ~suteteku yo~phrase~要拋下帶著走、一路放下（捨てていく）
どこまでも どこまでも|無論到哪裡，無論多遠。|doko made mo doko made mo|どこまでも~どこまでも~doko made mo~adv~無論到多遠；どこまでも~どこまでも~doko made mo~adv~無論到哪裡
荒れ狂う 季節の中も 群衆の中も|無論在狂亂的季節裡，還是在洶湧人群中，|arekuruu kisetsu no naka mo gunshuu no naka mo|荒れ狂う~あれくるう~arekuruu~verb~狂亂的；季節の中も~きせつのなかも~kisetsu no naka mo~phrase~在季節中也；群衆の中も~ぐんしゅうのなかも~gunshuu no naka mo~phrase~在人群中也
君とならば さらり さらり|只要與你一起，就能輕盈地、輕盈地走過。|kimi to naraba sarari sarari|君とならば~きみとならば~kimi to naraba~phrase~如果是和你一起；さらり~さらり~sarari~adv~輕盈俐落地；さらり~さらり~sarari~adv~輕盈俐落地
新しい日々も 拙い過去も 全てがきらり yeah|新的日子與笨拙的過去，一切都閃閃發亮，yeah。|atarashii hibi mo tsutanai kako mo subete ga kirari yeah|新しい日々も~あたらしいひびも~atarashii hibi mo~phrase~新的日子也；拙い過去も~つたないかこも~tsutanai kako mo~phrase~笨拙不成熟的過去也；全てがきらり~すべてがきらり~subete ga kirari~phrase~一切都閃耀；yeah~yeah~yeah~interj~耶
無くしてしまったものを振り返って ほろり|回望那些已經失去的事物，不禁落淚。|nakushite shimatta mono o furikaette horori|無くしてしまったものを~なくしてしまったものを~nakushite shimatta mono o~phrase~已失去的東西（帶遺憾）；振り返って~ふりかえって~furikaette~verb~回顧；ほろり~ほろり~horori~adv~淚水輕輕落下
時には途方に暮れてただ風に吹かれて ゆらり|有時茫然無措，只任風吹拂，輕輕搖晃。|toki ni wa tohou ni kurete tada kaze ni fukarete yurari|時には~ときには~toki ni wa~adv~有時；途方に暮れて~とほうにくれて~tohou ni kurete~phrase~茫然無措；ただ~ただ~tada~adv~只是；風に吹かれて~かぜにふかれて~kaze ni fukarete~phrase~被風吹拂；ゆらり~ゆらり~yurari~adv~悠悠搖晃
息せき切ってきたの|一路氣喘吁吁地趕來了嗎？|iki seki kitte kita no|息せき切ってきたの~いきせききってきたの~iki seki kitte kita no~phrase~一路急急忙忙、氣喘吁吁地過來嗎（息せき切る）
行き先は決めたの|已經決定要去哪裡了嗎？|ikisaki wa kimeta no|行き先は~いきさきは~ikisaki wa~phrase~目的地；決めたの~きめたの~kimeta no~phrase~決定了嗎
迷わずに行きたいけど保証はしないよ|雖然想毫不猶豫地前進，但我可不作保證。|mayowazu ni ikitai kedo hoshou wa shinai yo|迷わずに~まよわずに~mayowazu ni~adv~不迷惘、不猶豫地；行きたいけど~いきたいけど~ikitai kedo~phrase~雖然想前進；保証はしないよ~ほしょうはしないよ~hoshou wa shinai yo~phrase~不作保證喔
何か分かったようで|好像明白了些什麼，|nanika wakatta you de|何か~なにか~nanika~pronoun~某些什麼；分かったようで~わかったようで~wakatta you de~phrase~似乎明白了
何も分かってなくて|卻又什麼也不懂。|nani mo wakattenakute|何も~なにも~nani mo~phrase~什麼也（搭配否定）；分かってなくて~わかってなくて~wakattenakute~verb~還不明白
だけどそれが分かって本当に良かった|不過能明白這一點，真是太好了。|dakedo sore ga wakatte hontou ni yokatta|だけど~だけど~dakedo~conj~但是；それが分かって~それがわかって~sore ga wakatte~phrase~能懂這一點；本当に良かった~ほんとうによかった~hontou ni yokatta~phrase~真的太好了
新しい日々は探さずとも常に ここに|新的日子不必尋找，始終就在這裡。|atarashii hibi wa sagasazu tomo tsune ni koko ni|新しい日々は~あたらしいひびは~atarashii hibi wa~phrase~新的每一天；探さずとも~さがさずとも~sagasazu tomo~phrase~即使不找；常に~つねに~tsune ni~adv~始終；ここに~ここに~koko ni~phrase~在這裡
常にここに ここに ah|始終在這裡，就在這裡，啊。|tsune ni koko ni koko ni ah|常に~つねに~tsune ni~adv~始終；ここに~ここに~koko ni~phrase~在這裡；ここに~ここに~koko ni~phrase~在這裡；ah~ah~ah~interj~啊
永遠に きらり|永遠閃耀。|eien ni kirari|永遠に~えいえんに~eien ni~adv~永遠；きらり~きらり~kirari~adv~閃耀
Ah 生きてきたけど全ては夢みたい|啊，雖然一路活到現在，一切卻彷彿一場夢。|Ah ikite kita kedo subete wa yume mitai|Ah~Ah~Ah~interj~啊；生きてきたけど~いきてきたけど~ikite kita kedo~phrase~雖然一路活過來；全ては夢みたい~すべてはゆめみたい~subete wa yume mitai~phrase~一切像夢一樣
あれもこれも魅力的でも私は君がいい|這也迷人、那也迷人，但我選擇你。|are mo kore mo miryokuteki demo watashi wa kimi ga ii|あれもこれも~あれもこれも~are mo kore mo~phrase~這個那個都；魅力的でも~みりょくてきでも~miryokuteki demo~phrase~即使有魅力；私は君がいい~わたしはきみがいい~watashi wa kimi ga ii~phrase~我選擇你
Ah ah ah ah|啊、啊、啊、啊。||
'''.replace('；',';'))
base={a[0]:a[1:] for line in (ROOT/'lyrics/nan-nan.tsv').read_text().splitlines() if (a:=line.split('\t'))}
chunkrows=r'''
あんたのその歯にはさがった青さ粉に|あんたの~あんたの~anta no~phrase~你的（親近或直率）；その歯に~そのはに~sono ha ni~phrase~在那牙齒上；はさがった~はさがった~hasagatta~verb~卡住的（保留原文方言形式）；青さ粉に~あおさこに~aosako ni~phrase~對那海苔粉（接下一行的提及）
ふれるべきか否かで少し悩んでる|ふれるべきか否かで~ふれるべきかいなかで~fureru beki ka ina ka de~phrase~為了該不該提起；少し~すこし~sukoshi~adv~稍微；悩んでる~なやんでる~nayanderu~verb~正在煩惱（悩んでいる縮約）
口にしない方がいい真実もあるから|口にしない方がいい~くちにしないほうがいい~kuchi ni shinai hou ga ii~phrase~最好不要說出口；真実もあるから~しんじつもあるから~shinjitsu mo aru kara~phrase~因為也有這樣的真相
…知らない方が良かったなんて言わないで居て|知らない方が良かった~しらないほうがよかった~shiranai hou ga yokatta~phrase~不知道還比較好；なんて~なんて~nante~particle~之類的話；言わないで居て~いわないでいて~iwanaide ite~phrase~請不要說出來、不要變得這麼說
何があってもずっと大好きなのに|何があっても~なにがあっても~nani ga atte mo~phrase~不管發生什麼；ずっと~ずっと~zutto~adv~始終；大好きなのに~だいすきなのに~daisuki na noni~phrase~明明這麼喜歡你
どんなときも ここにいるのに|どんなときも~どんなときも~donna toki mo~phrase~無論何時；ここにいるのに~ここにいるのに~koko ni iru noni~phrase~明明就在這裡
近すぎて 見えなくて ムシされて|近すぎて~ちかすぎて~chikasugite~adj~太靠近；見えなくて~みえなくて~mienakute~verb~看不見；ムシされて~むしされて~mushi sarete~verb~被忽略（無視的片假名寫法）
雨の中一人行くあんた|雨の中~あめのなか~ame no naka~phrase~雨中；一人行く~ひとりゆく~hitori yuku~phrase~獨自前行；あんた~あんた~anta~pronoun~你
心の中でささやくのよ そっちに行ってはダメと|心の中で~こころのなかで~kokoro no naka de~phrase~在心中；ささやくのよ~ささやくのよ~sasayaku no yo~phrase~輕聲告訴你啊；そっちに行ってはダメと~そっちにいってはだめと~socchi ni itte wa dame to~phrase~說著「不能往那邊去」
聞かないフリ続けるあんた|聞かないフリ~きかないふり~kikanai furi~phrase~裝作沒聽見；続ける~つづける~tsuzukeru~verb~繼續；あんた~あんた~anta~pronoun~你
勢いにまかせて 肥溜めへとダイブ|勢いにまかせて~いきおいにまかせて~ikioi ni makasete~phrase~任由衝動帶著走；肥溜めへと~こえだめへと~koedame e to~phrase~朝著糞坑；ダイブ~だいぶ~daibu~noun~一頭跳入（dive）
それは何なん|それは~それは~sore wa~phrase~那究竟；何なん~なんなん~nan nan~phrase~是怎樣、是什麼（何なの方言）
先がけてワシは言うたが|先がけて~さきがけて~sakigakete~adv~事先、提前；ワシは~わしは~washi wa~phrase~我（方言自稱）；言うたが~ゆうたが~yuuta ga~phrase~不是說過了嗎（言った的方言形式）
それならば何なん|それならば~それならば~sore naraba~conj~既然如此；何なん~なんなん~nan nan~phrase~那是怎樣
何で何も聞いてくれんかったん|何で~なんで~nande~adv~為什麼；何も~なにも~nani mo~phrase~什麼也（後接否定）；聞いてくれんかったん~きいてくれんかったん~kiite kuren kattan~phrase~不肯聽我說呢（くれなかったの的方言）
その顔は何なんw|その顔は~そのかおは~sono kao wa~phrase~你那表情；何なん~なんなん~nan nan~phrase~是怎樣啦；w~わらい~warai~sym~網路笑聲標記，通常不另唱出
花咲く町の角誓った|花咲く~はなさく~hana saku~phrase~花開的；町の角~まちのかど~machi no kado~phrase~街角；誓った~ちかった~chikatta~verb~發誓了
あの時の笑顔は何なん|あの時の~あのときの~ano toki no~phrase~那時的；笑顔は~えがおは~egao wa~phrase~笑容；何なん~なんなん~nan nan~phrase~算什麼、是怎樣
あの時の涙は何じゃったん|あの時の~あのときの~ano toki no~phrase~那時的；涙は~なみだは~namida wa~phrase~眼淚；何じゃったん~なんじゃったん~nan jattan~phrase~到底是什麼呢（何だったの的方言）
たまには大胆に攻めたら良い|たまには~たまには~tama ni wa~adv~偶爾；大胆に~だいたんに~daitan ni~adv~大膽地；攻めたら良い~せめたらいい~semetara ii~phrase~進攻、積極出擊就好
時には慎重に歩めば良い|時には~ときには~toki ni wa~adv~有時；慎重に~しんちょうに~shinchou ni~adv~謹慎地；歩めば良い~あゆめばいい~ayumeba ii~phrase~前行就好
真実なんてもんはとっくのとうに|真実なんてもんは~しんじつなんてもんは~shinjitsu nante mon wa~phrase~真相這種東西；とっくのとうに~とっくのとうに~tokku no tou ni~adv~早就、很久以前就
知っていることを知らないだけでしょう|知っていることを~しっていることを~shitte iru koto o~phrase~自己知道的這件事；知らないだけでしょう~しらないだけでしょう~shiranai dake deshou~phrase~只是還不知道而已吧
あれほど刻んだ後悔も|あれほど~あれほど~are hodo~adv~那麼深地；刻んだ~きざんだ~kizanda~verb~刻下的；後悔も~こうかいも~koukai mo~phrase~連後悔也
くり返す毎日の中で かき消されていくのね|くり返す毎日の中で~くりかえすまいにちのなかで~kurikaesu mainichi no naka de~phrase~在反覆的每一天裡；かき消されていくのね~かきけされていくのね~kakikesarete iku no ne~phrase~就這樣逐漸被抹去了呢
真っさらになった決意を胸に|真っさらになった~まっさらになった~massara ni natta~phrase~變得全新、歸零的；決意を胸に~けついをむねに~ketsui o mune ni~phrase~把決心放在心中、懷著決心
あんたは堂々と また肥溜めへとダイブ|あんたは~あんたは~anta wa~phrase~你；堂々と~どうどうと~doudou to~adv~大搖大擺、堂而皇之地；また~また~mata~adv~又；肥溜めへと~こえだめへと~koedame e to~phrase~朝著糞坑；ダイブ~だいぶ~daibu~noun~一頭跳入
神様たすけて、やばめ やばめ やばめ やばめ|神様~かみさま~kamisama~noun~神啊；たすけて~たすけて~tasukete~verb~救救我；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙
足元照らして、やばめ やばめ やばめ やばめ|足元~あしもと~ashimoto~noun~腳下；照らして~てらして~terashite~verb~請照亮；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙；やばめ~やばめ~yabame~adj~有點不妙
目を閉じてみて 心の耳すまして 優しい気持ちで|目を閉じてみて~めをとじてみて~me o tojite mite~phrase~試著閉上眼睛；心の耳すまして~こころのみみすまして~kokoro no mimi sumashite~phrase~豎起心中的耳朵、專心聆聽；優しい気持ちで~やさしいきもちで~yasashii kimochi de~phrase~懷著溫柔心情
答えを聴いて もう歌わせないで|答えを聴いて~こたえをきいて~kotae o kiite~phrase~聽聽答案；もう歌わせないで~もううたわせないで~mou utawasenaide~phrase~別再讓我唱了（使役否定請求）
裏切りのブルース|裏切りの~うらぎりの~uragiri no~phrase~背叛的；ブルース~ぶるーす~buruusu~noun~藍調（blues）
それは「何なんw」|それは~それは~sore wa~phrase~那就是；何なん~なんなん~nan nan~phrase~這是怎樣；w~わらい~warai~sym~網路笑聲標記
…ワシは言うたが|ワシは~わしは~washi wa~phrase~我；言うたが~ゆうたが~yuuta ga~phrase~不是早就說過了嗎
何で聞いてくれんかったん|何で~なんで~nande~adv~為什麼；聞いてくれんかったん~きいてくれんかったん~kiite kuren kattan~phrase~不肯聽我說呢
何なん 何なん 何なん|何なん~なんなん~nan nan~phrase~到底怎樣；何なん~なんなん~nan nan~phrase~到底怎樣；何なん~なんなん~nan nan~phrase~到底怎樣
何なん|何なん~なんなん~nan nan~phrase~到底是怎樣
'''.replace('；',';')
rows=[]
for row in chunkrows.strip().splitlines():
    raw,tk=row.split('|'); zh,ro=base[raw];rows.append('|'.join([raw,zh,ro.strip(),tk]))
write('nan-nan','歌詞像一位親近的提醒者對反覆忽略勸告的人說話，吐槽中帶著關愛；也可以讀成自己與內心聲音的對話。',['「ワシ」「言うた」「くれんかった」「じゃった」呈現方言口吻，學習時可對照標準語「私／言った／くれなかった／だった」。','「青さ粉」「はさがった」依你提供的原文保留；前者按「あおさこ」讀，後者按「はさがった」讀，不擅自改寫成標準拼法。','「何なんw」的 w 是網路笑聲記號，表現吐槽語氣；羅馬字不把它當成歌唱音節。','「肥溜め」字面是糞坑，此處可作陷入糟糕處境的誇張意象。'], '\n'.join(rows))
base={a[0]:a[1] for line in (ROOT/'lyrics/its-alright.tsv').read_text().splitlines() if (a:=line.split('\t'))}
extras={
'母なる大地は私の愛し子':('haha naru daichi wa watashi no itoshigo','母なる~ははなる~haha naru~phrase~作為母親的;大地は~だいちは~daichi wa~phrase~大地（主題）;私の~わたしの~watashi no~phrase~我的;愛し子~いとしご~itoshigo~noun~心愛的孩子'),
'父なる太陽は私のまなこ':('chichi naru taiyou wa watashi no manako','父なる~ちちなる~chichi naru~phrase~作為父親的;太陽は~たいようは~taiyou wa~phrase~太陽（主題）;私の~わたしの~watashi no~phrase~我的;まなこ~まなこ~manako~noun~眼睛（較文學性的說法）'),
'この世は私の思わく通りに':('kono yo wa watashi no omowaku doori ni','この世は~このよは~kono yo wa~phrase~這個世界;私の~わたしの~watashi no~phrase~我的;思わく通りに~おもわくどおりに~omowaku doori ni~phrase~如心中所想、依照心意'),
'今日とて可愛く回っています':('kyou tote kawaiku mawatte imasu','今日とて~きょうとて~kyou tote~phrase~即使今天也、今天同樣;可愛く~かわいく~kawaiku~adv~可愛地;回っています~まわっています~mawatte imasu~verb~正轉動著（禮貌語）')}
base["It's all, right"]='這一切，都很好。'
base['Give it up, kama']='放下吧，那份欲望。'
base['Bring it on, Prema']='讓愛到來吧。'
rows=[]
for raw,zh in base.items():
    ro,tk=extras.get(raw,('',''));rows.append('|'.join([raw,zh,ro,tk]))
write('its-alright','以擁抱與內在神性的意象安慰聽者，從哭泣走向安心。日文段落將大地、太陽與「我」連結，可以作為整體與自我相連的詩性描寫。',['「母なる／父なる」的「なる」相當於較文學性的「作為……的」。','「cry your heart out」意為痛痛快快地哭；ur 是 your 的非正式縮寫。','「It’s all, right」把 alright 拆開，這裡保留為「這一切，都很好」的雙關讀法。','kama 與 Prema 在此分別按欲望與愛的對比理解；這是依語境的學習譯法，不等於歌詞對宗教概念的完整定義。','「愛し子」可有不同詞典讀法，此處採「いとしご」；實際歌唱連音請搭配原曲聽辨。'],'\n'.join(rows))
# Preserve every original character as ordered display tokens, including spaces.
for key in ['garden','hana','kirari','nan-nan','its-alright']:
    path=ROOT/'analysis'/f'{key}.json';obj=json.loads(path.read_text())
    for raw,line in obj['lines'].items():
        if not line['tk']:continue
        fixed=[];at=0
        for tok in line['tk']:
            pos=raw.index(tok['t'],at)
            if pos>at:fixed.append(dict(t=raw[at:pos],k='',r='',p='sym',m='空白或標點'))
            fixed.append(tok);at=pos+len(tok['t'])
        if at<len(raw):fixed.append(dict(t=raw[at:],k='',r='',p='sym',m='空白或標點'))
        line['tk']=fixed
        assert ''.join(t['t'] for t in fixed)==raw
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
    print(key,len(obj['lines']), 'unique lines OK')
