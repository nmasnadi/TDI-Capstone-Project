import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.layouts import column
from bokeh.models import Legend, ColumnDataSource, HoverTool, Range1d, CustomJSHover
from bokeh.embed import components

def make_cluster_plot(plot_data, pod, recs):

    main_pod = plot_data[plot_data['itunes_id'] == pod['itunes_id'][0]]
    recs = recs.merge(plot_data, on=["title", "itunes_id", "genre", "subgenre"])
    genre_list = list(plot_data.groupby(by="genre").groups.keys())
    show_list = recs["genre"].unique()

    # p = figure(title = "Podcast Clusters (t-SNE)",\
    p = figure(tools="wheel_zoom,pan,box_zoom,reset",\
        plot_width=700, plot_height=500,\
        toolbar_location="right")
    p.toolbar.active_drag = None
    p.title.align = "center"
    p.title.text_font_size = "20px"

    # plot all data points
    group = dict()
    items1 = []
    for i, g in enumerate(genre_list):
        genre_idx = plot_data[plot_data["genre"] == g].index.to_list()
        source = ColumnDataSource(dict(x=plot_data.loc[genre_idx,'x'],\
            y=plot_data.loc[genre_idx,'y'],\
            title = plot_data.loc[genre_idx, "title"],\
            genre = plot_data.loc[genre_idx, "genre"],\
            subgenre = plot_data.loc[genre_idx, "subgenre"]))
        group[g] = p.circle(x='x', y='y', size = 10,\
            color = Category20[19][-(i+1)],\
            fill_alpha=0.5,\
            line_alpha=0, muted_color="lightgray",\
            source = source, muted_alpha = 0.05)
        items1.append((g,[group[g]]))
        if g not in show_list:
            group[g].muted = True

    # plot the recommendations on the current page
    source = ColumnDataSource(dict(x=recs['x'], y=recs['y'], \
        title = recs['title'], artwork_url = recs["artwork_url"],\
        rank = recs.index))
    rend_main = p.hex('x', 'y', fill_color = 'ivory', line_color = "royalblue", \
        line_width = 3, size = 15, \
        fill_alpha = 1, source = source)
    # plot the main podcast
    p.circle(main_pod['x'], main_pod['y'], color = "red", size = 5)
    p.circle(main_pod['x'], main_pod['y'], fill_color = "red", \
        fill_alpha = 0.2, radius = 10, line_color = "red", \
        line_alpha = 0.2)

    custom_hover = HoverTool(mode="mouse", point_policy="snap_to_data", \
        muted_policy = "ignore", renderers = [rend_main])

    custom_formatter = CustomJSHover(code="""
        special_vars.indices = special_vars.indices.slice(0,3)
        if (special_vars.indices.indexOf(special_vars.index) >= 0)
        {
            return " "
        }
        else
        {
            return " hidden "
        }""")
    custom_hover.tooltips = """
    <div @title{custom|safe}>
        <div>
        <img
            src="@artwork_url" alt="@artwork_url" width="42"
            style="margin: 5px 5px 5px 5px;"
            border="2"
        ></img>
        <span style="font-size: 15px; font-weight: bold;">@title</span>
        </div>
    </div>
    """
    custom_hover.formatters = {'@title':custom_formatter}

    p.add_tools(custom_hover)

    p.outline_line_width = 7
    p.outline_line_alpha = 0.2
    p.outline_line_color = "navy"
    p.toolbar.autohide = True
    p.grid.visible = False

    legends = []
    for i in range(0, len(items1), 4):
        legends.append(Legend(items=items1[i:i+4]))
    for legend in legends:
        p.add_layout(legend,'below')

    p.plot_height = (600 + ((len(items1)-1)//4)*47)

    p.legend.click_policy="mute"
    p.legend.location = "bottom_center"
    p.legend.orientation = "horizontal"

    clusters = column([p], sizing_mode = "stretch_width")
    return components(clusters)
