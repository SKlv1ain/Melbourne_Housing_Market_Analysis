import housingController as controller
from tkinter import Tk

def main():
    root = Tk()
    app = controller.MelbourneHousingController(root)
    app.run()

if __name__ == "__main__":
    main()