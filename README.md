# Skills SEO Google Meu Negócio (GBP)

Duas skills do Claude Code pro serviço de GMN da Winners/OnTheTop, no método Localo.

- `primeira-pagina/` — protocolo completo: prospect, audit (24 checks), baseline, plano, semana e relatório. Roda via MCP do Localo.
- `agendar-gbp/` — agenda posts e fotos do Google no Localo pelo Chrome.

## Instalar
Copiar as duas pastas pra `.claude/skills/` do projeto (ou `~/.claude/skills/`) e ligar o MCP do Localo:

```
claude mcp add --scope user --transport http localo https://api.localo.com/api/mcp --header "Authorization: Bearer <ORG_ID>:<TOKEN>"
```

Uso: `/primeira-pagina` e `/agendar-gbp`.
