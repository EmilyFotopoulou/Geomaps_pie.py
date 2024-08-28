#!/usr/bin/env python

# Creates a geographic map with pie charts for given data.

__version__ = '0.1'
__date__ = '19-08-2024'
__author__ = 'E.F.Fotopoulou'

###### Imports
import argparse
import geopandas as gpd
from pyproj import CRS


def parse_args():
    description = "Fix shape file to contain column RGN21NM which will be shared in metadata file"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--shape_file', required=True, help="Path to shape file")
    parser.add_argument('--column', required=False, help="Column name to replace with 'RGN21NM'")
    return parser.parse_args()

def main():
    args = parse_args()
    fix_shape(args.shape_file, args.column)

# Function to test if the shape file is in correct format
def fix_shape(shapefile_path, column=None):
    gdf = gpd.read_file(shapefile_path)

    # The Geomaps_pie.py script runs with the requirement of a column named 'RGN21NM' which carries the names of the the regions to be ploted.
    if "RGN21NM" in gdf.columns:
        print("The 'RGN21NM' column already exists. No changes made.")
    else:
        if column is None:
            # If no column is provided, just print the top 5 rows of the shapefile
            print("The 'RGN21NM' column is missing. Here are the top 5 lines of the shapefile:")
            print(gdf.head())
        else:
            # Replace the specified column with 'RGN21NM'
            if column in gdf.columns:
                gdf = gdf.rename(columns={column: "RGN21NM"})

                # Reproject to geographic coordinates
                gdf = gdf.to_crs(CRS.from_epsg(4326))

                # Save the reprojected shapefile
                output_path = shapefile_path.replace(".shp", "_fixed.shp")
                gdf.to_file(output_path)

                print(f"Column '{column}' replaced with 'RGN21NM' and saved to {output_path}")
            else:
                print(f"Error: Column '{column}' does not exist in the shapefile.")

if __name__ == "__main__":
    main()
