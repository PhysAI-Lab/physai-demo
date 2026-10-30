'use strict';
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#site-nav');
menu?.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',String(open));});
nav?.addEventListener('click',event=>{if(event.target.closest('a')){nav.classList.remove('open');menu?.setAttribute('aria-expanded','false');}});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav?.classList.contains('open')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.focus();}});
const dialog=document.querySelector('#media-dialog'),mediaContent=document.querySelector('#media-content');
function clearMedia(){mediaContent.querySelectorAll('video').forEach(v=>{v.pause();v.removeAttribute('src');v.load();});mediaContent.replaceChildren();}
document.querySelectorAll('[data-media]').forEach(button=>button.addEventListener('click',()=>{
 clearMedia();document.querySelector('#media-title').textContent=button.dataset.title;
 const isVideo=button.dataset.kind==='video',media=document.createElement(isVideo?'video':'img');
 media.src=button.dataset.media;
 if(isVideo){media.controls=true;media.playsInline=true;media.preload='metadata';media.setAttribute('aria-label',button.dataset.title+' research video');}
 else media.alt=button.dataset.title+' research result';
 media.addEventListener('error',()=>{const error=document.createElement('p');error.className='media-error';error.textContent='This media could not load. Use the source project link below to view the original.';media.replaceWith(error);},{once:true});
 mediaContent.append(media);const link=document.querySelector('#media-project');link.href=button.dataset.project;link.hidden=!button.dataset.project;
 dialog.showModal();if(isVideo)media.play().catch(()=>{});
}));
document.querySelector('#close-dialog')?.addEventListener('click',()=>dialog.close());
dialog?.addEventListener('close',clearMedia);
dialog?.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
const form=document.querySelector('#publication-filters');
if(form){
 const papers=[...document.querySelectorAll('.paper-row')],search=document.querySelector('#paper-search');
 const fields=Object.fromEntries(['year','topic','status','scope'].map(name=>[name,document.querySelector('#filter-'+name)]));
 function filter(){const query=search.value.trim().toLowerCase();let count=0;papers.forEach(p=>{const match=(!query||p.dataset.search.toLowerCase().includes(query))&&Object.entries(fields).every(([key,field])=>!field.value||p.dataset[key]===field.value);p.hidden=!match;if(match)count++;});document.querySelector('#result-count').textContent=count+' publication'+(count===1?'':'s');document.querySelector('#no-results').hidden=count>0;}
 form.addEventListener('submit',event=>event.preventDefault());form.addEventListener('input',filter);form.addEventListener('change',filter);form.addEventListener('reset',()=>requestAnimationFrame(filter));document.querySelector('#clear-search').addEventListener('click',()=>{form.reset();search.focus();});
 const params=new URLSearchParams(location.search);search.value=params.get('author')||params.get('q')||'';
 Object.entries(fields).forEach(([key,field])=>{const v=params.get(key);if(v&&[...field.options].some(o=>o.value===v))field.value=v;});filter();
 document.querySelectorAll('[data-bib]').forEach(button=>button.addEventListener('click',()=>{
  const row=button.closest('.paper-body');let panel=row.querySelector('.bib-panel');
  if(panel){panel.hidden=!panel.hidden;button.setAttribute('aria-expanded',String(!panel.hidden));return;}
  panel=document.createElement('div');panel.className='bib-panel';panel.id='bib-'+button.dataset.bib;const pre=document.createElement('pre');pre.textContent=window.PHYSAI_CITATIONS[button.dataset.bib];const copy=document.createElement('button');copy.textContent='Copy citation';copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(pre.textContent);copy.textContent='Copied ✓';}catch{copy.textContent='Select the citation above to copy';}});panel.append(pre,copy);row.append(panel);button.setAttribute('aria-expanded','true');button.setAttribute('aria-controls',panel.id);
 }));
}
document.querySelectorAll('[data-demo-filter]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-demo-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('[data-demo-topic]').forEach(card=>{card.hidden=!!button.dataset.demoFilter&&card.dataset.demoTopic!==button.dataset.demoFilter;});}));
// Respect reduced-motion preferences: animated preview images remain available on demand.
if(matchMedia('(prefers-reduced-motion: reduce)').matches){document.querySelectorAll('img[src]').forEach(img=>{if(/\.gif(?:\?|$)/i.test(img.getAttribute('src'))){const placeholder=document.createElement('div');placeholder.className='media-placeholder';const label=document.createElement('small');label.textContent='Animated result · open preview to play';placeholder.append(label);img.replaceWith(placeholder);}});}
