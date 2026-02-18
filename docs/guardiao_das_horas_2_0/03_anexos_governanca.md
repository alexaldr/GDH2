# GDH2 — Anexos: Governança (Permissões + Catálogos) (v1)

Abaixo estão os conteúdos originalmente gerados como documentos DOCX nas discussões.

---

# GDH2 — Matriz de Permissões por Escopo (v1)

Fonte: Matriz_Permissoes_Escopo_GDH2_v1.docx

---

Matriz de Permissões por Escopo — GDH 2.0 (v1)

## Objetivo
Definir RBAC/ABAC para operações por escopo, separando: quem lança (Auxiliar), quem aprova/fecha (CIA), e quem consulta/recebe (COB/DRH).

## Princípios
- Menor privilégio.
- Separação de funções (SoD): lançar ≠ aprovar.
- Escopo canônico (CIA) controla permissões para PEL/PA/BRIGADA.

## Papéis (exemplos)
- Admin Global: configurações gerais, catálogo, gestão de usuários e papéis.
- CIA Gestor: planejar/publicar escala, aprovar desvios, lançar neutros, fechar mensal/trimestral, exportar DRH/COB.
- Auxiliar Operacional: confirmar real do dia, propor desvios, registrar ocorrências operacionais, consultar pendências do dia.
- COB Consultor: consultar/baixar relatórios trimestrais fechados (somente leitura).
- DRH Consultor: consultar/baixar relatórios mensais fechados para ajuda de custo (somente leitura).

## Operações críticas e permissões
### Escala (baseline)
- Criar/editar rascunho: CIA Gestor.
- Publicar: CIA Gestor.
- Cancelar item: CIA Gestor (gera log).

### Real do dia
- Criar/confirmar quando bate: Auxiliar (auto-aprovação).
- Criar com desvio: Auxiliar (status pendente).
- Aprovar/rejeitar desvio: CIA Gestor.

### Eventos
- Criar neutros: CIA Gestor.
- Criar eventos operacionais: Auxiliar (alguns tipos), outros restritos à CIA.
- Aprovar eventos: CIA Gestor.

### Fechamentos
- Fechar mensal: CIA Gestor.
- Reabrir: CIA Gestor (com justificativa e log).
- Fechar trimestral: CIA Gestor.

### Exportações
- Export mensal (DRH): CIA Gestor / DRH (se permitido) somente leitura.
- Export trimestral (COB): CIA Gestor / COB somente leitura.

### Importações
- Criar/importar: restrito (Admin Global e/ou CIA Gestor com permissão específica).
- Dry-run obrigatório.

### Auditoria
Todas as ações acima geram audit_log com user_id, escopo, objeto e diffs básicos.

---

# GDH2 — Catálogos e Regras de Precedência (v1)

Fonte: Catalogos_e_Regras_de_Precedencia_GDH2_v1.docx

---

Catálogos e Regras de Precedência — GDH 2.0 (v1)

## 1) Catálogo de tipos (eventos e lançamentos)
### Event Types (intercorrências)
- Férias
- Licença
- Afastamento
- Missão/viagem
- Dispensa
- Outros conforme legislação/anexos

### Tipos operacionais
- Serviço planejado
- Serviço realizado
- Hora extra
- Permuta
- Ausência

### Períodos neutros
**Definição:** não aumentam nem reduzem saldo (nem horas, nem ajuda de custo), conforme base legal.

## 2) Regras de precedência
### Baseline vs Real
- Real do dia prevalece sobre baseline quando aprovado.
- Se real coincide com baseline → auto-aprovação.
- Se diverge → requer aprovação CIA.

### Eventos vs Real
- Eventos aprovados podem justificar ausência ou alterar elegibilidade (ex.: desconto ajuda de custo), sem necessariamente criar horas.
- Períodos neutros não alteram saldo.

### Fechamentos
- Fechamento gera snapshot: meta, trabalhado, saldo, descontos e rule_version.
- Reabertura deve registrar motivo e criar novo snapshot (sem apagar histórico).

## 3) Versionamento de regras
### rule_version
- Cada fechamento e export carrega uma versão de regras para rastreabilidade.
- Mudanças em regras (catálogo, cálculo) devem gerar incremento de rule_version.

## 4) Idempotência e consistência
- Ledger append-only: correções por novos lançamentos (não editar passado sem trilha).
- Import/export com hash e controle de duplicidade.
