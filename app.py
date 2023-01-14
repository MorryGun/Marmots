from shiny import App, render, reactive, ui
import matplotlib.pyplot as plt
import numpy as np
import random


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
            ui.navset_tab_card(
                ui.nav(
                    "Basic settings",
                    ui.div(
                        ui.input_slider("seed", "Seed", 0, 100, value=50),
                        ui.input_slider("years", "Simulation duration (years)", 0, 100, value=50),
                        ui.input_slider("pasture", "Pasture (%)", 0, 100, value=20),
                        ui.input_checkbox("useSteps", "Step-by-step")
                    )
                    ),
                ui.nav(
                    "Detailed settings",
                    ui.div(
                        ui.input_slider("rows", "Rows", 3, 10, value=5),
                        ui.input_slider("columns", "Columns", 3, 10, value=5),
                        ui.input_slider("production", "Tile productivity", 20, 100, value=[30, 80]),
                        ui.input_slider("fertility", "Marmots fertility", 2, 10, value=[3, 8]),
                        ui.input_slider("consumption", "Marmots consumption", 2, 10, value=[3, 8]),
                    )
                    )
                ),
                    ui.div(
                        ui.div(
                            ui.input_action_button(
                            "run", 
                            "Run", 
                            class_="btn-primary w-100"
                        ),
                        ui.panel_conditional(
                            "input.useSteps",
                            ui.input_action_button(
                            "clear", 
                            "Clear", 
                            class_="btn-outline-primary w-100"
                            )
                        ),
                            class_="card mb-3"
                    )
                    )
                    ),
        ui.column(
            9,
            ui.div(
                ui.output_plot("grid"),
            )
        )
    ),
)


def server(input, output, session):
    def get_data():
        nrows = input.rows()
        ncols = input.columns()
        data = np.arange(nrows * ncols).reshape(nrows, ncols)

        with ui.Progress(min=1, max=15) as p:
            p.set(message="Calculation in progress", detail="This may take a while...")

            for i in range(1, 15):
                p.set(i, message="Computing")

        return data


    def create_colormesh(fig, data, ax, title, colormap, fontsize=16):
        # create axis
        x = np.arange(-0.5, data.shape[1], 1)
        y = np.arange(-0.5, data.shape[0], 1)

        pc = ax.pcolormesh(x, y, data, shading='flat', vmin=0, vmax=data.max(), cmap = colormap)

        ax.set_title(title, fontsize=fontsize)
        fig.colorbar(pc, ax=ax, location="bottom")

        return pc


    def create_plot(a, data, years, title, xlabel, ylabel):
        #temp data prep
        dataset = []
        for year in range(years-25):
            dataset.append(random.random()*25)

        a.plot(dataset)
        a.set_title(title)
        a.set_xlabel(xlabel)
        a.set_ylabel(ylabel)
        a.axis([0, years, 0, data.max()+2])
        

    @output
    @render.plot
    @reactive.event(input.run)
    def grid():
        data = get_data()
        fig, axs = plt.subplots(2, 2)
        gridspec = fig.add_gridspec(2, 2)

        # clear the left column for the subfigure:
        for a in axs[:, 0]:
            a.remove()

        # plot data in remaining axes:
        create_plot(axs[:,1:].flat[0], data, input.years(), "Marmot population", "years", "population")
        create_plot(axs[:,1:].flat[1], data, input.years(), "Pasture volumes", "years", "kg")

        # make the subfigure in the empty gridspec slots:
        subfig = fig.add_subfigure(gridspec[:, 0])

        axsLeft = subfig.subplots(1, 2)
        create_colormesh(fig, data, axsLeft[0], "Marmot population", "YlOrBr")
        create_colormesh(fig, data, axsLeft[1], "Vegetation", "Greens")
        fig.tight_layout()
    
        return fig


app = App(app_ui, server)
