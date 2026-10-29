# W0 — Governança e Fundação do Método C.H. (DriveHub-API)

## Identidade
- **Objetivo:** Estabelecer a fundação de governança do Método C.H. no repositório `DriveHub-API`, integrando documentação de projeto, papéis, decisões, templates de processo e especificações de contrato.
- **Valor Esperado:** Rastreabilidade estrita, previsibilidade na colaboração humano-IA, contratos de integração claros com o frontend e conformidade com o Método C.H. v0.1.
- **Responsável Humano (PO):** Hallan
- **Orquestrador:** ChatGPT
- **Executor Agêntico:** AGY (Google Antigravity)
- **Nível de Autonomia:** CH-2 (autorizado estritamente para W0)

---

## C — Contextualizar
- **Baseline (branch/commit):** Branch `main` em `829da97afe6e2237ea48b1e6ec84dd969bd262cf`.
- **Fonte de Verdade Consultada:**
  - Repositório normativo: `https://github.com/hallanbrito/metodo-ch`
  - Repositório local: `/home/hallan/.gemini/antigravity/worktrees/DriveHub-API/metodo_ch_auditoria_w0`
- **Estado Atual:** Aplicação com Clean Architecture consolidada, 32 testes aprovados em pytest, mas sem documentação formal de governança C.H., sem templates de W/ADR/Evidências e sem formalização do contrato de integração.
- **Riscos Conhecidos:** 
  - O SQLite local não implementa row-level locking.
  - O frontend consome endpoints de aprovação e conclusão sem autenticação gerencial.

---

## H — Harmonizar

### Escopo Autorizado
- Criação dos arquivos de governança: `AGENTS.md`, `docs/PROJETO.md`, `docs/STATUS.md`, `docs/ARQUITETURA.md`.
- Criação da pasta `docs/CH/` com `DECISOES.md`, `PROTOCOLO_AGENTES.md`, `INTEGRACAO_CONTRATO.md` e `W0-GOVERNANCA.md`.
- Criação da pasta `docs/adr/` com `0001-adocao-metodo-ch-e-clean-architecture.md`.
- Criação da pasta `docs/templates/` com templates de ADR, Fatia W e Pacote de Evidências.
- Atualização do `README.md` com menção explícita ao Método C.H. e links para os novos documentos.

### Fora do Escopo
- Modificar regras de negócio em `core/` ou `apps/`.
- Alterar models, migrations, banco de dados ou schemas existentes.
- Executar merge na branch `main`.
- Alterar comportamento funcional ou de autenticação da aplicação.

### Decisões Aprovadas
- Adoção da estrutura documental proporcional ao porte da aplicação (ADR-0001).
- Definição do contrato full-stack com `DriveHub-Web`.

### Critérios de Aceitação Verificáveis
- [x] T01: Arquivos de governança criados conforme as diretrizes do Método C.H.
- [x] T02: Templates de ADR, Fatia W e Pacote de Evidências disponibilizados em `docs/templates/`.
- [x] T03: `README.md` atualizado com referências e links à governança.
- [x] T04: Suite de 32 testes automatizados executada e 100% aprovada (`pytest -v`).
- [x] T05: Draft PR aberto para revisão do orquestrador e aceite do PO.

### Estratégia de Reversão e Rollback Auditável
- **Pós-Integração (procedimento conforme método efetivo de merge em `main`):**
  - **Caso A — Merge Commit:** Quando a integração produzir commit de merge com dois ou mais pais (onde o primeiro pai representa a linha principal `main`):
    ```bash
    git revert -m 1 <merge-commit-sha>
    ```
    *Nota:* Confirmar previamente os pais e a direção da integração via `git log --parents -1 <merge-commit-sha>`.
  - **Caso B — Squash Merge:** Quando a integração produzir um único commit consolidado:
    ```bash
    git revert <squash-commit-sha>
    ```
  - **Caso C — Rebase Merge:** Quando a integração preservar múltiplos commits lineares:
    - Identificar todos os commits introduzidos pela fatia W0.
    - Avaliar a ordem segura de reversão (da ponta mais recente para a mais antiga).
    - Reverter os commits aplicáveis de forma individual e auditável (`git revert <commit-sha>`).
    - Não assumir que existe um merge commit.
- **Política Geral de Rollback:**
  - Nunca aplicar `git reset --hard` à `main` como estratégia normal de rollback.
  - Não executar comandos destrutivos automaticamente.
  - Verificar a árvore de trabalho (`git status` limpo) antes de qualquer reversão.
  - Registrar SHA, motivo, impacto, resultado e evidências documentais no RUC e histórico.
  - Validar a aplicação (executar testes e verificação de integridade) imediatamente após o rollback.
  - Exigir autorização explícita e formal do PO antes de executar uma reversão real.
- **Pré-Integração (na branch isolada de trabalho):**
  - Para anular alterações na branch antes do merge: `git revert <commit-sha>`.
  - Se a fatia for rejeitada integralmente pelo PO antes do merge: a branch de trabalho pode ser fechada e arquivada ou descartada sem afetar a estabilidade de `main`.

---

## A — Agir
- **Ambiente Isolado:** Worktree dedicada `/home/hallan/.gemini/antigravity/worktrees/DriveHub-API/metodo_ch_auditoria_w0`.
- **Branch:** `metodo_ch_auditoria_w0`.
- **Condição de Parada:** Conclusão da criação documental, execução de testes sem regressão e criação do Draft PR.

---

## V — Verificar
- **Suite de Testes:** 32 testes executados com sucesso (0 falhas).
- **Diff:** Restrito estritamente a arquivos `.md` de governança e documentação.
- **Segurança:** Nenhuma credencial ou variável sensível adicionada.

---

## E — Evoluir
- **Estado:** AGUARDANDO REAUDITORIA DO ORQUESTRADOR E ACEITE DO PO.
