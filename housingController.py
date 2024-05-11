import housingModel as model
import housingView as view

class MelbourneHousingController:
    def __init__(self):
        self.model = model.MelbourneHousingModel()
        self.view = view.MelbourneHousingView(self)
        
        self.check_data = False
        self.summary = None

    def import_data(self):
        self.model.import_data()
        self.check_data = True
        self.view.imported()
        self.summary = self.model.get_data_summary()
        self.view.create_map()
    
    def import_melb_data(self):
        self.model.import_melbourne_data()
        self.view.imported()
        self.check_data = True
        self.summary = self.model.get_data_summary()
        self.view.create_map()
        
    def descriptive_statistics(self):
        self.view.DS_create_listbox(self.summary)
   
    def DS_selecting(self,event):
        index = self.view.column_listbox.curselection()[0]      # Get the index of the selected item
        selected_column = self.view.column_listbox.get(index)    # Get the value of the selected item
        if selected_column:                                     # Update the label text to show the selected item
            stats = self.summary[selected_column]
            self.view.clear_display_frame_right()           # Clear the existing display frame
            self.view.DS_show_static(stats)
            
    def data_visualization(self):
        self.view.DV_create_listbox()

    
    def get_data(self):
        data = self.model.get_data
        return data

    def get_numeric_columns(self):
        data = self.model.get_data_numeric_columns()
        return data
    
    def compare_houses(self):
        house_data = self.model.get_housing_data()
        self.view.CH_create_listbox(house_data)
    
    def get_houses_details(self, selected_indices):
        house1_details, house2_details = self.model.compare_houses(selected_indices)
        return house1_details, house2_details
    
    
    def create_map(self):
        self.model.create_map()
        
    
    def run(self):
        self.view.run()