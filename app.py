# shiny run --host 0.0.0.0 app.py
from shiny import App, ui, render, reactive

# Interface do usuário
app_ui = ui.page_fluid(
    ui.tags.div(
        [
            # NAVBAR fixo no topo
            ui.tags.nav(
                ui.div(
                    ui.div(
                        ui.img(
                            src="https://png.pngtree.com/png-vector/20240715/ourmid/pngtree-simple-black-and-white-calculator-icon-with-shadow-on-a-white-vector-png-image_7059435.png",
                            style="width: 50px; margin-right: 15px;"  # Tamanho da logo
                        ),
                        ui.h4("MédiaFácil", style="margin: 0;"),
                        style="display: flex; align-items: center;"
                    ),
                    style="""
                        max-width: 1200px;
                        margin: 0 auto;
                        padding: 10px 20px;
                        display: flex;
                        align-items: center;
                    """
                ),
                style="""
                    background-color: #4d4d70;
                    color: white;
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    z-index: 1050;
                """
            ),

            # Espaço para evitar sobreposição da navbar
            ui.tags.div(style="height: 80px;"),

            # CONTEÚDO principal
            ui.div(
                ui.row(
                    # Coluna da imagem
                    ui.column(
                        6,
                        ui.div(
                            ui.img(
                                src="https://sistemicacontabilidade.com.br/wp-content/themes/sistemica/img/img-servico-geral.png",
                                style=(
                                    "max-width: 100%; "
                                    "height: auto; "
                                    "object-fit: contain; "
                                    "display: block; "
                                    "margin: 0 auto;"
                                )
                            ),
                            style="text-align: center; padding: 40px;"
                        )
                    ),
                    # Coluna de inputs
                    ui.column(
                        6,
                        ui.div(
                            ui.h2("Calculadora de Média", style="margin-bottom: 20px;"),
                            ui.input_text("materia", "Matéria", placeholder="Ex: Matemática"),
                            ui.input_numeric("quantidade", "Quantidade de Avaliações", value=3, min=1, max=10),
                            ui.input_action_button(
                                "gerar",
                                "Gerar Campos",
                                style="background-color:#4d4d70; color:#ffff;"
                            ),
                            ui.hr(),
                            ui.output_ui("campos"),
                            ui.output_ui("botao_calcular"),
                            ui.hr(),
                            ui.output_ui("resultado"),
                            style="padding: 40px;"
                        )
                    )
                ),
                style="max-width: 1200px; margin: 0 auto;"
            )
        ],
        style="""
            padding: 20px;
        """
    ),

    # FOOTER
    ui.tags.footer(
        ui.div(
            [
                ui.h4("Média Fácil", style="margin: 0 20px 0 0;"),
                ui.h6("@Isabella Matsumoto", style="margin: 0 20px 0 0;"),
                ui.h6("@Nicollas Victor", style="margin: 0;")
            ],
            style="""
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            padding: 15px 0;
        """
        ),
        style="""
            background-color: #5c5c8e;
            color: white;
            width: 102.5%;
            margin-left:-2%;
            height: 60px;
            margin-top: auto;
        """
    )
)

# Lógica da aplicação
def server(input, output, session):
    campos_gerados = reactive.Value([])  # Guarda os campos gerados dinamicamente
    resultados = reactive.Value([])      # Lista de resultados calculados

    # Quando clicar no botão "Gerar Campos"
    @reactive.effect
    @reactive.event(input.gerar)
    def _():
        campos = []
        qtd = input.quantidade()
        for i in range(1, qtd + 1):
            campos.append(
                ui.row(
                    ui.column(6, ui.input_numeric(f"nota{i}", f"Nota {i}", value=0.0, min=0, max=10, step=0.1)),
                    ui.column(6, ui.input_numeric(f"peso{i}", f"Peso {i}", value=1, min=1, max=10))
                )
            )
        campos_gerados.set(campos)

    # Renderiza os campos gerados
    @output
    @render.ui
    def campos():
        return campos_gerados.get()

    # Mostra o botão de calcular se os campos existirem
    @output
    @render.ui
    def botao_calcular():
        return (
            ui.input_action_button("calcular", "Calcular Média", style="background-color:#fd7e03; color:#fff")
            if campos_gerados.get() else ""
        )

    # Quando clicar em "Calcular Média"
    @output
    @render.ui
    @reactive.event(input.calcular)
    def resultado():
        materia = input.materia().strip()
        if not materia:
            return ui.div("Digite o nome da matéria.", class_="text-danger")

        qtd = input.quantidade()
        soma_pesos = 0
        soma_ponderada = 0
        linhas_resultado = []

        # Cálculo da média ponderada
        for i in range(1, qtd + 1):
            nota = getattr(input, f"nota{i}")()
            peso = getattr(input, f"peso{i}")()

            if peso < 1 or peso > 10:
                return ui.div(f"Peso {i} inválido. Digite entre 1 e 10.", class_="text-danger")

            soma_pesos += peso
            soma_ponderada += nota * peso
            linhas_resultado.append(f"Nota {i}: {nota:.1f} (Peso: {peso})")

        if soma_pesos == 0:
            return ui.div("Os pesos não podem somar zero.", class_="text-danger")
        if soma_pesos != 10:
            return ui.div(f"A soma dos pesos precisa ser 10. Soma atual: {soma_pesos}", class_="text-danger")

        media = soma_ponderada / soma_pesos
        situacao = (
            "Aprovado" if media >= 6 else
            "Recuperação" if media >= 4 else
            "Reprovado"
        )

        cor_borda = {
            "Aprovado": "#28a745",
            "Recuperação": "#ffc107",
            "Reprovado": "#dc3545"
        }[situacao]

        # Cria cartão com resultado
        resultado_card = ui.div(
            ui.h4(materia),
            ui.tags.ul([ui.tags.li(item) for item in linhas_resultado]),
            ui.tags.p(f"Média: {media:.2f}"),
            ui.tags.p(f"Situação: {situacao}", style="font-weight: bold;"),
            class_="card p-3 mb-3 shadow-sm",
            style=f"border-left: 5px solid {cor_borda}; background-color: #f8f9fa;"
        )

        # Adiciona ao topo
        lista_atual = resultados.get()
        lista_atual.insert(0, resultado_card)
        resultados.set(lista_atual)

        # Limpa campos
        campos_gerados.set([])
        session.send_input_message("materia", {"value": ""})  # Limpa campo Matéria

        # Exibe os resultados acumulados
        return ui.div(*resultados.get())

# Executa o app
app = App(app_ui, server)
