# 🚀 Fluxo de Desenvolvimento — Simulação com Agentes Inteligentes

## 📌 Visão Geral

Este fluxo foi otimizado para execução prática, reduzindo riscos comuns como:
- retrabalho
- falhas de integração
- problemas com LLM
- atraso na entrega

---

# 🔹 Etapa 0 — Kickoff (ANTES DE TUDO)

## Objetivo
Evitar retrabalho e alinhar o time

## Tarefas
- Definir tema da simulação
- Definir escopo MVP (mínimo viável)
- Escolher stack (Python)
- Criar repositório Git com:
  - README.md
  - estrutura inicial

## Entregável
- README com:
  - descrição da ideia
  - objetivo
  - definição inicial dos agentes

---

# 🧠 Etapa 1 — Modelagem Teórica

## Objetivo
Garantir os 50% da nota (exatidão teórica)

## Tarefas
- Definir PEAS completo:
  - Performance
  - Environment
  - Actuators
  - Sensors

- Classificar as 6 dimensões:
  - Observabilidade
  - Número de agentes
  - Determinismo
  - Episódico vs Sequencial
  - Estático vs Dinâmico
  - Discreto vs Contínuo

## 🔥 Definições críticas

### Contrato do ambiente
    input: estado atual
    output: percepções

### Contrato dos agentes
    input: percepção
    output: ação

## Entregável
- Documento validado com:
  - PEAS completo
  - classificação correta
  - fluxo percepção → decisão → ação

---

# 🏗️ Etapa 2 — Construção do Ambiente

## Objetivo
Criar o “motor” da simulação

## Estrutura sugerida
    /environment
    /agents
    /simulation

## Tarefas
- Implementar estado do mundo
- Criar loop da simulação:

    while True:
        perceber()
        decidir()
        agir()
        atualizar_estado()

- Criar logs claros no terminal

## ⚠️ Importante
Rodar o ambiente SEM agentes primeiro

## Entregável
- Simulação rodando (mesmo sem inteligência)

---

# 🤖 Etapa 3 — Agente Clássico

## Objetivo
Garantir funcionamento base

## Tarefas
- Implementar agente:
  - reflexo simples ou baseado em regras
- Integrar com ambiente

## Por que fazer primeiro?
- Mais simples
- Determinístico
- Ajuda a validar o ambiente

## Entregável
- Agente funcional integrado

---

# 🧠 Etapa 4 — Agente com LLM

## Objetivo
Adicionar inteligência baseada em LLM

## Tarefas

### Prompt base
    Você é um agente no ambiente X.
    Seu objetivo é Y.
    Percepção atual: {estado}
    Responda apenas com a ação.

### Função de decisão
    def decidir(percepcao):
        resposta = llm(prompt)
        return acao

## ⚠️ Boas práticas

### Validar saída
    if acao not in acoes_validas:
        fallback()

### Debug
    print("LLM:", resposta)

## Entregável
- Agente LLM tomando decisões válidas

---

# 🔗 Etapa 5 — Integração

## Objetivo
Fazer todos os componentes funcionarem juntos

## Tarefas
- Rodar:
  - ambiente + agente clássico + LLM
- Ajustar:
  - conflitos
  - estados inválidos
  - tempo de execução

## Ordem de execução sugerida
    1. agente clássico
    2. agente LLM

## Entregável
- Simulação completa funcionando

---

# 📊 Etapa 6 — Refinamento

## Objetivo
Aumentar criatividade e complexidade (30% da nota)

## Ideias
- competição entre agentes
- cooperação
- sistema de pontuação
- eventos aleatórios

## Entregável
- Interação interessante e não trivial

---

# 📄 Etapa 7 — Relatório

## Objetivo
Documentar corretamente o projeto

## Tarefas
- Inserir:
  - PEAS
  - análise das dimensões
- Adicionar exemplos da simulação
- Garantir clareza

## ⚠️ Dica
Escreva ao longo do projeto, não só no final

## Entregável
- Relatório completo em PDF

---

# 📦 Etapa 8 — Entrega Final

## Checklist

- [ ] Código roda do zero
- [ ] README com instruções claras
- [ ] Relatório em PDF
- [ ] Email correto
- [ ] Assunto correto

## Informações de envio
- Email: vitor.a.cortez@gmail.com
- Assunto:
  iCEV Pós-Graduação IA 2026: Trabalho Avaliativo
- Prazo: 12/04/2026

---

# ⏱️ Cronograma Sugerido (6 dias)

| Dia | Atividade |
|-----|----------|
| 1 | Kickoff + Modelagem |
| 2 | Ambiente |
| 3 | Agente clássico |
| 4 | LLM |
| 5 | Integração + melhorias |
| 6 | Relatório + entrega |

---

# 💡 Principais Boas Práticas

- Definir contrato claro (input/output)
- Separar ambiente e agentes
- Construir ambiente antes dos agentes
- Implementar agente clássico primeiro
- Validar sempre a saída do LLM
- Criar loop de simulação explícito