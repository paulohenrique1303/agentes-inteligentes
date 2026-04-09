import ollama


ACOES_VALIDAS = {"COMPRAR", "VENDER", "ESPERAR"}
MODELO = "llama3.2:3b"


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
        preco = percepcao["preco_atual"]
        media = percepcao["media_movel"]
        desvio = ((preco - media) / media) * 100
        tendencia = "SUBINDO" if len(percepcao["historico"]) >= 2 and percepcao["historico"][-1] > percepcao["historico"][-2] else "CAINDO"

        return f"""Você é um trader disciplinado. Analise os dados e tome UMA decisão.

DADOS DO MERCADO:
- Preço atual: R$ {preco:.2f}
- Média móvel (MM5): R$ {media:.2f}
- Desvio em relação à MM5: {desvio:+.1f}%
- Tendência recente: {tendencia}
- Histórico: {historico}
- Evento: {percepcao['evento']}

SUA CARTEIRA:
- Saldo em caixa: R$ {percepcao['saldo']:.2f}
- Ações em carteira: {percepcao['acoes']} unidades

REGRAS:
- COMPRAR: se preço abaixo da MM5 (desvio negativo) E tiver saldo
- VENDER: se preço acima da MM5 (desvio positivo) E tiver ações
- ESPERAR: se não houver sinal claro ou sem recursos

Responda APENAS com uma palavra: COMPRAR, VENDER ou ESPERAR"""

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
