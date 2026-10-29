# Instruções aos Agentes — DriveHub-API / Método C.H.

> **Governança:** Método Ágil C.H. (Colaboração Híbrida)  
> **Fonte Normativa:** [hallanbrito/metodo-ch](https://github.com/hallanbrito/metodo-ch)  
> **Papéis:** Product Owner (Hallan) | Orquestrador (ChatGPT) | Executor Agêntico (AGY / outros autorizados)

---

## 1. Regras Obrigatórias Pré-Ação
1. **Consulte a Fonte da Verdade**: Leia `docs/PROJETO.md`, `docs/STATUS.md`, `docs/CH/PROTOCOLO_AGENTES.md` e a Fatia W correspondente antes de qualquer modificação.
2. **Reconstrua o Baseline**: Registre obrigatoriamente o commit SHA do baseline, a branch isolada de trabalho, o status da árvore de trabalho e o nível de autonomia formalmente autorizado pelo PO.
3. **Escopo e Limites Fechados**: Execute estritamente o escopo delimitado na Fatia W. Nunca interprete instruções gerais como autorização para merge, alteração de contratos públicos, deleção de arquivos ou mutação em produção.

---

## 2. Níveis de Autonomia Operacional
- **CH-0 (Consultar)**: Leitura, inspeção e análise técnica. Nenhuma modificação no repositório.
- **CH-1 (Propor)**: Elaboração de propostas, RFCs, diffs conceituais e planos de ação. Não altera código-fonte funcional nem fontes de verdade integradas.
- **CH-2 (Executar Isolado)**: Criação de branch isolada (`metodo_ch_auditoria_w0`, `agy/wXX-...`), implementação dentro do escopo, testes automatizados locais, commits rastreáveis e abertura de **Draft PR**. Proibido qualquer merge ou deploy.
- **CH-3 (Integrar Condicionado)**: Integração condicionada por gates pré-definidos. *Atenção: A política do projeto exige decisão humana e aprovação formal do PO antes de qualquer integração em `main`.*

---

## 3. Diretrizes de Qualidade e Segurança
- **Segurança Absoluta**: Proibido versionar credenciais, segredos, chaves de API, senhas ou dados sensíveis. O arquivo `.env` nunca deve ser comitado.
- **Testes Obrigatórios**: Nenhuma entrega pode ser dada como concluída sem execução real e aprovação da suite de testes (`pytest -v`). Nunca assuma que testes passam sem executá-los.
- **Separação Epistêmica**: Em relatórios e evidências, diferencie rigorosamente:
  - `OBSERVADO`: Fato diretamente verificado em execução ou consulta real.
  - `DECLARADO`: Afirmação recebida de terceiros sem checagem direta.
  - `INFERIDO`: Conclusão lógica derivada de premissas.
  - `NÃO_VERIFICADO`: Ausência de teste ou verificação direta.
- **Estratégia de Rollback Auditável**: Qualquer reversão pós-integração deve ser proporcional ao método de merge utilizado (Merge Commit: `git revert -m 1 <merge-sha>`; Squash Merge: `git revert <squash-sha>` sem `-m`; Rebase Merge: reversão ordenada dos commits lineares). Nunca aplicar `git reset --hard` à `main` nem executar push direto em `main`. Reversões pós-integração devem tramitar via branch isolada e Pull Request, sujeitas aos gates automatizados e ao aceite do PO. Reversões reais exigem árvore limpa, autorização prévia do PO, registro de evidências e validação pós-reversão.
- **Entrega e Fechamento**: Toda fatia agêntica termina com a árvore de trabalho limpa, Draft PR submetido e Pacote de Evidências / RUC preenchido. O estado final é sempre **AGUARDANDO REAUDITORIA DO ORQUESTRADOR E ACEITE DO PO**.
