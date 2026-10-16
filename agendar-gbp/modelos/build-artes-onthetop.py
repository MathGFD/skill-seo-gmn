"""Posts do Google (OnTheTop) out-dez/2026: valida, renderiza as artes e gera posts.md.

Uso: python3 build.py            -> valida + renderiza artes que faltam + posts.md
     python3 build.py --force    -> re-renderiza todas
Artes: ~/Desktop/onthetop-post-google/q4/NN-slug.jpg (1200x900, molde do post.html)
"""
import datetime, html, json, os, re, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.expanduser("~/Desktop/onthetop-post-google/q4")
ANTIGAS = os.path.expanduser("~/Desktop/onthetop-post-google")
FONTS = "./fonts"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
BASE = "https://onthetopmedia.com"
UTM = "utm_source=google&utm_medium=gbp&utm_campaign=post"
GMN = "/servicos/google-meu-negocio-porto-alegre/"
TRAF = "/servicos/gestao-de-trafego-pago-porto-alegre/"
SITE = "/servicos/criacao-de-sites-porto-alegre/"
VID = "/servicos/producao-de-video-para-empresas-porto-alegre/"
SOC = "/servicos/social-media-porto-alegre/"

# (data, slug, arte: arquivo existente ou (eyebrow, titulo com *enfase*, subtitulo), link, texto)
POSTS = [
("2026-10-12", "quem-aparece-primeiro", ("Google Meu Negócio", "Quem aparece *primeiro* recebe o PIX.", "Quem pesquisa o teu serviço\njá decidiu comprar."), GMN,
"""Quem pesquisa "dentista perto de mim" ou "oficina em Porto Alegre" não está passeando no Google. Já decidiu comprar. Só falta escolher de quem.

E a escolha quase sempre é um dos três primeiros nomes que aparecem no Maps. Quem está em 7º ou 8º lugar nem entra na conversa.

O que coloca um negócio nesses três primeiros não é sorte, nem ter a nota mais alta. É o perfil preenchido do jeito que o Google lê: categoria certa, serviços cadastrados, fotos reais, avaliações respondidas e site ligado ao perfil.

A gente faz isso para negócios locais de Porto Alegre. No botão tem como funciona."""),
("2026-10-14", "site-e-perfil", "02-site-e-perfil-conectados.jpg", SITE,
"""O cliente te acha no Google, clica no perfil, vai para o site e... não encontra o WhatsApp. Ou encontra um site que não abre direito no celular.

Perfil e site precisam conversar. O perfil traz a pessoa, o site convence e o botão de contato fecha. Se um dos três falha, o cliente volta para a busca e escolhe o próximo.

Quando a gente monta um site, ele já nasce ligado ao Perfil da Empresa no Google: mesmo nome, mesmo endereço, mesmo telefone, e um caminho só até o WhatsApp.

Um caminho entre a busca e a conversa. Sem desvio."""),
("2026-10-16", "case-linda", ("Case · Google Maps", "De *enterrada* a primeira em 15 dias.", "Micropigmentação · Araçatuba, SP"), "/#google-maps-cases",
"""A Linda Cintra faz micropigmentação em Araçatuba. Quem procurava o serviço na cidade via três concorrentes e escolhia uma delas. Ela nem aparecia.

O perfil dela no Google tinha informação faltando e nenhum motivo para o Google mostrar ela antes das outras.

Reestruturamos o perfil inteiro: categorias, serviços, fotos, descrição e botão de agendamento. Em 15 dias ela estava em primeiro na busca por "micropigmentação", com 4,9 estrelas e o botão de agendar na cara do cliente.

Detalhe: logo abaixo dela aparecem concorrentes com nota 5,0. Não foi a nota que colocou ela no topo. Foi o perfil trabalhado do jeito que o Google lê.

No botão tem o print do antes e depois."""),
("2026-10-19", "contatos-nao-cliques", "05-contatos-nao-cliques.jpg", TRAF,
"""Clique não paga boleto. Contato paga.

Muita campanha é avaliada pelo número de cliques, alcance ou curtidas. Só que o dono do negócio quer saber outra coisa: quantas pessoas ligaram, quantas chamaram no WhatsApp e quanto custou cada uma.

É isso que a gente mede no tráfego pago: ligações, mensagens e custo por contato. Se uma campanha traz muito clique e pouco contato, ela é cortada. Se traz contato barato, ela recebe mais verba.

Relatório em linguagem de dono de negócio, todo mês."""),
("2026-10-23", "case-templo", ("Case · Google Maps", "Do *9º lugar* ao pódio em 15 dias.", "Academia de jiu-jitsu · Porto Alegre"), "/#google-maps-cases",
"""A Templo é uma academia de jiu-jitsu em Porto Alegre. Já tinha nota boa, mas aparecia em 9º lugar no Maps, abaixo da dobra, onde ninguém rola a tela.

No mesmo bairro tem uma academia grande, com centenas de avaliações. Brigar por volume não ia dar. Fomos pela precisão: perfil completo, serviços por turma, fotos reais, resposta a cada avaliação e site ligado ao perfil.

15 dias depois: 1º em "escola de jiu-jitsu porto alegre" e 2º em "academia de jiu jitsu porto alegre".

Academia vive de mensalidade. Cada posição que sobe é um aluno que deixa de ir para o concorrente e passa a pagar todo mês aqui."""),
("2026-10-26", "a-nota-nao-decide", ("SEO local", "A nota *não* decide quem fica em primeiro.", "Relevância, distância e destaque."), "/blog/como-aparecer-no-google-maps-guia-google-meu-negocio/",
""""Quantas avaliações eu preciso para ficar em primeiro no Google?"

É a pergunta que mais recebemos, e a resposta surpreende: não existe um número. Já vimos busca em Porto Alegre em que o primeiro colocado tinha metade das avaliações do sexto.

O próprio Google diz que olha três coisas: relevância (o perfil explica bem o que tu faz?), distância (quão perto tu está de quem pesquisa) e destaque (o quanto o negócio é conhecido, e aí entram as avaliações).

Avaliação conta, mas sozinha não resolve. Perfil incompleto com 200 avaliações perde para perfil bem trabalhado com 50.

No botão tem um guia completo de como aparecer no Maps."""),
("2026-10-28", "pronto-para-anunciar", "03-pronto-para-anunciar.jpg", TRAF,
"""Antes de colocar dinheiro em anúncio, quatro perguntas:

1. Quando alguém clica, para onde vai? Site lento ou perfil incompleto desperdiçam o clique.
2. Tu consegue medir de onde veio cada contato? Sem rastreamento, não dá para saber o que funciona.
3. A oferta está clara? Quem chega precisa entender em 5 segundos o que tu faz e como chamar.
4. Quanto vale um cliente novo para ti? É isso que diz quanto dá para pagar por contato.

Se alguma resposta for "não sei", o primeiro passo não é anunciar. É arrumar a base. A gente começa sempre por esse diagnóstico."""),
("2026-10-30", "mito-comprar-avaliacao", ("Mitos do Google", "Comprar avaliação *derruba* o perfil.", "Atalho que custa caro."), GMN,
"""Mito: comprar avaliação ajuda a subir no Google.

O Google proíbe avaliação paga, avaliação em troca de desconto e avaliação feita por quem não foi cliente. Quando detecta, remove as avaliações e pode suspender o perfil inteiro. Aí some do Maps, com nota e tudo.

O que funciona é chato e simples: pedir avaliação para o cliente real, no momento certo, com o link direto, e responder cada uma. Inclusive as negativas, com calma e sem expor ninguém.

É uma rotina, não uma campanha. A gente monta essa rotina junto com o perfil."""),
("2026-11-02", "site-ou-instagram", ("Presença digital", "Site ou Instagram: *o que* vem primeiro?", "Depende de onde o teu cliente procura."), "/blog/site-ou-instagram-negocio-local/",
"""Site ou Instagram: o que um negócio local precisa primeiro?

Depende de onde o teu cliente procura. Se ele pesquisa no Google ("eletricista zona sul", "clínica de fisioterapia perto de mim"), o primeiro passo é o Perfil da Empresa no Google, seguido de um site simples ligado a ele.

Se o teu cliente descobre o serviço rolando o feed (moda, gastronomia, estética), o Instagram pesa mais no começo.

Na maioria dos negócios locais de Porto Alegre, quem chega pelo Google já está decidido a comprar. Quem chega pelo Instagram ainda está conhecendo. Os dois servem, mas em momentos diferentes.

No botão tem o artigo completo com a conta de cada caminho."""),
("2026-11-04", "site-que-ajuda", "04-site-que-converte.jpg", SITE,
"""O cliente te achou. E o site, ajuda ou atrapalha?

Três sinais de que o site está perdendo cliente:

Demora mais de 3 segundos para abrir no celular. A maioria desiste antes.
O WhatsApp está escondido no rodapé ou num menu.
Não diz em 5 segundos o que tu faz e em qual região atende.

Os sites que a gente faz são leves, claros no celular e com o contato a um toque. E já nascem preparados para o Google entender quem tu é e onde atende."""),
("2026-11-06", "quanto-custa-trafego", ("Tráfego pago", "Quanto custa *tráfego pago* para pequena empresa?", "A conta começa pelo valor do cliente."), "/blog/quanto-custa-trafego-pago-pequena-empresa-porto-alegre/",
""""Quanto eu preciso investir em anúncio?"

A resposta honesta começa por outra pergunta: quanto vale um cliente novo para ti? Se um cliente deixa R$ 2.000 no ano, pagar R$ 80 por contato pode ser ótimo negócio. Se deixa R$ 150, não fecha a conta.

Depois vem o nicho e a região. Clique de advogado custa diferente de clique de pizzaria. E Porto Alegre tem preço diferente de cidade pequena.

Por isso a gente não começa pelo orçamento. Começa pela conta: valor do cliente, quanto dá para pagar por contato e quanto testar antes de escalar.

No botão tem um artigo com números de referência para Porto Alegre."""),
("2026-11-09", "fotos-reais", ("Google Meu Negócio", "Foto *real* vende mais que foto bonita.", "Fachada, equipe e o serviço acontecendo."), GMN,
"""O Google pede fotos que representem a realidade: nítidas, bem iluminadas, sem filtro pesado. E o cliente também prefere.

Foto de banco de imagem e arte cheia de texto não mostram nada. O que ajuda o cliente a decidir:

A fachada, para ele te achar na rua.
A equipe, para saber com quem vai falar.
O espaço por dentro.
O serviço acontecendo ou o resultado entregue.

Perfil com fotos atualizadas passa a sensação de negócio ativo. Perfil com três fotos de 2019 passa a sensação contrária, mesmo que não seja verdade."""),
("2026-11-11", "responder-avaliacao", ("Avaliações", "Avaliação *sem resposta* é conversa pela metade.", "Inclusive (principalmente) as negativas."), GMN,
"""Quem lê as avaliações do teu negócio lê também as tuas respostas. E isso pesa na decisão.

Avaliação positiva: agradece, cita o que a pessoa elogiou, convida a voltar. Curto e de verdade, sem resposta copiada.

Avaliação negativa: responde com calma, sem discutir em público e sem expor dado do cliente. Reconhece, oferece um canal direto para resolver. Quem está lendo vê como tu trata problema, e isso convence mais do que dez avaliações cinco estrelas.

Responder todas, rápido, faz parte da rotina que a gente monta para os clientes."""),
("2026-11-13", "video-com-roteiro", ("Produção de vídeo", "Vídeo que vende começa *antes* da câmera.", "Roteiro primeiro, gravação depois."), VID,
"""Vídeo bonito sem roteiro vira só vídeo bonito.

Antes de ligar a câmera, a gente responde três perguntas: quem vai assistir, o que essa pessoa precisa entender e o que ela deve fazer no final (chamar no WhatsApp, agendar, visitar).

Com isso definido, o vídeo curto para Instagram e anúncio ganha um gancho nos primeiros segundos, uma ideia só no meio e um convite claro no fim. E o institucional apresenta o negócio do jeito que um cliente entende, não do jeito que o dono explicaria numa reunião.

Gravamos em Porto Alegre, com roteiro pensado para vender."""),
("2026-11-16", "black-friday-perfil", ("Black Friday", "3 ajustes no *perfil* antes da Black Friday.", "Quem procura agora já quer comprar."), GMN,
"""Black Friday é dia 27. Antes de pensar em anúncio, três ajustes no Perfil da Empresa no Google que custam zero:

Horário: se vai abrir em horário diferente, cadastra como horário especial. Cliente que chega com a porta fechada não volta.
Produtos e serviços: atualiza o que está em destaque, com foto real.
Atualização no perfil: avisa o que tu vai ter na semana, de forma clara, com o botão certo.

São os ajustes que mais rendem contato na semana mais concorrida do ano. Se quiser ajuda para revisar o teu, chama a gente."""),
("2026-11-18", "case-google-ads", ("Case · Google Ads", "R$ 2 mil investidos, *R$ 21 mil* em vendas.", "Rede de pesquisa + Performance Max."), "/#cases",
"""Um negócio estagnado precisava voltar a vender.

Começamos pela rede de pesquisa do Google, com termos de marca e de serviço: aparecer para quem já está procurando. Com o rastreamento funcionando, expandimos com Performance Max só no que estava trazendo venda.

Resultado: R$ 2 mil investidos, R$ 21 mil em vendas.

O que fez diferença não foi uma configuração mágica. Foi medir certo desde o primeiro dia e cortar rápido o que não convertia.

Números reais de campanha conduzida pelo nosso time de tráfego, cliente preservado."""),
("2026-11-20", "site-lento", ("Sites", "Cada segundo de *espera* é cliente indo embora.", "Nosso site: 76 → 99 no teste do Google."), SITE,
"""O nosso próprio site tirava 76 no teste de velocidade do Google no celular. Mudamos quatro coisas e ele foi para 99.

Por que isso importa para um negócio local? Porque quem pesquisa no celular, na rua, com pressa, não espera. Se o site demora, a pessoa volta e clica no concorrente. E tu nem fica sabendo que perdeu o cliente.

Os sites que a gente entrega passam pelo mesmo teste antes de ir ao ar: leves, rápidos no 4G e com o contato a um toque."""),
("2026-11-23", "horario-especial", ("Google Meu Negócio", "Feriado chegando: *horário* atualizado.", "Black Friday, Natal e Ano-Novo."), GMN,
"""Cliente que vai até a tua porta e encontra fechado não dá segunda chance. E ainda pode deixar avaliação ruim.

Entre Black Friday, Natal e Ano-Novo, muito negócio muda o horário e esquece de avisar o Google. O Perfil da Empresa tem um campo só para isso: horário especial. Tu cadastra a data e o horário diferente, e o Google mostra para quem pesquisa naquele dia.

O próprio Google recomenda confirmar o horário dos feriados, mesmo quando ele não muda.

Leva dois minutos e evita a pior experiência que um cliente pode ter."""),
("2026-11-25", "instagram-ate-whatsapp", ("Redes sociais", "Instagram com *caminho* até o WhatsApp.", "Constância e direção, não postagem aleatória."), SOC,
"""Postar todo dia sem caminho até o WhatsApp é trabalhar para o algoritmo de graça.

Na gestão de redes sociais, a gente começa pelo destino: o que a pessoa deve fazer depois de ver o post? Chamar no direct, clicar no link, agendar. A partir disso vem o planejamento do mês, com conteúdo que mostra o trabalho, tira dúvida real e convida para a conversa.

Constância importa, mas direção importa mais. Um perfil com três posts bons por semana e um convite claro vende mais do que um perfil com post todo dia sem rumo."""),
("2026-11-27", "black-friday-hoje", ("Black Friday", "Hoje quem procura *já decidiu*.", "Esteja na frente de quem está comprando."), TRAF,
"""É Black Friday. Hoje a pessoa que pesquisa um serviço ou produto no Google não está só olhando: está com a decisão tomada, comparando onde comprar.

Três lembretes para o dia:

Responde rápido. Mensagem que espera duas horas vira venda do concorrente.
Confere se o horário no Google está certo.
Se está anunciando, olha os contatos ao longo do dia, não só no fim. Campanha que não traz contato até o meio-dia precisa de ajuste agora, não amanhã.

Boas vendas para todo mundo."""),
("2026-11-30", "case-meta-ads", ("Case · Meta Ads", "R$ 2,7 mil investidos, *R$ 35 mil* em vendas.", "16 campanhas testadas, só o que vendia ficou."), "/#cases",
"""Uma loja queria vender direto pelo anúncio, sem depender de vendedor.

Rodamos 16 campanhas testando abordagens diferentes no Meta Ads: criativo, público, oferta. A regra era simples: o que não trazia compra era cortado rápido, e a verba ia para o que estava vendendo.

Resultado: R$ 2,7 mil investidos, R$ 35 mil em vendas.

Teste controlado é isso: começar com verba pequena, medir compra (não curtida) e só ampliar o que se paga. Números reais, cliente preservado."""),
("2026-12-02", "como-trabalhamos", ("Como trabalhamos", "Quatro etapas, *sem* caixa-preta.", "Diagnóstico, plano, execução, relatório."), "/#processo",
"""Como a OnTheTop trabalha, do primeiro contato ao relatório:

Diagnóstico: entendemos o negócio, o cliente ideal, o que já funciona e o que trava. A conversa termina com a conta feita.
Plano: prioridade clara do que fazer nos primeiros 30 dias e do que fica para depois. Ninguém precisa de tudo ao mesmo tempo.
Execução: configuramos, publicamos e rastreamos. Tu acompanha o que está no ar.
Relatório: todo mês, contatos, custo por contato e o que vamos mudar, em linguagem de dono de negócio.

Sem pacote fechado de tudo e sem caixa-preta."""),
("2026-12-04", "mito-blog-maps", ("Mitos do Google", "Blog *não* coloca ninguém no Maps.", "Perfil e avaliações pesam mais."), GMN,
"""Mito: escrever blog faz o negócio aparecer no Google Maps.

Blog ajuda o site a aparecer na busca normal, para quem pesquisa uma dúvida. Mas o ranking do Maps é outro jogo. O Google olha relevância do perfil, distância de quem pesquisa e destaque do negócio.

Para o Maps, o que pesa mais: categoria certa, serviços cadastrados, fotos reais, avaliações frequentes e respondidas, e informação igual em todo lugar (nome, endereço e telefone).

Blog vale a pena, mas depois do perfil arrumado. Começar pelo blog com o perfil incompleto é investir na ordem errada."""),
("2026-12-07", "categoria-certa", ("Google Meu Negócio", "A *categoria* certa vale mais que mil posts.", "É o primeiro sinal que o Google lê."), GMN,
"""A categoria principal é uma das primeiras coisas que o Google usa para decidir em quais buscas o teu negócio aparece.

Erro comum: escolher a categoria mais genérica ("Loja", "Empresa de serviços") ou a mais bonita, em vez da que descreve o que tu mais vende. Um negócio de estética cadastrado numa categoria genérica disputa buscas que não são as dele.

A regra: categoria principal = o serviço que mais fatura. Secundárias = os outros serviços reais, sem exagero. Nada de marcar categoria para todo produto.

É a primeira coisa que a gente revisa num perfil."""),
("2026-12-09", "custo-por-contato", ("Tráfego pago", "O número que importa: *custo por contato*.", "Relatório que dono de negócio entende."), TRAF,
"""Impressões, alcance, CTR, CPM. Relatório de tráfego cheio de sigla e nenhuma resposta para a pergunta do dono: valeu a pena?

No relatório que a gente entrega, o número principal é o custo por contato. Quantas pessoas ligaram ou chamaram no WhatsApp, e quanto custou cada uma.

Com esse número, a decisão fica simples. Se um cliente novo vale mais do que o custo para trazê-lo, aumenta a verba. Se não vale, ajusta ou para.

Todo mês, em linguagem de dono de negócio, com o que vamos mudar no mês seguinte."""),
("2026-12-11", "case-b2b", ("Case · Google Ads B2B", "*120 leads* para projetos acima de R$ 100 mil.", "Móveis planejados para empresas."), "/#cases",
"""Móveis planejados para empresas: venda alta, ciclo longo, cliente difícil de alcançar.

Montamos campanhas na rede de pesquisa do Google mirando quem decide a compra: arquitetos, gestores de compras e empresários. Termos específicos, sem desperdiçar verba com quem procura móvel para casa.

Resultado: 120 leads qualificados para projetos acima de R$ 100 mil.

Em B2B, volume de clique não importa. O que importa é falar com as poucas pessoas que assinam o contrato. Números reais, cliente preservado."""),
("2026-12-14", "landing-page", ("Landing pages", "Anúncio bom em página *ruim* é dinheiro jogado.", "Uma página, uma oferta, um botão."), SITE,
"""O anúncio fez o trabalho dele: a pessoa clicou. Agora ela cai numa página com menu, cinco serviços, três botões e um formulário longo. Resultado: sai sem chamar.

Para campanha, a página de captação tem regras simples:

Uma oferta só, a mesma do anúncio.
O que a pessoa ganha, dito em uma frase.
Prova: depoimento, número, foto real.
Um botão, de preferência para o WhatsApp.

Página leve e focada costuma fazer o mesmo anúncio render mais contatos, sem gastar um real a mais."""),
("2026-12-16", "video-institucional", ("Produção de vídeo", "Teu negócio explicado em *um* minuto.", "Vídeo institucional para site, perfil e anúncio."), VID,
"""Quanto tempo tu leva para explicar o que a tua empresa faz? Agora imagina que o cliente te dá um minuto.

O vídeo institucional resolve isso: apresenta o negócio, as pessoas e o jeito de trabalhar, num formato que dá para colocar no site, no Perfil da Empresa no Google e nos anúncios.

O segredo é o roteiro. Nada de discurso de missão e valores. É o que o cliente quer saber: o que tu faz, para quem, como funciona e como chamar.

Gravamos em Porto Alegre, do roteiro à edição."""),
("2026-12-18", "horario-fim-de-ano", ("Fim de ano", "Recesso? Avisa o *Google* antes.", "Horário especial de 24/12 a 02/01."), GMN,
"""Vai fechar ou mudar o horário nas festas? Avisa o Google antes de avisar o Instagram.

No Perfil da Empresa, o campo "horário especial" mostra o horário diferente só nas datas que tu escolher. Se o fechamento for de até 6 dias, usa horário especial. Se for de 7 dias ou mais, o Google pede para marcar como "temporariamente fechado".

E vale um post avisando a volta, com a data em que o atendimento normal recomeça.

Cliente que encontra a informação certa volta em janeiro. Cliente que encontra a porta fechada procura outro."""),
("2026-12-21", "planejar-janeiro", ("Planejamento 2027", "Janeiro começa *agora*.", "O que fazer nos primeiros 30 dias."), "/#processo",
"""Quem começa a planejar em janeiro, começa a vender em março.

Três coisas para decidir ainda em dezembro:

Qual serviço tu quer vender mais em 2027? É ele que define categoria, anúncio e conteúdo.
Quanto vale um cliente novo? É isso que diz quanto dá para investir para trazê-lo.
O que está travando hoje: perfil, site, anúncio ou atendimento?

Com essas três respostas, os primeiros 30 dias do ano se planejam sozinhos. É exatamente o diagnóstico que a gente faz no primeiro contato."""),
("2026-12-23", "boas-festas", ("Boas festas", "Obrigado por *2026*.", "Um ótimo fim de ano para ti e tua família."), "/",
"""Obrigado a cada cliente, parceiro e negócio de Porto Alegre que confiou no nosso trabalho em 2026.

Foi o ano em que a OnTheTop virou empresa de verdade, com cases que nos orgulham: negócios que saíram do fundo da lista do Google para o topo, campanhas que se pagaram e sites que deixaram de perder cliente.

Uma dica para as festas: muito cliente fica feliz com o atendimento de fim de ano. É um ótimo momento para pedir aquela avaliação no Google, com o link direto e sem oferecer nada em troca.

Boas festas, e até 2027."""),
("2026-12-28", "revisao-do-ano", ("Revisão do ano", "5 números para olhar *antes* de 2027.", "Sem número, o plano é chute."), TRAF,
"""Antes de virar o ano, cinco números para olhar no teu negócio:

Quantos clientes novos chegaram em 2026.
De onde eles vieram: Google, Instagram, indicação, anúncio.
Quanto custou trazer cada um (quando teve investimento).
Quanto um cliente deixa por ano, em média.
Quantas avaliações novas o perfil no Google recebeu.

Com esses cinco, dá para saber onde investir em 2027 e onde parar de gastar. Se faltar algum, esse é o primeiro ajuste do ano: começar a medir."""),
("2026-12-30", "ordem-certa-2027", ("Para 2027", "Perfil, site e anúncio, *nessa* ordem.", "A base primeiro, a verba depois."), "/",
"""Se a meta de 2027 é ter mais clientes vindos da internet, a ordem importa:

Primeiro o Perfil da Empresa no Google, completo e com rotina de avaliações. É de graça e é onde o cliente local procura.
Depois o site, rápido no celular e ligado ao perfil.
Só então o anúncio, com rastreamento e conta feita.

Anunciar antes de arrumar a base é pagar para levar o cliente até uma porta mal sinalizada.

Feliz 2027. Se quiser começar o ano com o diagnóstico do teu negócio, chama a gente pelo botão."""),
]

PROIBIDO = [r"\(?\d{2}\)?\s?9\d{4}-?\d{4}", r"wa\.me", r"garant", r"100 ?%", r"\bmelhor agência"]


def render(p, arquivo):
    eb, h1, sb = p
    h1 = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(h1))
    sb = html.escape(sb).replace("\n", "<br>")
    tpl = open(os.path.join(ANTIGAS, "post.html"), encoding="utf-8").read()
    tpl = tpl.replace("./fonts", FONTS)
    tpl = tpl.replace("url(logo.jpeg)", f"url(file://{ANTIGAS}/logo.jpeg)")
    tpl = re.sub(r'<div class="eb">.*?</div>', f'<div class="eb">{html.escape(eb)}</div>', tpl)
    tpl = re.sub(r"<h1>.*?</h1>", f"<h1>{h1}</h1>", tpl, flags=re.S)
    tpl = re.sub(r'<div class="sb">.*?</div>', f'<div class="sb">{sb}</div>', tpl, flags=re.S)
    tmp = arquivo.replace(".jpg", ".html")
    open(tmp, "w", encoding="utf-8").write(tpl)
    png = arquivo.replace(".jpg", ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                    "--window-size=1200,900", f"--screenshot={png}", f"file://{tmp}"], check=True, capture_output=True)
    from PIL import Image
    Image.open(png).convert("RGB").save(arquivo, quality=88)
    os.remove(png); os.remove(tmp)


def main():
    os.makedirs(OUT, exist_ok=True)
    erros, linhas = [], ["# Posts Google OnTheTop · out-dez/2026\n\n3 por semana (seg/qua/sex 10h). Botão: Saiba mais.\n"]
    datas = [p[0] for p in POSTS]
    assert len(set(datas)) == len(datas), "data repetida"
    for i, (data, slug, arte, link, texto) in enumerate(POSTS, 1):
        d = datetime.date.fromisoformat(data)
        if d.weekday() not in (0, 2, 4): erros.append(f"{data} não é seg/qua/sex")
        if len(texto) > 1500: erros.append(f"{data} {len(texto)} chars")
        for pad in PROIBIDO:
            if re.search(pad, texto, re.I): erros.append(f"{data} termo /{pad}/")
        nome = f"{i:02d}-{slug}.jpg"
        if isinstance(arte, str):
            src = os.path.join(ANTIGAS, arte)
            if not os.path.exists(src): erros.append(f"arte não existe {arte}")
            foto = src
        else:
            foto = os.path.join(OUT, nome)
            if "--force" in sys.argv or not os.path.exists(foto): render(arte, foto)
        url = BASE + link
        url = url.replace("#", "?" + UTM + "#", 1) if "#" in link else url + "?" + UTM
        linhas.append(f"\n## {i:02d} · {data} 10:00\nFoto: `{foto}`\nLink: {url}\n\n```\n{texto}\n```\n")
    for e in erros: print("ERRO", e)
    if erros: sys.exit(1)
    open(os.path.join(AQUI, "posts.md"), "w", encoding="utf-8").write("".join(linhas))
    json.dump([{"n": f"{i:02d}", "d": p[0], "t": p[4], "u": l.split("Link: ")[1].split("\n")[0], "foto": l.split("Foto: `")[1].split("`")[0]}
               for i, (p, l) in enumerate(zip(POSTS, linhas[1:]), 1)], open(os.path.join(AQUI, "posts.json"), "w"), ensure_ascii=False)
    print(f"{len(POSTS)} posts ok · maior {max(len(p[4]) for p in POSTS)} chars · artes em {OUT}")


if __name__ == "__main__":
    main()
