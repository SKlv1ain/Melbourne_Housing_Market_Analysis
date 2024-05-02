import housingView as view
import housingModel as model
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx

class MelbourneHousingController:
    def __init__(self, master):
        self.master = master
        self.model = model.MelbourneHousingModel()
        self.view = view.MelbourneHousingView(master)
        
        self.view.import_button.config(command=self.import_data)
        self.view.stats_button.config(command=self.show_statistics)
        self.view.visualization_button.config(command=self.show_visualization)
        self.view.predict_button.config(command=self.predict_prices)
        self.view.compare_button.config(command=self.compare_houses)
        self.view.quit_button.config(command=quit)

    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.model.import_data(file_path)
            messagebox.showinfo("Success", "Data imported successfully!")
            label = tk.Label(self.view.menu_frame, text="Data imported", fg="green", bg="white")
            label.pack(pady=10)
            self.view.set_house_data(self.model.get_housing_data())

    def show_statistics(self):
        # data_summary = self.model.get_data_summary()
        # if data_summary is not None:
        #     statistics_window = tk.Toplevel(self.master)
        #     statistics_window.title("Descriptive Statistics")
        #     text = tk.Text(statistics_window)
        #     text.insert(tk.END, data_summary)
        #     text.pack()
        
        summary = self.model.get_data_summary()
        if summary is not None:
            # listbox = tk.Listbox(self.view.display_frame)
            # for column_name, stats in summary.items():
            #     listbox.insert(tk.END, column_name)
            # listbox.grid(row=0, column=0)
            # listbox.delete(0, tk.END)
            # for column, stat in summary.items():
            #     listbox.insert(tk.END, column)
                
            # statistics_window = tk.Toplevel(self.master)
            # statistics_window.title("Descriptive Statistics")
            
            row_index = 0
            for column_name, stats in summary.items():
                label = tk.Label(self.view.display_frame, text=column_name)
                label.grid(row=row_index, column=0, padx=5, pady=5)
                
                stats_text = "\n".join([f"{stat}: {value}" for stat, value in stats.items()])
                stats_label = tk.Label(self.view.display_frame, text=stats_text)
                stats_label.grid(row=row_index, column=1, padx=5, pady=5)
                
                row_index += 1


    def show_visualization(self):
        # self.plot_network_graph()
        self.plot_price_vs_land_size()
        self.plot_histograms()

    def plot_network_graph(self):
        """Show a network graph of the Melbourne housing data"""
        g = nx.Graph()
        for i, row in self.model.data.iterrows():
            g.add_node(i, attr_dict=row.to_dict())
        for i in g.nodes():
            for j in g.nodes():
                if i != j:
                    g.add_edge(i, j)
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(g)
        nx.draw(g, pos, with_labels=False, node_size=30, node_color='skyblue', edge_color='gray')
        plt.title('Melbourne Housing Data Network Graph')
        plt.show()

    def plot_price_vs_land_size(self):
        plt.figure(figsize=(8, 6))
        plt.scatter(self.model.data['Landsize'], self.model.data['Price'], alpha=0.5)
        plt.title('Price vs Land Size')
        plt.xlabel('Land Size')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()

    def plot_histograms(self):
        plt.figure(figsize=(10, 8))
        plt.subplot(3, 2, 1)
        plt.hist(self.model.data['Price'], bins=20, color='skyblue', edgecolor='black')
        plt.title('House Price Distribution')
        plt.xlabel('Price')
        plt.ylabel('Frequency')

        plt.subplot(3, 2, 2)
        plt.hist(self.model.data['Bedroom2'], bins=10, color='salmon', edgecolor='black')
        plt.title('Number of Bedrooms Distribution')
        plt.xlabel('Number of Bedrooms')
        plt.ylabel('Frequency')

        plt.subplot(3, 2, 3)
        plt.hist(self.model.data['Bathroom'], bins=5, color='lightgreen', edgecolor='black')
        plt.title('Number of Bathrooms Distribution')
        plt.xlabel('Number of Bathrooms')
        plt.ylabel('Frequency')

        plt.subplot(3, 2, 4)
        plt.hist(self.model.data['Landsize'], bins=20, color='orange', edgecolor='black')
        plt.title('Land Size Distribution')
        plt.xlabel('Land Size')
        plt.ylabel('Frequency')

        plt.subplot(3, 2, 5)
        plt.hist(self.model.data['Car'], bins=5, color='lightpink', edgecolor='black')
        plt.title('Number of Cars Distribution')
        plt.xlabel('Number of Cars')
        plt.ylabel('Frequency')

        plt.subplot(3, 2, 6)
        plt.hist(self.model.data['BuildingArea'], bins=20, color='lightblue', edgecolor='black')
        plt.title('Building Area Distribution')
        plt.xlabel('Building Area')
        plt.ylabel('Frequency')

        plt.tight_layout()
        plt.show()

    def predict_prices(self):
        pass  # Add code for price prediction

    def compare_houses(self):
        selected_indices = self.view.house_listbox.curselection()
        if len(selected_indices) != 2:
            messagebox.showerror("Error", "Please select exactly two houses for comparison.")
        else:
            house1_details, house2_details = self.model.compare_houses(selected_indices)
            if house1_details is not None and house2_details is not None:
                comparison_window = tk.Toplevel(self.master)
                comparison_window.title("Comparison Result")
                for i, (attr, value1, value2) in enumerate(zip(house1_details.index, house1_details.values, house2_details.values)):
                    label = tk.Label(comparison_window, text=attr)
                    label.grid(row=i, column=0, padx=5, pady=5)
                    value1_label = tk.Label(comparison_window, text=value1)
                    value1_label.grid(row=i, column=1, padx=5, pady=5)
                    value2_label = tk.Label(comparison_window, text=value2)
                    value2_label.grid(row=i, column=2, padx=5, pady=5)

def main():
    root = tk.Tk()
    app = MelbourneHousingController(root)
    root.mainloop()

if __name__ == "__main__":
    main()