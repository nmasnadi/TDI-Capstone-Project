import pandas as pd
import numpy as np

from bokeh.plotting import figure #, show, output_file, save
from bokeh.palettes import Category20
from bokeh.layouts import column
from bokeh.models import Legend, ColumnDataSource, HoverTool, Range1d
from bokeh.resources import CDN
from bokeh.embed import file_html

def make_cluster_plot(plot_data, genre_show_list = []):

    genre_list = list(plot_data.groupby(by="genre").groups.keys())

    p = figure(title = "Podcast Clusters (t-SNE)",\
       tools="wheel_zoom,pan,box_zoom,reset",\
       plot_width=700, plot_height=500,\
       toolbar_location="left")
    # title properties
    p.title.align = "center"
    p.title.text_font_size = "20px"

    group = dict()
    items1 = []
    items2 = []
    rends = []
    for i, g in enumerate(genre_list):
        genre_idx = plot_data[plot_data["genre"] == g].index.to_list()
        source = ColumnDataSource(\
            dict(x=plot_data.loc[genre_idx,'x'],\
               y=plot_data.loc[genre_idx,'y'],\
               title = plot_data.loc[genre_idx, "titles"],\
               genre = plot_data.loc[genre_idx, "genre"],\
               subgenre = plot_data.loc[genre_idx, "subgenre"]))
        group[g] = p.circle(x='x', y='y', size = 10,\
                 color = Category20[19][-(i+1)],\
                 fill_alpha=0.5,\
                 line_alpha=0, muted_color="lightgray",\
                 source = source, muted_alpha = 0.05\
                )
        if g not in genre_show_list:
            group[g].muted = True
            items2.append((g,[group[g]]))
        else:
            items1.append((g,[group[g]]))
            rends.append(group[g])

    # create the hover tool - modified to show only one result
    custom_hover = HoverTool(mode="mouse", point_policy="follow_mouse",\
        renderers = rends)
    custom_hover.tooltips = """
        <style>
            .bk-tooltip>div:not(:first-child) {display:none;}
        </style>

        <b>Title: </b> @title <br>
        <b>Genre: </b> @genre | @subgenre
    """
    p.add_tools(custom_hover)

    # p.axis.visible = False
    p.outline_line_width = 7
    p.outline_line_alpha = 0.2
    p.outline_line_color = "navy"
    p.toolbar.autohide = True
    p.grid.visible = False

    legends = []
    legends.append(Legend(items=items1))
    # for i in range(0, len(items2), 6):
    #     legends.append(Legend(items=items2[i:i+6]))
    for legend in legends:
        p.add_layout(legend,'below')

    p.legend.click_policy="mute"
    p.legend.location = "bottom_center"
    p.legend.orientation = "horizontal"

    clusters = column([p], sizing_mode = "scale_width")
    return file_html(clusters, CDN, "my plot")
