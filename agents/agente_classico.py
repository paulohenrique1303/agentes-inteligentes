class AgenteClassico:
    """
    Agente baseado em utilidade que usa estratégia de média móvel.

    Regra de decisão:
      - COMPRAR  se preço atual < média_móvel × (1 - margem)
      - VENDER   se preço atual > média_móvel × (1 + margem)
      - ESPERAR  caso contrário
    """

    def __init__(self, nome: str, saldo_inicial: float = 1000.0, margem: float = 0.05):
        self.nome = nome
        self.saldo = saldo_inicial
        self.acoes = 0
        self.ultima_acao = "ESPERAR"
        self.margem = margem

    def decidir(self, percepcao: dict) -> tuple[str, int]:
        """
        Recebe percepção do ambiente e retorna (acao, quantidade).
        """
        preco = percepcao["preco_atual"]
        media = percepcao["media_movel"]
        saldo = percepcao["saldo"]
        acoes = percepcao["acoes"]

        quantidade = self._calcular_quantidade(preco, saldo, acoes)

        if preco < media * (1 - self.margem) and saldo >= preco:
            return "COMPRAR", quantidade
        elif preco > media * (1 + self.margem) and acoes > 0:
            return "VENDER", quantidade
        else:
            return "ESPERAR", 0

    def _calcular_quantidade(self, preco: float, saldo: float, acoes: int) -> int:
        """Investe até 20% do saldo disponível por operação."""
        if preco <= 0:
            return 0
        max_compra = int((saldo * 0.2) / preco)
        max_venda = max(1, acoes // 2)  # vende até metade da posição
        return max(1, min(max_compra, max_venda))
