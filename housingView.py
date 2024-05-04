import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class MelbourneHousingView:
    def __init__(self, master):
        self.master = master
        self.master.title("Melbourne Housing Market Analysis")
        self.master.geometry("1000x600")
        
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
         # Create a frame for the menu on the left side
        self.menu_frame = ttk.LabelFrame(self.main_frame, text="Menu...")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create a frame for displaying on the right side
        self.display_frame = ttk.LabelFrame(self.main_frame, text="Display...")
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a frame for displaying on the right side of the display frame
        self.display_frame_right = ttk.LabelFrame(self.display_frame, text="Showing")
        self.display_frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create a frame for displaying on the left side of the display frame
        self.display_frame_left = ttk.LabelFrame(self.display_frame, text="Selecteing")
        self.display_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.init_menu_components()
        self.init_display_components()
    
    def init_menu_components(self):
        self.import_button = tk.Button(self.menu_frame, text="Import Data")
        self.import_button.pack(fill=tk.BOTH, expand=True, pady=10)

        self.stats_button = tk.Button(self.menu_frame, text="Descriptive Statistics")
        self.stats_button.pack(fill=tk.BOTH, expand=True, pady=10)

        self.visualization_button = tk.Button(self.menu_frame, text="Data Visualization")
        self.visualization_button.pack(fill=tk.BOTH, expand=True, pady=10)

        self.predict_button = tk.Button(self.menu_frame, text="Price Prediction")
        self.predict_button.pack(fill=tk.BOTH, expand=True, pady=10)
        

        self.compare_button = tk.Button(self.menu_frame, text="Compare Houses")
        self.compare_button.pack(fill=tk.BOTH, expand=True, pady=10)


        self.quit_button = ttk.Button(self.menu_frame, text="Quit")
        self.quit_button.pack(fill=tk.BOTH, expand=True, pady=10)

        self.compare_button.bind("<Button-1>", self.compare_houses_event)
        
    def init_display_components(self):
        self.house_listbox = tk.Listbox(self.menu_frame, selectmode=tk.MULTIPLE)
        self.house_listbox.pack(pady=10)
        
    
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