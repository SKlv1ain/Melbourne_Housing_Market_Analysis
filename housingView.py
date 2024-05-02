import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class MelbourneHousingView:
    def __init__(self, master):
        self.master = master
        self.master.title("Melbourne Housing Market Analysis")
        self.master.geometry("750x400")
        
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
         # Create a frame for the menu on the left side
        self.menu_frame = ttk.LabelFrame(self.main_frame, text="Menu...")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create a frame for displaying on the right side
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Display...")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.init_menu_components()
        self.init_display_components()
    
    def init_menu_components(self):
        self.import_button = tk.Button(self.menu_frame, text="Import Data")
        self.import_button.pack(pady=10)

        self.stats_button = tk.Button(self.menu_frame, text="Descriptive Statistics")
        self.stats_button.pack(pady=10)

        self.visualization_button = tk.Button(self.menu_frame, text="Data Visualization")
        self.visualization_button.pack(pady=10)

        self.predict_button = tk.Button(self.menu_frame, text="Price Prediction")
        self.predict_button.pack(pady=10)
        

        self.compare_button = tk.Button(self.menu_frame, text="Compare Houses")
        self.compare_button.pack(pady=10)


        self.quit_button = ttk.Button(self.menu_frame, text="Quit")
        self.quit_button.pack(pady=10)

        self.compare_button.bind("<Button-1>", self.compare_houses_event)
        
    def init_display_components(self):
        self.house_listbox = tk.Listbox(self.menu_frame, selectmode=tk.MULTIPLE)
        self.house_listbox.pack(pady=10)
        
    # def create_descriptive_listbox(self, data):
    #     self.descriptive_listbox = tk.Listbox(self.display_frame)
    #     self.descriptive_listbox.grid(row=0, column=0)
        
    #     for column_name, stat in data.items():
    #         self.descriptive_listbox.insert(tk.END, column_name)
            
    #     self.descriptive_listbox.bind("<<ListboxSelect>>", self.on_select)
        
    
    def set_house_data(self, data):
        self.house_listbox.delete(0, tk.END)
        for address in data:
            self.house_listbox.insert(tk.END, address)


    def compare_houses_event(self, event):
        selected_indices = self.house_listbox.curselection()
        if len(selected_indices) != 2:
            messagebox.showerror("Error", "Please select exactly two houses for comparison.")
        else:
            self.controller.compare_houses(selected_indices)
