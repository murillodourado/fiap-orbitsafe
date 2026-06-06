from funcoes import (
    limpar,
    linha,
    regioes,
    sobre_o_projeto,
    cadastrar_regiao,
    calcular_risco,
    consultar_historico,
    gerar_relatorio
)
from calculo_funcoes import analisar_funcoes, gerar_graficos

# ============================================================
#   ORBITSAFE — Programa Principal
#   Global Solution 2026 · FIAP · Engenharia de Software
# ============================================================


def menu():
    while True:
        limpar()
        print("\n" + "=" * 60)
        print("           🛰️  ORBITSAFE — MENU PRINCIPAL")
        print("=" * 60)
        print("  [0] Sobre o projeto")
        print("  [1] Cadastrar região de monitoramento")
        print("  [2] Calcular IRO de uma região")
        print("  [3] Consultar histórico de alertas")
        print("  [4] Gerar relatório de risco")
        print("  [5] Análise matemática do IRO")
        print("  [6] Gerar gráficos")
        print("  [7] Sair")
        linha()

        opcao = input("  Escolha uma opção: ").strip()

        match opcao:
            case "0":
                sobre_o_projeto()
            case "1":
                cadastrar_regiao()
            case "2":
                calcular_risco()
            case "3":
                consultar_historico()
            case "4":
                gerar_relatorio(regioes)
            case "5":
                analisar_funcoes()
            case "6":
                gerar_graficos()
            case "7":
                limpar()
                print("\n  Encerrando o OrbitSafe. Até logo! 🛰️\n")
                break
            case _:
                print("\n  ⚠️  Opção inválida. Digite um número de 0 a 5.")
                input("  Pressione ENTER para continuar...")


# ============================================================
#   INICIALIZAÇÃO
# ============================================================

if __name__ == "__main__":
    menu()
