---
name: primeira-pagina
description: Protocolo Primeira Página — entrega do serviço de Google Meu Negócio (GBP) da Winners/OnTheTop no método do Localo, operado pelo MCP do Localo. Fases- prospect (Leads Finder + Visibility Scan), gate, keywords, audit (24 checks), baseline (Position Map + estatísticas), plano (High Impact + Smart Tasks), semana (tasks, posts, fotos, reviews, concorrentes) e medir (relatório Localo). Use quando o Matheus disser "/primeira-pagina", "roda o protocolo no cliente X", "baseline do GMN", "audit do perfil", "diagnóstico do Google", "como tá o ranking do cliente", "relatório do GMN", "plano do Google Meu Negócio", ou citar Localo. NÃO é o site do cliente (isso é /site-local).
---

# /primeira-pagina — Protocolo Primeira Página (método Localo)

**Uso:** `/primeira-pagina {cliente} [fase]` · fases: `prospect` · `gate` · `keywords` · `audit` · `baseline` · `plano` · `semana` · `medir`.
Sem fase → ler `status.md` do cliente e rodar a próxima pendente.

**Regra-mãe (decidida em 2026-10-09): só entra no plano o que o Google escreve, com prova.** Toda ação leva a frase oficial do Google (inglês original + tradução) e o link. Fonte: [google-oficial.md](google-oficial.md); as frases centrais foram conferidas letra por letra no HTML da Central de Ajuda (3038177 nome/área, 7091 ranking, 3474122 avaliações, 7249669 categorias, 6303076 horário especial, 6103862 fotos, 3039617 descrição, 7342169 posts, 9157481 área de atendimento).
**O Localo é a régua de medição, não a regra.** Ele dá score, mapa, concorrentes e estatística. Quando o Localo sugere algo que o Google não escreve (keyword no nome, post a cada 5-7 dias, meta de fotos, citações em massa), vai pra tabela "o que ficou de fora", nunca pro plano. Números do Localo aparecem só como "referência dos concorrentes". O método do Localo segue documentado em [localo-metodo.md](localo-metodo.md) pra entender a ferramenta.
Cautela nossa (não é regra do Google, e dizer isso no texto): uma mudança sensível por vez (nome, categoria, endereço). O Google só escreve que editar categoria pode pedir nova verificação.

Modelo pronto de relatório: `1-Projetos/onthetop-media/relatorios/2026-10-09-plano-4-perfis/` (`fonte/build.py` gera o site na identidade OnTheTop a partir de `data.json` e `grids.json`; `pull.py` e `grids.py` puxam do Localo).

## O que "primeira página" significa aqui

**Visibilidade do Localo = % dos pontos do grid em que o perfil está no top 3.** Junto com a posição média. Faixas do Localo: 1-3 muito alta · 4-10 boa · 11-20 média · 20+ baixa.
A meta é por **área realista**. Usar o Area Difficulty Index: verde mostra resultado em até 3 meses, amarelo leva mais de 3, vermelho "quase impossível em 3 meses". Começar pelas zonas verdes.
**Prazos do Localo** (é o que se fala pro cliente): perfil melhor otimizado em 1-2 semanas, visibilidade e interações em 4-6 semanas, ranking em ~2-3 meses. Nicho competitivo pode levar 1 ano ou mais. **Score 100% não garante #1.** Vende processo e entregável, nunca posição.

## A única trava que não vem do Localo: diretriz do Google sobre o nome

O audit do app tem o check `BUSINESS_NAME_KEYWORDS`. Ele dá ERROR quando o nome não contém as keywords sugeridas e **empurra keyword pro nome** (testado num cliente em 09/10: sugeriu "porto alegre", "clínica", "harmonização facial"). A doc do Localo não recomenda isso em lugar nenhum. Esse critério é interno do app.
A diretriz do Google proíbe: o nome tem que ser o nome real da fachada, sem keyword, cidade ou serviço (support.google.com/business/answer/3038177). Isso suspende perfil.
**Regra:** `BUSINESS_NAME_KEYWORDS` é ignorado no diagnóstico e nunca vira tarefa. As keywords vão pra descrição, serviços, posts e poster de review, que é onde o próprio Localo manda pôr.
O mesmo cuidado vale pra sugestão de keyword de serviço que o cliente **não faz**. As sugestões saem dos concorrentes, então conferir com o briefing antes de usar.

## Localo MCP — o que faz e o que não faz

MCP `localo` (escopo user). São 3 tools: `docs(category)`, `query` (GraphQL de leitura), `mutation` (GraphQL de escrita).
**Antes de montar query, ler [localo-api.md](localo-api.md)** ou rodar `docs("<categoria>")`. Se der erro de campo, rodar `docs("introspection")`. Não chutar nome de campo.

**Não publica nada no Google, e isso é de propósito do Localo:** não edita o perfil, não posta, não responde review. A execução é no app do Localo (posts, Photo Planner, respostas, ofertas) ou direto no GBP, feita pelo operador. A skill entrega o texto pronto.
**As `mutation`s mexem só dentro do Localo.** Toda mutation precisa de confirmação do Matheus. Exceções que rodam sem perguntar: `synchronizeGoogleReviews`, `refreshPlace`, `refreshPlaceKeyword` (o refresh manual é 1 por dia).
Gasta cota: `createResearchGrid` (Visibility Scan, 50 por mês no plano atual) e `addPlaceKeyword` (máximo 10 por perfil, mais a cota mensal). Avisar antes.
`listPlaceTasks` **gera** Smart Tasks na 1ª chamada (efeito colateral).

### Mapa de tools por fase

| Necessidade | GraphQL (via `query`/`mutation`) | Fase |
|---|---|---|
| Perfis da conta | `placesList(input:{pageNo,pageSize,active:true})` | gate |
| Detalhe do perfil (nome, categoria, nota, reviews, verificado) | `place(id){ verified latestPlaceSnapshot{…} }` | gate |
| Buscar/importar prospect | `listQueryPlaceSnapshots` → `importGooglePlaceFromPlaceSnapshot` | prospect |
| Visibility Scan de prospect | `createResearchGrid` (+ `sales:{city}`) | prospect |
| Leads list | `upsertSalesProspect` | prospect |
| Termos que o Google já associa (impressões) | `placeGoogleSearchTerms` | keywords |
| Sugestão de keyword com volume e intenção | `placeKeywordSuggestions` | keywords |
| Adicionar keyword (dispara 1º scan) | `addPlaceKeywords` | keywords |
| Audit e score (24 checks, com stats) | `getPlaceGuidelines` → `audit(id){ score{ checks{ checkId status stats } } }` | audit |
| Frases fortes do top 5 (título/descrição/reviews) | `audit(id){ *ProminentPhrases }` | audit/plano |
| Keywords monitoradas + visibilidade | `place{ activePlaceKeywords{ visibility ahrefsOverview latestGrids } }` | baseline/medir |
| Grid ponto a ponto | `grid(id){ audits{ position difficulty } }` | baseline/medir |
| Concorrentes do grid | `grid(id){ competitors{…} }` | baseline |
| Ligações, rotas, cliques, impressões | `googleMetricSeries` (`CALL_CLICKS`, `BUSINESS_DIRECTION_REQUESTS`, `WEBSITE_CLICKS`, `BUSINESS_IMPRESSIONS_*`) | baseline/medir |
| Reviews sem resposta / estatística | `listReviews(replyFilter:NO_REPLY)`, `reviewsStats`, `reviewsChart` | baseline/semana |
| Smart Tasks | `listPlaceTasks`, `markTaskAsCompleted`, `getOneMoreTask` | plano/semana |
| Posts e fotos | `listGooglePosts`, `listScheduledLocalPosts`, `getSchedules`, `publicationMetricSeries` | semana |
| Citações | `fetchPlaceCitations`, `fetchPlaceCitationsStats` | plano |
| Movimento dos concorrentes | `auditActionsTrack` (paginado pra trás) | semana/medir |
| Relatório pro cliente | `createSingleRaport` → poll `placeReports`/`report` → `createReportSharedPermalink` | medir |

Se o MCP `localo` não aparecer na sessão: `claude mcp get localo`. Não simular dado.

## Pasta do cliente

`1-Projetos/cliente-{slug}/gbp/`
```
status.md            fase atual, datas, keywords, grid usado, operador
baseline-dia0.md     números congelados do dia 0 (NUNCA editar depois)
audit.md             24 checks + o que fazer em cada um
plano.md             High Impact → Medium, com texto pronto
semanas/AAAA-MM-DD.md  log do ciclo semanal
medicoes/AAAA-MM-DD.md
relatorio-AAAA-MM.md   versão pro cliente (vai pra fora: sem decisão interna, sem pendência)
```
Cliente já tem pasta em `1-Projetos/` ? Usar a existente + subpasta `gbp/`. Conferir antes.

---

## Fase `prospect` — Leads Finder + Visibility Scan (pré-venda)

O fluxo de agência do Localo pra lead que ainda não é cliente. Gasta 1 scan da cota (avisar antes).
1. `listQueryPlaceSnapshots` com nome + cidade → confirmar o perfil certo com o Matheus.
2. `importGooglePlaceFromPlaceSnapshot` → `createResearchGrid` com a keyword principal, grid 5x5 ou 7x7 na área do bairro, `sales:{city}`.
3. Saída em `1-Projetos/prospects-gbp/{slug}.md`: visibilidade (% top 3), posição média, top 3 por ponto (reviews, nota, categoria), o que falta no perfil (sem site, poucas fotos, sem post). Fechar com **3 pontos críticos em número**. O "como resolver" não vai pro lead.
4. Lead entrou no pipeline → `upsertSalesProspect` (`TODO` → `CONTACTED` → `CONVERTED`), só com ok dele.

## Fase `gate` — o cliente pode entrar?

Registrar em `status.md`. Qualquer ❌ = **para** e avisa.
1. Endereço real ou área de atendimento real. A doc do Localo manda listar só onde atende, no máximo 20 áreas e a 2-3 horas de viagem.
2. Google conectado no Localo com acesso de admin/manager. `GOOGLE_CONNECTION` = OK.
3. Perfil ativo no Localo, com **slot de Optimization**. Sem isso não tem Audit nem Tasks.
4. `VERIFICATION` = OK.
5. Nome = nome real da fachada. Se tiver keyword/cidade → avisar o Matheus do risco (ver a trava acima). A decisão de limpar é dele e do cliente.

## Fase `keywords` — escolher antes de tudo (o audit depende delas)

Regras do Localo (`localo-metodo.md` §4):
1. Começar pelos termos reais: `placeGoogleSearchTerms` (o que já gera impressão). Depois `placeKeywordSuggestions`, que traz volume e intenção.
2. **2-3 keywords principais, cada uma em duas versões:** sem local e com cidade/bairro. Cidade, não "near me". Priorizar o que dispara Local Pack.
3. Nunca nome da marca como keyword. Usar a linguagem do cliente final (reviews, WhatsApp), não a de agência.
4. **Teto: 10 por perfil.** Cada keyword tem que ser serviço que o cliente faz de verdade (conferir com o briefing).
5. Mostrar a lista pro Matheus → ok → `addPlaceKeywords`.
6. **Trocar keyword reinicia a otimização do zero.** Depois de travar, só mexe com motivo forte, e registra em `status.md`.

## Fase `audit` — diagnóstico (antes de mexer em qualquer coisa)

`getPlaceGuidelines` → `audit(id){ score{ percent checks{ checkId status stats } } }`. Salvar em `audit.md`:
- Score % + pontos (ex: 15/36). O peso de cada check vem do estudo de 16.098 perfis do Localo, então % não é "fração de checks passados".
- Tabela dos 24 checks: status, o número que o stats traz (ex: fotos 4 vs mínimo 81, categorias adicionais alvo 3, máximo 9; descrição com X de Y termos sugeridos) e a ação.
- Checks com `null` = sem dado (reviews zerados, por exemplo). Dizer isso, não tratar como OK.
- `*ProminentPhrases` do top 5: as frases que os concorrentes do topo usam em título, descrição e reviews. É matéria-prima pra descrição, posts e poster.
- `BUSINESS_NAME_KEYWORDS`: marcar "ignorado — diretriz do Google".
- O audit roda sozinho a cada 7 dias e quando as keywords mudam. Mudança demora a refletir no score.

## Fase `baseline` — dia 0 (sem isso não existe prova depois)

Congelar em `baseline-dia0.md` com a data:
- Por keyword: visibilidade (% top 3), posição média, distribuição nas faixas 1-3/4-10/11-20/20+, tamanho do grid e área. **As medições futuras usam o mesmo grid, a mesma área e as mesmas keywords.** O Localo avisa: mudar grid ou keyword quebra a comparação.
- Medir com o negócio **aberto** (o horário de funcionamento é fator ao vivo de ranking).
- Area Difficulty: quais zonas são verdes, amarelas e vermelhas.
- Top 3 concorrentes: nome, categoria, reviews, nota. Marcar como favoritos no tracker (mutation, pedir ok).
- `googleMetricSeries` dos últimos 30 e 90 dias: ligações, rotas, cliques no site, impressões Maps/Search.
- Reviews: total, nota, % respondida (`reviewsStats`).
- Score do audit do dia.
Fechar com 3 linhas: onde ele está, quem domina, o gap em número.

## Fase `plano` — High Impact primeiro, poucas mudanças por vez

1. Ordem: os checks **High Impact (vermelho)** do audit → Medium (laranja) → o resto. Dentro disso, as Smart Tasks da semana (`listPlaceTasks`).
2. **Ritmo do Localo:** poucas mudanças por semana, de propósito. Mudar muita coisa de uma vez parece suspeito pro Google e pode levar à suspensão. Nunca juntar categoria + endereço + telefone na mesma semana.
3. Cada tarefa sai **pronta pra executar**: campo do GBP ou tela do Localo, texto exato e quem faz. O operador cola, não pensa. Por check:
   - `PRIMARY_CATEGORY` / `ADDITIONAL_CATEGORIES_COUNT`: categorias com base nos concorrentes do top (`target` e `hardMax` do stats).
   - `BUSINESS_DESCRIPTION_KEYWORDS`: descrição reescrita com os termos sugeridos que forem **verdade** pro cliente e com as frases fortes do top 5. Sem repetição forçada.
   - `OPENING_HOURS`: horários + feriados. É fator ao vivo.
   - `PHOTOS_COUNT` / `PHOTOS_GROWTH`: meta do stats (`optimalMin`). Fotos reais, sem IA e sem banco de imagem. Subir pelo Photo Planner (até 20 por vez) com agendamento.
   - `POSTS_COUNT` / `POSTS_FREQUENCY` / `OFFERS`: calendário de 1 post a cada 5-7 dias (mais que isso não ajuda), sempre com foto, até 1.500 caracteres, com CTA. Oferta se a categoria permitir.
   - `REVIEWS_*`: poster QR com no mínimo 4 termos de destaque + templates de resposta por estrela. Responder todas. Review falsa nunca.
   - `CITATIONS`: diretórios da lista do Localo (onde os concorrentes estão), com NAP idêntico.
   - `SOCIAL_MEDIA_LINKS`: as redes que os concorrentes têm e o cliente não.
   - `PROTECTION`: ligar o Localo Protection (protege nome, telefone e endereço de edição sugerida).
   - Área de atendimento: só onde atende de verdade, no máximo 20.
4. Zonas verdes do Area Difficulty: citar bairro/zona na descrição, nos posts e nas ofertas, sem forçar.
5. Mostrar o plano pro Matheus antes de mandar pro operador ou pro cliente.

## Fase `semana` — o ciclo semanal do Localo

`semanas/AAAA-MM-DD.md`:
- Smart Tasks da semana (`listPlaceTasks`): o que fazer, com texto pronto. Feita → `markTaskAsCompleted` (com ok). Acabou → `getOneMoreTask`.
- 1 post (a cada 5-7 dias) com texto e sugestão de foto. Feriado da semana → horário especial.
- Reviews novas sem resposta (`listReviews NO_REPLY`, depois de `synchronizeGoogleReviews`): rascunho de resposta personalizada pra cada uma.
- Fotos agendadas no Photo Planner (`getSchedules`): tem fila pra semana?
- Concorrentes (`auditActionsTrack`): quem mudou o quê (categoria, fotos, reviews, post) e se a posição deles mexeu. Copiar o que correlacionou com subida.
- Grid: só alarmar se cair **mais de 5 posições em muitos pontos, por vários ciclos, junto com queda de ligações e rotas**. Fora isso é volatilidade normal.

## Fase `medir` — mensal (e marcos de 30/60/90)

- Mesmas keywords, mesmo grid e mesma área do baseline. Tabela baseline → agora por keyword: visibilidade, posição média, faixas. Mais score do audit, ligações, rotas, cliques e reviews. Delta em número, não adjetivo.
- Ler contra os prazos do Localo: 4-6 semanas pra interação, 2-3 meses pra ranking. Antes disso, "não moveu" é esperado e não é motivo pra trocar keyword.
- Leitura crítica: o que moveu, o que não moveu, hipótese, ajuste no plano.
- Relatório oficial do Localo: listar `placeReports` (reusar se já cobre o período) → `createSingleRaport` (com ok) → poll `report` até `readyForEmail` → `createReportSharedPermalink`. Link: `https://app.localo.com/shared-reports/<permalink>/reports/<reportId>`. **E-mail pro cliente só com ok explícito**, porque sai pra fora.
- `relatorio-AAAA-MM.md`: os números, 3 frases e o próximo passo. **Ligações e rotas primeiro.** Ranking vem depois.

---

## Regras

- Nunca inventar número. Dado que não veio do Localo = "sem dado", e diz de onde viria.
- Nunca tocar credencial do cliente. O acesso é por convite de admin no GBP.
- Ao fim de cada fase: atualizar `status.md`, append em `log.md` do vault. Se sobrou ação pro Matheus → CRM (ver `/encerrar-sessao`).
- A doc do Localo muda. Se uma regra numérica parecer velha, conferir no artigo citado em `localo-metodo.md`.

## Conexão (feita em 2026-10-09)

`claude mcp add --scope user --transport http localo https://api.localo.com/api/mcp --header "Authorization: Bearer <ORG_ID>:<TOKEN>"`
Organização: tua conta Localo (Research mode tem cota de 50 scans).
Token novo (rotação): criar em Localo → Settings → MCP → Create Token, rodar `claude mcp remove localo -s user` e adicionar de novo. **Token nunca em arquivo do vault.**
