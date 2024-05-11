import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
from tkinter import filedialog

class MelbourneHousingModel:
    def __init__(self):
        self.origin_df = None
        self.model = None
        self.data = None
        
        self.numerical_df = None
        
    @property
    def get_data(self):
        return self.data    

    def import_data(self):
        """ This method will import the data from the file path """
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.origin_df = pd.read_csv(file_path)    
        self.data = self.origin_df.copy() 
        self.handle_missing_values()
    
    def import_melbourne_data(self):
        """ This method will import the melbourne housing data """
        
        self.origin_df = pd.read_csv('Data/melb_data.csv')
        self.data = self.origin_df.copy()
        self.handle_missing_values()
        
    def handle_missing_values(self):
        """ This method will handle missing values in the data """
        
        if self.data is not None:
            self.data.dropna(inplace=True)
        else:
            return None
    
    def get_shape(self):
        """ This method will return the shape of the data"""
        
        if self.data is not None:
            return self.data.shape
        else:
            return None

    def get_data_summary(self):
        if self.data is not None:
            return self.data.describe()
        else:
            return None
    
    def get_data_columns(self):
        if self.data is not None:
            return self.data.columns.tolist()
        else:
            return []
    
    
    def get_data_numeric_columns(self):
        if self.data is not None:
            self.numerical_df = self.data.select_dtypes(include=[np.number])
        else:
            return None 
        
    def Cal_correlation(self):
        if self.numerical_df is not None:
            return self.numerical_df.corr()
        else:
            return None
    
    def get_housing_data(self):
        if self.data is not None:
            return self.data['Address'].tolist()
        else:
            return []

    def compare_houses(self, house_indices):
        if len(house_indices) != 2:
            return None
        else:
            house1_index, house2_index = house_indices
            house1_details = self.data.iloc[house1_index]
            house2_details = self.data.iloc[house2_index]
            return house1_details, house2_details
    
    
    def get_house_details(self, house_index):
        if self.data is not None:
            return self.data.iloc[house_index]
        else:
            return None
        
    def create_histogram(self, column_name):
        if self.data is not None:
            return self.data[column_name].plot.hist()
        else:
            return None
        
    def create_scatter_plot(self, x_column, y_column):
        if self.data is not None:
            return self.data.plot.scatter(x=x_column, y=y_column)
        else:
            return None
        
    def create_box_plot(self, column_name):
        if self.data is not None:
            return self.data.boxplot(column=column_name)
        else:
            return None

    def get_numerical_columns(self):
        if self.data is not None:
            return self.data.select_dtypes(include=[np.number]).columns.tolist()
        else:
            return []

    def create_map(self):
        # Create a GeoDataFrame from the housing data
        geometry = [Point(xy) for xy in zip(self.data['Longtitude'], self.data['Lattitude'])]
        gdf = gpd.GeoDataFrame(self.data, geometry=geometry)

        # Create a base map of Australia
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        australia = world[world.name == 'Australia']
    

        # Plot the base map
        base = australia.plot(figsize=(10, 6), color='lightblue', edgecolor='black', legend=True, alpha=0.5, linewidth=0.5, zorder=1, legend_kwds={'loc': 'upper left'}, label='Australia')
        
        # Plot the housing data
        gdf.plot(ax=base, color='red', marker='o', markersize=5, legend=True)

        # Set plot title and labels
        plt.title('Map of Australia with Housing Data', fontsize=16)
        plt.xlabel('Longitude', fontsize=14)
        plt.ylabel('Latitude', fontsize=14)

        # Display the map
        # plt.axis('off')
        plt.show()

    
    

 