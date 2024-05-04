import pandas as pd

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