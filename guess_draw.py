from bokeh.plotting import figure, output_file
from bokeh.io import save, show
from bokeh.models import ColumnDataSource,HoverTool, Div, Label
from bokeh.transform import linear_cmap
from bokeh.palettes import Turbo256
from bokeh.layouts import column
import random

class render_history:

    def __init__(self,xmax,ymax):
        self.xmax = xmax
        self.ymax = ymax

    def generate_history(self, attempdata, guessdata):
        x = list(range(1, self.xmax+1))
        y = list(range(10, self.ymax+1, 10))
        f = figure(
                height=100,
                title="📊 Lucky Number Guess History",
                x_axis_label="Attempt",
                y_axis_label="Guessed Number",
                x_range= (1,self.xmax+1),
                y_range= (1, self.ymax+1),
                toolbar_location=None,
                background_fill_color="#f9fafc",
            )
        f.xaxis.ticker = x
        f.yaxis.ticker = y
        f.xaxis.major_label_overrides = {i: str(i) for i in x}
        f.title.text_color = "white"
        f.title.background_fill_color = "blue"
        f.title.text_font_size = "15px"

        source = ColumnDataSource(data={
                "attempt": list(range(1,attempdata+1)),
                "guess": guessdata
        })

        mapper = linear_cmap(field_name="guess", palette=Turbo256, low=1, high=100)
        f.line(x="attempt", y="guess", source=source, line_width=2, color="gray", alpha=0.4)
        circles = f.scatter(
            x="attempt",
            y="guess",
            source=source,
            size=12,
            color=mapper,
            marker="circle",
            line_color="black",
            line_width=0.5,
        )
        h = HoverTool(renderers=[circles],
                      tooltips=[("Attempt", "@attempt"),("Guess Value", "@guess")])
        f.add_tools(h)
        return f
        # --- Display ---
        #output_file("guess_chart.html")
        #save(f)
        #show(f)

"""
f.title.text = "Lucky Number Guessing Game"
f.title.align = "center"
f.title.text_color = "white"
f.title.background_fill_color = "blue"
f.title.text_font_size = "25px"

f.circle(x=x, y=y, size=20, color="red")
show(f)
"""