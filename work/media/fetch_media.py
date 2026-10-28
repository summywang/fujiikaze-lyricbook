import json,re,pathlib,urllib.request,urllib.parse,html,concurrent.futures
ROOT=pathlib.Path('/Users/SummyWang/Documents/Codex/2026-10-28/clo/work/media-research')
refs={html.unescape(name):url for url,name in re.findall(r'<a href="(https://open.spotify.com/track/[^"]+)" target="_blank">([^<]+)</a>',(ROOT/'kworb.html').read_text())}
entries=[('casket-girl','Casket Girl'),('its-alright',"It's Alright"),('i-need-u-back','I Need U Back'),('nan-nan','Nan-Nan'),('shinunoga-e-wa','Shinunoga E-Wa'),('garden','Garden'),('kirari','Kirari'),('hana','Hana'),('it-aint-over',"It Ain't Over"),('love-like-this','Love Like This'),('you','You'),('workin-hard',"Workin' Hard"),('damn','damn'),('tabiji','Tabiji'),('michi-teyu-ku','満ちてゆく'),('prema','Prema'),('okay-goodbye','Okay, Goodbye'),('matsuri','Matsuri'),('hachiko','Hachikō'),('forever-young','Forever Young'),('masshiro','真っ白')]
def get(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as r:return r.read().decode()
def fetch(pair):
 key,name=pair;url=refs[name];trackid=url.rsplit('/',1)[1]
 oeurl='https://open.spotify.com/oembed?url='+urllib.parse.quote(url,safe='')
 oe=json.loads(get(oeurl)); emburl='https://open.spotify.com/embed/track/'+trackid
 page=get(emburl);m=re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',page)
 entity=json.loads(m.group(1))['props']['pageProps']['state']['data']['entity']
 assert any(a['uri']=='spotify:artist:6bDWAcdtVR3WHz2xtiIPUi' for a in entity['artists']),entity.get('artists')
 assert entity['title'].casefold()==name.casefold(),(name,entity['title'])
 imgs=entity['visualIdentity']['image'];cover=max(imgs,key=lambda i:i['maxWidth'])['url']
 sanitized={k:entity[k] for k in ['id','title','artists','releaseDate','duration','visualIdentity']}
 (ROOT/(key+'-spotify.json')).write_text(json.dumps({'oembed':oe,'entity':sanitized},ensure_ascii=False,indent=2))
 return key,{'spotify':url,'spotifyTrackId':trackid,'artist':'Fujii Kaze','title':entity['title'],'coverUrl':cover,'thumbnailUrl':oe['thumbnail_url'],'coverSource':'Spotify','coverSourceUrl':url,'releaseDate':entity['releaseDate']['isoString'][:10],'durationMs':entity['duration'],'verifiedAt':'2026-10-28','provenance':[oeurl,emburl]}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 results=dict(pool.map(fetch,entries))
(ROOT/'media-map.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'count':len(results),'tracks':[{ 'key':k,'title':v['title'],'releaseDate':v['releaseDate']} for k,v in results.items()]},ensure_ascii=False,indent=2))
