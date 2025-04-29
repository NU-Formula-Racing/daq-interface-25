import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class CustomToolbar(NavigationToolbar2Tk):#just to redraw the zoom box
    def __init__(self, canvas, window):
        super().__init__(canvas, window)
    
    def zoom(self, *args):
        super().zoom(*args)
        if hasattr(self, '_zoom_rect') and self._zoom_rect is not None:
            self._zoom_rect.set_edgecolor('black')
            # Force a redraw so the change is visible
            self.canvas.draw_idle()

NU_PURPLE_HEX = "#4E2A84"
PURPLE_60_HEX = "#836EAA"
PURPLE_160_HEX = "#1d0235"
NU_SILVER_HEX = "#C0C0C0"

class MultiFrameApp(ctk.CTk):
    def __init__(self, dataframe) -> None:
        ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("Multi-Frame System")
        self.geometry("900x700")


        # current active layout
        self.current_layout = None
        self.current_layout_state = None
        self.current_graph_state = None
        self.current_data_state = None

        #dictionaries to maintain state
        self.data_dict = {}
        self.graph_dict = {}

        #our data
        self.df = dataframe


        self.create_layout()

    def create_layout(self):
        # main container
        main_container = ctk.CTkFrame(self)#holds the grpah part and sidebar
        main_container.pack(fill="both", expand=True)#Packs that frame into the window so it expands in both directions and fills the available space.

        # side option bar
        #Creates a frame that will be a sidebar, nested within main_container.
        self.side_bar = ctk.CTkScrollableFrame(main_container, width=150, corner_radius=0)
        self.side_bar.pack(side="left", fill="y")
        #Positions the sidebar to the left side of main_container and makes it fill vertically (fill="y"

        # main content
        self.main_content = ctk.CTkFrame(main_container)
        self.main_content.pack(side="right", fill="both", expand=True)
        #Positions this frame to the right of the sidebar and makes it fill the remaining space both horizontally and vertically.

        # layout frame
        self.layout_frame = ctk.CTkFrame(self.side_bar, width=100)
        self.layout_frame.pack(side='top', pady=(0,10))
        self.master_layout_button = ctk.CTkButton(self.layout_frame, text="Layout", command=self.layout_show, fg_color=NU_PURPLE_HEX, bg_color=PURPLE_160_HEX, hover_color=PURPLE_160_HEX, text_color="white")
        self.master_layout_button.pack(pady=10, padx=10, fill="x")
        #Packs it at the top of the sidebar, with some vertical padding at the bottom (pady=(0, 10)).

        #graph choices frame
        self.graph_frame = ctk.CTkFrame(self.side_bar, width=100)
        self.graph_frame.pack(side='top', pady=(0,10))
        self.master_graph_button = ctk.CTkButton(self.graph_frame, text="Graphs", command=self.graph_show, fg_color=NU_PURPLE_HEX, bg_color=PURPLE_160_HEX, hover_color=PURPLE_160_HEX, text_color="white")
        self.master_graph_button.pack(pady=10, padx=10, fill="x")
        # Places it at the top (under the layout frame, since they are stacked) of self.side_bar.

        #data frame for choosing the columns to plot
        self.data_frame = ctk.CTkFrame(self.side_bar, width=100)
        self.data_frame.pack(side='top',pady=(0,10))
        self.master_data_button = ctk.CTkButton(self.data_frame, text="Data", command=self.data_show, fg_color=NU_PURPLE_HEX, bg_color=PURPLE_160_HEX, hover_color=PURPLE_160_HEX, text_color="white")
        self.master_data_button.pack(pady=10, padx=10, fill="x")

        #plot buttons frame
        self.plot_buttons_frame = ctk.CTkFrame(self.side_bar, width=100)
        self.plot_buttons_frame.pack(side='top', pady=(0,10))

        #reset button
        self.reset_frame = ctk.CTkFrame(self.side_bar, width=100)
        self.reset_frame.pack(side='top')
        self.master_reset_button = ctk.CTkButton(self.reset_frame, text="Reset", command=self.reset, fg_color=NU_PURPLE_HEX, bg_color=PURPLE_160_HEX, hover_color=PURPLE_160_HEX, text_color="white")
        self.master_reset_button.pack(pady=10, padx=10, fill="x")

        #dict to store the values chosen
        self.plotting_parameters = {}
        self.plotting_parameters["columns"] = []

        #graph state
        self.bar_graph_state = None
        self.show_four_frames()#init wiht 4 frames

    def layout_show(self):#display layout buttons
            if self.current_layout_state == "layout choices displayed":
                self.clear_layout_buttons()
                return#This makes the button behave like a toggle. If you click it again while the layouts are displayed, it will remove them.
            self.current_layout_state = "layout choices displayed"
    
            ctk.CTkButton(self.layout_frame, text="1-Frame Layout", fg_color= "white", bg_color=NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.show_one_frame).pack(pady=10, padx=10, fill="x")
            ctk.CTkButton(self.layout_frame, text="2-Frame Layout", fg_color= "white", bg_color=NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.show_two_frames).pack(pady=10, padx=10, fill="x")
            ctk.CTkButton(self.layout_frame, text="3-Frame Layout", fg_color= "white", bg_color=NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.show_three_frames).pack(pady=10, padx=10, fill="x")
            ctk.CTkButton(self.layout_frame, text="4-Frame Layout", fg_color= "white", bg_color=NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.show_four_frames).pack(pady=10, padx=10, fill="x")
           

    def clear_layout_buttons(self):#clears all buttons except the master
        for widget in self.layout_frame.winfo_children():
            if widget != self.master_layout_button:
                widget.destroy()
        self.current_layout_state = None

    def clear_graph_buttons(self):
        for widget in self.graph_frame.winfo_children():
            if widget != self.master_graph_button:
                widget.destroy()
        self.current_graph_state = None

    def clear_data_buttons(self):
        for widget in self.data_frame.winfo_children():
            if widget != self.master_data_button:
                widget.destroy()
        self.current_data_state = None 

    def clear_plot_buttons(self):
        for widget in self.plot_buttons_frame.winfo_children():
            widget.destroy()
        # self.current_data_state = None 



        
    def graph_show(self):#display graph buttons
        if self.current_graph_state == "graph choices displayed":
                self.clear_graph_buttons()
                return
        self.current_graph_state = "graph choices displayed"
        # ctk.CTkButton(self.graph_frame, text="Line Graph", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.display_graph).pack(pady=10, padx=10, fill="x")
        # ctk.CTkButton(self.graph_frame, text="Scatterplot", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.display_graph).pack(pady=10, padx=10, fill="x")
        # ctk.CTkButton(self.graph_frame, text="Bar Graph", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=self.display_graph).pack(pady=10, padx=10, fill="x")
        graphs= ["Bar", "Line", "Scatterplot"]
        for label in graphs:
            btn = ctk.CTkButton(self.graph_frame, text=label, fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda lbl=label: self.graph_choice(lbl))
            btn.pack(pady=10, padx=10, fill="x")
            self.graph_dict[label] = btn #save it in a dictionary
            


    def data_show(self):#display graph buttons
        if self.current_data_state == "data choices displayed":
                self.clear_data_buttons()
                return
        self.current_data_state = "data choices displayed"
        # columns = ["Byte 1", "Byte 2", "Byte 3"]
        # for label in columns:
        #     btn = ctk.CTkButton(self.data_frame, text=label, fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda lbl=label: self.data_choice(lbl))
        #     btn.pack(pady=10, padx=10, fill="x")#display buttons for all columns
        #     self.data_dict[label] = btn#save it in a dictionary

        columns = self.df.columns
        for label in columns[1::]:
            btn = ctk.CTkButton(self.data_frame, text=label, fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda lbl=label: self.data_choice(lbl))
            btn.pack(pady=10, padx=10, fill="x")#display buttons for all columns
            self.data_dict[label] = btn#save it in a dictionary
 

    
    #Frame commands
    def show_one_frame(self):
        if self.current_layout == "1-frame":
            return  
        self.current_layout = "1-frame"
        self.clear_main_content()

        frame = ctk.CTkFrame(self.main_content, corner_radius=10, border_width=2, border_color=NU_PURPLE_HEX)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(frame, text="Single Frame", font=("Arial", 16)).pack(pady=10)

        #show the button to plot one graph
        self.clear_plot_buttons()
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 1-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(frame, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")

    def show_two_frames(self):
        if self.current_layout == "2-frame":
            return 
        self.current_layout = "2-frame"
        self.clear_main_content()

        self.frame1 = ctk.CTkFrame(self.main_content, corner_radius=10, border_width=2, border_color=NU_PURPLE_HEX)
        self.frame2 = ctk.CTkFrame(self.main_content, corner_radius=10, border_width=2, border_color="white")

        self.frame1.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.frame2.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.frame1, text="Frame A", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.frame2, text="Frame B", font=("Arial", 16)).pack(pady=10)

        #show the button to plot two graphs
        self.clear_plot_buttons()
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 1-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame1, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 2-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame2, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")

    def show_three_frames(self):
        if self.current_layout == "3-frame":
            return  
        self.current_layout = "3-frame"
        self.clear_main_content()

        left_frame = ctk.CTkFrame(self.main_content, corner_radius=10, border_width=2, border_color=NU_PURPLE_HEX)
        right_container = ctk.CTkFrame(self.main_content)

        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        right_container.pack(side="right", fill="both", expand=True)

        top_right_frame = ctk.CTkFrame(right_container, corner_radius=10, border_width=2, border_color="white")
        bottom_right_frame = ctk.CTkFrame(right_container, corner_radius=10, border_width=2, border_color="silver")

        top_right_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)
        bottom_right_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(left_frame, text="Big Frame", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(top_right_frame, text="Top Right Frame", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(bottom_right_frame, text="Bottom Right Frame", font=("Arial", 16)).pack(pady=10)

        #show the button to plot three graphs
        self.clear_plot_buttons()
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 1-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(left_frame, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 2-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(top_right_frame, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 3-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(bottom_right_frame, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")

    def show_four_frames(self):
        if self.current_layout == "4-frame":
            return  
        self.current_layout = "4-frame"
        self.clear_main_content()

        # Create a four-frame layout
        top_row = ctk.CTkFrame(self.main_content)
        bottom_row = ctk.CTkFrame(self.main_content)

        top_row.pack(side="top", fill="both", expand=True)
        bottom_row.pack(side="top", fill="both", expand=True)

        self.frame1 = ctk.CTkFrame(top_row, corner_radius=10, border_width=2, border_color=NU_PURPLE_HEX)
        self.frame2 = ctk.CTkFrame(top_row, corner_radius=10, border_width=2, border_color="white")
        self.frame3 = ctk.CTkFrame(bottom_row, corner_radius=10, border_width=2, border_color="white")
        self.frame4 = ctk.CTkFrame(bottom_row, corner_radius=10, border_width=2, border_color=NU_PURPLE_HEX)

        self.frame1.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.frame2.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.frame3.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.frame4.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(self.frame1, text="Frame 1", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.frame2, text="Frame 2", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.frame3, text="Frame 3", font=("Arial", 16)).pack(pady=10)
        ctk.CTkLabel(self.frame4, text="Frame 4", font=("Arial", 16)).pack(pady=10)

        #show the button to plot four graphs
        self.clear_plot_buttons()
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 1-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame1, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 2-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame2, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 3-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame3, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(self.plot_buttons_frame, text="Graph 4-frame", fg_color="white", bg_color= NU_SILVER_HEX, hover_color=NU_SILVER_HEX, text_color='black', command=lambda: self.plot(self.frame4, graph_choice=self.plotting_parameters['graph'], data_choice=self.plotting_parameters["columns"])).pack(pady=10, padx=10, fill="x")


    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        self.current_layout = None


    #CHOICE COMMANDS
    def graph_choice(self, choice):
        #takes in the choice depending on what was selected
        for btn in self.graph_dict.values():
            btn.configure(fg_color="white")

        # Change the clicked button's color to indicate selection
        self.graph_dict[choice].configure(fg_color=PURPLE_60_HEX)
        self.plotting_parameters["graph"] = choice

        return choice
    

    def data_choice(self, choice):
        #takes in the choice depending on what was selected
        # for btn in self.data_dict.values():
        #     btn.configure(fg_color="white")
        # Move this step to plot func to accomodate multiple lines

        # Change the clicked button's color to indicate selection
        
        if choice not in self.plotting_parameters["columns"]:
            self.data_dict[choice].configure(fg_color=PURPLE_60_HEX)
            self.plotting_parameters["columns"].append(choice) #save the choice
        else:
            self.data_dict[choice].configure(fg_color="white")
            self.plotting_parameters["columns"].remove(choice) #remove the choice
        return choice
    
    #PLOT COMMANDS
    def plot(self,frame, graph_choice, data_choice):
        #takes in the frame and graph choice and data choice and plots that graph on the said frame.
        if not graph_choice or not data_choice:
            return
        # Clear the frame of any previous content
        for widget in frame.winfo_children():
            widget.destroy()

        # #data points
        if len(data_choice) <= 1:
            y = self.df[data_choice[0]]
        else:
            y = self.df[data_choice]
        times = self.df.columns[0]
        x = self.df[times]

        fig, ax = plt.subplots(figsize=(5,4))
        # Example: choose a plot type based on graph_choice
        if graph_choice == "Line":
            # For example, a simple line plot (replace with your data_choice logic)
            ax.plot(x,y, label=data_choice)
        elif graph_choice == "Scatterplot":
            ax.scatter(x,y, label=data_choice)
        elif graph_choice == "Bar":
            ax.bar(x,y, label=data_choice)
        else:
            ax.text(0.5, 0.5, "No valid graph type", ha="center")
        concat_title = ""
        for dc in data_choice:
            concat_title += f"{dc}, "
        concat_title = concat_title.strip()
        ax.set_title(f"{concat_title} v Time")
        #canvas to draw figure
        
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()# returns the underlying Tkinter widget associated with the Matplotlib canvas.
        canvas_widget.pack(side="top", fill="both", expand=True)
        #navigation toolbar for zooming and panning
        toolbar = CustomToolbar(canvas, frame)
        toolbar.update()
        # Pack the toolbar
        toolbar.pack(side="bottom", fill="x")

        #reset selections
        for btn in self.graph_dict.values():
            btn.configure(fg_color="white")

        for btn in self.data_dict.values():
            btn.configure(fg_color="white")

        self.plotting_parameters["columns"] = []


    def reset(self):#resets the graphs and everything to initialization stage
        self.clear_main_content()
        self.clear_layout_buttons()
        self.clear_graph_buttons()
        self.clear_data_buttons()
        self.show_four_frames()




# Run the application
if __name__ == "__main__":
    df = pd.read_csv("dummy_can_data_expanded.csv")
    app = MultiFrameApp(df)
    app.mainloop()


#Notes: 
"""
So when you call the bar graph fucntion it displays on each child on the main content (however the main content has two containers that's why its displaying on two frames)
"""
