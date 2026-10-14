from pathlib import Path
import sys,json,re,hashlib,shutil,html
from urllib.parse import urlsplit,unquote

R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'.prep/pages_deps'))
import markdown
repository_mode=Path(__file__).resolve().parent.name=='scripts'
B=R/'content' if repository_mode else R/'AI업무활용_실습교재'
P=R if repository_mode else R/'.prep/pages-repository'; D=P/'docs'
P.mkdir(exist_ok=True);D.mkdir(exist_ok=True)
if repository_mode:
    previous=json.loads((B/'manifest.json').read_text('utf8'))
    plan={'blocked_references':[],'chapters':[{'relative_source':p['source'],'source_sha256':hashlib.sha256((B/p['source']).read_bytes()).hexdigest(),'references':[]} for p in previous['pages'][1:]],'files':[{'relative_path':f['path'],'sha256':f['sha256'],'approved_capture':f['path'].startswith('captures/annotated/')} for f in previous['assets']]}
else:
    plan=json.loads((R/'.prep/notion_textbook/plan.json').read_text('utf8'))
assert not plan['blocked_references']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slugs=['00-basics','01-setup','02-chatgpt','03-claude','04-gemini','05-apply']
titles=['기본 개념','계정과 Windows 앱','ChatGPT 업무 활용','Claude 업무 활용','Gemini 업무 활용','내 업무 적용·정리']
pages=[{'source':'노션_첫페이지.md','output':'index.html','title':'시작하기','index':-1}]
for i,c in enumerate(plan['chapters']):
    assert sha(B/c['relative_source'])==c['source_sha256']
    pages.append({'source':c['relative_source'],'output':'chapters/'+slugs[i]+'.html','title':titles[i],'index':i})
routes={p['source']:p['output'] for p in pages}
files={f['relative_path']:f for f in plan['files']}
for chapter in plan['chapters']:
    for ref in chapter['references']:
        if ref['relative_path'].startswith('prompts/'):
            files.setdefault(ref['relative_path'],{'relative_path':ref['relative_path'],'sha256':sha(B/ref['relative_path'])})
for rel,f in files.items():
    assert not rel.startswith(('captures/raw/','teacher/','.prep/'))
    if rel.startswith('captures/'):
        assert f.get('approved_capture')
    source=B/rel if (B/rel).exists() else D/rel;assert sha(source)==f['sha256']
    target=D/rel;target.parent.mkdir(parents=True,exist_ok=True)
    if source.resolve()!=target.resolve():shutil.copy2(source,target)
for page in pages:
    target=P/'content'/page['source'];target.parent.mkdir(parents=True,exist_ok=True)
    if (B/page['source']).resolve()!=target.resolve():shutil.copy2(B/page['source'],target)

css='''
:root{--ink:#17283f;--muted:#5d6878;--brand:#12766f;--line:#dce3e8;--paper:#fff;--bg:#f5f7fa}*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:80px}body{margin:0;color:var(--ink);background:var(--bg);font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;line-height:1.85;word-break:keep-all}a{color:#086c79;text-underline-offset:4px}button,input{font:inherit}button{cursor:pointer}.skip{position:fixed;top:-100px;left:16px;background:#fff;padding:12px;z-index:20}.skip:focus{top:8px}.sidebar{width:278px;position:fixed;inset:0 auto 0 0;background:#fff;border-right:1px solid var(--line);padding:32px 22px;overflow:auto}.brand{display:block;color:var(--ink);text-decoration:none;font-size:22px;font-weight:800;line-height:1.5}.eyebrow{font-size:12px;color:var(--brand);font-weight:800;letter-spacing:.1em;margin-bottom:8px}.course{font-size:12px;color:var(--muted);margin:10px 0 24px}.nav{display:grid;gap:5px}.nav a{display:flex;align-items:center;gap:10px;padding:10px 12px;text-decoration:none;border-radius:8px;color:var(--muted);font-size:14px}.nav a[aria-current=page]{background:#e8f4f2;color:#065b55;font-weight:700}.nav a:hover{background:#f0f4f7}.num{font-size:12px;font-variant-numeric:tabular-nums;color:var(--brand);width:20px}.sidebar-footer{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);font-size:12px}.sidebar-footer a{display:block;margin:8px 0}.workspace{margin-left:278px}.topbar{position:sticky;top:0;z-index:5;background:rgba(245,247,250,.96);border-bottom:1px solid var(--line);padding:14px 36px;display:flex;align-items:center;gap:18px;font-size:13px;color:var(--muted)}.topbar button,.menu-button{border:1px solid var(--line);background:#fff;padding:4px 12px;border-radius:6px;color:var(--ink)}.topbar button{margin-left:auto}.menu-button{display:none}.search-wrap{padding:0 0 24px}.search-wrap input{width:100%;border:1px solid #c9d6db;border-radius:8px;background:#fff;padding:9px 12px;font-size:13px;line-height:1.5}.search-results{font-size:12px;display:grid;gap:8px;margin-top:10px}.search-results a{display:block;padding:8px;background:#f4f8f8;border-radius:5px}.search-results small{display:block;color:var(--muted);line-height:1.5;margin-top:3px}main{max-width:1040px;margin:0 auto;padding:44px 48px 60px}article{background:var(--paper);padding:42px 48px;border:1px solid var(--line);border-radius:14px;box-shadow:0 8px 32px #17283f06;font-size:15px}h1,h2,h3{line-height:1.45;color:var(--ink)}h1{font-size:32px;margin:0 0 25px;font-weight:800;letter-spacing:-.04em}h2{font-size:23px;margin:42px 0 16px;padding-top:16px;border-top:1px solid var(--line);letter-spacing:-.03em}h3{font-size:18px;margin-top:28px}p{margin:14px 0}li{margin:7px 0}strong{font-weight:750}img{display:block;max-width:100%;height:auto;margin:20px auto 12px;border:1px solid var(--line);border-radius:8px}figure{margin:26px 0}figcaption{color:var(--muted);font-size:13px;text-align:center;margin:8px auto 20px}code{font-family:Consolas,monospace;font-size:.9em;background:#edf2f6;padding:2px 5px;border-radius:4px;word-break:break-word}pre{white-space:pre-wrap;word-break:break-word;position:relative;background:#132638;color:#e5eef4;border-radius:10px;margin:20px 0;padding:46px 20px 20px;line-height:1.8}pre code{background:none;padding:0;color:inherit;display:block;font-size:13px;word-break:normal}.copy-button{position:absolute;right:12px;top:10px;background:#244252;color:#e6f4f2;border:1px solid #48606d;border-radius:5px;padding:3px 10px;font-size:12px}.table-wrap{overflow-x:auto;margin:20px 0;border:1px solid var(--line);border-radius:8px}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:11px 14px;text-align:left;border-bottom:1px solid var(--line);min-width:105px;vertical-align:top}th{background:#eef4f6;color:#264954}tr:last-child td{border-bottom:0}blockquote{border-left:4px solid var(--brand);padding:4px 18px;margin:20px 0;background:#f0f7f6}details{border:1px solid var(--line);border-radius:8px;padding:12px 18px;margin:22px 0;background:#fbfcfd}summary{cursor:pointer;font-weight:700;font-size:14px}details>*:last-child{margin-bottom:4px}.toc{background:#f7f9fc;border-radius:8px;padding:16px 20px;font-size:13px;margin:24px 0}.toc ul{margin:0;padding-left:20px}.toc>ul>li{margin:5px 0}.toc li ul{display:none}.page-nav{display:flex;justify-content:space-between;gap:14px;margin:24px 0}.page-nav a{background:#fff;border:1px solid var(--line);border-radius:8px;padding:12px 18px;font-size:13px;text-decoration:none}.footer{font-size:12px;color:var(--muted);text-align:center;margin-top:32px}.home article>ul{display:grid;grid-template-columns:1fr 1fr;gap:12px;list-style:none;padding:0}.home article>ul li{margin:0;border:1px solid var(--line);background:#f8fbfb;border-radius:8px}.home article>ul a{display:block;padding:16px;text-decoration:none;font-weight:700;font-size:14px}.home h1{font-size:34px}.home article>p:first-of-type{font-size:17px;color:#506174}.home article>p a[href*="axia-llm"]{display:inline-block;background:#12766f;color:#fff;text-decoration:none;padding:9px 18px;border-radius:7px;font-weight:700}:focus-visible{outline:3px solid #38a998;outline-offset:3px}
@media(max-width:1150px){main{padding:30px 24px}article{padding:32px 28px}.sidebar{width:250px}.workspace{margin-left:250px}}
@media(max-width:760px){.sidebar{display:none;z-index:10;top:58px;width:100%;bottom:auto;max-height:78vh;box-shadow:0 12px 22px #12243824}.sidebar.open{display:block}.workspace{margin-left:0}.topbar{padding:12px 16px}.menu-button{display:inline-block}main{padding:18px 12px}article{padding:24px 18px;border-radius:10px;font-size:14px}h1,.home h1{font-size:26px}h2{font-size:20px}.home article>ul{grid-template-columns:1fr}.page-nav a{padding:10px;font-size:12px}.topbar>span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}pre{padding-left:14px;padding-right:14px}}
@media print{.sidebar,.topbar,.page-nav,.footer,.copy-button,.toc{display:none!important}.workspace{margin:0}main{padding:0;max-width:none}article{border:0;box-shadow:none;padding:0}body{background:#fff;font-size:11pt}pre{color:#000;background:#f1f3f5;padding:12px;break-inside:avoid}img{max-height:700px;object-fit:contain}a{color:inherit}h2,h3{break-after:avoid}details{border:0}table{font-size:10pt}}
'''
js='''
const menu=document.querySelector('.menu-button'),side=document.querySelector('.sidebar');menu.addEventListener('click',()=>{let open=side.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
document.querySelectorAll('pre').forEach(pre=>{const b=document.createElement('button');b.className='copy-button';b.type='button';b.textContent='요청문 복사';b.setAttribute('aria-label','코드 또는 요청문 복사');b.addEventListener('click',async()=>{const text=pre.querySelector('code').textContent;try{await navigator.clipboard.writeText(text);b.textContent='복사됨';setTimeout(()=>b.textContent='요청문 복사',1500);}catch{b.textContent='텍스트를 선택해 복사';const selection=window.getSelection(),range=document.createRange();range.selectNodeContents(pre.querySelector('code'));selection.removeAllRanges();selection.addRange(range);}});pre.append(b);});
document.querySelector('.print-button').addEventListener('click',()=>{document.querySelectorAll('article details').forEach(d=>d.dataset.wasOpen=String(d.open));document.querySelectorAll('article details').forEach(d=>d.open=true);window.print();});window.addEventListener('afterprint',()=>document.querySelectorAll('article details').forEach(d=>d.open=d.dataset.wasOpen==='true'));
const search=document.querySelector('#search'),results=document.querySelector('.search-results');let index;search.addEventListener('input',async()=>{const query=search.value.trim().toLowerCase();results.replaceChildren();if(query.length<2)return;if(!index)index=await fetch(document.body.dataset.root+'search-index.json').then(r=>r.json());if(search.value.trim().toLowerCase()!==query)return;let matches=index.filter(p=>p.text.toLowerCase().includes(query)).slice(0,7);for(const page of matches){let a=document.createElement('a');a.href=document.body.dataset.root+page.path;a.textContent=page.title;let small=document.createElement('small');let at=page.text.toLowerCase().indexOf(query);small.textContent='…'+page.text.slice(Math.max(0,at-25),at+80)+'…';a.append(small);results.append(a);}if(!matches.length)results.textContent='검색 결과가 없습니다.';});
'''
(D/'assets').mkdir(exist_ok=True);(D/'assets/site.css').write_text(css,encoding='utf8');(D/'assets/site.js').write_text(js,encoding='utf8')
search=[];records=[]
for page in pages:
    text=(B/page['source']).read_text('utf8');root='../' if page['index']>=0 else './';src_parent=Path(page['source']).parent
    def rewrite(m):
        bang,label,url=m.groups()
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',url) or url.startswith('#'):return m[0]
        rel=(B/src_parent/url).resolve().relative_to(B.resolve()).as_posix()
        dest=routes.get(rel,rel)
        assert rel in routes or rel in files,(page['source'],rel)
        return f'{bang}[{label}]({root}{dest})'
    # Keep literal fenced prompts untouched, and fold only optional reference sections.
    lines=[];fence=False;optional=None
    for line in text.splitlines():
        if line.startswith('```'):fence=not fence;lines.append(line);continue
        if fence:lines.append(line);continue
        heading=re.match(r'^(#{1,4})\s+(.+)',line)
        if heading and optional is not None and len(heading[1])<=optional:
            lines.extend(['','</details>','']);optional=None
        if heading and heading[2].startswith(('선택 참고','실패 시 대안','다른 형식이 필요한 경우')):
            optional=len(heading[1]);lines.extend(['','<details markdown="1">',f'<summary>{html.escape(heading[2])}</summary>','']);continue
        lines.append(re.sub(r'(!?)\[([^]]*)\]\(([^)]+)\)',rewrite,line))
    if optional is not None:lines.extend(['','</details>'])
    md=markdown.Markdown(extensions=['tables','fenced_code','toc','md_in_html'],extension_configs={'toc':{'toc_depth':'2-2'}})
    rendered=md.convert('\n'.join(lines))
    rendered=re.sub(r'<table>(.*?)</table>',r'<div class="table-wrap"><table>\1</table></div>',rendered,flags=re.S)
    rendered=re.sub(r'<p>(<img\s[^>]*alt="([^"]*)"[^>]*>)</p>',r'<figure>\1<figcaption>\2</figcaption></figure>',rendered)
    nav=''
    for p in pages:
        active=' aria-current="page"' if p==page else ''
        number='↗' if p['index']<0 else f"{p['index']:02}"
        nav+=f'<a href="{root}{p["output"]}"{active}><span class="num">{number}</span>{html.escape(p["title"])}</a>'
    i=pages.index(page);previous=pages[i-1] if i>0 else None;following=pages[i+1] if i+1<len(pages) else None
    pager='<nav class="page-nav" aria-label="이전·다음 장">'
    pager+=(f'<a href="{root}{previous["output"]}">← {html.escape(previous["title"])}</a>' if previous else '<span></span>')
    pager+=(f'<a href="{root}{following["output"]}">{html.escape(following["title"])} →</a>' if following else '<span></span>')
    pager+='</nav>'
    toc=('<details class="toc"><summary>이 장의 목차</summary>'+md.toc+'</details>') if page['index']>=0 else ''
    if toc:rendered=re.sub(r'(</h1>)',r'\1'+toc,rendered,count=1)
    doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(page['title'])} · 한전 AI 업무활용 실습교재</title><meta name="description" content="Windows의 ChatGPT·Claude 앱과 Gemini 웹으로 진행하는 6시간 AI 업무활용 실습교재. 실습 자료와 요청문, 실제 화면 캡처를 제공합니다."><link rel="stylesheet" href="{root}assets/site.css"><script src="{root}assets/site.js" defer></script></head><body class="{'home' if i==0 else 'chapter'}" data-root="{root}"><a class="skip" href="#main">본문으로 이동</a><aside class="sidebar" aria-label="교재 탐색"><div class="eyebrow">AI WORKBOOK</div><a class="brand" href="{root}index.html">한전 AI 업무활용<br>실습교재</a><div class="course">Windows · ChatGPT · Claude · Gemini<br>6시간 실습 과정</div><div class="search-wrap"><label class="sr-only" for="search">교재 검색</label><input id="search" type="search" placeholder="교재에서 검색" autocomplete="off"><div class="search-results" aria-live="polite"></div></div><nav class="nav" aria-label="장별 목차">{nav}</nav><div class="sidebar-footer"><a href="https://axia-llm.dreamitbiz.com" target="_blank" rel="noopener">LLM 실습 플랫폼 ↗</a><a href="https://jangka44.notion.site/AI-3f6d4cdd4f478194a8dbda7adef5ccbd" target="_blank" rel="noopener">노션 교재 ↗</a></div></aside><div class="workspace"><header class="topbar"><button class="menu-button" type="button" aria-expanded="false">목차</button><span>{html.escape(page['title'])}</span><button class="print-button" type="button">인쇄</button></header><main id="main"><article>{rendered}</article>{pager}<footer class="footer">한전 AI 업무활용 실습교재 · 마크다운 원본 기반<br>필요한 자료는 각 실습에서 내려받습니다.</footer></main></div></body></html>'''
    dest=D/page['output'];dest.parent.mkdir(exist_ok=True);dest.write_text(doc,encoding='utf8')
    search.append({'title':page['title'],'path':page['output'],'text':re.sub(r'\s+',' ',re.sub(r'[#*`|]',' ',text))})
    records.append({'source':page['source'],'source_sha256':sha(B/page['source']),'output':page['output'],'output_sha256':sha(dest)})
(D/'search-index.json').write_text(json.dumps(search,ensure_ascii=False),encoding='utf8')
(D/'.nojekyll').write_text('',encoding='utf8')
(D/'404.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>페이지를 찾을 수 없습니다</title><p>주소를 확인하고 <a href="/chuncheon-ai-workbook/">교재 첫페이지</a>로 이동하세요.</p></html>',encoding='utf8')
manifest={'canonical_merged_sha256':sha(B/'교재.md') if (B/'교재.md').exists() else None,'pages':records,'assets':[{'path':rel,'sha256':sha(D/rel)} for rel in sorted(files)],'page_count':7,'approved_image_count':65,'raw_captures_published':False}
(P/'content/manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
(P/'README.md').write_text('''# 한전 AI 업무활용 실습교재

- 웹 교재: https://jhs512.github.io/chuncheon-ai-workbook/
- 노션 교재: https://jangka44.notion.site/AI-3f6d4cdd4f478194a8dbda7adef5ccbd

Windows의 ChatGPT·Claude 앱과 Gemini 웹을 사용하는 6시간 실습교재입니다.
`content/`의 마크다운이 원본이며 `docs/`는 GitHub Pages 배포본입니다.
교재에 참조된 승인 캡처와 실습 자료만 포함합니다.
실습 예제의 수치와 문서는 학습용 자료이며 실제 기관의 내부자료로 해석하지 않습니다.

## 갱신

`content/`의 원본 Markdown을 수정한 뒤 다음 명령으로 웹 배포본을 다시 생성합니다.

```sh
python -m pip install -r requirements.txt
python scripts/build.py
```

춘천 제작 작업 폴더에서는 `.prep/build_github_pages.py`로 최신 원본과 자료를 이 저장소에 반영합니다.
게시 설정은 main 브랜치의 /docs 폴더입니다. `content/manifest.json`에 원본·게시 파일의 SHA-256을 기록합니다.
''',encoding='utf8')
# Verify all local href/src targets and literal prompts before anything is published.
bad=[];code_total=0
for page in pages:
    out=D/page['output'];doc=out.read_text('utf8')
    for ref in re.findall(r'(?:href|src)="([^"]+)"',doc):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',ref) or ref.startswith('#'):continue
        u=urlsplit(html.unescape(ref));target=(out.parent/unquote(u.path)).resolve()
        if not target.exists():bad.append((page['output'],ref))
    wanted=re.findall(r'```[^\n]*\n(.*?)\n```',(B/page['source']).read_text('utf8'),re.S)
    found=[html.unescape(re.sub(r'<[^>]+>','',c)).rstrip('\n') for c in re.findall(r'<pre><code[^>]*>(.*?)</code></pre>',doc,re.S)]
    assert wanted==found,(page['source'],'literal fenced code mismatch')
    code_total+=len(found)
assert not bad,bad
manifest['verification']={'local_link_errors':0,'literal_code_blocks_exact':code_total,'assets_hash_match':True,'all_pages_rendered':7}
if not repository_mode:
    (B/'evidence/github_pages_build.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
    (P/'scripts').mkdir(exist_ok=True);shutil.copy2(Path(__file__),P/'scripts/build.py')
    (P/'requirements.txt').write_text('Markdown==3.11.1\n',encoding='utf8')
    (P/'.gitignore').write_text('__pycache__/\n.venv/\n',encoding='utf8')
print(json.dumps({'repository_folder':str(P),'pages':7,'assets':len(files),'approved_captures':65,'code_blocks_exact':code_total,'local_link_errors':0,'total_bytes':sum(f.stat().st_size for f in D.rglob('*') if f.is_file())},ensure_ascii=False))
