import random


EVENTOS = ["POSITIVO", "NEGATIVO", "NEUTRO"]
IMPACTO_EVENTO = {"POSITIVO": 0.03, "NEGATIVO": -0.03, "NEUTRO": 0.0}


class Bolsa:
    def __init__(self, preco_inicial: float = 100.0, volatilidade: float = 0.02):
        self.preco_atual = preco_inicial
        self.volatilidade = volatilidade
        self.historico = [preco_inicial]
        self.evento_atual = "NEUTRO"

    # --- Estado do mercado ---

    def avancar_tick(self):
        """Gera novo preço com ruído gaussiano + evento de mercado."""
        self.evento_atual = random.choices(
            EVENTOS, weights=[0.3, 0.3, 0.4]
        )[0]
        ruido = random.gauss(0, self.volatilidade)
        impacto = IMPACTO_EVENTO[self.evento_atual]
        self.preco_atual = round(self.preco_atual * (1 + ruido + impacto), 2)
        self.preco_atual = max(self.preco_atual, 1.0)  # preço mínimo de R$1
        self.historico.append(self.preco_atual)

    def media_movel(self, janela: int = 5) -> float:
        """Média simples dos últimos N preços."""
        ultimos = self.historico[-janela:]
        return round(sum(ultimos) / len(ultimos), 2)

    # --- Percepção entregue ao agente ---

    def obter_percepcao(self, agente) -> dict:
        return {
            "preco_atual": self.preco_atual,
            "historico": self.historico[-5:],
            "media_movel": self.media_movel(),
            "saldo": agente.saldo,
            "acoes": agente.acoes,
            "evento": self.evento_atual,
        }

    # --- Processamento de ordens ---

    def processar_ordem(self, agente, acao: str, quantidade: int = 1):
        """Executa a ação do agente no mercado."""
        if acao == "COMPRAR":
            custo = self.preco_atual * quantidade
            if agente.saldo >= custo:
                agente.saldo = round(agente.saldo - custo, 2)
                agente.acoes += quantidade
            else:
                acao = "ESPERAR"  # sem saldo suficiente

        elif acao == "VENDER":
            if agente.acoes >= quantidade:
                agente.saldo = round(agente.saldo + self.preco_atual * quantidade, 2)
                agente.acoes -= quantidade
            else:
                acao = "ESPERAR"  # sem ações suficientes

        agente.ultima_acao = acao

    def valor_carteira(self, agente) -> float:
        return round(agente.saldo + agente.acoes * self.preco_atual, 2)
