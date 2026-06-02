from datetime import datetime
import random
import os
import requests

# ============================================================
#   ORBITSAFE — Funções do Sistema
#   Global Solution 2026 · FIAP · Engenharia de Software
# ============================================================

regioes = []
historico = []
estados_validos = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
    "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
    "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
]


# ============================================================
#   UTILITÁRIOS
# ============================================================

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def linha():
    print("-" * 60)

def cabecalho(titulo):
    print("\n" + "=" * 60)
    print(f"  🛰️  ORBITSAFE — {titulo}")
    print("=" * 60)

def pausar():
    input("\nPressione ENTER para voltar ao menu...")
    limpar()


# ============================================================
#   CÁLCULO E CLASSIFICAÇÃO DO IRO
# ============================================================

def calcular_iro(temperatura, umidade, historico_regional):
    iro = (temperatura * 0.4) + ((100 - umidade) * 0.4) + (historico_regional * 0.2)
    return min(100, max(0, round(iro, 1)))


def classificar_iro(iro):
    match True:
        case _ if iro <= 30:
            return "🟢 NORMAL", "Sem risco aparente na região."
        case _ if iro <= 60:
            return "🟡 ATENÇÃO", "Risco moderado. Monitorar com frequência."
        case _ if iro <= 80:
            return "🟠 RISCO ALTO", "Acionar equipes de prevenção imediatamente."
        case _:
            return "🔴 EMERGÊNCIA", "Alerta máximo! Acionar Defesa Civil agora."


def registrar_alerta(nome_regiao, iro, classificacao):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    historico.append({
        "data": agora,
        "regiao": nome_regiao,
        "iro": iro,
        "nivel": classificacao
    })


# ============================================================
#   BUSCA DE DADOS CLIMÁTICOS
# ============================================================

def buscar_clima(nome_cidade):
    # Tentativa 1: CPTEC/INPE
    try:
        busca = requests.get(
            f"http://servicos.cptec.inpe.br/XML/cidade/7/dias/{nome_cidade}/previsao.xml",
            timeout=5
        )
        if busca.status_code == 200 and "<tempo>" in busca.text:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(busca.text)
            temperatura = float(root.find(".//maxima").text)
            umidade = float(root.find(".//umidade").text)
            return temperatura, umidade
    except:
        pass

    # Tentativa 2: wttr.in como fallback
    try:
        url = f"https://wttr.in/{nome_cidade}?format=j1"
        resposta = requests.get(url, timeout=5).json()
        temperatura = float(resposta["current_condition"][0]["temp_C"])
        umidade = float(resposta["current_condition"][0]["humidity"])
        return temperatura, umidade
    except:
        return None, None


# ============================================================
#   OPÇÃO 0 — SOBRE O PROJETO
# ============================================================

def sobre_o_projeto():
    cabecalho("SOBRE O PROJETO")
    linha()
    print("  O OrbitSafe monitora riscos de queimadas e enchentes")
    print("  usando dados do INPE em tempo real.")
    print("  Calcula o IRO (Índice de Risco OrbitSafe) por região")
    print("  e emite alertas automáticos para comunidades em risco,")
    print("  conectando tecnologia espacial à proteção de vidas.")
    linha()
    pausar()


# ============================================================
#   OPÇÃO 1 — CADASTRAR REGIÃO
# ============================================================

def cadastrar_regiao():
    cabecalho("CADASTRAR REGIÃO")

    print("\nPreencha os dados da região a ser monitorada.")
    linha()

    nome = input("\n  Nome da região (ex: Vale do Ribeira): ").strip()
    if not nome:
        print("\n  ⚠️  Nome inválido. Tente novamente.")
        pausar()
        return

    estado = input("  Estado (ex: SP): ").strip().upper()
    if estado not in estados_validos:
        print("\n  ⚠️  Estado inválido. Informe uma sigla de estado brasileiro (ex: SP).")
        pausar()
        return

    print("\n  Tipo de risco monitorado:")
    print("  [1] Queimada")
    print("  [2] Enchente")
    print("  [3] Ambos")

    tipo_opcao = input("\n  Escolha (1, 2 ou 3): ").strip()

    match tipo_opcao:
        case "1":
            tipo = "Queimada"
        case "2":
            tipo = "Enchente"
        case "3":
            tipo = "Ambos"
        case _:
            print("\n  ⚠️  Opção inválida.")
            pausar()
            return

    historico_regional = round(random.uniform(10, 50), 1)

    regiao = {
        "nome": nome,
        "estado": estado,
        "tipo": tipo,
        "historico": historico_regional
    }

    regioes.append(regiao)

    linha()
    print(f"\n  ✅ Região cadastrada com sucesso!")
    print(f"\n  Nome   : {nome} — {estado}")
    print(f"  Tipo   : {tipo}")
    print(f"  Índice histórico simulado: {historico_regional}")
    linha()
    pausar()


# ============================================================
#   OPÇÃO 2 — CALCULAR IRO
# ============================================================

def calcular_risco():
    cabecalho("CALCULAR IRO DA REGIÃO")

    if not regioes:
        print("\n  ⚠️  Nenhuma região cadastrada ainda.")
        print("  Acesse a opção 1 para cadastrar uma região primeiro.")
        pausar()
        return

    print("\n  Regiões cadastradas:")
    linha()
    for i, r in enumerate(regioes):
        print(f"  [{i + 1}] {r['nome']} — {r['estado']} ({r['tipo']})")
    linha()

    try:
        escolha = int(input("\n  Escolha o número da região: ")) - 1
        if escolha < 0 or escolha >= len(regioes):
            raise ValueError
    except ValueError:
        print("\n  ⚠️  Opção inválida.")
        pausar()
        return

    regiao = regioes[escolha]

    print(f"\n  Região selecionada: {regiao['nome']} — {regiao['estado']}")
    linha()

    print(f"\n  🌐 Buscando dados climáticos para {regiao['nome']}...")
    temperatura, umidade = buscar_clima(regiao['nome'])

    if temperatura is None or umidade is None:
        print("\n  ⚠️  Não foi possível buscar os dados climáticos.")
        print("  Verifique sua conexão e tente novamente.")
        pausar()
        return

    print(f"  ✅ Dados obtidos com sucesso!")

    iro = calcular_iro(temperatura, umidade, regiao["historico"])
    nivel, descricao = classificar_iro(iro)

    registrar_alerta(regiao["nome"], iro, nivel)

    linha()
    print(f"\n  📍 Região       : {regiao['nome']} — {regiao['estado']}")
    print(f"  🌡️  Temperatura  : {temperatura}°C")
    print(f"  💧 Umidade      : {umidade}%")
    print(f"  📊 IRO calculado: {iro} / 100")
    print(f"\n  Classificação : {nivel}")
    print(f"  Recomendação  : {descricao}")
    linha()
    pausar()


# ============================================================
#   OPÇÃO 3 — HISTÓRICO DE ALERTAS
# ============================================================

def consultar_historico():
    cabecalho("HISTÓRICO DE ALERTAS")

    if not historico:
        print("\n  ⚠️  Nenhum alerta registrado ainda.")
        print("  Calcule o IRO de uma região para gerar alertas.")
        pausar()
        return

    print("\n  Filtrar por:")
    print("  [1] Todos os alertas")
    print("  [2] Somente alertas críticos (RISCO ALTO ou EMERGÊNCIA)")
    print("  [3] Buscar por nome da região")
    linha()

    filtro = input("  Escolha uma opção: ").strip()

    if filtro == "3":
        busca = input("  Nome da região: ").strip().lower()
        print()
        linha()
        print(f"  {'DATA':<18} {'REGIÃO':<22} {'IRO':<8} NÍVEL")
        linha()
        encontrou = False
        for a in historico:
            if busca in a["regiao"].lower():
                print(f"  {a['data']:<18} {a['regiao']:<22} {a['iro']:<8} {a['nivel']}")
                encontrou = True
        if not encontrou:
            print("  Nenhum alerta encontrado para essa região.")
        linha()
        pausar()
        return

    print()
    linha()
    print(f"  {'DATA':<18} {'REGIÃO':<22} {'IRO':<8} NÍVEL")
    linha()

    encontrou = False
    for alerta in historico:
        exibir = False

        if filtro == "1":
            exibir = True
        elif filtro == "2":
            if "RISCO ALTO" in alerta["nivel"] or "EMERGÊNCIA" in alerta["nivel"]:
                exibir = True
        else:
            print("\n  ⚠️  Opção inválida.")
            pausar()
            return

        if exibir:
            print(f"  {alerta['data']:<18} {alerta['regiao']:<22} {alerta['iro']:<8} {alerta['nivel']}")
            encontrou = True

    if not encontrou:
        print("  Nenhum alerta encontrado com esse filtro.")

    linha()
    pausar()


# ============================================================
#   OPÇÃO 4 — RELATÓRIO DE RISCO
# ============================================================

def gerar_relatorio(lista_regioes):
    cabecalho("RELATÓRIO DE RISCO POR REGIÃO")

    if not lista_regioes:
        print("\n  ⚠️  Nenhuma região cadastrada ainda.")
        print("  Acesse a opção 1 para cadastrar regiões primeiro.")
        pausar()
        return

    print("\n  Buscando dados climáticos para todas as regiões cadastradas...")
    linha()

    resultados = []

    for regiao in lista_regioes:
        print(f"\n  🌐 Buscando dados para {regiao['nome']}...")
        temperatura, umidade = buscar_clima(regiao['nome'])

        if temperatura is None or umidade is None:
            print(f"  ⚠️  Não foi possível obter dados de {regiao['nome']}. Região ignorada.")
            continue

        print(f"  ✅ Dados obtidos!")

        iro = calcular_iro(temperatura, umidade, regiao["historico"])
        nivel, descricao = classificar_iro(iro)
        registrar_alerta(regiao["nome"], iro, nivel)

        resultados.append({
            "nome": regiao["nome"],
            "estado": regiao["estado"],
            "iro": iro,
            "nivel": nivel,
            "descricao": descricao
        })

    if not resultados:
        print("\n  Nenhum resultado para exibir.")
        pausar()
        return

    resultados.sort(key=lambda x: x["iro"], reverse=True)

    print()
    linha()
    print("  RELATÓRIO FINAL — REGIÕES ORDENADAS POR NÍVEL DE RISCO")
    linha()
    print(f"  {'#':<4} {'REGIÃO':<24} {'ESTADO':<8} {'IRO':<8} NÍVEL")
    linha()

    for i, r in enumerate(resultados):
        print(f"  {i+1:<4} {r['nome']:<24} {r['estado']:<8} {r['iro']:<8} {r['nivel']}")

    linha()
    print(f"\n  Total de regiões analisadas : {len(resultados)}")

    criticos = [r for r in resultados if r["iro"] > 60]
    if criticos:
        print(f"  Regiões em estado crítico   : {len(criticos)}")
        print(f"  Maior IRO registrado        : {resultados[0]['iro']} ({resultados[0]['nome']})")

    linha()
    pausar()
