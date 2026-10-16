---
name: agendar-gbp
description: Calendário de posts e fotos do Perfil da Empresa no Google (GBP) de um cliente e agendamento no Localo pelo Chrome. Escreve N posts (texto + foto real ou arte no molde da marca), valida (limites do Google + regras do conselho), gera as artes, agenda tudo no Localo com conferência antes de cada Schedule e confirma pelo MCP. Também agenda fotos no Photo Planner e edita posts já agendados. Use quando o Matheus disser "/agendar-gbp", "agenda os posts do Google do cliente X", "deixa X meses de post agendado", "posts do Google até o fim do ano", "gera imagem e escreve post pro Google", "sobe as fotos no Localo", "troca o link dos posts agendados". NÃO é o protocolo/diagnóstico do perfil (isso é /primeira-pagina) nem o site (/site-local).
---

# /agendar-gbp — calendário de posts e fotos do Google, agendado no Localo

Feito em 09-10/10/2026 em dois clientes: um de saúde (26 posts + 32 fotos reais) e uma agência (33 posts com arte gerada). Os dois conferidos pelo MCP do Localo.

## Limites que não mudam
- **MCP do Localo é só leitura** pra posts, fotos, serviços e produtos. Agendamento é pela tela, no Chrome (`claude-in-chrome`). Serviço/produto do perfil vai direto no Google (o Localo nem lê).
- **Aba do Localo visível e ativa.** Aba oculta (`document.visibilityState === 'hidden'`) congela tudo. Pedir pro Matheus deixar a aba numa janela só dela, na frente. Checar antes de cada post (o OPEN já retorna `HIDDEN`).
- **Google não liga post a ranking** (`primeira-pagina/google-oficial.md`). Localo recomenda 1 post a cada 5-7 dias e diz que postar mais não ajuda. Se ele pedir "1 por dia", perguntar com recomendação de 3/semana (ele escolheu isso em 10/10).
- Post com mais de 6 meses é arquivado pelo Google: calendário fecha antes disso e fica anotado quando gerar o próximo lote.

## Fase 1 — Levantar (antes de escrever)
1. MCP Localo: `placesList` (PLACE_ID), `listGooglePosts` + `listScheduledLocalPosts` (já tem algo agendado? não duplicar data), `getSchedules` (fotos), `place.latestPlaceSnapshot` (nome, categoria, link).
2. O que o cliente vende de verdade: site, nota do projeto no vault, áudio/transcrição da cliente. **Só entra serviço confirmado.** Serviço não confirmado = informação falsa no perfil.
3. Conselho de classe (saúde): sem preço, sem promessa, sem antes/depois, sem depoimento, registro (CREFITO/CRM/CRO) na assinatura. Faltou o número do registro → trava e pergunta.
4. Domínio do site: botão aponta pro **domínio próprio**, nunca pro `*.vercel.app` (some se sair da Vercel). Testar cada link com `curl -o /dev/null -w "%{http_code}"`.

## Fase 2 — Escrever
- Calendário: dia fixo e 10h; pular data já ocupada e Natal. Temas por época (Black Friday, feriado, verão/inverno, recesso de janeiro sem chamar pra agenda).
- Cada post: 1 ideia, 500-900 caracteres, botão "Learn more" (= "Saiba mais") pra página/artigo do assunto com `?utm_source=google&utm_medium=gbp&utm_campaign=post` (âncora `#` vai depois da query).
- Sem telefone no texto (Google rejeita), sem `wa.me`, sem "garantido/100%/melhor".
- **Não usar cliente como exemplo de erro** (escapou "Clínica especializada" = perfil do próprio cliente). **Não ensinar regra que o próprio perfil descumpre** (ex.: keyword no nome com o nome ainda errado).
- Fonte única: um `.py` com a lista de posts que valida e gera `posts.md` + `posts.json`. Modelos em `modelos/`:
  - `checar-fotos-reais.py`: posts em markdown + foto real + assinatura com registro (`--crefito`).
  - `build-artes-onthetop.py`: posts em Python + artes 1200×900 renderizadas por Chrome headless a partir de `molde-arte-1200x900.html` (eyebrow, título com `*ênfase*`, subtítulo). Contact sheet com PIL pra conferir antes de subir.
- Fotos reais: conferir contact sheet (sem rosto de paciente), ≤5 MB, não repetir foto em semanas seguidas.

## Fase 3 — Agendar no Localo (Chrome)
Scripts prontos em `localo-js.md`. Ritmo: 1 chamada `browser_batch` por post (upload N + CHECK + recarrega + OPEN N+1 + find).
1. Post 1 sozinho, mostra pro Matheus conferir no Localo (Content → Posts → Scheduled). Só depois o lote.
2. CHECK só clica em Schedule se data, texto, link, botão e foto baterem. `ok:false` = parar e olhar.
3. Fotos: 9 "Publish now" (capa primeiro) + resto no Photo Planner, 1 por semana. Capa o Localo não define: ele marca no Google.
4. Edição (trocar link): cancela + recria. Os CANCELLED no MCP são os antigos.

## Fase 4 — Conferir e registrar
- MCP `listScheduledLocalPosts` (campos `scheduledAt state apiError post{callToAction{url} media{sourceUrl}}`): contar SCHEDULED, nenhum `apiError`, toda mídia presente. `getSchedules` pras fotos.
- Horário no MCP vem em UTC (10h BRT = 13:00Z).
- Registrar no `_index.md` do projeto do cliente (status, período, próxima data de lote novo) + `log.md`.
