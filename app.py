from shiny import App, render, reactive, ui
import matplotlib.pyplot as plt
import numpy as np

from generator import Generator


def simulation_tab():
    return ui.div(
        ui.input_slider("seed", "Seed", 0, 100, value=50),
        ui.input_slider("years", "Simulation duration (years)", 0, 100, value=50),
        ui.input_slider("pasture", "Pasture (%)", 0, 100, value=20)
    )


app_ui = ui.page_fluid(
    ui.h2("Marmots"),
    ui.row(
        ui.column(
            3,
            ui.div(
                ui.input_slider("seed", "Seed", 0, 100, value=50),
                ui.input_slider("years", "Simulation duration (years)", 0, 100, value=50),
                ui.input_slider("pasture", "Pasture (%)", 0, 100, value=20)
            ),
            ui.navset_tab_card(
                ui.nav(
                    "Step-by-step",
                    ui.div(
                        ui.input_action_button(
                        "run", 
                        "Next step", 
                        class_="btn-outline-primary w-100"
                        ),
                        ui.input_action_button(
                        "clear", 
                        "Clear", 
                        class_="btn-outline-primary w-100"
                        ),
                        class_="card mb-3"
                    )
                    ),
                ui.nav(
                    "Deterministic",
                    ui.div(
                        ui.input_action_button(
                        "run", 
                        "Run simulation", 
                        class_="btn-outline-primary w-100"
                        ),
                        class_="card mb-3"
                    )
                    ),
                ui.nav(
                    "Test",
                    ui.output_text_verbatim("random")
                    )
                ),
        ),
        ui.column(
            5,
            ui.div(
                ui.output_plot("vegetation", width = "400px"),
                ui.output_plot("marmots", width = "400px"),
            )
        ),
        ui.column(
            4,
            ui.div(
                ui.output_plot("population", width = "400px"),
                ui.output_plot("pasture", width = "400px"),
            )
        )
    ),
)

def dummy_plot():
    nrows = 5
    ncols = 5
    Z = np.arange(nrows * ncols).reshape(nrows, ncols)
    x = np.arange(ncols + 1)
    y = np.arange(nrows + 1)

    fig, ax = plt.subplots()
    ax.pcolormesh(x, y, Z, shading='flat', vmin=Z.min(), vmax=Z.max())
    
    return fig

def dummy_graf():
    # make data
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)

    # plot
    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth=2.0)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
       ylim=(0, 8), yticks=np.arange(1, 8))
    
    return fig


def server(input, output, session):
    @output
    @render.plot
    @reactive.event(input.run, ignore_none=False)
    def vegetation():
        return dummy_plot()

    @output
    @render.plot
    @reactive.event(input.run, ignore_none=False)
    def marmots():
        return dummy_plot()

    @output
    @render.plot
    @reactive.event(input.run, ignore_none=False)
    def pasture():
        return dummy_graf()

    @output
    @render.plot
    @reactive.event(input.run, ignore_none=False)
    def population():
        return dummy_graf()

    @output
    @render.text
    def random():
        generator = Generator(input.seed())

        min = 2
        max = 20

        mean = 10
        sigma = 4

        return f"""Test: random[{generator.random()}, {generator.random()}, {generator.random()}],
         uniform[{generator.uniform(min, max)}, {generator.uniform(min, max)}, {generator.uniform(min, max)}],
         gauss[{generator.gauss(mean, sigma)}, {generator.gauss(mean, sigma)}, {generator.gauss(mean, sigma)}]"""


app = App(app_ui, server)
