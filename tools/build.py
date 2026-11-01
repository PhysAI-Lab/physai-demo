"""Build the PhysAI static website. Python standard library only."""
import json, re, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'data/publications.json').read_text(encoding='utf-8'))
MEDIA=json.loads((ROOT/'data/media-map.json').read_text(encoding='utf-8')) if (ROOT/'data/media-map.json').exists() else {}
def local(src):return MEDIA.get(src,src)
def e(s):return html.escape(str(s),quote=True)
def find(prefix):return next(p for p in P if p['title'].lower().startswith(prefix.lower()))
def a(url,label,cls=''):
 return f'<a href="{e(url)}"'+(f' class="{cls}"' if cls else '')+'>'+label+'</a>'
def plinks(p):return ''.join(a(u,e(k)) for k,u in p['links'].items())
def thumb(p,cls='',priority=False):
 src=p.get('image') or p.get('poster')
 return f'<img class="{cls}" src="{e(local(src))}" alt="{e(p["title"])} — research result" '+('fetchpriority="high"' if priority else 'loading="lazy"')+' decoding="async">' if src else '<div class="media-placeholder" aria-hidden="true"></div>'
def button(p,label='Watch demo',cls=''):
 media=p.get('video') or p.get('image')
 if not media:return ''
 kind='video' if p.get('video') else 'image'
 return f'<button class="{cls}" data-media="{e(media)}" data-kind="{kind}" data-title="{e(p["title"])}" data-project="{e(p["links"].get("Project",p["links"].get("Paper","")))}">{label}</button>'
PEOPLE=[
 dict(name='Caoliwen Wang',role='PhD student',area='World models · Physical AI',url='https://wclw1021.github.io/',photo='https://wclw1021.github.io/assets/img/prof_pic.jpg',source='https://wclw1021.github.io/'),
 dict(name='Siyuan Chen',role='PhD student',area='Neural simulation · Biomolecular modeling',url='https://chensiyuan030105.github.io/',photo='',source='https://chensiyuan030105.github.io/about/'),
 dict(name='Heng Zhang',role='PhD student · co-advised with Chao Liu',area='Robotics · Differentiable simulation',url='https://peterchencyc.com/joining',photo='',source='https://peterchencyc.com/joining'),
 dict(name='Weijia Zeng',role='PhD student · co-advised with Kwang Moo Yi',area='3D vision · Graphics',url='https://www.cs.ubc.ca/~kmyi/team/',photo='',source='https://www.cs.ubc.ca/~kmyi/team/'),
 dict(name='Xiyang Tan',role='PhD student · co-advised with Kwang Moo Yi',area='Generative AI · Physics-based simulation',url='https://supertan0204.github.io/',photo='https://supertan0204.github.io/images/xiyang.jpg',source='https://peterchencyc.com/joining'),
 dict(name='Shixun Huang',role='PhD student',area='Physics AI · Model reduction',url='https://alessange.github.io/',photo='https://alessange.github.io/images/profile/shixun_huang_grad_profile.png',source='https://alessange.github.io/'),
 dict(name='Qianjun Xia',role='PhD student',area='Robotics · Physical intelligence',url='https://qianjun-xia.github.io/',photo='',source='https://qianjun-xia.github.io/about/'),
 dict(name='Guanxiong Chen',role='PhD student · co-advised with Chao Liu',area='Deformable simulation · Robot manipulation',url='https://www.cs.ubc.ca/~gxchen/',photo='https://www.cs.ubc.ca/~gxchen/images/profile_2024-04-10.jpg',source='https://www.cs.ubc.ca/~gxchen/'),
]
INCOMING=[
 dict(name='Zhenyi Wang',role='Incoming PhD student',area='',url='',photo='',source='Lab-provided roster update, 2026-11-01',source_type='lab-provided',publications=False),
 dict(name='Shenyifan Lu',role='Incoming PhD student',area='',url='',photo='',source='Lab-provided roster update, 2026-11-01',source_type='lab-provided',publications=False),
]
MASTERS=[
 dict(name='Ziyi Jiao',role='Master’s student',area='',url='',photo='',source='Lab-provided roster update, 2026-11-01',source_type='lab-provided'),
]
POSTDOCS=[
 dict(name='Mengdi Wang',role='Postdoctoral fellow',area='Physical simulation · World models · GPU solvers',url='https://wang-mengdi.github.io/',photo='https://wang-mengdi.github.io/assets/img/mengdi.jpg',source='https://wang-mengdi.github.io/'),
]
VISITORS=[
 dict(name='Yiwen Chen',role='Visiting undergraduate student',area='',url='',photo='',source='Lab-provided roster update, 2026-11-01',source_type='lab-provided',publications=False),
 dict(name='Baiming Zhang',role='Visiting International Research Student · Oct 2026–Jan 2027 (expected)',area='Zhejiang University undergraduate · Scientific machine learning',url='https://baiming-zhang.github.io/',photo='https://baiming-zhang.github.io/images/my-pic.jpg',source='https://baiming-zhang.github.io/',publications=False),
]
roster=[dict(p,category=category) for category,group in [('doctoral',PEOPLE),('postdoctoral',POSTDOCS),('incoming-doctoral',INCOMING),('masters',MASTERS),('visiting',VISITORS)] for p in group]
(ROOT/'data/people.json').write_text(json.dumps(roster,ensure_ascii=False,indent=2),encoding='utf-8')
def member_name(p):
 return a(p['url'],e(p['name'])) if p.get('url') else '<span class="member-name">'+e(p['name'])+'</span>'

def person(p,mini=False):
 initials=''.join(s[0] for s in p['name'].split())
 portrait=f'<img src="{e(local(p["photo"]))}" alt="{e(p["name"])}" loading="lazy">' if p['photo'] else f'<div class="initials" aria-hidden="true">{initials}</div>'
 portrait=a(p['url'],portrait,'portrait') if p.get('url') else '<div class="portrait">'+portrait+'</div>'
 name=a(p['url'],e(p['name'])+' ↗') if p.get('url') else e(p['name'])
 area='<p>'+e(p['area'])+'</p>' if p.get('area') else ''
 work=''
 if p.get('publications',True):work=a('publications.html?author='+p['name'].replace(' ','%20'),'Publications ↗','person-work')
 elif p.get('url'):work=a(p['url'],'Research profile ↗','person-work')
 return f'<article class="person">{portrait}<h3>{name}</h3><p class="person-role">{e(p["role"])}</p>{area}{work}</article>'
NAV=[('index.html','Home'),('research.html','Research'),('publications.html','Publications'),('demos.html','Demos'),('people.html','People'),('news.html','News'),('join.html','Join')]
def layout(page,title,body,description):
 nav=''.join(f'<a href="{url}"'+(' aria-current="page"' if page==url else '')+'>'+name+'</a>' for url,name in NAV)
 brand='<span class="brand-name">PhysAI Lab</span><span class="brand-at">at UBC</span>'
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)} | PhysAI Lab · UBC</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#fafaf7"><meta property="og:title" content="{e(title)} | PhysAI Lab · UBC"><meta property="og:description" content="{e(description)}"><meta property="og:type" content="website"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/fonts.css?v=team-4"><link rel="stylesheet" href="assets/site.css?v=team-4"><script src="assets/site.js?v=team-4" defer></script></head><body data-page="{page.removesuffix('.html')}"><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="container header-inner"><a class="brand" href="index.html" aria-label="PhysAI Lab home">{brand}</a><button class="menu-toggle" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">＋</span></button><nav id="site-nav" aria-label="Main navigation">{nav}</nav></div></header><main id="main">{body}</main><footer class="site-footer"><div class="container footer-grid"><div><a class="brand" href="index.html">{brand}</a><p>Department of Computer Science<br>University of British Columbia<br>Vancouver, Canada</p></div><div><h2>Pages</h2><a href="research.html">Research</a><a href="publications.html">Publications</a><a href="people.html">People</a><a href="join.html">Join the lab</a></div><div><h2>Contact</h2><a href="mailto:peter.chen@ubc.ca">peter.chen@ubc.ca</a><a href="https://www.cs.ubc.ca/people/peter-yichen-chen">UBC faculty profile</a><a href="https://peterchencyc.com/">Peter’s website</a><a href="https://scholar.google.com/citations?user=9TX3RmEAAAAJ">Google Scholar</a></div></div><div class="container footer-bottom"><span>© 2026 PhysAI Lab</span><span>Research media courtesy of the linked projects and authors.</span><a href="https://github.com/chensiyuan030105/physai-demo">Website source</a></div></footer><dialog id="media-dialog" aria-labelledby="media-title"><div class="dialog-head"><p id="media-title"></p><button id="close-dialog" aria-label="Close preview">Close ×</button></div><div id="media-content"></div><div class="dialog-bottom"><span>Research demo · media from the project authors</span><a id="media-project">Open source project ↗</a></div></dialog></body></html>'''
def page_intro(label,title,desc):return f'<div class="container page-intro"><p class="eyebrow">{label}</p><h1>{title}</h1><p class="lede">{desc}</p></div>'
def section_head(label,title,link='',url=''):
 return f'<div class="section-head"><div><p class="eyebrow">{label}</p><h2>{title}</h2></div>'+(a(url,link+' ↗','text-link') if url else '')+'</div>'
SUMMARIES={
 'WorldParticle':'One Transformer architecture spanning fluids, cloth, solids, granular materials, and molecular dynamics.',
 'WorldAgent':'A verification-guided agent that constructs and checks physically simulatable worlds.',
 'WorldContact':'Contact-centric deformable world modeling for robot learning.',
 'DiagGen':'Agentic deformable-asset generation with simulation-based diagnostics and repair.',
 'Agentic Real2Sim':'Recovering physics-based worlds from real interaction using vision-language agents.',
 'Closing Trajectories':'Equation-free cyclic animation through learned Koopman surrogates.',
 'Shape Space Spectra':'Eigenanalysis across continuously parameterized shape families for simulation and design.',
 'Lifting the Winding':'Neural fields that represent precise cuts and discontinuities for physics simulation.',
 'NeuralActuator':'Learned actuator dynamics for robot simulation and sensorless force perception.',
 'Physically Valid Biomolecular':'Differentiable Gauss–Seidel projection for physically valid biomolecular structures.',
 'From Surfaces':'Registered volumetric geometry for protein representation learning.',
 'Fast Subspace Fluid':'A temporally-aware reduced basis for fast fluid simulation.',
 'Efficient Open-Boundary':'Open-boundary field solving, illustrated with ferrofluid dynamics.',
}
for p in P:
 for prefix,desc in SUMMARIES.items():
  if p['title'].startswith(prefix):p['summary']=desc

awards=[('SIGGRAPH 2025','Best Paper Award','Shape Space Spectra','https://www.dgp.toronto.edu/projects/sss/'),('SIGGRAPH 2025','Best Paper Honorable Mention','Lifting the Winding Number','https://www.dgp.toronto.edu/projects/windlifter/'),('RSS 2026','Outstanding Systems Paper','NeuralActuator','https://frank-zy-dou.github.io/projects/NeuralActuator/'),('SCA 2026','Early Career Researcher Award','Peter Yichen Chen','https://www.cs.ubc.ca/news/2026/07/dr-chen-ecr-sca')]
def award_grid():return '<div class="award-grid">'+''.join(a(u,f'<span class="eyebrow">{venue}</span><strong>{award}</strong><small>{work} ↗</small>','award') for venue,award,work,u in awards)+'</div>'
RESEARCH=[
 ('02','Neural simulation','How can learned models retain the structure of physics?','We combine numerical methods and neural representations to simulate physical dynamics efficiently, across materials, geometries, and discretizations.',['WorldParticle','Closing Trajectories','Fast Subspace Fluid','Neural Monte Carlo','CROM'], 'simulation'),
 ('01','Robotics and world models','How can AI turn observation into a simulatable world?','We connect robot interaction, actuation modeling, and physical world construction to simulation and robot learning.',['NeuralActuator','Agentic Real2Sim','WorldContact','DiagGen','WorldAgent'],'world-models'),
 ('03','Geometry and scientific computing','How can physical structure guide generation and design?','We develop geometric representations and optimization tools for physical constraints, computational design, and scientific computing.',['Shape Space Spectra','Lifting the Winding','AI-Enhanced Automatic','Physically Valid Biomolecular','From Surfaces'],'science'),
]
RESEARCH.sort(key=lambda direction:direction[0])
NEWS=[
 ('2026-09','Publications','September research releases','New papers include WorldParticle, WorldAgent, WorldContact, DiagGen, and Agentic Real2Sim.','publications.html?year=2026'),
 ('2026-07-17','Award','NeuralActuator receives the RSS Outstanding Systems Paper Award','Collaborative research on actuation modeling for robot dynamics and external-force perception.','https://cdfg.mit.edu/news/#neuralactuator-wins-outstanding-systems-paper-in-memory-of-seth'),
 ('2026-07-08','Recognition','Peter receives the SCA Early Career Researcher Award','Recognizing his contributions to computer animation and physics simulation.','https://www.cs.ubc.ca/news/2026/07/dr-chen-ecr-sca'),
 ('2026-01-13','UBC profile','Physics and AI for real-world computer simulations','UBC introduces Peter and his interdisciplinary research spanning art, engineering, and science.','https://www.cs.ubc.ca/news/2026/01/new-faculty-dr-peter-yichen-chen'),
 ('2025-08','Awards','Two SIGGRAPH research distinctions','Shape Space Spectra wins Best Paper; Lifting the Winding Number receives an Honorable Mention.','https://www.cs.ubc.ca/news/2025/08/ubc-computer-science-researchers-win-multiple-best-paper-awards-siggraph-conference-and-symposium'),
]
def news_rows(items):return ''.join(f'<article class="news-row"><time datetime="{date}">{date}</time><div><span class="eyebrow">{tag}</span><h3>{a(url,title)}</h3><p>{desc}</p></div></article>' for date,tag,title,desc,url in items)
def editorial_project(prefix):
 p=find(prefix)
 authors=p['authors']
 if len(authors)>170:authors=authors[:authors.rfind(',',0,150)]+', et al.'
 award=f'<span class="inline-award">{e(p["award"])}</span>' if p.get('award') else ''
 return f'<article class="selected-project"><div class="selected-visual">{thumb(p)}{button(p,"View research film" if p.get("video") else "View result","view-research")}</div><div class="selected-text"><p class="project-meta">{e(p["venue"])} {award}</p><h3>{a("publications.html#"+p["id"],e(p["title"]))}</h3><p class="authors">{e(authors)}</p><p>{e(p.get("summary",""))}</p><div class="resource-links">{plinks(p)}</div></div></article>'
def recent_paper(prefix):
 p=find(prefix);target=p['links'].get('Project') or p['links'].get('Paper')
 return f'<article class="recent-paper"><span>{p["year"]}</span><div><h3>{a(target,e(p["title"]))}</h3><p>{e(p["venue"])}</p></div><a href="publications.html#{p["id"]}" aria-label="Details for {e(p["title"])}">Details</a></article>'
robotics=find('Agentic Real2Sim')
hero=dict(robotics,image='https://www.cs.ubc.ca/~gxchen/images/agentic_real2sim.png')
home=f'''<section class="lab-hero"><div class="container lab-hero-inner"><div class="lab-introduction"><p class="eyebrow">University of British Columbia</p><h1>PhysAI Lab</h1><p class="lab-subtitle">Robotics, simulation<br>and physical AI.</p><p class="lab-description">We study how robots can model and interact with the physical world, led by <a href="people.html#peter">Peter Yichen Chen</a> at UBC Computer Science.</p><div class="lab-links"><a href="research.html">Our research</a><a href="people.html">People</a></div></div><figure class="lab-figure"><div class="lab-figure-image">{thumb(hero,priority=True)}</div><figcaption><a href="publications.html#{robotics['id']}">Agentic Real2Sim</a><span>Robot interaction → physical world models · 2026</span>{button(robotics,'View film','figure-film')}</figcaption></figure></div></section>
<div class="affiliation-line"><div class="container"><span>UBC Computer Science</span><a href="https://caida.ubc.ca/aim-si">AI4Science</a><a href="https://www.iam.ubc.ca/">Institute of Applied Mathematics</a></div></div>
<section class="container introduction-section"><h2>Research at PhysAI</h2><div><p>We develop simulation and learning methods for robotics: recovering physical properties from interaction, modeling actuation and contact, and constructing worlds in which robots can learn.</p><p>Our work spans robot manipulation, Real2Sim, and contact-aware world models, supported by research in neural simulation, geometry, and scientific computing.</p></div></section>
<section class="container research-briefs"><p class="eyebrow">Research areas</p><div class="research-columns">{''.join(f'<article><h3>{a("research.html#"+slug,name)}</h3><p>{desc}</p></article>' for num,name,q,desc,ps,slug in RESEARCH)}</div></section>
<section class="container section selected-section">{section_head('Selected research','Selected research','All publications','publications.html')}{''.join(editorial_project(x) for x in ['NeuralActuator','Agentic Real2Sim','WorldContact'])}</section>
<section class="container section recent-section">{section_head('Recent work','Recent publications','Publication archive','publications.html')}{''.join(recent_paper(x) for x in ['WorldAgent','DiagGen','BoxTwin','WorldParticle','Learning Object Properties'])}</section>
<section class="container section home-news">{section_head('News','News','All news','news.html')}{news_rows(NEWS[1:4])}</section>
<section class="container section home-people">{section_head('People','The group','People & profiles','people.html')}<div class="home-group"><div class="home-pi"><img src="https://peterchencyc.com/assets/img/prof_pic.jpg" alt="Peter Yichen Chen" loading="lazy"><div><a href="people.html#peter">Peter Yichen Chen</a><p>Principal investigator<br>Assistant Professor, Computer Science</p></div></div><div class="home-members"><p class="eyebrow">Postdoctoral researchers</p><div>{''.join(member_name(p) for p in POSTDOCS)}</div><p class="eyebrow">Doctoral researchers</p><div>{''.join(member_name(p) for p in PEOPLE)}</div><p class="eyebrow">Incoming PhD students</p><div>{''.join(member_name(p) for p in INCOMING)}</div><p class="eyebrow">Master’s students</p><div>{''.join(member_name(p) for p in MASTERS)}</div><p class="eyebrow">Visiting students</p><div>{''.join(member_name(p) for p in VISITORS)}</div></div></div></section>
<section class="container home-joining"><h2>Join the lab</h2><p>We welcome enquiries from prospective graduate students, postdoctoral researchers, and collaborators. <a href="join.html">Application and contact information →</a></p></section>'''
(ROOT/'index.html').write_text(layout('index.html','Home',home,'PhysAI Lab at the University of British Columbia, led by Peter Yichen Chen. Research in robotics, physical world models, and physics simulation.'),encoding='utf-8')

research=page_intro('PhysAI Lab','Research','We study robot manipulation and physical world modeling through simulation and machine learning.')
for num,name,q,desc,ps,slug in RESEARCH:
 research+=f'<section class="container section research-detail" id="{slug}"><div class="research-heading"><p class="eyebrow">{num} / Research direction</p><h2>{name}</h2><p>{desc}</p></div><div class="direction-projects">'+''.join(f'<article><div>{thumb(find(prefix))}</div><div><p class="eyebrow">{e(find(prefix)["venue"])}</p><h3>{a("publications.html#"+find(prefix)["id"],e(find(prefix)["title"]))}</h3><p>{e(find(prefix).get("summary",""))}</p><div class="resource-links">{plinks(find(prefix))}</div></div></article>' for prefix in ps)+'</div></section>'
research+='<div class="container research-context"><p class="eyebrow">A connected research community</p><h2>Research community</h2><p>Our work connects visual computing, mechanics, scientific machine learning, and robotics. Peter is affiliated with UBC’s <a href="https://caida.ubc.ca/aim-si">AI4Science community</a> and <a href="https://www.iam.ubc.ca/">Institute of Applied Mathematics</a>.</p><p>Peter and his collaborators also work with industry on simulation challenges. Learn more about these collaborations on <a href="https://peterchencyc.com/">Peter’s research profile ↗</a>.</p></div>'
(ROOT/'research.html').write_text(layout('research.html','Research',research,'Neural simulation, physical world models, robotics, geometry, and AI for science at UBC PhysAI Lab.'),encoding='utf-8')

def paper_row(p):
 authors=e(p['authors'])
 for name in ['Peter Yichen Chen']+[p['name'] for p in PEOPLE+POSTDOCS+INCOMING+MASTERS]:authors=authors.replace(e(name),f'<strong>{e(name)}</strong>')
 badge=f'<span class="award-badge">{e(p["award"])}</span>' if p.get('award') else ''
 meta={'year':str(p['year']),'topic':p['topic'],'status':p['status'],'scope':p['scope'],'search':p['title']+' '+p['authors']+' '+p['venue']}
 attrs=' '.join(f'data-{k}="{e(v)}"' for k,v in meta.items())
 target=p['links'].get('Project') or p['links'].get('Paper') or p['links'].get('PDF') or '#'+p['id']
 return f'''<article class="paper-row" id="{p['id']}" {attrs}><a class="paper-thumb" href="{e(target)}">{thumb(p)}</a><div class="paper-body"><p class="paper-venue">{e(p['venue'])} {badge}</p><h2>{a(target,e(p['title']))}</h2><p class="paper-authors">{authors}</p><div class="paper-tags"><span>{e(p['status'])}</span><span>{e(p['scope'])}</span></div><div class="resource-links">{plinks(p)}<button data-bib="{p['id']}">BibTeX</button><a href="#{p['id']}" aria-label="Permanent link to {e(p['title'])}">Permalink ↗</a></div></div></article>'''
def select(name,label,values):return f'<label>{label}<select name="{name}" id="filter-{name}"><option value="">All {label.lower()}</option>'+''.join(f'<option value="{e(v)}">{e(v)}</option>' for v in values)+'</select></label>'
pubs=page_intro('PhysAI Lab','Publications','Research by Peter and PhysAI members, with collaborators across institutions. Includes earlier affiliations and members’ independent collaborations.')
pubs+=f'<div class="container"><form class="filters" id="publication-filters" role="search"><label class="search-label">Search papers<input name="q" id="paper-search" type="search" placeholder="Title, author, venue, or keyword…"></label><div class="filter-row">{select("year","Years",sorted({str(p["year"]) for p in P},reverse=True))}{select("topic","Topics",sorted({p["topic"] for p in P}))}{select("status","Statuses",["Published / accepted","Preprint"])}{select("scope","Collections",["Peter + collaborators","Member collaborations"])}<button type="reset" class="reset">Reset filters ↺</button></div></form><div class="results-bar"><span id="result-count" role="status">{len(P)} publications</span><span>* Equal contribution · † Corresponding author</span></div><div id="papers">'+''.join(paper_row(p) for p in P)+'</div><div id="no-results" hidden><h2>No matching papers.</h2><p>Try a different author, keyword, or filter.</p><button class="button" id="clear-search">Clear all filters</button></div><p class="collection-note">Publication details are drawn from author and project pages. Accepted papers and preprints are labeled separately. This collection includes work undertaken before members joined UBC.</p></div>'
(ROOT/'publications.html').write_text(layout('publications.html','Publications',pubs,'Explore publications by Peter Yichen Chen and PhysAI Lab members. Search papers, preprints, project pages, code, videos, and citations.'),encoding='utf-8')

demo_prefixes=['Agentic Real2Sim','NeuralActuator','WorldContact','DiagGen','WorldAgent','WorldParticle','Closing Trajectories','Fast Subspace Fluid','Efficient Open-Boundary','Shape Space Spectra','Lifting the Winding','Physically Valid Biomolecular','From Surfaces']
demos=page_intro('Research resources','Demos','Real research results, project films, and open resources. Play a preview or open the full project to explore the methods and experiments.')
demos+='<div class="container"><div class="demo-filters" role="group" aria-label="Filter research demos">'+''.join(f'<button data-demo-filter="{value}" aria-pressed="{str(not value).lower()}">{label}</button>' for value,label in [('','All projects'),('Simulation','Simulation'),('Robotics','Robotics'),('Geometry & Design','Geometry & design'),('AI for Science','AI for science')])+'</div><div class="demo-grid">'
for prefix in demo_prefixes:
 p=find(prefix);media=thumb(p);play=button(p,'▶ Play video' if p.get('video') else ('▶ Play animation' if '.gif' in p.get('image','') else '↗ View result'),'preview-button')
 demos+=f'<article class="demo-card" data-demo-topic="{p["topic"]}"><div class="demo-media">{media}{play}</div><div class="demo-body"><p class="eyebrow">{e(p["venue"])}</p><h2>{e(p["title"].split(":")[0])}</h2><p>{e(p.get("summary",""))}</p><div class="resource-links">{plinks(p)}</div><a class="demo-detail" href="publications.html#{p["id"]}">Authors & publication ↗</a></div></article>'
demos+='</div><p class="collection-note">Previews show results from the linked research projects. Full videos, code, and interactive resources are provided where publicly released by the authors.</p></div>'
(ROOT/'demos.html').write_text(layout('demos.html','Demos',demos,'Watch robotics, physical world modeling, and simulation research demos from Peter Yichen Chen and the UBC PhysAI Lab.'),encoding='utf-8')

people=page_intro('PhysAI Lab','People','An interdisciplinary group working across physics, graphics, machine learning, and robotics at the University of British Columbia.')
people+='''<section class="container pi-section" id="peter"><p class="eyebrow">Principal investigator</p><div class="pi-profile"><img src="https://peterchencyc.com/assets/img/prof_pic.jpg" alt="Peter Yichen Chen"><div><h2>Peter Yichen Chen</h2><p class="pi-title">Assistant Professor · UBC Computer Science</p><p>Peter leads PhysAI Lab, developing physical simulators at the intersection of computer graphics, machine learning, scientific computing, and robotics. His research connects efficient computation with applications in science, engineering, and 3D content creation.</p><div class="education"><span>Postdoc · MIT CSAIL</span><span>PhD · Columbia University</span><span>BS · UCLA</span></div><div class="resource-links"><a href="https://peterchencyc.com/">Personal website ↗</a><a href="https://www.cs.ubc.ca/people/peter-yichen-chen">UBC profile ↗</a><a href="mailto:peter.chen@ubc.ca">Email ↗</a><a href="publications.html?author=Peter%20Yichen%20Chen">Publications ↗</a></div></div></div></section>'''
people+='<section class="container section" id="postdocs">'+section_head('Postdoctoral research','Postdoctoral researchers')+'<div class="people-grid">'+''.join(person(p) for p in POSTDOCS)+'</div></section>'
people+='<section class="container section">'+section_head('Doctoral researchers','Doctoral students')+'<div class="people-grid">'+''.join(person(p) for p in PEOPLE)+'</div></section>'
people+='<section class="container section" id="incoming">'+section_head('Incoming researchers','Incoming PhD students')+'<div class="people-grid">'+''.join(person(p) for p in INCOMING)+'</div></section>'
people+='<section class="container section" id="masters">'+section_head('Master’s research','Master’s students')+'<div class="people-grid">'+''.join(person(p) for p in MASTERS)+'</div></section>'
people+='<section class="container section" id="visitors">'+section_head('Visiting research','Visiting students')+'<div class="people-grid">'+''.join(person(p) for p in VISITORS)+'</div></section>'
people+='<section class="container section"><div class="section-head"><div><p class="eyebrow">Research community</p><h2>Research collaborators</h2></div><p class="section-desc">Our papers bring together researchers at UBC and partner institutions. Complete coauthor credits appear alongside every publication.</p></div><div class="collaborator-links"><a href="https://cdfg.mit.edu/">MIT Computational Design & Fabrication Group ↗</a><a href="https://www.dgp.toronto.edu/">University of Toronto · Dynamic Graphics Project ↗</a><a href="https://chaoliu.tech/">Chao Liu · UBC ↗</a><a href="https://www.cs.ubc.ca/~kmyi/">Kwang Moo Yi · UBC ↗</a><a href="https://www.minghaoguo.com/">Minghao Guo ↗</a></div></section><section class="container people-join"><h2>Joining PhysAI</h2><p>Interested in working with the group?</p><a class="button primary" href="join.html">Explore opportunities ↗</a></section>'
(ROOT/'people.html').write_text(layout('people.html','People',people,'Meet Peter Yichen Chen, postdoctoral researchers, doctoral students, incoming PhD students, master’s students, and visiting students at UBC PhysAI Lab.'),encoding='utf-8')

news=page_intro('PhysAI Lab','News','Research releases, awards, and updates from PhysAI and its collaborators.')+'<div class="container">'+award_grid()+'</div><section class="container section">'+news_rows(NEWS)+'</section><section class="container section"><p class="eyebrow">Selected press</p><h2>In the press</h2><div class="press-grid"><article><span>MIT NEWS · JULY 2025</span><h3><a href="https://news.mit.edu/2025/ai-shapes-autonomous-underwater-gliders-0709">AI shapes autonomous underwater gliders ↗</a></h3><p>Computational design and learning for more efficient underwater robots.</p></article><article><span>MIT NEWS · MAY 2025</span><h3><a href="https://news.mit.edu/2025/system-lets-robots-identify-objects-properties-through-handling-0508">Robots identify object properties through handling ↗</a></h3><p>Differentiable simulation connects robot proprioception with physical object properties.</p></article></div></section>'
(ROOT/'news.html').write_text(layout('news.html','News',news,'Research news and recognition for Peter Yichen Chen and collaborators, including SIGGRAPH, RSS, and SCA awards.'),encoding='utf-8')

join=page_intro('PhysAI Lab','Join the lab','We welcome researchers interested in the intersection of artificial intelligence and physics simulation, across computer science, mathematics, engineering, and related fields.')+'''<div class="container join-layout"><aside><p class="eyebrow">At a glance</p><p>University of British Columbia<br>Vancouver, Canada</p><p>Physics simulation<br>Machine learning<br>Graphics & geometry<br>Robotics & scientific computing</p><a href="mailto:peter.chen@ubc.ca">peter.chen@ubc.ca ↗</a></aside><div><section><p class="eyebrow">Graduate research</p><h2>Graduate students</h2><p>Read Peter’s joining guide to learn about the group’s research environment and application guidance. Graduate applications follow UBC’s official admissions process.</p><div class="resource-links"><a href="https://peterchencyc.com/joining">Peter’s joining guide ↗</a><a href="https://www.cs.ubc.ca/students/grad/prospective">UBC CS graduate admissions ↗</a></div></section><section><p class="eyebrow">Postdoctoral research</p><h2>Postdoctoral researchers</h2><p>If your research is a strong fit, Peter invites you to reach out with your CV, selected publications, and a research agenda for the next one to two years.</p><a href="mailto:peter.chen@ubc.ca?subject=%5BProspective%20Member%5D%20Postdoctoral%20research">Introduce your research ↗</a></section><section><p class="eyebrow">Collaboration</p><h2>Research collaboration</h2><p>For research collaborations across academia and industry, describe the problem, the relevant physical system, and how it connects to the group’s work.</p><a href="mailto:peter.chen@ubc.ca?subject=PhysAI%20research%20collaboration">Get in touch ↗</a></section></div></div><div class="container join-callout"><h2>Contact</h2><p>For prospective membership, Peter asks that you include <strong>[Prospective Member]</strong> in the email subject. Tell us about your interests and the questions you want to pursue.</p><a class="button primary" href="mailto:peter.chen@ubc.ca?subject=%5BProspective%20Member%5D%20PhysAI">Contact Peter ↗</a></div>'''
(ROOT/'join.html').write_text(layout('join.html','Join',join,'Graduate research, postdoctoral opportunities, and collaboration with PhysAI Lab at UBC.'),encoding='utf-8')

# Browser-side citation data contain only public bibliographic metadata.
(ROOT/'assets').mkdir(exist_ok=True)
bib={}
for p in P:
 names=re.sub(r'[*†+]','',p['authors']);authors=' and '.join(n.strip() for n in names.split(','));url=p['links'].get('Paper') or p['links'].get('Project') or p['links'].get('PDF') or ''
 bib[p['id']]='@misc{'+p['id'].replace('-','')[:45]+str(p['year'])+',\n  title = {'+p['title']+'},\n  author = {'+authors+'},\n  year = {'+str(p['year'])+'},\n  howpublished = {'+p['venue']+'},\n  url = {'+url+'}\n}'
(ROOT/'assets/citations.js').write_text('window.PHYSAI_CITATIONS = '+json.dumps(bib,ensure_ascii=False)+';',encoding='utf-8')
for file in ROOT.glob('*.html'):
 content=file.read_text(encoding='utf-8')
 for url,path in MEDIA.items():content=content.replace('src="'+e(url)+'"','src="'+path+'"')
 file.write_text(content,encoding='utf-8')
pubfile=ROOT/'publications.html';pubfile.write_text(pubfile.read_text(encoding='utf-8').replace('<script src="assets/site.js?v=team-4"','<script src="assets/citations.js?v=team-4" defer></script><script src="assets/site.js?v=team-4"'),encoding='utf-8')
print(f'Built {len(NAV)} pages, {len(P)} publications, {len(PEOPLE)} doctoral profiles, {len(POSTDOCS)} postdocs, {len(INCOMING)} incoming PhD students, {len(MASTERS)} master’s students, {len(VISITORS)} visitors, {len(demo_prefixes)} demos.')
