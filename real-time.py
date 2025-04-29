"""  
This is example code I got off the web on real time plotting

"""

import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import pandas as pd
import time

def read_new_data():
    """Simulates reading new data from a CSV (replace with your actual logic)"""
    try:
        # Efficiently read only the new lines if possible
        df = pd.read_csv("your_data.csv") # Replace with your file and efficient reading
        return df['timestamp'].tolist()[-10:], df['value'].tolist()[-10:] # Example: last 10 points
    except FileNotFoundError:
        return [], []

def update_plot(i, x_data, y_data, ax):
    x, y = read_new_data()
    x_data.extend(x)
    y_data.extend(y)
    ax.clear()
    ax.plot(x_data, y_data)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Value")
    ax.set_title("Real-time Data Plot")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real-time Plotting App")
        self.geometry("800x600")

        self.fig, self.ax = plt.subplots()
        self.x_data = []
        self.y_data = []

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=customtkinter.BOTH, expand=True)

        self.ani = animation.FuncAnimation(self.fig, update_plot, fargs=(self.x_data, self.y_data, self.ax), interval=1000) # Update every 1000 ms (1 second)
        self.canvas.draw()

if __name__ == "__main__":
    app = App()
    app.mainloop()