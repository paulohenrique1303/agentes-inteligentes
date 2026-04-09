import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from environment.bolsa import Bolsa
from agents.agente_classico import AgenteClassico
from agents.agente_llm import AgenteLLM

# --- Configuração ---
NUM_TICKS = 20
SALDO_INICIAL = 1000.0

# --- Inicialização ---
bolsa = Bolsa(preco_inicial=100.0, volatilidade=0.02)
classico = AgenteClassico(nome="Classico", saldo_inicial=SALDO_INICIAL)
llm = AgenteLLM(nome="LLM", saldo_inicial=SALDO_INICIAL)

print("=" * 80)
print("   SIMULACAO - MERCADO FINANCEIRO COM DOIS AGENTES")
print("=" * 80)
print(f"Saldo inicial: R$ {SALDO_INICIAL:.2f} | Preco inicial: R$ {bolsa.preco_atual:.2f}")
print(f"{'Tick':<5} {'Preco':>8} {'MM5':>8} {'Evento':<10} "
      f"{'Classico':>12} {'ROI-C':>7} {'LLM':>12} {'ROI-L':>7}")
print("-" * 80)

# --- Loop de simulação ---
for tick in range(1, NUM_TICKS + 1):
    bolsa.avancar_tick()

    # Agente Clássico
    perc_c = bolsa.obter_percepcao(classico)
    acao_c, qtd_c = classico.decidir(perc_c)
    bolsa.processar_ordem(classico, acao_c, qtd_c)
    val_c = bolsa.valor_carteira(classico)
    roi_c = ((val_c - SALDO_INICIAL) / SALDO_INICIAL) * 100

    # Agente LLM
    perc_l = bolsa.obter_percepcao(llm)
    acao_l, qtd_l = llm.decidir(perc_l)
    bolsa.processar_ordem(llm, acao_l, qtd_l)
    val_l = bolsa.valor_carteira(llm)
    roi_l = ((val_l - SALDO_INICIAL) / SALDO_INICIAL) * 100

    acao_c_str = f"{classico.ultima_acao}(x{qtd_c})"
    acao_l_str = f"{llm.ultima_acao}(x{qtd_l})"

    print(
        f"{tick:<5} "
        f"R${perc_c['preco_atual']:>6.2f} "
        f"R${perc_c['media_movel']:>6.2f} "
        f"{perc_c['evento']:<10} "
        f"{acao_c_str:>12} {roi_c:>+6.1f}% "
        f"{acao_l_str:>12} {roi_l:>+6.1f}%"
    )

# --- Resultado Final ---
print("-" * 80)
val_c_final = bolsa.valor_carteira(classico)
val_l_final = bolsa.valor_carteira(llm)
roi_c_final = ((val_c_final - SALDO_INICIAL) / SALDO_INICIAL) * 100
roi_l_final = ((val_l_final - SALDO_INICIAL) / SALDO_INICIAL) * 100

print(f"\nRESULTADO FINAL:")
print(f"  Agente Classico : R$ {val_c_final:.2f} | ROI: {roi_c_final:+.2f}%"
      f" | Acoes: {classico.acoes} | Caixa: R$ {classico.saldo:.2f}")
print(f"  Agente LLM      : R$ {val_l_final:.2f} | ROI: {roi_l_final:+.2f}%"
      f" | Acoes: {llm.acoes} | Caixa: R$ {llm.saldo:.2f}")

vencedor = "Classico" if val_c_final >= val_l_final else "LLM"
print(f"\n  Vencedor: {vencedor}!")
print("=" * 80)
