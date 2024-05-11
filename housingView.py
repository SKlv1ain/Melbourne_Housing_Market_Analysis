import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import seaborn as sns

class MelbourneHousingView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller    
        self.title("Melbourne Housing Market Analysis")
        # self.geometry("800x600")
        
        self.init_frame_components()
        self.init_menu_components()

        self.histograms = {
            "Price vs Land Size": self.plot_price_vs_land_size,
            "Price vs Rooms": self.plot_price_vs_rooms,
            "Price vs Bedroom": self.plot_price_vs_bedroom,
            "Price vs Bathroom": self.plot_price_vs_bathroom,
            "Price vs Car": self.plot_price_vs_car,
            "Price vs Building Area": self.plot_price_vs_building_area,
            "House Price Distribution": self.plot_house_price_distribution,
            "Number of Bedrooms Distribution": self.plot_bedroom_distribution,
            "Number of Bathrooms Distribution": self.plot_bathroom_distribution,
            "Land Size Distribution": self.plot_land_size_distribution,
            "Number of Cars Distribution": self.plot_car_distribution,
            "Building Area Distribution": self.plot_building_area_distribution
        }
        
    def init_frame_components(self):
        
        # Create a frame for the main window
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for the menu on the left side
        self.menu_frame = ttk.LabelFrame(self.main_frame, text="Menu...")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.data_frame = ttk.LabelFrame(self.menu_frame, text="Import DATA")
        self.data_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a frame for displaying on the right side
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Display...")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a frame for displaying on the right side of the display frame
        self.display_frame_right = ttk.LabelFrame(self.display_frame, text="Showing")
        self.display_frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a frame for displaying on the left side of the display frame
        self.display_frame_left = ttk.LabelFrame(self.display_frame, text="Selecteing")
        self.display_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
    
    def init_menu_components(self):
        
        # Create a button for importing data
        self.import_button = tk.Button(self.data_frame, 
                                       text="Import Another Data", 
                                       bg="white", fg="red",
                                       command=self.controller.import_data)
        self.import_button.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a button for importing Melbourne data
        self.melb_data_button = tk.Button(self.data_frame, 
                                          text="Melbourne Data", 
                                          bg="white", fg="blue",
                                          command=self.controller.import_melb_data)
        self.melb_data_button.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create a button for Feature Descriptive Statistics
        self.stats_button = tk.Button(self.menu_frame, 
                                      text="Descriptive Statistics",
                                      command=self.controller.descriptive_statistics)
        self.stats_button.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create a button for Data Visualization
        self.visualization_button = tk.Button(self.menu_frame, 
                                              text="Data Visualization",
                                              command=self.controller.data_visualization)
        self.visualization_button.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create a button for Feature Comparison
        self.compare_button = tk.Button(self.menu_frame, text="Compare Houses",
                                        command=self.controller.compare_houses)
        self.compare_button.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.quit_button = ttk.Button(self.menu_frame, text="Quit",
                                      command=self.quit)
        self.quit_button.pack(fill=tk.BOTH, expand=True, pady=10,)


    def clear_all_display_frame(self):
        for widget in self.display_frame_left.winfo_children():
            widget.destroy()
        for widget in self.display_frame_right.winfo_children():
            widget.destroy()    
            
    def clear_display_frame_right(self):
        for widget in self.display_frame_right.winfo_children():
            widget.destroy()
            
    def clear_display_frame_left(self):
        for widget in self.display_frame_left.winfo_children():
            widget.destroy()

    def imported(self):
        messagebox.showinfo("Data Imported", "Data has been imported successfully.")
        label = tk.Label(self.menu_frame, text="Data imported", 
                                                fg="green", bg="white")
        label.pack(pady=10)
        
    def DS_create_listbox(self, data):
        if data is not None:
            self.clear_all_display_frame()
            self.column_listbox = tk.Listbox(self.display_frame_left)
            self.column_listbox.pack(fill=tk.BOTH, expand=True)
            for column_name in data.columns:
                self.column_listbox.insert(tk.END, column_name)

            self.column_listbox.bind("<<ListboxSelect>>", self.controller.DS_selecting)
        else:
            messagebox.showerror("Error", "Please import data first.")
            
    def DS_show_static(self, stats):
        row_index = 0
        for stat_name, stat_value in stats.items():
            label = tk.Label(self.display_frame_right, 
                                text=f"{stat_name}: {stat_value}")
            label.grid(row=row_index, column=1, padx=5, pady=5)
            row_index += 1
    
    def DV_create_listbox(self):
        # Clear the display frame
        self.clear_all_display_frame()
            
        # Create listbox for selecting histogram
        self.histogram_listbox = tk.Listbox(self.display_frame_left)
        self.histogram_listbox.pack(fill=tk.BOTH, expand=True)

        
        # Insert histogram names into the listbox
        for histogram_name in self.histograms.keys():
            self.histogram_listbox.insert(tk.END, histogram_name)
            
        # Bind selection event to display selected histogram
        self.histogram_listbox.bind("<<ListboxSelect>>", self.display_selected_histogram)
        

    def display_selected_histogram(self, event):
        selected_index = self.histogram_listbox.curselection()[0]
        selected_histogram = self.histogram_listbox.get(selected_index)
        self.histograms[selected_histogram]()
    
    # Define the plot functions for each histogram
    
    def plot_price_vs_land_size(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['Landsize'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Land Size')
        ax.set_xlabel('Land Size')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
        
    def plot_price_vs_rooms(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['Rooms'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Rooms')
        ax.set_xlabel('Rooms')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
    
    def plot_price_vs_bedroom(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['Bedroom2'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Bedroom')
        ax.set_xlabel('Bedroom')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
    
    def plot_price_vs_bathroom(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['Bathroom'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Bathroom')
        ax.set_xlabel('Bathroom')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
    
    def plot_price_vs_car(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['Car'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Car')
        ax.set_xlabel('Car')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
    
    def plot_price_vs_building_area(self):
        self.clear_display_frame_right()
        data = self.controller.get_data()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(data['BuildingArea'], data['Price'], alpha=0.5)
        ax.set_title('Price vs Building Area')
        ax.set_xlabel('Building Area')
        ax.set_ylabel('Price')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
    
    

    def plot_house_price_distribution(self):
        
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['Price'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('House Price Distribution')
        ax.set_xlabel('Price')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
        

    def plot_bedroom_distribution(self):
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['Bedroom2'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Number of Bedrooms Distribution')
        ax.set_xlabel('Number of Bedrooms')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)

    def plot_bathroom_distribution(self):
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['Bathroom'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Number of Bathrooms Distribution')
        ax.set_xlabel('Number of Bathrooms')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)

    def plot_land_size_distribution(self):
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['Landsize'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Land Size Distribution')
        ax.set_xlabel('Land Size')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
        
        

    def plot_car_distribution(self):
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['Car'], bins=20, color='skyblue', edgecolor='black')
        ax.set_title('Number of Cars Distribution')
        ax.set_xlabel('Number of Cars')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
        

    def plot_building_area_distribution(self):
        self.clear_display_frame_right()
        fig, ax = plt.subplots(figsize=(6, 4))
        data = self.controller.get_data()
        ax.hist(data['BuildingArea'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Building Area Distribution')
        plt.xlabel('Building Area')
        ax.set_ylabel('Frequency')
        canvas = FigureCanvasTkAgg(fig, master=self.display_frame_right)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True)
            
    def CH_create_listbox(self, data):
        if self.controller.check_data:
            self.clear_all_display_frame()

            self.house_listbox = tk.Listbox(self.display_frame_left, selectmode=tk.MULTIPLE)
            self.house_listbox.pack(fill=tk.BOTH, expand=True)
            self.house_listbox.delete(0, tk.END)
            
            for address in data:
                self.house_listbox.insert(tk.END, address)
            
            self.button = tk.Button(self.display_frame_right, text="Compare Houses")
            self.button.grid(row=0, column=0, padx=5, pady=5)

            self.button.bind("<Button-1>", self.compare_houses_event)
        else:
            messagebox.showerror("Error", "Please import data first.")
             
    def compare_houses_event(self, event):
        selected_indices = self.house_listbox.curselection()
        if len(selected_indices) != 2:
            messagebox.showerror("Error", "Please select exactly two houses for comparison.")
        else:
            house1_details, house2_details = self.controller.get_houses_details(selected_indices)
            
            if house1_details is not None and house2_details is not None:
                comparison_window = tk.Toplevel(master=self.display_frame_right)
                comparison_window.title("Comparison Result")
                
                for i, (attr, value1, value2) in enumerate(zip(house1_details.index
                                    , house1_details.values, house2_details.values)):
                    label = tk.Label(comparison_window, text=attr)
                    label.grid(row=i, column=0, padx=5, pady=5)
                    
                    value1_label = tk.Label(comparison_window, text=value1)
                    value1_label.grid(row=i, column=1, padx=5, pady=5)
                    value2_label = tk.Label(comparison_window, text=value2)
                    value2_label.grid(row=i, column=2, padx=5, pady=5)   
                    if attr in ['Rooms', 'Bedroom2', 'Bathroom', 'Car', 'Landsize', 'BuildingArea',
                                'YearBuilt']:
                        if value1 > value2:
                            value1_label.config(fg="green")
                            value2_label.config(fg="red")
                        elif value1 < value2:
                            value1_label.config(fg="red")
                            value2_label.config(fg="green")
                        elif value1 == value2:
                            value1_label.config(fg="yellow")
                            value2_label.config(fg="yellow")
                    elif attr == 'Price':
                        if value1 > value2:
                            value1_label.config(fg="red")
                            value2_label.config(fg="green")
                        elif value1 < value2:
                            value1_label.config(fg="green")
                            value2_label.config(fg="red")
                        elif value1 == value2:
                            value1_label.config(fg="yellow")
                            value2_label.config(fg="yellow")
                        
                            
    def create_map(self):
        self.clear_all_display_frame()
        self.controller.create_map()

        
    def run(self):
        self.mainloop()