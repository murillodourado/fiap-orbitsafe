# Modelagem Matemática: OrbitSafe

## Onde está a parte de cálculo

A modelagem matemática do projeto está no arquivo **`calculo_funcoes.py`**.

Ele é separado do `funcoes.py` principal e importa apenas os utilitários de interface
(`cabecalho`, `linha`, `pausar`) para manter o mesmo padrão visual do sistema.

---

## O que foi modelado

O IRO (Índice de Risco OrbitSafe) é calculado no `funcoes.py` com base em três
variáveis: temperatura, umidade e histórico regional. O `calculo_funcoes.py` aprofunda
essa lógica usando duas funções matemáticas contínuas que modelam o comportamento
real de cada variável.

---

## Função 1 — Polinomial (Risco de Queimada)
R_q(T) = 0.05 · T² - 0.5 · T + 5

**Variável:** T = temperatura em °C  
**Resultado:** R_q = índice de risco de queimada (0 a 100)

**Por que polinomial?**  
O risco de queimada não cresce de forma constante com a temperatura. Em dias
amenos o impacto é pequeno, mas a partir de certos patamares (acima de 35°C)
o risco dispara de forma acelerada. Esse comportamento de crescimento cada vez
mais intenso é típico de uma parábola (grau 2), o que justifica a escolha.

**Análise:**
- Domínio: T ∈ [0, 60] °C
- Vértice (mínimo): T = 5°C → R_q = 3,75
- Decrescente em [0°C, 5°C]
- Crescente em [5°C, 60°C]
- Risco ALTO (R_q ≥ 60) a partir de aproximadamente 37°C

---

## Função 2 — Logarítmica (Risco de Enchente)
R_e(U) = 100 - 28 · ln(U + 1)

**Variável:** U = umidade relativa do ar em %  
**Resultado:** R_e = índice de risco de enchente (0 a 100)

**Por que logarítmica?**  
Quando a umidade sobe de 0% para 30%, o risco cai muito rapidamente. Mas quando
já está acima de 60%, cada ponto a mais de umidade tem cada vez menos efeito.
Esse comportamento de impacto decrescente ao longo do tempo é exatamente o que
uma função logarítmica representa, tornando-a a escolha natural para este fenômeno.

**Análise:**
- Domínio: U ∈ [0, 100] %
- Estritamente decrescente em todo o domínio
- Zona segura (R_e ≤ 30): a partir de aproximadamente U = 76%
- Em U = 0%: R_e = 100 (risco máximo)
- Em U = 100%: R_e ≈ 0 (sem risco)

---

## Função combinada — IRO Analítico
IRO(T, U) = 0.5 · R_q(T) + 0.5 · R_e(U)

Combina as duas funções com peso igual (50% cada) para gerar um índice de risco
geral da região, que pode ser comparado diretamente com o IRO calculado no
`funcoes.py`.

---

## Gráficos

A função `gerar_graficos()` gera dois gráficos lado a lado salvos em
`graficos_iro.png`:

- **Gráfico 1:** curva polinomial R_q(T) com faixas coloridas de risco
- **Gráfico 2:** curva logarítmica R_e(U) com faixas coloridas de risco

As faixas de cor seguem o mesmo critério de classificação do sistema:

| Cor | Faixa | Nível |
|-----|-------|-------|
| Verde | 0 – 30 | Normal |
| Amarelo | 30 – 60 | Atenção |
| Vermelho | 60 – 100 | Risco Alto / Emergência |

> Após salvar, o terminal exibe `salvo` e o gráfico é aberto automaticamente.

---

## Como usar no projeto

No `main.py`, adicione o import:

```python
from calculo_funcoes import analisar_funcoes, gerar_graficos
```

E as opções no menu:

```python
case "6":
    analisar_funcoes()
case "7":
    gerar_graficos()
```

Dependências necessárias:
pip install numpy matplotlib