import ollama


ACOES_VALIDAS = {"COMPRAR", "VENDER", "ESPERAR"}
MODELO = "minimax-m2.7:cloud"


class AgenteLLM:
    """
    Agente cujo processo de decisão é baseado em um LLM via Ollama.
    Recebe a percepção do ambiente como texto e retorna uma ação válida.
    """

    def __init__(self, nome: str, saldo_inicial: float = 1000.0):
        self.nome = nome
        self.saldo = saldo_inicial
        self.acoes = 0
        self.ultima_acao = "ESPERAR"
        self.ultimo_raciocinio = ""

    def decidir(self, percepcao: dict) -> tuple[str, int]:
        """
        Consulta o LLM com a percepção atual e retorna (acao, quantidade).
        """
        prompt = self._montar_prompt(percepcao)

        try:
            resposta = ollama.chat(
                model=MODELO,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2},
            )
            texto = resposta["message"]["content"].strip().upper()
            self.ultimo_raciocinio = texto
            acao = self._extrair_acao(texto)
        except Exception as e:
            print(f"  [LLM ERRO] {e} — usando ESPERAR como fallback")
            acao = "ESPERAR"

        quantidade = self._calcular_quantidade(percepcao, acao)
        return acao, quantidade

    def _montar_prompt(self, percepcao: dict) -> str:
        historico = " → ".join([f"R${p:.2f}" for p in percepcao["historico"]])
        return f"""Você é um trader profissional operando em uma bolsa de valores simulada.

SITUAÇÃO ATUAL:
- Preço atual da ação: R$ {percepcao['preco_atual']:.2f}
- Média móvel (últimos 5 ticks): R$ {percepcao['media_movel']:.2f}
- Histórico de preços: {historico}
- Evento de mercado: {percepcao['evento']}
- Seu saldo em caixa: R$ {percepcao['saldo']:.2f}
- Ações em sua carteira: {percepcao['acoes']} unidades

OBJETIVO: Maximizar o valor total da sua carteira (saldo + ações × preço).

Com base nessas informações, qual é sua decisão?
Responda APENAS com uma das palavras: COMPRAR, VENDER ou ESPERAR"""

    def _extrair_acao(self, texto: str) -> str:
        """Extrai ação válida do texto do LLM."""
        for acao in ACOES_VALIDAS:
            if acao in texto:
                return acao
        return "ESPERAR"  # fallback seguro

    def _calcular_quantidade(self, percepcao: dict, acao: str) -> int:
        preco = percepcao["preco_atual"]
        saldo = percepcao["saldo"]
        acoes = percepcao["acoes"]

        if acao == "COMPRAR" and preco > 0:
            return max(1, int((saldo * 0.2) / preco))
        elif acao == "VENDER" and acoes > 0:
            return max(1, acoes // 2)
        return 0
