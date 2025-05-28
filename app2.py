from shiny import App, ui, reactive, render

desenhos = ["Gato Espacial", "Dragão Azul", "Unicórnio Pixelado", "Robô Retro", "Floresta Mágica"]

app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel(
            "Loja",
            ui.row(
                ui.column(
                    12,
                    ui.h3("Loja de Desenhos"),
                    *[
                        ui.card(
                            ui.input_checkbox(f"check_{i}", label=desenho),
                            ui.p("Um incrível desenho para colorir!"),
                            style="margin-bottom: 15px;"
                        ) for i, desenho in enumerate(desenhos)
                    ],
                    ui.input_action_button("comprar", "Comprar Selecionados"),
                    ui.hr(),
                    ui.output_text("compra_status"),
                    style="padding: 20px;"
                )
            )
        ),
        ui.nav_panel(
            "Admin",
            ui.h3("Itens Comprados"),
            ui.output_ui("compras_list")
        )
    )
)

def server(input, output, session):
    compras = reactive.Value([])

    @output
    @render.text
    @reactive.event(input.comprar)
    def compra_status():
        selecionados = []
        for i, desenho in enumerate(desenhos):
            if input[f"check_{i}"]():
                selecionados.append(desenho)

        if selecionados:
            lista = compras.get()
            nova_lista = lista + selecionados
            compras.set(nova_lista)

            # Não é possível resetar inputs via server no Shiny Python ainda
            return f"Você comprou: {', '.join(selecionados)} 🎨"
        else:
            return "Nenhum desenho selecionado."

    @output
    @render.ui
    def compras_list():
        lista = compras.get()
        if lista:
            return ui.tags.ul(*[ui.tags.li(item) for item in lista])
        else:
            return ui.p("Nenhuma compra registrada ainda.")

app = App(app_ui, server)
