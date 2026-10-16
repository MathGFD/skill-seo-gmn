# Scripts do Localo (aba do Chrome via claude-in-chrome)

Testados em 09-10/10/2026 em dois perfis reais. Preenchem por script (setter nativo + evento), então funcionam sem depender de foco de teclado. **A aba precisa estar `visible`**: aba oculta congela o React e até o script trava.

URL de posts: `https://app.localo.com/place-x/{PLACE_ID}/posts` (o slug é ignorado). PLACE_ID via MCP `placesList`.

## Ciclo por post (1 chamada `browser_batch`)

`[file_upload(foto do post N), CHECK, navigate(posts), OPEN(post N+1), find("file input (type=file) for image upload in dialog")]`

A ref do file input só existe depois do `find`, então o upload do N+1 vai na chamada seguinte. Recarregar a página entre posts é obrigatório: o modal antigo fica no DOM e confunde a conferência.

## OPEN (abre o modal, data/hora manual, texto e link)

Trocar `P` pelo JSON do post (`{"n","d":"AAAA-MM-DD","t":texto,"u":url}`; gerar com `json.dumps(..., ensure_ascii=True)`).

```js
const w=ms=>new Promise(r=>setTimeout(r,ms));const S=(el,v)=>{const p=el.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype;Object.getOwnPropertyDescriptor(p,'value').set.call(el,v);el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));};const P=window.__P=/*JSON*/;
if(document.visibilityState!=='visible'){'HIDDEN'}else{let b;for(let k=0;k<60&&!(b=[...document.querySelectorAll('button')].find(x=>x.innerText.trim()==='Create post'));k++)await w(250);await w(800);b.click();let d;for(let k=0;k<40&&!(d=[...document.querySelectorAll('[role=dialog]')].pop());k++)await w(250);await w(800);[...d.querySelectorAll('button')].find(x=>x.innerText.includes('Manually')).click();await w(800);[...d.querySelectorAll('label')].find(x=>x.innerText.trim()==='Manual').click();await w(800);
for(const [ph,v] of [['Select date',P.d],['Select time','10:00']]){const i=d.querySelector(`input[placeholder="${ph}"]`);i.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));i.focus();i.click();await w(400);S(i,v);await w(400);i.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',code:'Enter',keyCode:13,which:13,bubbles:true}));await w(400);}
[...document.querySelectorAll('button')].filter(x=>x.innerText.trim()==='OK'&&x.offsetParent).forEach(x=>x.click());await w(300);document.activeElement.blur();
S(d.querySelector('textarea'),P.t);await w(300);const u=[...d.querySelectorAll('input')].find(i=>(i.placeholder||'').includes('example.com'));if(u)S(u,P.u);await w(300);JSON.stringify({cta:d.innerText.includes('Learn more'),url:!!u})}
```

Se voltar `cta:false` (primeiro post do perfil): `find` no combobox "No call to action" → clicar → `.ant-select-item-option` com texto `Learn more` → setar a URL no input `example.com`. Dali em diante o Localo lembra o botão (e o último link: por isso o OPEN sempre sobrescreve).

## CHECK (só agenda se tudo bater)

```js
const w=ms=>new Promise(r=>setTimeout(r,ms));const P=window.__P;const d=[...document.querySelectorAll('[role=dialog]')].pop();let img=0;for(let k=0;k<40&&!(img=[...d.querySelectorAll('img')].filter(i=>i.src.includes('localo-user-content')&&i.complete&&i.naturalWidth>0).length);k++)await w(500);const st={dt:[...d.querySelectorAll('input[placeholder^="Select"]')].map(i=>i.value).join(' '),ta:d.querySelector('textarea').value===P.t,u:[...d.querySelectorAll('input')].some(i=>i.value===P.u),cta:d.innerText.includes('Learn more'),img};const ok=st.dt===P.d+' 10:00'&&st.ta&&st.u&&st.cta&&img>0;if(ok){[...d.querySelectorAll('button')].find(x=>x.innerText.trim()==='Schedule').click();await w(3500);st.sched=document.body.innerText.includes('successfully scheduled');}JSON.stringify({n:P.n,ok,...st})
```

`ok:false` = não agendou nada. Investigar antes de seguir.

## Editar post agendado (ex.: trocar link)

Botão "Edit Post" do card abre dropdown (Edit / **Delete**). Só abre com clique real: pegar a posição com `getBoundingClientRect()` do botão do card, `left_click` na coordenada, `find` "Edit Post menuitem (not Delete)". No modal, setar o input e `Schedule`. **O Localo cancela o post antigo (state CANCELLED no MCP) e cria um novo**: não é duplicata.

## Fotos (Photo Planner)

`/place-x/{ID}/scheduledPhotos` → `find` file input da área "Drop your images" → `file_upload` (máx. 20 por vez, <10 MB por chamada) → botão Manual → date/time por setter → combobox "3 photos" = `1 photo`, "3 days" = `Once a week` (`.ant-select-item-option`) → `Schedule (N photos)`. "Publish now" publica todas na hora. Segundo lote: começar na semana seguinte ao último do primeiro. Conferir: MCP `getSchedules`.
