#!/usr/bin/env python

__version__ = '1.0'
__date__ = '02-09-2024'
__author__ = 'E.F.Fotopoulou'

import pandas as pd
import numpy as np
import geopandas as gpd
import os

from mpl_toolkits.basemap import Basemap
import plotly.express as px
import fiona
from shapely.geometry import MultiPolygon, Polygon

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.patheffects as PathEffects
import matplotlib.lines as mlines
from matplotlib.colors import LinearSegmentedColormap, Normalize

import argparse
import ast

import time
import progressbar

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def parse_args():
    description = "Map creation with pie charts"
    parser = argparse.ArgumentParser(description=description)
    
    #essential parameters
    parser.add_argument('--shape_file', required=True, help="Path to shape file")
    parser.add_argument('--metadata_file', required=True, help="Path to metadata file")
    parser.add_argument('--agg_column', required=True, help="Aggregation column for pie charts")
    parser.add_argument('--colours_dict', required=True, type=str, help="Colours dictionary for pie charts")

    #parameters for maps outside England
    parser.add_argument('--llcrnrlon', type=float, default=-6, help="Lower left corner longitude of the map")
    parser.add_argument('--llcrnrlat', type=float, default=49.9, help="Lower left corner latitude of the map")
    parser.add_argument('--urcrnrlon', type=float, default=2, help="Upper right corner longitude of the map")
    parser.add_argument('--urcrnrlat', type=float, default=55.9, help="Upper right corner latitude of the map")


    #parameters for background map information
    parser.add_argument('--agg_mapinfo', default=None, help="Optional aggregation column for map density (Chloropleth)")
    parser.add_argument('--colormap', default='BuPu', type=str, help="Colormap for the map. Colour Palettes: 'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'. Alternatively create a custom list of at least two Hex codes (eg. --colormap='[\"#E0ECF4\", \"#4D004B\"]')")

    #parameters for simple map
    parser.add_argument('--plainmapcol', default="lightsteelblue", help="Colour of the simple map")
    parser.add_argument('--simple_map_boundaries', action='store_true', help="Flag for adding map boundaries on the simple map plot")

    #pie chart arguments
    parser.add_argument('--label_style', default=None, help="Style of the pie chart labels. Default: None. If not set no label is printed on the pie charts. Options:style1 or style2. Style1: percentages of pie segments. Style2: Total number of counts per region.")
    parser.add_argument('--pie_fontsize', type=int, default=15, help="Font size of the pie chart labels. Suggested range: 5-10")
    parser.add_argument('--pie_rotation', type=int, default=0, help="Rotation of the pie chart labels. Range: 0-180")
    parser.add_argument('--pie_size', type=float, default=100, help="Size of pie chart circle. Default size 100. Suggested range: 100-1000")
    parser.add_argument('--pie_text_loc', type=float, default=0.17, help="Pie marker location. Range: 0.01 - 1")

    #colour bar legend parameters
    parser.add_argument('--colorbar_title', default='ColourBar', help="Title for the colorbar for map density")
    parser.add_argument('--colorbar_fontsize', type=int, default=20, help="Font size of the colorbar")

    #figure legend parameters
    parser.add_argument('--legend_title', default='Legend', help="Title for pie chart legend")
    parser.add_argument('--legend_fontsize', type=int, default=20, help="Font size of the legend")
    parser.add_argument('--legend_bbox_to_anchor', nargs=4, type=float, default=[0.005,0.6,0,0], help="Coordinates for position of legend box. Default = 0.005 0.6 0 0. Range: 0 - 1. Follows the same structure as Matplotlib's legend function bbox_to_anchor where tuple is (x,y,width, height).")

    #paramenters for outout file save
    parser.add_argument('--output_file_prefix', default='Output_map', help="Title of the output map file. Omit file format extension. (eg 'Figure01' not 'Figure01.png')")
    parser.add_argument('--file_format', default='png', help="Format type for output figure. Default is png. Options: png,jpeg,svg,pdf")
    parser.add_argument('--dpi', type=float, default=300, help="Figure resolution in dots per inch. Default is 300")

    args = parser.parse_args()
    # Convert the colours_dict string to an actual dictionary
    args.colours_dict = ast.literal_eval(args.colours_dict)

    
    # Convert colormap to a list if it’s a string that represents a list
    try:
        args.colormap = ast.literal_eval(args.colormap)
        if not isinstance(args.colormap, list):
            raise ValueError
    except (ValueError, SyntaxError):
        # If it's not a list, keep it as a string (for standard colormaps)
        pass

    return args

def main():
    args = parse_args()
    
    create_map_with_pie_charts(args.shape_file, args.metadata_file, args.agg_column, args.colours_dict,
                                args.agg_mapinfo, args.plainmapcol,
                                args.pie_size, args.simple_map_boundaries,
                                args.legend_title, args.colorbar_title, args.colormap,
                                args.label_style, args.pie_fontsize, args.pie_rotation,
                                args.legend_fontsize, args.colorbar_fontsize,
                                args.llcrnrlon, args.llcrnrlat, args.urcrnrlon, args.urcrnrlat,
                                args.output_file_prefix, args.file_format, args.dpi,
                                args.legend_bbox_to_anchor,
                                args.pie_text_loc)

#function generating pie charts in scatter plot
def draw_pie(dist, xpos, ypos, pie_size, colors, basemap, ax=None, label_style=None, pie_fontsize=10, pie_rotation=25, pie_text_loc=0.17):
    if ax is None:
        fig, ax = plt.subplots(figsize=(20, 18))
    
    total = np.sum(dist)
    cumsum = np.cumsum(dist)
    cumsum = cumsum / cumsum[-1]
    pie = [0] + cumsum.tolist()
    
    for r1, r2, color, value in zip(pie[:-1], pie[1:], colors, dist):
        angles = np.linspace(2 * np.pi * r1, 2 * np.pi * r2, 100)
        x = [0] + np.cos(angles).tolist()
        y = [0] + np.sin(angles).tolist()
        xy = np.column_stack([x, y])

        #calculate the midpoint angle for the section
        mid_angle = (r1 + r2) * np.pi
        center_x = xpos + pie_text_loc * np.cos(mid_angle)
        center_y = ypos + pie_text_loc * np.sin(mid_angle)
        percentage = value * 100

        #convert center_x and center_y of pie charts to map projection
        mcx, mcy = basemap(center_x, center_y)
        
        #setting markers for style1 of pie charts
        if label_style == 'style1':
            t = ax.text(mcx, mcy, f'{percentage:.1f}%', ha='center', va='center', 
                        fontsize=pie_fontsize, fontweight="bold", color='black', 
                        rotation=pie_rotation)
            t.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])
        
        # Convert scatter plot xpos and ypos coordinates to map projection
        mx, my = basemap(xpos, ypos)
        ax.scatter(mx, my, marker=xy, s=pie_size, color=color, edgecolor='white', alpha=1)

#start progress bar
bar = progressbar.ProgressBar().start()

def create_map_with_pie_charts(shape_file, metadata_file, agg_column, colours_dict,
                               agg_mapinfo=None, plainmapcol="lightsteelblue", 
                               pie_size=100,
                               simple_map_boundaries=False, legend_title='Legend', colorbar_title='ColourBar',
                               colormap='BuPu', label_style=None, pie_fontsize=15, pie_rotation=0,
                               legend_fontsize=20, colorbar_fontsize=20,
                               llcrnrlon=-6, llcrnrlat=49.9, urcrnrlon=2, urcrnrlat=55.9, 
                               output_file_prefix='Output_map',file_format="png", dpi=300, legend_bbox_to_anchor=[0.005,0.6,0,0],
                               pie_text_loc=0.17):


    #set two input files. Shapefile and metadatafile
    shape = gpd.read_file(shape_file)
    human_meta = pd.read_excel(metadata_file)

    #merge two input files
    shape = shape.merge(human_meta, how="right", on="RGN21NM")
    shape = shape.dropna(subset=["RGN21NM"])
    
    #setting format of shapefile for simple map to read region directories
    shape_dir = os.path.dirname(shape_file)
    base_name = os.path.splitext(os.path.basename(shape_file))[0]

    #reformating projection of shape file (requires fiona library)
    shape = shape.to_crs(epsg=4326)

    fig, ax = plt.subplots(figsize=(20, 18))

    #creating bounding box coordinates to ensure shape file coordinates are contained within the box.
    bounding_box = Polygon([(llcrnrlon, llcrnrlat), (urcrnrlon, llcrnrlat), (urcrnrlon, urcrnrlat), (llcrnrlon, urcrnrlat)])
    shapes_in_bbox = shape[shape.geometry.apply(lambda geom:
        (isinstance(geom, Polygon) and geom.intersects(bounding_box)) or
        (isinstance(geom, MultiPolygon) and any(poly.intersects(bounding_box) for poly in geom.geoms))
    )]

    #raising Errors
    if shapes_in_bbox.empty:
        raise ValueError("The Background map coordinates are not within the bounds of the shape file. Please adjust the coordinates.")
            
    if not pd.api.types.is_string_dtype(shape[agg_column]) and not pd.api.types.is_object_dtype(shape[agg_column]):
        raise ValueError("The aggregation column used for the pie charts, must be non-numeric categorical data.")

    if label_style != None and label_style != 'style1' and label_style != 'style2': 
        raise ValueError("The label styles can only be blank, 'style1': displaying percentages of each pie segment, or 'style2': displaying total number of counts.")        

    #extract the representative points for regions and split them into X and Y coordinates
    shape['coords'] = shape['geometry'].apply(lambda x: x.representative_point().coords[:])
    shape['coords'] = [coords[0] for coords in shape['coords']]
    shape["X"], shape["Y"] = zip(*shape["coords"])
    
    if agg_mapinfo is None:
        #create a Basemap instance
        m = Basemap(projection='merc', resolution='i', area_thresh=0.1, 
                    llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat,
                    ax=ax)
        m.drawcountries()
        m.drawmapboundary(linewidth=0)
        m.fillcontinents(color=plainmapcol)
        m.drawcoastlines()
        
        #creating boundaries on simple map
        if simple_map_boundaries:
            m.readshapefile(os.path.join(shape_dir, base_name), base_name)

        #editing metadata input data for pie chart on Map
        region_agg2 = shape.groupby(["RGN21NM", "X", "Y"])[agg_column].value_counts().to_frame(name="Counts")
        region_agg2 = region_agg2.reset_index()

        total_counts = region_agg2.groupby("RGN21NM")["Counts"].sum()
        region_agg2["Total cases"] = region_agg2["RGN21NM"].map(total_counts)

        for (region_name, xpos, ypos), group in region_agg2.groupby(["RGN21NM", "X", "Y"]):
            group["colours"] = group[agg_column].map(colours_dict)
            colors = group["colours"].tolist()
            total_cases = group["Total cases"].iloc[0]
            num_cases = group["Counts"].tolist()
            dist = [num / total_cases for num in num_cases]
            tx, ty = m(xpos, ypos)

            draw_pie(dist, xpos, ypos, total_cases * pie_size, colors, m, ax=ax, label_style=label_style, pie_fontsize=pie_fontsize, pie_rotation=pie_rotation, pie_text_loc=pie_text_loc)
            
            #setting markers for style2 of pie charts
            if label_style == 'style2':
                t = plt.annotate('n= {}'.format(total_cases), (tx, ty),
                                 color='black', fontsize=20, fontweight="bold",
                                 path_effects=[PathEffects.withStroke(linewidth=5, foreground='w')])


            #setting legend for pies
            legend_handles = [mlines.Line2D([], [], color=color, marker='o', linestyle='None', 
                                        markersize=10, label=label) 
                          for label, color in colours_dict.items()]
            plt.legend(handles=legend_handles, title=legend_title, title_fontsize=legend_fontsize + 5, 
                     fontsize=legend_fontsize, bbox_to_anchor=legend_bbox_to_anchor)

    #code for complex map with background information (Chloropleth)
    else:
        #raise error
        if not pd.api.types.is_numeric_dtype(shape[agg_mapinfo]):
            raise ValueError("The aggregation column for Choropleth map (Map density) must be numeric data.")

        #create Background map
        m = Basemap(projection='merc', resolution='i', area_thresh=0.1, llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat, urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, ax=ax)
        m.drawcountries()
        m.drawmapboundary()

        # Determine if the colormap is a custom list or a predefined palette
        if isinstance(colormap, str):
            cmap = cm.get_cmap(colormap, 100)
        elif isinstance(colormap, list):
            cmap = LinearSegmentedColormap.from_list('custom_colormap', colormap, N=100)
        else:
            raise ValueError("Invalid colormap format. Provide a colormap name or a list of at least two HEX colors.")

        # Normalize values for the colormap
        norm = Normalize(vmin=shape[agg_mapinfo].min(), vmax=shape[agg_mapinfo].max())

        #adjust shapefile for coordinates in both MultiPolygon and Polygon formats
        for idx, row in shape.iterrows():
            color = cmap(norm(row[agg_mapinfo]))
            geom = row['geometry']
            if isinstance(geom, Polygon):
                geom = [geom]
            elif isinstance(geom, MultiPolygon):
                geom = geom.geoms
            for poly in geom:
                x, y = zip(*list(poly.exterior.coords))
                mx, my = m(x, y)
                ax.fill(mx, my, color=color)

        #as previously edit metadata input data for pie chart on Map
        region_agg2 = shape.groupby(["RGN21NM", "X", "Y"])[agg_column].value_counts().to_frame(name="Counts")
        region_agg2 = region_agg2.reset_index()

        total_counts = region_agg2.groupby("RGN21NM")["Counts"].sum()
        region_agg2["Total cases"] = region_agg2["RGN21NM"].map(total_counts)

        for (region_name, xpos, ypos), group in region_agg2.groupby(["RGN21NM", "X", "Y"]):
            group["colours"] = group[agg_column].map(colours_dict)
            colors = group["colours"].tolist()
            total_cases = group["Total cases"].iloc[0]
            num_cases = group["Counts"].tolist()
            dist = [num / total_cases for num in num_cases]
            tx, ty = m(xpos, ypos)

            draw_pie(dist, xpos, ypos, total_cases * pie_size, colors, m, ax=ax, label_style=label_style, pie_fontsize=pie_fontsize, pie_rotation=pie_rotation, pie_text_loc=pie_text_loc)
    
            #setting markers for style2 of pie charts
            if label_style == 'style2':
                t = plt.annotate('n= {}'.format(total_cases), (tx, ty), fontsize=pie_fontsize, color="black", weight="black")
                t.set_path_effects([PathEffects.withStroke(linewidth=5, foreground='w')])

        #setting parameters for colour bar of map
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, orientation='vertical', shrink=0.4)
        cbar.set_label(colorbar_title, labelpad=-65, fontsize=colorbar_fontsize)

        #setting parameters of pie chart legend
        legend_handles = [mlines.Line2D([], [], color=color, marker='o', linestyle='None', 
                                        markersize=10, label=label) 
                          for label, color in colours_dict.items()]
        plt.legend(handles=legend_handles, title=legend_title, title_fontsize=legend_fontsize + 5, 
                    fontsize=legend_fontsize, bbox_to_anchor=legend_bbox_to_anchor)

    plt.axis("off")
    valid_formats = ['png', 'jpeg', 'svg', 'pdf']

    #raise error
    if file_format not in valid_formats:
        raise ValueError(f"Invalid format: {file_format}. Choose from {valid_formats}.")

    #save output
    plt.savefig(f"{output_file_prefix}.{file_format}", format=file_format, dpi=dpi)
    
   #finish progress bar 
    bar.finish()
    plt.show()

if __name__ == "__main__":
    main()

