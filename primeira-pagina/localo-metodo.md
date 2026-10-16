---
tipo: referencia
area: _skill
tags: [localo, gbp, seo-local, metodo]
atualizado: 2026-10-09
sources: [docs.localo.com]
---

# Método Localo (destilado de docs.localo.com)

> Só o que a doc diz. Onde não há informação: "não coberto pela doc". Nenhuma das coleções traz pesos numéricos de ranking nem a lista nominal dos 17 checks do Audit.
> Aviso: a doc é de um fornecedor de ferramenta. Vários números abaixo (ex.: "post a cada 5-7 dias") são regra do Localo, não regra do Google.

## 1. Visão do Localo — como o ranking local funciona

- Três fatores primários: **Distância** (proximidade do buscador, pode vencer perfil não otimizado), **Relevância** (match entre busca e categoria/nome/descrição), **Prominência** (reviews de qualidade, menções, reputação offline). Prominência pesa mesmo em área de baixa competição. Pesos numéricos: não coberto pela doc. (https://docs.localo.com/en/articles/12060782-how-can-i-learn-local-seo)
- Versão do vídeo-guia: Relevância (info do perfil bate com a busca), Distância, Prominência (reviews, autoridade do site, citações, atividade no Google). (https://docs.localo.com/en/articles/5542624-how-to-check-your-position-in-google-search-results-using-localo-video-guide)
- Pilares de local SEO listados: otimização do GBP, citações com NAP consistente, reviews, keywords com localização, site mobile/rápido. (https://docs.localo.com/en/articles/10903219-what-is-local-seo)
- **Fator "live": horário de funcionamento.** Desde nov/2023 negócio aberto tende a ranquear acima do fechado (mesmo negócio, mesma keyword, posição diferente às 11h e às 23h). Outros fatores citados como possíveis: trânsito, transporte público, às vezes clima/qualidade do ar. Recomendação: medir posição com o negócio aberto; manter horários e feriados atualizados; pode não valer para alguns setores (ex.: advogados). A própria doc diz que é observação, "ninguém sabe como o algoritmo funciona". (https://docs.localo.com/en/articles/8600574-what-are-live-ranking-factors, https://docs.localo.com/en/articles/8699585-when-should-i-manually-refresh-the-position-map-in-localo)
- Ranking varia por ponto: top 3 num ponto, fora do top 10 a poucas ruas. (https://docs.localo.com/en/articles/5733381-how-is-ranking-calculated-and-how-do-you-read-the-results-map-in-localo)
- Sinal de alerta real vs. volatilidade: queda de **mais de 5 posições em muitos pontos do grid**, persistindo por **vários ciclos de medição**, junto com queda de ligações/rotas/cliques. Aí investigar: categorias e título do GBP, endereço/área de atuação, volume e recência de reviews, conteúdo do site, concorrentes spam. (https://docs.localo.com/en/articles/12646566-why-localo-rankings-differ-from-what-you-see-in-google-maps)
- Local Business Schema (JSON-LD): **não melhora ranking diretamente**, ajuda o Google a entender e ligar site ao GBP; elegibilidade para rich results. Vai no `<body>`; validar em validator.schema.org; gerador grátis do Localo. (https://docs.localo.com/en/articles/10666957-how-to-generate-local-business-schema-with-localo)

## 2. Onboarding de um perfil novo

**Dono do negócio (sessão 1, três ações):** (1) escolher keywords, (2) revisar o Audit, (3) concluir uma recomendação prioritária. Depois: Smart Tasks, Position Map, Reviews (link/QR Poster). (https://docs.localo.com/en/articles/11431571-what-are-the-first-steps-for-business-owners-in-localo)

**Especialista/agência:** (https://docs.localo.com/en/articles/11799159-what-are-the-first-steps-for-local-seo-specialists-in-localo)
1. Conectar o e-mail Google; Localo detecta GBPs onde há acesso de manager/admin (ou adicionar manualmente pelo nome).
2. Definir keywords (serviços + modificadores locais + termos de marca se aplicável).
3. **Rodar o Audit antes de mexer em qualquer coisa** (ponto de partida). Fluxo: diagnosticar, priorizar, agir, re-checar, mostrar progresso. Serve para demonstrar trabalho feito antes do ranking subir.
4. Position Map + Competitor Activity Tracking.
5. Reports (Growth Statistics + Audit Reports).
6. Review Manager e QR Poster.
7. Avançado: publicação em massa, Area Difficulty, Citations Manager, AI Agent.

Setup do perfil: área de busca é definida na adição; se o negócio é service-area (sem endereço), Localo usa a área configurada no Google. Mudar endereço/área de busca pode alterar ranking; próximo refresh usa a nova área. (https://docs.localo.com/en/articles/6027943-how-to-update-the-search-area-and-business-address-in-localo)
Adicionar perfil: importar da conta Google ("Gather profiles") ou manual pelo nome. Perfis importados ficam em "Inactive" até ativar. (https://docs.localo.com/en/articles/5763044-how-to-add-and-remove-business-profiles-in-localo)
Monitoring vs Optimization: Monitoring = rank tracking, mapa, estatísticas, conteúdo. **Optimization** adiciona Audit, Tasks, AI Agent, Business Directory. Plano Single: optimization sempre ligada; PRO: optimization em metade dos perfis. (https://docs.localo.com/en/articles/5652438-what-is-the-difference-between-monitoring-and-optimization-slots)

## 3. Audit / score do perfil

- Score 0-100%, **17 checks automáticos**, cobrindo: nome, endereço, categoria primária e adicionais, horário, descrição, fotos, reviews, links de redes sociais, posição vs concorrentes locais. A lista individual dos 17 checks, faixas ótimas e como corrigir cada um: **não coberto pela doc**. (https://docs.localo.com/en/articles/12115771-what-is-audit-in-localo)
- Pesos diferentes por item; 72% não significa 72% dos checks passados. Pesos derivados de estudo de **16.098 perfis** (peso exato não publicado).
- Prioridades: High Impact (vermelho, começar por aqui), Medium Impact (laranja), Everything is fine (verde).
- Compara com **5 concorrentes locais fortes** onde relevante (ex.: nº de reviews vs média deles).
- Re-audit automático a cada **7 dias** e quando keywords monitoradas mudam. Mudanças demoram a refletir no score.
- **Score não é ranking.** 100% não garante #1. Audit não aplica mudanças sozinho.
- Rodar o Audit depois de definir as keywords (parte da análise depende delas).
- Dá para compartilhar Audit com cliente sem marca Localo.

## 4. Keywords

(https://docs.localo.com/en/articles/11142856-how-to-choose-keywords-for-local-seo-in-localo, https://docs.localo.com/en/articles/10300383-how-to-add-or-remove-keywords-in-localo, https://docs.localo.com/en/articles/6241589-find-out-which-keywords-you-are-already-ranking-for)
- Máximo **10 keywords por perfil** em todos os planos; há também cota mensal de keywords (reseta no ciclo de cobrança; removidas podem ser re-adicionadas no mesmo ciclo).
- "2 ou 3 keywords principais, em duas variações": sem modificador de local (mais amplas, mais concorrência) e com modificador (cidade/bairro).
- Servir + local ("emergency plumber Chicago"). **Usar nome da cidade/região em vez de "near me".**
- **Não usar nome da empresa/marca como keyword de descoberta** (quem busca a marca já te achou). Pode ranquear para a marca, mas não é o foco.
- Linguagem do cliente, não "linguagem de agência" (copiar termos de reviews, e-mails, ligações). Checar dados, não intuição.
- Evitar só termos gigantes ("restaurant"); incluir long-tail.
- Priorizar keywords que disparam o **Local Pack**.
- Fontes de dados: GBP > Performance (termos de busca, atualização mensal), Google Search Console (queries, posições 11-30 com impressão alta como quick wins), Google Trends (sazonalidade). Localo mostra volume, dificuldade e long-tail no app.
- **Evitar trocar keywords com frequência: a cada troca a otimização reinicia do zero.** "Não mudar as keywords principais cedo demais."
- Aviso "competidores insuficientes": keyword de marca/nicho demais não gera comparação; adicionar keywords mais gerais. (https://docs.localo.com/en/articles/8153201-why-is-there-an-insufficient-number-of-competitors-for-analysis)

## 5. Position Maps / grid

(https://docs.localo.com/en/articles/5733381-how-is-ranking-calculated-and-how-do-you-read-the-results-map-in-localo, https://docs.localo.com/en/articles/6890330-what-is-the-advanced-grid-in-localo-and-how-does-it-work, https://docs.localo.com/en/articles/6890631-what-is-the-area-difficulty-index-in-localo, https://docs.localo.com/en/articles/11812621-what-are-the-key-metrics-data-insights-in-localo)
- Cada ponto = busca simulada daquele GPS. Faixas: **1-3** visibilidade muito alta; **4-10** boa; **11-20** média; **20+** baixa. Cores no vídeo-guia: verde top 3, amarelo 4-10, vermelho fora do top 10.
- Raio padrão do mapa: círculo de ~**23 km**. Grids 3x3, 5x5, 7x7 com tamanho configurável; **cobertura máxima 2.500 km²**. Concorrentes mostrados até **100 km** do centro.
- Posição "do negócio" = rank da média de posição entre todos os pontos, comparada com os demais negócios.
- Métricas do dashboard: posição média (todas as keywords); **visibilidade = % de pontos em que está no top 3**; variação vs checagem anterior; perfil views 30 dias.
- Metodologia estável do Localo: um ponto GPS por célula, zoom fixo, só orgânico (sem ads), mesmo método sempre. Divergência vs Google Maps do celular é esperada (personalização, zoom, ads).
- Recomendações de leitura: usar uma ferramenta só; olhar tendência (posição média, % top 3/top 10, semana a semana/mês a mês); olhar pontos vizinhos; **não mudar grid, zoom ou keywords com frequência**; priorizar keywords de alta intenção. (https://docs.localo.com/en/articles/12646566-why-localo-rankings-differ-from-what-you-see-in-google-maps)
- Frequência: grids atualizam automaticamente a cada **7 dias** (doc do Advanced Grid); refresh manual limitado a **1 por dia** (doc do dashboard). Outra doc diz "rankings update daily" (contradição interna, ver seção 13).
- **Area Difficulty Index**: densidade + força dos concorrentes. Fácil (verde): resultados em **até 3 meses**; Médio (amarelo): **acima de 3 meses**; Difícil (vermelho): "quase impossível ver melhora em 3 meses". Estratégia: focar áreas fáceis, usar keywords locais dessas zonas em descrição, posts e ofertas.
- Clicar num ponto mostra o top 20 daquele local e os concorrentes. Research mode (Pro) mostra o grid dos concorrentes. (https://docs.localo.com/en/articles/6254763-how-to-check-your-competitor-s-location-and-results-in-localo)

## 6. Smart Tasks

(https://docs.localo.com/en/articles/10673664-how-to-use-tasks-in-localo)
- Lista nova **semanal**, priorizada, gerada a partir do perfil, concorrentes e keywords escolhidas. Ao completar tudo dá para pedir tarefa adicional.
- Poucas tarefas **de propósito**: mudanças demais em pouco tempo podem parecer suspeitas ao Google e levar à **suspensão do perfil**; ritmo regular importa.
- Tipos citados (exemplos): publicar Google Post, atualizar informações do perfil, pedir reviews, "adicionar fotos dos serviços". Catálogo completo de tipos: não coberto pela doc. (https://docs.localo.com/en/articles/11431571-what-are-the-first-steps-for-business-owners-in-localo, https://docs.localo.com/en/articles/12098254-how-to-manage-my-google-business-profiles-in-localo)
- AI Agent pode disparar tasks; nunca implementa mudança sem autorização. (https://docs.localo.com/en/articles/10703741-what-is-localo-ai-agent-for-google-business-profile)
- Ciclo semanal sugerido pela doc de resultados: completar GBP, responder reviews, postar semanalmente, keywords locais na descrição/áreas, monitorar position map semanalmente, atacar Smart Tasks de maior impacto primeiro. (https://docs.localo.com/en/articles/6859762-when-should-you-expect-results-in-google-business-profile-seo-with-localo)

## 7. Reviews

(https://docs.localo.com/en/articles/10525975-what-is-the-google-review-management-tool-in-localo, https://docs.localo.com/en/articles/5815308-how-to-use-the-google-review-poster-in-localo)
- Reviews são fator de ranking local (segundo a doc) e de conversão.
- Responder **todas** as reviews, rápido. Templates por nota (1 a 5 estrelas); respostas de IA nunca publicam sozinhas, sempre editáveis; tom: natural, empático, personalizado ({{Name}}, {{Owner name}}).
- Localo promove pedir reviews honestas e **rejeita geração de review falsa**.
- Poster com QR: título, descrição, **mínimo 4 termos de destaque** para influenciar o conteúdo da review; imprimir e expor onde o cliente tem alguns minutos (mesa, balcão, sala de espera, vitrine, entrega, junto da nota/recibo).
- Frequência/meta de volume de reviews: não coberto pela doc (apenas comparação com média dos 5 concorrentes no Audit).

## 8. Conteúdo

- **Posts**: limite de **1.500 caracteres**; foto recomendada em todo post; CTA com **6 opções**; UTM tracking opcional; agendamento manual ou horário automático; publicação conjunta no Facebook; ação em massa para vários perfis. **Frequência: a cada 5 a 7 dias; postar mais não ajuda** porque o Google pode não exibir todos. Outra doc: semanal ótimo, mínimo mensal, evitar postar todo dia. (https://docs.localo.com/en/articles/9554147-what-are-some-ideas-for-post-topics, https://docs.localo.com/en/articles/6411734-how-to-schedule-and-publish-posts-in-localo, https://docs.localo.com/en/articles/11640347-what-is-google-business-profile-gbp, https://docs.localo.com/en/articles/11550063-how-to-add-posts-for-multiple-business-profiles-at-once-mass-management, https://docs.localo.com/en/articles/8889445-how-to-schedule-and-publish-facebook-posts-from-localo)
- Tipos/ideias de post: educacional (mitos, estatísticas, guias), institucional (equipe, história, cases, FAQ), produto/serviço (lançamento, evento, horário de feriado, promoção, pedido de review, reviews positivas). Aviso: não habilitar automação que publica sem revisão.
- **Ofertas**: tipo de post que pode aparecer separado; campos: foto, título, detalhes, duração; indisponível para algumas categorias (hotéis, clínicas médicas/spa, etc.; >98% das categorias têm). (https://docs.localo.com/en/articles/8598066-how-to-create-an-offer-with-localo)
- **Fotos / Photo Planner**: upload de **até 20 imagens de uma vez**, agendamento automático (baseado no padrão dos concorrentes) ou manual (quantas por vez, frequência, horário). "Publicar com frequência". **Fotos reais, sem IA, sem banco de imagens; geotag desnecessário.** Google avalia nitidez, relevância, frescor, autenticidade. Número de fotos por mês: não coberto pela doc. (https://docs.localo.com/en/articles/8217500-what-is-the-photo-planner-in-localo)
- **Brand Voice**: gerado automaticamente por perfil (6 seções); controla posts, respostas, descrições, ofertas, AI Agent; regeneração completa só **1 vez por trimestre**. (https://docs.localo.com/en/articles/12108646-what-is-brand-voice-in-localo)
- Atributos: preencher só com fatos reais; aparecem em poucos dias. (https://docs.localo.com/en/articles/6633420-how-to-add-attributes-to-a-google-business-profile)
- Service area: cidades/CEPs/regiões; Google permite **até 20 áreas**; ideal dentro de **2-3 horas** de viagem; ser específico; não listar onde não atende. (https://docs.localo.com/en/articles/6713759-how-to-check-and-add-service-area-for-your-business)
- Pin do mapa e Street View: posicionar pin na porta; 360° pelo app Street View. (https://docs.localo.com/en/articles/6637934-how-to-update-the-map-position-and-street-view-in-localo)
- Proteção do perfil (Localo Protection): monitora nome, telefone, endereço e status contra edições sugeridas indevidas. (https://docs.localo.com/en/articles/6758242-how-to-protect-your-google-business-profile-in-google-maps)

## 9. Citações

(https://docs.localo.com/en/articles/9926048-how-do-i-add-and-manage-google-business-citation-in-localo)
- Citação = menção com NAP (nome, endereço, telefone). Consistência de NAP é "crítica". Disponível em planos pagos.
- Lista de diretórios sugeridos: onde concorrentes estão + pré-definidos por região; atualizada **semanalmente (domingo à noite)**.
- Status: All, To do, Processing (marcada feita, aguardando indexação, "pode levar semanas ou meses"), Active, Lost, Ignored.
- Localo não cria listagens novas no Google (dono deve criar o próprio perfil).
- Diretórios específicos recomendados por nome: não coberto pela doc.

## 10. Concorrentes

(https://docs.localo.com/en/articles/8600847-what-is-the-competitor-action-tracker-in-localo, https://docs.localo.com/en/articles/6254763-how-to-check-your-competitor-s-location-and-results-in-localo)
- Competitor Action Tracker: resumo por IA + feed de mudanças (aumento de imagens/reviews, troca de categorias, descrição), detalhe da mudança e efeito na posição, concorrentes fixados (pin), última mudança detectada, posição média por concorrente.
- Uso recomendado: observar padrões e timing, comparar semanas/meses, copiar o que correlacionou com subida.
- Mapa de concorrentes: top 20 por keyword; clicar no ponto central.

## 11. Relatórios e estatísticas

(https://docs.localo.com/en/articles/12596836-how-to-create-local-seo-reports-in-localo, https://docs.localo.com/en/articles/6499623-what-is-the-growth-statistic-feature-in-localo)
- Conteúdo do report: ranking, concorrentes, crescimento de visibilidade, insights do GBP (views, buscas, ligações, mensagens, rotas), progresso de reviews (nº e nota), atividade de conteúdo, progresso de citações. Mapas de posição clicáveis (PDF e link).
- Auto-report: período semana/mês/ano + frequência; gerado para todos os perfis ativos do workspace; envio por e-mail (pode usar SMTP próprio), link ou PDF. Mensagem privada ao cliente.
- Growth Statistics em 3 blocos: interação, ações executadas, economia estimada vs anúncios pagos. Exportável.
- Valor para cliente segundo a doc: provar ROI e mostrar trabalho feito antes do ranking mover (Audit).

## 12. Fluxo de agência

(https://docs.localo.com/en/articles/10868150-how-to-find-potential-leads-with-the-client-acquisition-feature, https://docs.localo.com/en/articles/11105366-what-is-the-visibility-scan-in-localo, https://docs.localo.com/en/articles/11496684-how-to-invite-team-members-and-clients-to-localo, https://docs.localo.com/en/articles/9233989-how-to-segregate-and-tag-locations-for-easy-management-in-localo)
- **Leads Finder**: escolher categoria + cidade; lista de GBPs com ranking, **Growth Potential** (baseado em Area Difficulty + visibilidade; alto = mais espaço para crescer), reviews, itens faltando (ex.: sem site). Marcar lead como contacted/converted/ignored, comentários.
- **Visibility Scan** (Pro/Enterprise): gera grid de qualquer negócio sem adicioná-lo, top 20 por ponto, mapas white-label para prospecção. Cota mensal compartilhada (grid + Leads Finder): PRO 10 = 50; PRO 30 = 150; PRO 60 = 300; PRO 120 = 600.
- Onboarding do cliente fechado: ativar com 1 clique.
- Operação: workspaces, tags, Bulk Actions, pin de perfis, equipe (Owner/Member) e clientes como Guests via localagency.app (white label, permissões por feature: sem acesso/ver/total). Convite vale 7 dias. Um workspace = uma assinatura.
- Pitch de venda da ferramenta (afirmação do fornecedor, sem fonte): "clientes de #18 para #2 em um mês" e "visibilidade +35%" seguindo as tasks.
- Artigo "How to Use Localo as an Agency": não localizado nas coleções lidas.

## 13. Números e limites (todos explícitos)

| Item | Valor | Fonte |
|---|---|---|
| Keywords por perfil | até 10 | 10300383, 11431571 |
| Grid | 3x3, 5x5, 7x7; máx. 2.500 km² | 6890330 |
| Raio do mapa (padrão) | ~23 km | 5733381 |
| Distância máx. de concorrentes | 100 km do centro | 12646566 |
| Atualização do grid | a cada 7 dias (auto) | 6890330 |
| Refresh manual | 1x por dia | 11840161 |
| "Rankings update daily" | contradiz os 7 dias acima | 11799159 |
| Audit | 17 checks, re-run a cada 7 dias | 12115771 |
| Estudo base do Audit | 16.098 perfis | 12115771 |
| Concorrentes de comparação | 5 | 12115771 |
| Faixas de rank | 1-3 / 4-10 / 11-20 / 20+ | 5733381 |
| Queda que importa | >5 posições em muitos pontos, por vários ciclos | 12646566 |
| Smart Tasks | lista nova semanal | 10673664 |
| Posts | 1 a cada 5-7 dias; limite 1.500 caracteres; 6 CTAs | 9554147, 6411734 |
| Fotos (Photo Planner) | upload de até 20 de uma vez | 8217500 |
| Poster de review | mínimo 4 termos de destaque | 5815308 |
| Service area | até 20 áreas; 2-3 h de viagem | 6713759 |
| Brand Voice | regenerar 1x por trimestre | 12108646 |
| Citações | lista atualizada domingo à noite; indexação semanas a meses | 9926048 |
| Primeiros resultados | GBP melhor em 1-2 semanas; visibilidade e interações em 4-6 semanas; ranking significativo nos meses seguintes | 11070186 |
| Prazo médio de melhora | ~2-3 meses; 2-4 semanas em nicho fácil/keyword de baixo volume; competitivo até 1 ano ou mais | 6859762 |
| Area Difficulty | verde até 3 meses; amarelo >3 meses; vermelho quase impossível em 3 meses | 6890631 |
| Convite de equipe | válido 7 dias | 11496684 |
| Cotas Visibility Scan | PRO10 50 / PRO30 150 / PRO60 300 / PRO120 600 por mês | 11105366 |
| Frequência de update do GBP | mínimo mensal; quinzenal/semanal ideal; post semanal | 11640347 |

Contradições internas da doc: (a) grid atualiza "a cada 7 dias" vs "rankings atualizam diariamente"; (b) post "a cada 5-7 dias, mais não ajuda" vs "mínimo mensal, quinzenal ou semanal ideal".

## 14. Recomendações do Localo que são arriscadas perante as diretrizes do Google

**Keyword no nome da empresa: a doc NÃO recomenda isso.** Literalmente:
- "Don't use your business name or brand" como keyword a rastrear (é sobre a keyword monitorada, não sobre o nome do GBP). (6241589)
- Relevância é descrita como match entre a busca e "category, name, or description" do negócio (12060782), e o Audit checa "business name" (12115771), sem dizer o que fazer com o nome.
- Diagnóstico de queda: investigar "Google Business Profile categories and title" (12646566). Sem instrução de inserir keyword no título.
- Proteção: Localo protege nome, telefone, endereço e status contra edições (6758242).
- Não coberto pela doc: qualquer orientação de colocar palavra-chave ou cidade no nome do perfil. Portanto o "audit que pede keyword no nome" não vem desta doc; se aparecer, é do Audit interno do app, e a doc não explica o critério.

Outros pontos que merecem cautela (a doc recomenda, sem ressalva de política):
- "Add local keywords to your business description and service areas" (6859762) e "optimize GBP descriptions incorporating key phrases related to low-difficulty zones" (6890631). Risco: stuffing na descrição/áreas; Google exige que áreas de atuação sejam realistas, e a própria doc diz para não listar onde não atende (6713759).
- Posts e ofertas "especificamente mencionando keywords locais" das zonas fáceis (6890631).
- Postagem/publicação automática por IA e agendamento por algoritmo: a doc mesma manda manter revisão manual (6411734).
- Mudar muita coisa de uma vez pode ser lido como suspeito e causar suspensão (10673664): é por isso que as tasks são poucas.
- Alterar o endereço/pin no Localo/GBP muda o ranking (6027943); endereço deve ser real.
- Fotos: a doc diz fotos reais, sem IA nem banco de imagens (8217500).
- Reviews: a doc proíbe geração de reviews falsas (10525975).

## Artigos lidos
https://docs.localo.com/en/articles/10300383-how-to-add-or-remove-keywords-in-localo
https://docs.localo.com/en/articles/10525975-what-is-the-google-review-management-tool-in-localo
https://docs.localo.com/en/articles/10553544-what-is-the-local-business-pack-and-why-is-it-worth-displaying-in-it
https://docs.localo.com/en/articles/10666957-how-to-generate-local-business-schema-with-localo
https://docs.localo.com/en/articles/10673664-how-to-use-tasks-in-localo
https://docs.localo.com/en/articles/10703741-what-is-localo-ai-agent-for-google-business-profile
https://docs.localo.com/en/articles/10868150-how-to-find-potential-leads-with-the-client-acquisition-feature
https://docs.localo.com/en/articles/10903219-what-is-local-seo
https://docs.localo.com/en/articles/11001028-who-is-localo-for
https://docs.localo.com/en/articles/11070186-what-is-localo-and-how-does-it-work
https://docs.localo.com/en/articles/11105366-what-is-the-visibility-scan-in-localo
https://docs.localo.com/en/articles/11142856-how-to-choose-keywords-for-local-seo-in-localo
https://docs.localo.com/en/articles/11431571-what-are-the-first-steps-for-business-owners-in-localo
https://docs.localo.com/en/articles/11496684-how-to-invite-team-members-and-clients-to-localo
https://docs.localo.com/en/articles/11550063-how-to-add-posts-for-multiple-business-profiles-at-once-mass-management
https://docs.localo.com/en/articles/11640347-what-is-google-business-profile-gbp
https://docs.localo.com/en/articles/11799159-what-are-the-first-steps-for-local-seo-specialists-in-localo
https://docs.localo.com/en/articles/11812621-what-are-the-key-metrics-data-insights-in-localo
https://docs.localo.com/en/articles/11840161-how-to-navigate-the-localo-dashboard
https://docs.localo.com/en/articles/11936930-how-the-localo-app-compare-to-other-tools
https://docs.localo.com/en/articles/12060782-how-can-i-learn-local-seo
https://docs.localo.com/en/articles/12098254-how-to-manage-my-google-business-profiles-in-localo
https://docs.localo.com/en/articles/12108646-what-is-brand-voice-in-localo
https://docs.localo.com/en/articles/12115771-what-is-audit-in-localo
https://docs.localo.com/en/articles/12596836-how-to-create-local-seo-reports-in-localo
https://docs.localo.com/en/articles/12646566-why-localo-rankings-differ-from-what-you-see-in-google-maps
https://docs.localo.com/en/articles/5542624-how-to-check-your-position-in-google-search-results-using-localo-video-guide
https://docs.localo.com/en/articles/5652438-what-is-the-difference-between-monitoring-and-optimization-slots
https://docs.localo.com/en/articles/5733381-how-is-ranking-calculated-and-how-do-you-read-the-results-map-in-localo
https://docs.localo.com/en/articles/5763044-how-to-add-and-remove-business-profiles-in-localo
https://docs.localo.com/en/articles/5815308-how-to-use-the-google-review-poster-in-localo
https://docs.localo.com/en/articles/6027943-how-to-update-the-search-area-and-business-address-in-localo
https://docs.localo.com/en/articles/6241589-find-out-which-keywords-you-are-already-ranking-for
https://docs.localo.com/en/articles/6254763-how-to-check-your-competitor-s-location-and-results-in-localo
https://docs.localo.com/en/articles/6411734-how-to-schedule-and-publish-posts-in-localo
https://docs.localo.com/en/articles/6499623-what-is-the-growth-statistic-feature-in-localo
https://docs.localo.com/en/articles/6633420-how-to-add-attributes-to-a-google-business-profile
https://docs.localo.com/en/articles/6637934-how-to-update-the-map-position-and-street-view-in-localo
https://docs.localo.com/en/articles/6713759-how-to-check-and-add-service-area-for-your-business
https://docs.localo.com/en/articles/6758242-how-to-protect-your-google-business-profile-in-google-maps
https://docs.localo.com/en/articles/6859762-when-should-you-expect-results-in-google-business-profile-seo-with-localo
https://docs.localo.com/en/articles/6890330-what-is-the-advanced-grid-in-localo-and-how-does-it-work
https://docs.localo.com/en/articles/6890631-what-is-the-area-difficulty-index-in-localo
https://docs.localo.com/en/articles/8153201-why-is-there-an-insufficient-number-of-competitors-for-analysis
https://docs.localo.com/en/articles/8217500-what-is-the-photo-planner-in-localo
https://docs.localo.com/en/articles/8598066-how-to-create-an-offer-with-localo
https://docs.localo.com/en/articles/8600574-what-are-live-ranking-factors
https://docs.localo.com/en/articles/8600847-what-is-the-competitor-action-tracker-in-localo
https://docs.localo.com/en/articles/8699585-when-should-i-manually-refresh-the-position-map-in-localo
https://docs.localo.com/en/articles/8889445-how-to-schedule-and-publish-facebook-posts-from-localo
https://docs.localo.com/en/articles/9233989-how-to-segregate-and-tag-locations-for-easy-management-in-localo
https://docs.localo.com/en/articles/9554147-what-are-some-ideas-for-post-topics
https://docs.localo.com/en/articles/9926048-how-do-i-add-and-manage-google-business-citation-in-localo
