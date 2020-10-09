import pandas as pd
import numpy as np

from bokeh.plotting import figure
from bokeh.palettes import Category20
from bokeh.layouts import column
from bokeh.models import Legend, ColumnDataSource, HoverTool, Range1d, CustomJSHover
from bokeh.embed import components

from bokeh.models import TapTool, CustomJS

# def make_cluster_plot(plot_data, pod, recs):
#
#     # get x, y coordinates for pod and recs
#     main_pod = plot_data[plot_data['itunes_id'] == pod['itunes_id'][0]]
#     recs = recs.merge(plot_data, on=["title", "itunes_id", "genre", "subgenre"])
#
#     genre_list = list(plot_data.groupby(by="genre").groups.keys())
#     show_list = recs["genre"].unique()
#
#     p = figure(tools="wheel_zoom,pan,box_zoom,reset",\
#         plot_width=700, plot_height=500,\
#         toolbar_location="right")
#     p.toolbar.active_drag = None # disabling pan helps with scrolling on smartphones
#
#     # plot all data points and group them by genres for the legends
#     group = dict()
#     legend_items = []
#     for i, g in enumerate(genre_list):
#         source = ColumnDataSource(plot_data.loc[plot_data["genre"] == g])
#         group[g] = p.circle(x='x', y='y', size = 10,\
#             color = Category20[19][-(i+1)],\
#             fill_alpha=0.5,\
#             line_alpha=0, muted_color="lightgray",\
#             source = source, muted_alpha = 0.05)
#         legend_items.append((g,[group[g]]))
#         if g not in show_list: # only show genres that are in the recommendations
#             group[g].muted = True
#
#     # plot the recommendations on the current page
#     rend_main = p.hex('x', 'y', fill_color = 'ivory', line_color = "royalblue", \
#         line_width = 3, size = 15, \
#         fill_alpha = 1, source = ColumnDataSource(recs))
#     # plot the main podcast
#     p.circle(main_pod['x'], main_pod['y'], color = "red", size = 5)
#     p.circle(main_pod['x'], main_pod['y'], fill_color = "red", \
#         fill_alpha = 0.2, radius = 10, line_color = "red", \
#         line_alpha = 0.2)
#
#     custom_hover = HoverTool(mode="mouse", point_policy="snap_to_data", \
#         muted_policy = "ignore", renderers = [rend_main])
#
#     # limit the hover list to 5 items in case of overlapping glyphs
#     custom_formatter = CustomJSHover(code="""
#         special_vars.indices = special_vars.indices.slice(0,5)
#         if (special_vars.indices.indexOf(special_vars.index) >= 0)
#         {
#             return " "
#         }
#         else
#         {
#             return " hidden "
#         }""")
#     custom_hover.tooltips = """
#     <div @title{custom|safe}>
#         <div>
#         <img
#             src="@artwork_url" alt="@artwork_url" width="42"
#             style="margin: 5px 5px 5px 5px;"
#             border="2"
#         ></img>
#         <span style="font-size: 15px; font-weight: bold;">@title</span>
#         </div>
#     </div>
#     """
#     custom_hover.formatters = {'@title':custom_formatter}
#
#     p.add_tools(custom_hover)
#
#     p.outline_line_width = 7
#     p.outline_line_alpha = 0.2
#     p.outline_line_color = "navy"
#     p.toolbar.autohide = True
#     p.grid.visible = False
#
#     legends = []
#     for i in range(0, len(legend_items), 4):
#         legends.append(Legend(items=legend_items[i:i+4], margin=2))
#     for legend in legends:
#         p.add_layout(legend,'below')
#
#     p.plot_height = (600 + ((len(legend_items)-1)//4)*40)
#
#     p.legend.click_policy="mute"
#     p.legend.location = "bottom_center"
#     p.legend.orientation = "horizontal"
#
#     clusters = column([p], sizing_mode = "stretch_width")
#     return components(clusters)

def make_cluster_plot(plot_data, pod, recs):

    # get x, y coordinates for pod and recs
    main_pod = plot_data[plot_data['itunes_id'] == pod['itunes_id'][0]]
    recs = recs.merge(plot_data, on=["title", "itunes_id", "genre", "subgenre"])

    genre_list = list(plot_data.groupby(by="genre").groups.keys())
    show_list = recs["genre"].unique()

    p = figure(tools="wheel_zoom,pan,box_zoom,reset,tap",\
        plot_width=700, plot_height=500,\
        toolbar_location="right")
    p.toolbar.active_drag = None # disabling pan helps with scrolling on smartphones

    # plot all data points and group them by genres for the legends
    group = dict()
    legend_items = []
    for i, g in enumerate(genre_list):
        source = ColumnDataSource(plot_data.loc[plot_data["genre"] == g])
        group[g] = p.circle(x='x', y='y', size = 10,\
            color = Category20[19][-(i+1)],\
            fill_alpha=0.5,\
            line_alpha=0, muted_color="lightgray",\
            source = source, muted_alpha = 0.05)
        legend_items.append((g,[group[g]]))
        if g not in show_list: # only show genres that are in the recommendations
            group[g].muted = True

    # plot the recommendations on the current page
    recs_source = ColumnDataSource(recs)
    rend_main = p.hex('x', 'y', fill_color = 'ivory', line_color = "royalblue", \
        line_width = 3, size = 15, \
        fill_alpha = 1, source = recs_source)
    # plot the main podcast
    p.circle(main_pod['x'], main_pod['y'], color = "red", size = 5)
    p.circle(main_pod['x'], main_pod['y'], fill_color = "red", \
        fill_alpha = 0.2, radius = 10, line_color = "red", \
        line_alpha = 0.2)

    custom_hover = HoverTool(mode="mouse", point_policy="snap_to_data", \
        muted_policy = "ignore", renderers = [rend_main])

    # limit the hover list to 5 items in case of overlapping glyphs
    custom_formatter = CustomJSHover(code="""
        special_vars.indices = special_vars.indices.slice(0,5)
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
    for i in range(0, len(legend_items), 4):
        legends.append(Legend(items=legend_items[i:i+4], margin=2))
    for legend in legends:
        p.add_layout(legend,'below')

    p.plot_height = (600 + ((len(legend_items)-1)//4)*40)

    p.legend.click_policy="mute"
    p.legend.location = "bottom_center"
    p.legend.orientation = "horizontal"

    # url for selected recommendation
    code = """
    var ind = source.selected.indices
    if (ind.length==1) {
        var itunes_id = source.data['itunes_id'][ind]
    } else {
        var itunes_id = source.data['itunes_id'][ind[0]]
    }
    var url = "/itunes_id=".concat(itunes_id, "&offset=0")
    window.open(url, "_self")
    """
    taptool = p.select(type=TapTool)
    taptool.renderers = [rend_main]
    taptool.callback = CustomJS(args=dict(source=recs_source), code=code)

    clusters = column([p], sizing_mode = "stretch_width")
    return components(clusters)
