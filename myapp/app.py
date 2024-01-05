from shiny import App, render, ui
from shiny.ui import h2, tags

import matplotlib.pyplot as plt

app_ui = ui.page_fluid(

    # Permitir formulas em LaTeX

    ui.head_content(
        ui.tags.script(
            src="https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
        ),
        ui.tags.script(
            "if (window.MathJax) MathJax.Hub.Queue(['Typeset', MathJax.Hub]);"
        ),
    ),

    # Titulo

    ui.panel_title("Modelo IS LM"),

    ui.row(
        ui.column(
            12,
            {"class": "col-lg-6 py-5 mx-auto"},
            # LaTeX
            ui.p( "$$IS: r = \\frac{A_{0}}{I_{2}} - \\frac{1-C_{1}*(1-t) - I_{1}}{I_{2}}*Y$$" ),
            ui.p( "$$LM: r = \\frac{ e }{ f }*Y - \\frac{ M^{s} }{ f }$$" ),
        ),
        ui.column(
            4,

            tags.h4("Plot Parameters"),
            ui.input_slider("x", "X axis Max Range", 0, 100, 30),
            ui.input_slider("y", "Y axis Max Range", 0, 100, 30),
        ),
        ui.column(
            4,

            tags.h4("IS Curve Parameters"),
            ui.input_slider("m", "Inclinação Curva IS", 0.0, 1.0, 1.0),
            ui.input_slider("A", "$$A_0$$", 0, 100, 30),
        ),
        ui.column(
            4,

            tags.h4("LM Curve Parameters"),
            ui.input_slider("n", "Inclinação Curva LM", 0.0, 1.0, 1.0),
            ui.input_slider("Md","$$M_d$$", 0, 100, 0),
        ),
    ),
    ui.column(
        4,

        tags.h4( "Policy Parameters"),
        ui.input_slider("fp", "Fiscal Policy", -1.0, 1.0, 0.0 ),
        ui.input_slider("mp", "Monetary Policy", -1.0, 1.0, 0.0 ),
    ),
    ui.column(
        12,
        {"class": "col-lg-6 py-5 mx-auto"},
        ui.output_plot("my_plot"),
    )
    
)

def server(input, output, session):

    @output

    @render.plot()

    def my_plot():

        # LM Curve

        lm_x_axis = [i for i in range(0, input.x())]
        lm_y_axis = [input.Md() + input.n() * i for i in lm_x_axis]

        # IS Curve

        is_x_axis = [i for i in range(0, input.x())]
        is_y_axis = [input.A() - i * input.m() for i in is_x_axis]
 
        # Otimização do Modelo IS-LM

        x_eq = (input.A() - input.Md()) / (input.m() + input.n())
        y_eq = input.Md() + input.n() * x_eq

        # Economic Policys

        fp_power = input.fp()*5

        mp_power = input.mp()*5*(-1)

        is_y_pol = [i + fp_power for i in is_y_axis] 

        lm_y_pol = [i + mp_power for i in lm_y_axis]

        x_eq_2 = (input.A() + fp_power - (input.Md() + mp_power)) / (input.m() + input.n())
        y_eq_2 = input.Md() + mp_power + input.n() * x_eq_2
        
        # Plot

        fig, ax = plt.subplots()

        ax.plot(lm_x_axis, lm_y_axis, label="LM")
        ax.plot(is_x_axis, is_y_axis, label="IS")

        # Economic Policies - plot
        
        ax.plot( is_x_axis, is_y_pol , label = "IS'",
                 linestyle = "--", color = "#FF0000A1" )

        ax.plot( lm_x_axis, lm_y_pol , label = "LM'",
                linestyle = "--", color = "#0100FFFF")

        

        ax.hlines(y_eq_2, xmin=0, xmax=x_eq_2, linestyles="dashed", colors="grey")
        ax.vlines(x_eq_2, ymin=0, ymax=y_eq_2, linestyles="dashed", colors="grey")

        ax.hlines(y_eq, xmin=0, xmax=x_eq, linestyles="dashed", colors="black")
        ax.vlines(x_eq, ymin=0, ymax=y_eq, linestyles="dashed", colors="black")

        ax.plot(x_eq, y_eq, "ro")

        ax.plot(x_eq_2, y_eq_2, "ro")
        
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.4), ncol=4)
        ax.text( 1.5, input.y() + 1, f"Y = {x_eq}, r = {y_eq}, Y' ={x_eq_2}, r' = {y_eq_2} ")

        plt.xlim(0, input.x())
        plt.ylim(0, input.y())
        plt.xlabel("Y - National Income")
        plt.ylabel("r - Interest Rate")

app = App(app_ui, server)