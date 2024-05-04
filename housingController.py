import tkinter as tk
import tkinter as tkinter
from tkinter import filedialog, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

import housingModel as model
import housingView as view


class MelbourneHousingController:
    def __init__(self, master):
        self.master = master
        self.model = model.MelbourneHousingModel()
        self.view = view.MelbourneHousingView(master)
        
        self.view.import_button.config(command=self.import_data)
        self.view.stats_button.config(command=self.show_statistics)
        self.view.visualization_button.config(command=self.show_visualization)
        self.view.predict_button.config(command=self.predict_prices)
        self.view.compare_button.config(command=self.compare_houses_button)
        self.view.quit_button.config(command=quit)
        
        self.histograms = {
            "Price vs Land Size": self.plot_price_vs_land_size,
            "House Price Distribution": self.plot_house_price_distribution,
            "Number of Bedrooms Distribution": self.plot_bedroom_distribution,
            "Number of Bathrooms Distribution": self.plot_bathroom_distribution,
            "Land Size Distribution": self.plot_land_size_distribution,
            "Number of Cars Distribution": self.plot_car_distribution,
            "Building Area Distribution": self.plot_building_area_distribution
        }

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.model.import_data(file_path)
            messagebox.showinfo("Success", "Data imported successfully!")
            label = tk.Label(self.view.menu_frame, text="Data imported", fg="green", bg="white")
            label.pack(pady=10)
            # self.view.set_house_data(self.model.get_housing_data())
            
    def show_statistics(self):
        summary = self.model.get_data_summary()
        if summary is not None:
            # Clear the display frame
            # self.clear_display_frame()
            for widget in self.view.display_frame_left.winfo_children():
                widget.destroy()  
                
            for widget in self.view.display_frame_right.winfo_children():
                widget.destroy()    

            # Create the listbox for column names
            self.column_listbox = tk.Listbox(self.view.display_frame_left)
            self.column_listbox.pack(fill=tk.BOTH, expand=True)
            for column_name in summary.columns:
                self.column_listbox.insert(tk.END, column_name)

            # Bind the selection event to show statistics
            self.column_listbox.bind("<<ListboxSelect>>", self.on_select)
   
    def on_select(self,event):
        
        # Get the index of the selected item
        index = self.column_listbox.curselection()[0]
        # Get the value of the selected item
        selected_column = self.column_listbox.get(index)
        # Update the label text to show the selected item
        if selected_column:
            summary = self.model.get_data_summary()
            stats = summary[selected_column]
            # Clear the existing display frame
            # self.clear_display_frame()
            
            for widget in self.view.display_frame_right.winfo_children():
                widget.destroy()
            
            # Display the statistics
            row_index = 0
            for stat_name, stat_value in stats.items():
                label = tk.Label(self.view.display_frame_right, text=f"{stat_name}: {stat_value}")
                label.grid(row=row_index, column=1, padx=5, pady=5)
                row_index += 1
    
    def show_visualization(self):
        # Clear the display frame
        for widget in self.view.display_frame_left.winfo_children():
            widget.destroy()
            
        # Create listbox for selecting histogram
        self.histogram_listbox = tk.Listbox(self.view.display_frame_left)
        self.histogram_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Clear the display frame
        for widget in self.view.display_frame_right.winfo_children():
            widget.destroy()
        # Create a Label massage
        label = tk.Label(self.view.display_frame_right, text="The graph shows up in a new window.", 
                         fg="white", bg="gray")
        label.pack(fill=tk.BOTH, expand=True)
        
        # Insert histogram names into the listbox
        for histogram_name in self.histograms.keys():
            self.histogram_listbox.insert(tk.END, histogram_name)
            
        # Bind selection event to display selected histogram
        self.histogram_listbox.bind("<<ListboxSelect>>", self.display_selected_histogram)
        

    def display_selected_histogram(self, event):
        selected_index = self.histogram_listbox.curselection()[0]
        selected_histogram = self.histogram_listbox.get(selected_index)
        # Clear the display frame
        # for widget in self.view.display_frame_right.winfo_children():
        #     widget.destroy()
        # Plot the selected histogram
        self.histograms[selected_histogram]()
    
    # Define the plot functions for each histogram
    def plot_price_vs_land_size(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.model.data['Landsize'], self.model.data['Price'], alpha=0.5)
        plt.title('Price vs Land Size')
        plt.xlabel('Land Size')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()

    def plot_house_price_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['Price'], bins=20, color='skyblue', edgecolor='black')
        plt.title('House Price Distribution')
        plt.xlabel('Price')
        plt.ylabel('Frequency')
        plt.show()

    def plot_bedroom_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['Bedroom2'], bins=10, color='salmon', edgecolor='black')
        plt.title('Number of Bedrooms Distribution')
        plt.xlabel('Number of Bedrooms')
        plt.ylabel('Frequency')
        plt.show()

    def plot_bathroom_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['Bathroom'], bins=5, color='lightgreen', edgecolor='black')
        plt.title('Number of Bathrooms Distribution')
        plt.xlabel('Number of Bathrooms')
        plt.ylabel('Frequency')
        plt.show()

    def plot_land_size_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['Landsize'], bins=20, color='orange', edgecolor='black')
        plt.title('Land Size Distribution')
        plt.xlabel('Land Size')
        plt.ylabel('Frequency')
        plt.show()

    def plot_car_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['Car'], bins=5, color='lightpink', edgecolor='black')
        plt.title('Number of Cars Distribution')
        plt.xlabel('Number of Cars')
        plt.ylabel('Frequency')
        plt.show()

    def plot_building_area_distribution(self):
        plt.figure(figsize=(8, 6))
        plt.hist(self.model.data['BuildingArea'], bins=20, color='lightblue', edgecolor='black')
        plt.title('Building Area Distribution')
        plt.xlabel('Building Area')
        plt.ylabel('Frequency')
        plt.show()
    
    def predict_prices(self):
        
        for widget in self.view.display_frame_left.winfo_children():
                widget.destroy()  
                
        for widget in self.view.display_frame_right.winfo_children():
                widget.destroy()   
        messagebox.showerror("Error", "This feature is not implemented yet.")
        label = tk.Label(self.view.display_frame_left, 
                         text="This feature is not implemented yet.", 
                         fg="white", bg="gray")
        label.pack(fill=tk.BOTH, expand=True)
        label2 = tk.Label(self.view.display_frame_right, 
                         text="This feature is not implemented yet.", 
                         fg="white", bg="gray")
        label2.pack(fill=tk.BOTH, expand=True)
    
    def compare_houses_button(self):
        
        # Clear the display frame
        for widget in self.view.display_frame_left.winfo_children():
                widget.destroy()  
        for widget in self.view.display_frame_right.winfo_children():
                widget.destroy()  
        
        # # Remove the display frame right
        # self.view.display_frame_right.pack_forget()
        
        # Create a listbox for selecting houses
        self.house_listbox = tk.Listbox(self.view.display_frame_left
                                        , selectmode=tk.MULTIPLE)
        self.house_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Create a listbox for selecting houses
        label = tk.Label(self.view.display_frame_right, 
                         text="The Comparison Result shows up in a new window.", 
                         fg="white", bg="gray")
        label.pack(fill=tk.BOTH, expand=True)

        # Get the housing data for listbox
        data = self.model.get_housing_data()
        self.house_listbox.delete(0, tk.END)
        for address in data:
            self.house_listbox.insert(tk.END, address)
        
        # Create a button to compare houses
        self.button = tk.Button(self.view.display_frame_left, text="Compare Houses")
        self.button.pack(pady=10)

        self.button.bind("<Button-1>", self.compare_houses_event)
        
    def compare_houses_event(self, event):
        selected_indices = self.house_listbox.curselection()
        if len(selected_indices) != 2:
            messagebox.showerror("Error", "Please select exactly two houses for comparison.")
        else:
            house1_details, house2_details = self.model.compare_houses(selected_indices)
            if house1_details is not None and house2_details is not None:
                comparison_window = tk.Toplevel(self.view.display_frame_right)
                comparison_window.title("Comparison Result")
                
                for i, (attr, value1, value2) in enumerate(zip(house1_details.index
                                    , house1_details.values, house2_details.values)):
                    label = tk.Label(comparison_window, text=attr)
                    label.grid(row=i, column=0, padx=5, pady=5)
                    value1_label = tk.Label(comparison_window, text=value1)
                    value1_label.grid(row=i, column=1, padx=5, pady=5)
                    value2_label = tk.Label(comparison_window, text=value2)
                    value2_label.grid(row=i, column=2, padx=5, pady=5)          
                    
    def run(self):
        self.master.mainloop()
