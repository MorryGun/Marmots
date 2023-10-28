from shiny import App, render, reactive, ui
import matplotlib.pyplot as plt
import numpy as np
from batch_simulator import BatchSimulator
from simulator import Simulator


def simulation_tab():
    return ui.div(
        ui.panel_conditional(
                "!input.batch",
                ui.input_slider("seed", "Seed", 0, 100, value=50),
                ui.input_slider("pasture", "Pasture (%)", 0, 100, value=20),
            ),   
        ui.panel_conditional(
                "input.batch",
                ui.input_slider("batch_size", "Batch size", 2, 100, value=5),
            ),        
        ui.input_slider("years", "Simulation duration (years)", 0, 100, value=50),
        ui.input_checkbox("batch", "Compute batch")
    )


def detailed_settings_tab():
    return ui.div(
        ui.panel_conditional(
                "!input.batch",
                ui.input_slider("columns", "Columns", 1, 10, value=5),
                ui.input_slider("rows", "Rows", 1, 10, value=5),
            ),
        ui.input_slider("production", "Tile productivity, tons/year", 0.5, 10, value=[1, 8]),
        ui.input_slider("fertility", "Marmots fertility", 2.0, 10.0, value=3.0),
        ui.input_slider("initial_population", "Initial population", 0, 10, value=5),
        ui.input_slider("consumption", "Marmots consumption, kg/year", 0, 120, value=[40, 100]),
        ui.input_slider("shrubbing", "Shrubbing limit, tons", 0, 120, value=72.5),
    )


app_ui = ui.page_fluid(
    ui.h2("Marmots"),
    ui.row(
        ui.column(
            3,
            ui.navset_tab_card(
                ui.nav(
                    "Basic settings",
                    simulation_tab(),
                    ),
                ui.nav(
                    "Detailed settings",
                    ui.div(
                        detailed_settings_tab(),
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
                        class_="card mb-3"
                    )
                    )
                    ),
        ui.column(
            9,
            ui.panel_conditional(
                "!input.batch",
                ui.div(
                    ui.output_plot("grid"),
                    ui.output_text_verbatim("text")
            ),
            ),
            ui.panel_conditional(
                "input.batch",
                ui.div(
                    ui.output_plot("batch_plot"),
                    ui.output_text_verbatim("batch_text")
                )
            ),
        )
    ),
)


def server(input, output, session):
    def get_data():
        if (not input.batch()):
            print("======Initiating a single run======")
            simulator = Simulator(input.seed(), input.columns(), input.rows(), input.production(), input.fertility(), input.consumption(), input.shrubbing(), input.initial_population())
            simulator.initiate()
            simulator.simulate(input.pasture(), input.years())

            return simulator.results
        else:
            print("======Initiating a batch run======")
            simulator = BatchSimulator(input.batch_size(), input.production(), input.fertility(), input.consumption(), input.shrubbing(), input.initial_population())
            simulator.batch_simulate(input.years())

            return simulator.batch_results

    def create_colormesh(fig, data, ax, title, colormap, fontsize=16):
        # create axis
        x = np.arange(-0.5, data.shape[1], 1)
        y = np.arange(-0.5, data.shape[0], 1)

        pc = ax.pcolormesh(x, y, data, shading='flat', vmin=0, vmax=data.max(), cmap = colormap)

        ax.set_title(title, fontsize=fontsize)
        fig.colorbar(pc, ax=ax, location="bottom")

        return pc


    def create_plot(a, data, years, title, xlabel, ylabel):
        a.plot(data)
        a.set_title(title)
        a.set_xlabel(xlabel)
        a.set_ylabel(ylabel)
        a.axis([0, years, 0, max(data)+2])
        

    @output
    @render.plot
    @reactive.event(input.run)
    def grid():
        data = get_data()
        marmots_grid = data[-1].marmots
        vegetation_grid = data[-1].vegetation
        marmots_population = [data[x].marmots.sum() for x in range(len(data))]
        pasture = [data[x].pasture.sum() for x in range(len(data))]

        fig, axs = plt.subplots(2, 2)
        gridspec = fig.add_gridspec(2, 2)

        # clear the left column for the subfigure:
        for a in axs[:, 0]:
            a.remove()

        # plot data in remaining axes:
        create_plot(axs[:,1:].flat[0], marmots_population, input.years(), "Marmot population", "years", "population")
        create_plot(axs[:,1:].flat[1], pasture, input.years(), "Pasture volumes", "years", "tons")

        # make the subfigure in the empty gridspec slots:
        subfig = fig.add_subfigure(gridspec[:, 0])

        axsLeft = subfig.subplots(1, 2)
        create_colormesh(fig, marmots_grid, axsLeft[0], "Marmot population", "YlOrBr")
        create_colormesh(fig, vegetation_grid, axsLeft[1], "Vegetation, tons", "Greens")
        fig.tight_layout()
    
        return fig
    

    @output
    @render.plot
    @reactive.event(input.run)
    def batch_plot():
        data = get_data()
        # create data 
        pasture = [sublist[0] for sublist in data] 
        viability = [sublist[1]*100 for sublist in data] 
        mean_population = [sublist[2] for sublist in data] 
        
        # plot trends
        fig = plt.figure()
        plt.plot(pasture, viability, label = "Viability, %") 
        plt.plot(pasture, mean_population, label = "Mean population")
        plt.xlabel("Pasture, %")
        plt.legend()

        return fig
    

    @output
    @render.text
    @reactive.event(input.run)
    def text():
        data = get_data()
        inline_output = "Inline marmot population: "
        for year in range(input.years()):
            inline_output += f"\n {year+1} {data[year].marmots.sum()}"
        return inline_output
    

    @output
    @render.text
    @reactive.event(input.run)
    def batch_text():
        data = get_data()
        inline_output = "Pasture, %    Viability, %   Mean population"
        for row in range(len(data)):
            inline_output += f"\n {data[row]}"
        return inline_output


app = App(app_ui, server)
