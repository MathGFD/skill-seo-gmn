"""Valida o calendario-6-meses.md e gera posts-prontos.md com CREFITO e UTM.

Uso: python3 checar.py [--crefito 123456-F]
Sem --crefito so valida (e avisa que falta).
"""
import datetime, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FOTOS = os.path.expanduser("~/Desktop/FOTOS-CLIENTE/SELECIONADAS-GOOGLE")
BASE = "https://site-do-cliente.com"
UTM = "utm_source=google&utm_medium=gbp&utm_campaign=post"
ASSINATURA = "Nome do Profissional · Especialidade · CREFITO-X {CREFITO}"
LIMITE = 1500  # Google posts
# COFFITO art. 15/40 + Google (telefone no texto derruba o post)
PROIBIDO = [r"R\$", r"\bpreço", r"\bvalor(?:es)? de\b", r"garant", r"\bmelhor (?:clínica|resultado)", r"antes e depois",
            r"\b100 ?%", r"\binfalível", r"\(?\d{2}\)?\s?9?\d{4}-?\d{4}", r"wa\.me", r"desconto", r"promoç"]


def ler(caminho):
    txt = open(caminho, encoding="utf-8").read()
    bloco = txt.split("<!-- FIM POSTS -->")[0]
    partes = re.split(r"^## (\d\d) \| (\S+) \| (\S+) \| (\S+)\n", bloco, flags=re.M)[1:]
    return [dict(n=partes[i], data=partes[i + 1], foto=partes[i + 2], link=partes[i + 3], corpo=partes[i + 4].strip())
            for i in range(0, len(partes), 5)]


def montar(p, crefito):
    texto = p["corpo"] + "\n\n" + ASSINATURA.replace("{CREFITO}", crefito or "{CREFITO}")
    url = BASE + p["link"]
    url = url.replace("#", "?" + UTM + "#", 1) if "#" in url else url + "?" + UTM
    return texto, url


def checar(posts, crefito):
    erros = []
    for p in posts:
        texto, _ = montar(p, crefito or "000000-F")
        if len(texto) > LIMITE:
            erros.append(f"{p['n']}: {len(texto)} caracteres (>{LIMITE})")
        for padrao in PROIBIDO:
            if re.search(padrao, p["corpo"], re.I):
                erros.append(f"{p['n']}: termo proibido /{padrao}/")
        if datetime.date.fromisoformat(p["data"]).weekday() != 1:
            erros.append(f"{p['n']}: {p['data']} não é terça")
        f = os.path.join(FOTOS, p["foto"])
        if not os.path.exists(f):
            erros.append(f"{p['n']}: foto não existe {p['foto']}")
        elif not 10_000 <= os.path.getsize(f) <= 5_000_000:
            erros.append(f"{p['n']}: foto fora de 10KB-5MB")
    datas = [p["data"] for p in posts]
    if len(set(datas)) != len(datas):
        erros.append("datas repetidas")
    return erros


if __name__ == "__main__":
    # self-check do parser e das regras
    fake = [dict(n="99", data="2026-10-13", foto="x.jpg", link="/#a", corpo="Ligue (11) 90000-0000, preço ótimo")]
    e = checar(fake, None)
    assert any("proibido" in x for x in e) and any("foto" in x for x in e), e
    assert montar(fake[0], "1-F")[1] == BASE + "/?" + UTM + "#a"

    crefito = sys.argv[sys.argv.index("--crefito") + 1] if "--crefito" in sys.argv else None
    posts = ler(os.path.join(AQUI, "calendario-6-meses.md"))
    erros = checar(posts, crefito)
    print(f"{len(posts)} posts | {posts[0]['data']} → {posts[-1]['data']}")
    print("maior:", max(len(montar(p, '000000-F')[0]) for p in posts), "caracteres")
    for x in erros:
        print("ERRO", x)
    if erros:
        sys.exit(1)
    if not crefito:
        print("OK, mas falta --crefito: posts-prontos.md não foi gerado")
        sys.exit(0)
    out = ["# Posts prontos pra colar no Localo\n", "Botão: **Saiba mais**. Horário: 10:00.\n"]
    for p in posts:
        texto, url = montar(p, crefito)
        out.append(f"\n## {p['n']} · {p['data']} 10:00\nFoto: `{p['foto']}`\nLink: {url}\n\n```\n{texto}\n```\n")
    open(os.path.join(AQUI, "posts-prontos.md"), "w", encoding="utf-8").write("".join(out))
    print("posts-prontos.md gerado")
