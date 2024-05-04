import pandas as pd
# from sklearn.linear_model import LinearRegression

class MelbourneHousingModel:
    def __init__(self):
        self.data = None
        self.model = None

    def import_data(self, file_path):
        self.data = pd.read_csv(file_path)

    def get_data_summary(self):
        if self.data is not None:
            return self.data.describe()
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
        
    # def create_price_prediction_model(self):
    #     if self.data is not None:
    #         self.model = LinearRegression()
    #         self.model.fit(self.data[['Rooms', 'Bathroom', 
    #                                   'Landsize', 'BuildingArea', 
    #                                   'YearBuilt']], self.data['Price'])
    #     else:
    #         return None
    
    #