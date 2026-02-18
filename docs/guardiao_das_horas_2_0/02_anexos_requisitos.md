# GDH2 — Anexos: Requisitos (v1)

Abaixo estão os conteúdos originalmente gerados como documentos DOCX nas discussões.

---

# GDH2 — Levantamento de Requisitos (v1)

Fonte: Guardiao_das_Horas_2_0_Levantamento_de_Requisitos_v1.docx

---

Guardião das Horas 2.0
Levantamento de Requisitos (v1)
Escopo: Controle de escala/plantões, banco de horas, compensações e ajuda de custo (alimentação)
Stack alvo: Python + Flask + SQLAlchemy | Banco: PostgreSQL
Data: 2026-02-18
Princípios: Seguro • Simples • Boas práticas • Moderno • Regras de negócio bem definidas

## 1. Contexto e objetivos

### Objetivo do sistema
Controlar escala planejada e serviço realizado, contabilizar banco de horas, permitir compensações e produzir relatórios mensais/trimestrais confiáveis para DRH e COB.
O sistema não realiza pagamentos: calcula e persiste snapshots de cálculos para auditoria e exportação.

### Atores (papéis operacionais)
- CIA (Companhia): planeja e publica a escala mensal; realiza fechamentos mensal e trimestral; aprova desvios e lança eventos neutros quando aplicável.
- Auxiliar/CBU/Chefe de serviço: confirma diariamente o serviço realizado; registra desvios (hora extra, permuta, faltas) que seguem para aprovação.
- COB: recebe relatórios trimestrais fechados para acompanhamento (saldo convertido em dias).
- DRH: recebe relatórios mensais fechados para cálculo de ajuda de custo (descontos cabíveis conforme legislação).

### Escopo organizacional
Hierarquia operacional principal: COB → BBM/CIA IND → CIA → (PEL | PA | BRIGADA).
PEL, PA e BRIGADA compartilham o mesmo escopo (ancorado na CIA).

## 2. Requisitos Funcionais (RF)
- RF-001 — Cadastro e gestão de unidades (Org Units)
  - Cadastrar COB, BBM, CIA IND, CIA, PEL, PA e BRIGADA.
  - Relacionamentos hierárquicos e escopo canônico por CIA.
- RF-002 — Cadastro e gestão de militares
  - Manter cadastro mínimo (identificadores, nome de guerra, status, lotação vigente).
  - Histórico de lotação e regimes (vigência sem sobreposição).
- RF-003 — Cadastro de regimes e metas (jornadas)
  - Regimes padrão conforme legislação (8h, 12h, 24h).
  - Jornada reduzida altera meta mensal (parametrizada por vigência).
- RF-004 — Planejamento de escala mensal (baseline)
  - CIA cria e publica escala mensal por escopo.
  - Itens de escala por dia/turno com local e militar previsto.
- RF-005 — Confirmação do real diário (serviço realizado)
  - Auxiliar confirma a escala do dia (auto-aprovação quando coincide).
  - Registro de desvios (extra, permuta, substituição, falta) gera pendência de aprovação CIA.
- RF-006 — Registro de eventos/intercorrências
  - Férias, licenças, afastamentos e demais eventos conforme catálogo.
  - Eventos “períodos neutros” não aumentam nem reduzem saldo e seguem legislação.
- RF-007 — Permutas de serviço
  - Registrar permuta (swap) com relação aos itens planejados e/ou serviço realizado.
  - Aplicar regras de aprovação e auditoria.
- RF-008 — Banco de horas e compensações
  - Lançamentos em ledger append-only.
  - Compensações consomem saldo disponível, respeitando regras de precedência.
- RF-009 — Fechamento mensal (CIA)
  - Fechamento por militar e escopo com snapshot persistido (meta, trabalhado, saldo, justificativas).
  - Exportação para DRH (ajuda de custo).
- RF-010 — Fechamento trimestral (CIA)
  - Trimestres fixos: jan-mar, abr-jun, jul-set, out-dez.
  - Converter frações completas de 24h (1440 min) não utilizadas no trimestre em dias para férias.
  - Saldo remanescente em minutos permanece disponível como horas para compensações.
  - Exportação para COB.
- RF-011 — Ajuda de custo (alimentação)
  - Cálculo mensal com base em relatórios fechados.
  - Regra operacional: “ajuda cheia” menos descontos cabíveis conforme legislação.
  - Persistir cálculo/snapshot para auditoria (sem executar pagamentos).
- RF-012 — Importação e exportação de dados por escopo
  - Importar dados (cargas) com validação e dry-run.
  - Exportar relatórios/dados conforme escopo e permissões.
  - (Detalhado em anexo específico.)
- RF-013 — Auditoria e trilha de alterações
  - Log de ações (quem, quando, o quê) em objetos críticos: escala, real diário, eventos, aprovações, fechamentos.
- RF-014 — Controle de acesso por escopo (RBAC/ABAC)
  - Permissões por papel e por escopo (CIA vs Auxiliar vs COB vs DRH).
  - (Detalhado em anexo específico.)
- RF-015 — Relatórios e consultas
  - Relatórios mensais (DRH) e trimestrais (COB) exportáveis.
  - Consultas operacionais: pendências, desvios, saldos por militar, histórico.

## 3. Requisitos Não-Funcionais (RNF)
- RNF-001 — Segurança
  - Autenticação forte (hash de senha, sessões seguras).
  - Autorização por escopo e trilha de auditoria.
  - Princípio do menor privilégio.
- RNF-002 — Confiabilidade e integridade
  - Constraints no banco (EXCLUDE/UNIQUE) para impedir sobreposição e duplicidade.
  - Idempotência para import e ledger.
- RNF-003 — Manutenibilidade
  - Domínio separado do ORM.
  - Padrão de camadas (domain/application/infra/web).
  - Migrations como fonte de verdade.
- RNF-004 — Observabilidade
  - Logs estruturados e métricas de pendências/erros.
- RNF-005 — Performance
  - Índices adequados (GIST em ranges).
  - Consultas eficientes por escopo e período.
- RNF-006 — Portabilidade e DX
  - PostgreSQL em todos os ambientes.
  - Bootstrap simples com Poetry.

## 4. Itens em aberto / decisões a confirmar
- Catálogo final de eventos e períodos neutros conforme legislação anexada.
- Regras exatas de desconto da ajuda de custo por tipo de evento (base legal).
- Formato padrão de export para DRH/COB (CSV, XLSX, PDF), com versionamento.

---

# GDH2 — Requisitos: Escala Dinâmica, Transferências e Banco de Horas (v1)

Fonte: Requisitos_Escala_Dinamica_Transferencias_BancoHoras_Guardiao_2_0_v1.docx

---

Guardião das Horas 2.0 — Requisitos
Escala dinâmica, transferências, banco de horas e precedência de regras (v1)

## Contexto
A realidade operacional exige que o ciclo/jornada de um militar possa mudar com frequência (missões, viagens, permutas, reforços, afastamentos).
O sistema deve permitir registrar uma escala “planejada” (baseline) e o “real do dia”, sem engessar regras no ciclo.

## Objetivo
Preservar integridade, auditabilidade e continuidade do histórico/saldos, mesmo com mudanças de escala, lotação e escopo.

## 1) Jornada/ciclo: templates vs parametrização
### Templates pré-cadastrados
O sistema deve oferecer templates de jornada/ciclo conforme legislação anexada.
Ex.: 8h, 12h, 24h (e variações autorizadas).

### Parâmetros que podem variar
- Meta mensal (minutos) por regime vigente.
- Distribuição de turnos no mês (planejamento), sem alterar regra de cálculo.

### Possibilidade de ciclos personalizados (opcional)
Viável, desde que:
(a) o ciclo personalizado não quebre o fechamento mensal/trimestral;
(b) seja vinculado por vigência e auditável;
(c) não substitua as regras legais, apenas parametrize o planejamento.

## 2) Dinâmica operacional: baseline x real
### Baseline mensal (planejado)
- Lançado pela CIA por escopo.
- Serve como referência para conferência e para detectar desvios.

### Real do dia (executado)
- Lançado pelo Auxiliar do dia.
- Se coincidir com o planejado → aprovação automática.
- Se divergir (hora extra, permuta, substituição, ausência) → pendente para aprovação CIA.

## 3) Períodos neutros
### Definição
Períodos neutros não acrescentam nem retiram saldo.

### Padrões
Devem seguir a legislação anexada.

### Fluxo
Normalmente repassados para a CIA lançar/validar.

## 4) Transferências (mudança de escopo/unidade)
### Requisito central
O militar leva seus saldos e histórico para onde for transferido.

### Mudanças comuns
- Mudança de BBM/CIA IND, CIA, PEL/PA/BRIGADA, ou estruturas administrativas.
- Mudança de escala/jornada após transferência.

### Implementação (requisito de domínio)
- Lotação por vigência (assignment) sem sobreposição.
- Escopo canônico independente da árvore real.
- Saldos vinculados ao militar (não “ficam” na unidade).
- Relatórios e fechamentos respeitam o escopo do período.

## 5) Banco de horas e conversão em dias
### Cálculo por fechamento
- Fechamento mensal observa meta mensal (ex.: 160h em minutos, ou jornada reduzida).
- Fechamento trimestral em trimestres fixos.

### Conversão em dias (trimestral)
- Converter apenas blocos completos de 24h (1440 min) não utilizados no trimestre.
- Saldo restante de minutos permanece disponível para compensação.

## 6) Aprovação e auditoria
- Todo desvio do real em relação ao planejado gera registro auditável e requer aprovação CIA.
- Todas as alterações relevantes devem gerar audit_log.

---

# GDH2 — Requisitos: Importação e Exportação por Escopo (v1)

Fonte: Requisitos_Importacao_Exportacao_por_Escopo_GDH2_v1.docx

---

Guardião das Horas 2.0 — Requisitos
Importação e Exportação por escopo e permissões (v1)

## Objetivo
Permitir carga e extração de dados de forma segura, auditável e idempotente, respeitando escopo e permissões.

## 1) Requisitos de Importação
### Importar por escopo
Toda importação deve estar vinculada a um escopo (CIA/BBM/CIA IND etc.).
Usuário deve ter permissão explícita no escopo.

### Dry-run obrigatório
O sistema deve permitir simulação (dry-run) mostrando:
- registros válidos/inválidos,
- impacto esperado,
- conflitos detectados.

### Idempotência
Importações devem ser idempotentes, evitando duplicidades quando o mesmo arquivo for enviado novamente.
Sugestão: hash do arquivo + escopo + competência/período.

### Validações
- Validação de schema (colunas/formatos).
- Validação de regras (sobreposição, duplicidade, coerência de período).
- Bloqueio de órfãos: sem criar referências quebradas.

### Trilha de auditoria
Guardar:
- quem importou,
- quando,
- arquivo (hash),
- resultado,
- linhas processadas,
- erros.

## 2) Requisitos de Exportação
### Exportar por escopo
Usuário só exporta dados do escopo permitido.

### Exportações típicas
- Relatório mensal fechado para DRH (ajuda de custo).
- Relatório trimestral fechado para COB (saldo/dias).
- Consultas operacionais (pendências, saldos, históricos).

### Formatos
- CSV/XLSX para dados tabulares.
- PDF opcional para relatórios “oficiais”.

### Versionamento
Export deve carregar:
- competência,
- versão de regras (rule_version),
- data/hora,
- escopo,
- assinatura/identificador.

## 3) Segurança e governança
- Princípio do menor privilégio.
- Logs de export.
- Mascaramento de campos sensíveis quando aplicável.
