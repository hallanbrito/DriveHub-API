# Protocolo de Execução Agêntica — DriveHub / Método C.H.

Este documento define os procedimentos operacionais para agentes autônomos e assistentes de IA (AGY, Gemini CLI, Codex, ChatGPT) atuando nos repositórios do ecossistema DriveHub.

---

## 1. Princípios Operacionais Fundamentais
1. **Responsabilidade Humana Intransferível**: O Product Owner (Hallan) detém a autoridade e responsabilidade sobre decisões, escopo, segurança e homologação. O agente é um executor ou orquestrador agêntico, não um decisor soberano.
2. **Ciclo CHAVE Mandatório**:
   - **C — Contextualizar**: Inspecione o estado real dos repositórios, branches, arquivos, dependências e testes antes de agir.
   - **H — Harmonizar**: Defina e valide o escopo da Fatia W, limites, caminhos permitidos e critérios verificáveis.
   - **A — Agir**: Execute estritamente na branch isolada com autonomia calibrada (CH-0 a CH-3).
   - **V — Verificar**: Execute a suite de testes, linters, checagens de integridade e diffs. Nunca declare aprovação sem execução real.
   - **E — Evoluir**: Produza o Pacote de Evidências / RUC, submeta Draft PR e aguarde parecer do orquestrador e decisão do PO.
3. **Isolamento de Branches**: Nunca comite diretamente em `main`. Trabalhe exclusivamente em branches isoladas de W.

4. **Estratégia de Reversão Auditável**:
   - Qualquer reversão pós-integração deve ser proporcional ao método de merge efetivamente utilizado:
     - **Caso A — Merge Commit:** Se a integração produziu commit de merge com dois ou mais pais (primeiro pai representando `main`), reverter via `git revert -m 1 <merge-commit-sha>`, após confirmação prévia dos pais.
     - **Caso B — Squash Merge:** Se a integração produziu commit consolidado único, reverter via `git revert <squash-commit-sha>`.
     - **Caso C — Rebase Merge:** Se a integração preservou múltiplos commits lineares, identificar todos os commits introduzidos e revertê-los em ordem cronológica inversa de forma auditável (não assumir existência de merge commit).
   - **Política Geral de Rollback:**
     - Nunca aplicar `git reset --hard` à `main` como estratégia normal de rollback.
     - Não executar comandos destrutivos automaticamente.
     - Verificar e assegurar árvore de trabalho limpa antes da reversão.
     - Registrar SHA, motivo, impacto, resultado e evidências no histórico/RUC.
     - Validar a aplicação (testes e build) imediatamente após a reversão.
     - Exigir autorização explícita do PO antes de executar qualquer reversão real.

---

## 2. Gates de Qualidade e Critérios de Conclusão (DoD)
Antes de finalizar qualquer intervenção técnica, o agente deve comprovar:
- [ ] Árvore de trabalho limpa (`git status` sem arquivos não rastreados ou pendentes).
- [ ] Suite de testes automatizados executada e 100% aprovada (`pytest -v`).
- [ ] Ausência de segredos, chaves privadas ou credenciais reais versionadas.
- [ ] Nenhuma alteração fora dos caminhos e escopo autorizados na Fatia W.
- [ ] Documentação de governança (`docs/STATUS.md`, `docs/CH/DECISOES.md`) devidamente atualizada com dados fáticos.
- [ ] Draft PR criado com descrição clara dos commits, evidências e plano de reversão.
- [ ] Estado final declarado obrigatoriamente como: **AGUARDANDO REAUDITORIA DO ORQUESTRADOR E ACEITE DO PO**.
