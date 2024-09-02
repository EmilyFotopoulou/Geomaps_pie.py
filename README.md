
![Final_final_logo](https://github.com/user-attachments/assets/599c5bb0-8bfe-46c3-8785-5ed5afeb4230)


# Overview

Geomaps_pie.py  is a Python program designed to plot geographical locations and overlay pie charts at the centre of each plotted area. It also features the ability to present map density information using a choropleth map. 

The program requires a shapefile for the geographic plotting and a corresponding metadata file (in xlsx format) to generate the pie chart visualizations.

![examples](https://github.com/user-attachments/assets/fed14800-53cf-4768-a03a-b129ba5daba2)


![examples3](https://github.com/user-attachments/assets/fa86d557-b252-461a-b384-9f07fc813779)



> [!IMPORTANT]
> Please note that all examples shown are based on dummy data, created solely for the purpose of demonstrating the program's capabilities. The figures presented do not reflect actual trends.


# Table of contents
* [Installation](#Installation)
* [Inputs](#Inputs)
* [Arguments](#Arguments)
* [Output](#Output)
* [Usage and Examples](#Usage)
* [Online Tutorial](#Tutorial)
* [Acknowledgments](#Acknowledgments)

# Installation <a name="Installation"></a>
## Dependencies
### Manual Installation

```
>you can manually install all dependencies by running:
conda install conda-forge::matplotlib-base=3.5.2 conda-forge::pandas conda-forge::basemap conda-forge::geopandas plotly::plotly conda-forge::fiona conda-forge::shapely conda-forge::openpyxl conda-forge::typed-ast conda-forge::progressbar
```

> [!NOTE]
> Note version of matplotlib that works faster is 3.5.2*

\
_Alternatively, by downloading the Github repository and activating the environment like shown in section below._

### GitHub repository installation

```
# Download this GitHub repository
git clone https://github.com/EmilyFotopoulou/Geomaps_pie.py.git

# Set up conda dependencies 
conda env create -f env_geomaps.yml 

# Activate environment
conda activate env_geomaps
```

![conda_env](https://github.com/user-attachments/assets/2c9c7194-cc25-45df-a587-952a0603add1)


> [!TIP]
> Test successful instalation by running:
> 
> `python Geomaps_pie.py --shape_file jam_admbnda_adm1_sdc_20240802_fixed.shp --metadata_file Jamaica_metadata_test.xlsx --llcrnrlon=-78.397064 --llcrnrlat=17.691129 --urcrnrlon=-76.164093 --urcrnrlat=18.553834 --agg_column 'Plasmids' --colours_dict "{'InCFIB':'yellow', 'InCP':'deeppink', 'InCA/C':'#00DD08', 'InCN':'darkturquoise'}"`

# Inputs <a name="Inputs"></a>
The program requires 4 inputs to run.
1)	A shapefile (.shp) with the country and or regions to be plotted. Shapefiles vary throughout different databases, may not have the required columns. File needs to contain a column with geographical named divisions (e.g.ADM1_EN). To amend this, please see section below. E.g.:

<div align="center">
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/719f4e97-0a57-42eb-8b4b-3a8b0e77c144">
</div>

2) 	A metadata file (.xlsx) is required. It should have a minimum of two columns for the program to run. One column should be the country and/or regions to be plotted (the column must be named “RGN21NM” and this column should match the shapefile *) and at least one column with categorical values (e.g. Plasmids) used for the pie charts.  Optional numerical column used for the background map density values (e.g. Population). Any additional columns can be added (e.g. Isolates) without affecting the efficiency or function of the program. E.g.:
  
<div align="center">
  <img width="500" alt="image" src="https://github.com/user-attachments/assets/f7af83e2-6058-47d0-83cd-b5c1a7cf3817">
</div>

> [!NOTE]
> If your shapefile is missing the column 'RGN21NM' it can be adjusted with the `fix_shapefile.py` script.* [Editing shapefiles](https://github.com/EmilyFotopoulou/Geomaps_pie.py/blob/main/README.md#editshape)
<br/>

3) The name of the column containing the categorical values to be used for the pie charts.
E.g.: 'Plasmids'

4) A dictionary linking the categorical values of the pie charts to the desired colours for the pie chart sections. 
E.g.: 
"{'InCFIB':'yellow', 'InCP':'red', 'InCA/C':'pink’, 'InCN':'blueviolet'}"

## Editing shapefiles <a name="editshape"></a>
_This script will edit your shapefile to adjust your headers to the correct name structure._


The script needs to be run twice. For the first run, simply provide the directory path to your shapefile. E.g.:

`python fix_shapefile.py –-shapefile jam_admbnda_adm1_sdc_20240802.shp`

> [!NOTE]
> The areas could be regions, countries, cities or any geographic specification you require.
> 
> Ensure that the areas chosen on your shapefile are in the same format as in your metadata file. (e.g. if your shapefile contains 'London' and your metadata contains "Greater London Area") Geomaps_pie.py wont run successfully.
<br/>

The program will display the first 5 rows of your shapefile, allowing you to identify the column that contains the area names you want to plot.  
<br/>

After identifying the column of interest, run the code a second time, specifying the column you want to plot.

`python fix_shapefile.py –-shapefile jam_admbnda_adm1_sdc_20240802_fixed.shp --column "ADM1_EN"`

This will adjust your shapefile for the Geomaps_pie.py to run.

> [!TIP]
> Don’t forget to adjust your input shapefile to 'the _fixed' version.


### Exaple

![fix_shape](https://github.com/user-attachments/assets/a7d8178b-fbec-4555-928b-6b1b80f296b0)


# Arguments <a name="Arguments"></a>
`
usage: Geomaps_pie.py [-h] (--shape_file --metadata_file --agg_column --colours_dict --llcrnrlon --llcrnrlat --urcrnrlon --urcrnrlat --agg_mapinfo --colormap --plainmapcol --simple_map_boundaries --label_style --pie_fontsize --pie_rotation --pie_size --pie_text_loc --colorbar_title --colorbar_fontsize --legend_title --legend_fontsize --legend_bbox_to_anchor --output_file_prefix --file_format --dpi)
`
## Mandatory
**`--shape_file`** : directory to input shapefile .shp

**`--metadata_file`**  : directory to metadata excel file .xlsx

**`--agg_column`**  : a string with the name of the column for the pie charts

**`--colours_dict`**  : a dictionary (see format above) assigning pie values to colours 

## Optional

**`--llcrnrlon –llcrnrlat --urcrnrlon --urcrnrlat`**  : a set of four numerical values setting the bounding box coordinates for regions outside of England. Default set to England.
```
LLCRNRLON Lower left corner longitude of the map 
LLCRNRLAT Lower left corner latitude of the map 
URCRNRLON Upper right corner longitude of the map 
URCRNRLAT Upper right corner latitude of the map 
```

You can find find the bounding box coordinates using a number of geographic map tools including:
http://bboxfinder.com

<div align="center">
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/49f97931-b7df-4943-ad94-1b914b5f267d">
</div>

<br />
<div align="center">
  <img width="800" alt="image" src="https://github.com/user-attachments/assets/f989f6e4-7d2b-4575-bdee-cfe92afb81c3">
</div>


#### Embelished map - diplays choropleth information on map along the pie charts:

**`--agg_mapinfo`**  : a string with the name of the column for the map background density information

**`--colormap`**  : a string with the name of a Matplotlib pallet, or a list of at least two custom Hex colour codes. (use -h for colour pallet options and example of list of Hex code in examples section). 

#### Simple map - only displays map area and boundaries along the pie charts:

**`--plainmapcol`**  : a string of a Matplotlib colour or Hex colour code setting the background colour of the map. Default: “lightsteelblue”

**`--simple_map_boundaries`**  : a default argument that adds boundary lines to the simple version of the map. Does not require setting to True. 

#### Pie chart editing:

**`--label_style`**  : Option of strings: ‘None’, ‘style1‘, ‘style2’. Setting the marker label style printed on top of the pie charts. Style1 shows the precentages of each pie segment. ‘style2‘ shows the total number of counts per region. 

**`--pie_fontsize`**  : a numerical value setting the font of the marker labels on the pie chart charts. 

**`--pie_rotation`**  : a numerical value setting the angle of rotation.

**`--pie_size`**  : a numerical value setting the size of the pie chart. Default size: 100. 

**`--pie_text_loc`**  : a numerical value setting the distance from the centre of each pie chart to display the text marker. Range: 0-1.

#### Colour bar editing:

**`--colorbar_title`**  : a string setting the title of the Colorbar displaying map density. 

**`--colorbar_fontsize`**  : a numerical value setting the font size of the title of the colorbar.

#### Figure legend editing:

**`--legend_title`**  : a string setting the title of the information displayed on the pie charts. 

**`--legend_fontsize`**  : a numerical value setting the font size of the legend box. Note, the title of the legend will always be 5 points larger than the rest of the legend box.

**`--legend_bbox_to_anchor`**  : a set of four numerical values that set the coordinates for position of legend box. Default: 0.005 0.6 0 0. Follows the same structure as Matplotlib's legend function bbox_to_anchor where tuple is (x, y, width, height).

```
The bbox_to_anchor parameter in Matplotlib’s legend function allows you to specify the location of the legend relative to the bounding box of the axes or figure. This parameter takes a tuple of the form (x, y, width, height), where:
•	x and y specify the position of the legend box anchor point.
•	width and height are optional and specify the size of the legend box. These are typically set to 1 if not specified.
Ranges for bbox_to_anchor
1)	x (horizontal position): The x-coordinate specifies the horizontal position of the legend. It ranges from negative infinity to positive infinity.
  • 0 corresponds to the left side of the bounding box.
  • 0.5 corresponds to the center.
  • 1 corresponds to the right side.
2)	y (vertical position): The y-coordinate specifies the vertical position of the legend. It ranges from negative infinity to positive infinity.
  • 0 corresponds to the bottom of the bounding box.
  • 0.5 corresponds to the center.
  • 1 corresponds to the top.
3)	width: Specifies the width of the legend box. Generally, it’s set to 1 to use the full width. This is typically not set unless you have specific size constraints.
4)	height: Specifies the height of the legend box. Similar to width, it’s usually set to 1. It’s not commonly adjusted unless needed.
```
#### Editing output file export:

**`--output_file_prefix`**  : a string of the name for the desired output map file. Omit file format extension.

**`--file_format`**  : a string of the format type for output figure. Default is png. Options: png, jpeg, svg, pdf 

**`--dpi`**  : a numerical value of the DPI figure resolution saved in dots per inch. Default is 300.

# Output <a name="Output"></a>

The program generates a geographical map plot, which is displayed and exported as an image in the desired format (PNG, JPEG, SVG, or PDF) with PNG as the default.

Unless otherwise specified, the output file will be saved in the working directory with the name “Output_map.png.”

# Usage and Examples <a name="Usage"></a>

#### Simple graph:
```
python Geomaps_pie4.py --shape_file /home/phe.gov.uk/emily.fotopoulou/Documents/PythonScripts/python-scripts/shapes/shaaaaaaaaapes/jam_admbnda_adm1_sdc_20240802_fixed.shp --metadata_file Jamaica_metadata_test.xlsx --llcrnrlon=-78.397064 --llcrnrlat=17.691129 --urcrnrlon=-76.164093 --urcrnrlat=18.553834 --agg_column 'Plasmids' --colours_dict "{'InCFIB':'yellow', 'InCP':'deeppink', 'InCA/C':'#00DD08', 'InCN':'darkturquoise'}"
```
![image](https://github.com/user-attachments/assets/a991f403-d2c6-464b-ad13-aea02798fe83)


#### Embelished graph:
```
python Geomaps_pie.py --shape_file /home/phe.gov.uk/emily.fotopoulou/Documents/PythonScripts/python-scripts/shapes/shaaaaaaaaapes/jam_admbnda_adm1_sdc_20240802_fixed.shp --metadata_file Jamaica_metadata_test.xlsx --agg_column 'Plasmids' --colours_dict "{'InCFIB':'yellow', 'InCP':'deeppink', 'InCA/C':'#00DD08', 'InCN':'darkturquoise'}" --llcrnrlon=-78.397064 --llcrnrlat=17.691129 --urcrnrlon=-76.164093 --urcrnrlat=18.553834 --agg_mapinfo="Population" --colormap="['#E7F3FF', 'pink']" --label_style='style1' --pie_fontsize=15 --pie_rotation=45 --pie_size=500 --pie_text_loc=0.05 --colorbar_title="Population Density" --colorbar_fontsize=20 --legend_title='Plasmids' --legend_fontsize=15 --output_file_prefix='Jamaica_map_population_and_plasmids' --file_format="pdf"
```
![figure_1](https://github.com/user-attachments/assets/d915717e-d201-4194-98e2-9bffdd9b8ef9)

# Online Tutorial <a name="Tutorial"></a>    [![General Badge](https://img.shields.io/badge/YouTube-Tutorial-%23FF0000?style=plastic&labelColor=%23282828&color=%23FF0000&link=https%3A%2F%2F)](https://www.youtube.com/watch?v=wGJHwc5ksMA)

youtube link

# Acknowledgments <a name="Acknowledgments"></a> 

I would like to extend my sincere gratitude to [_**Dr. Duncan Berger**_](https://github.com/duncanberger) for their invaluable contributions during the development of this program. Their time and effort, insightful input, assistance with bug testing, and unwavering support have been instrumental in the finalisation of this work. I deeply appreciate their collaboration and commitment throughout the development process.
