"""
Find a way to NOT hardcode the columns DONE


"""





    #PLOTTING
    def bar_graph(self, file_path, x_col=None, y_col=None):
        if self.bar_graph_state == "Bar Graph displayed":
            return
        else:    
            self.bar_graph_state = "Bar Graph displayed"#to avaoid multiple graphs
            data = pd.read_csv(file_path)
            print("Data Loaded Successfully!")

            # Check for required columns
            if x_col not in list(data.columns) or y_col not in list(data.columns):
                raise ValueError(f"Specified columns '{x_col}' or '{y_col}' not found in the CSV file.")
            
            frame_bg = (0.2,0.2,0.2)

            # Create a Matplotlib figure
            fig, ax = plt.subplots()
            fig.patch.set_facecolor(frame_bg)  # Set figure background to match frame

            # Customize plot appearance
            ax.set_facecolor(frame_bg)  # Set axes background
            ax.bar(data[x_col], data[y_col], color=NU_PURPLE_HEX)  # Bar color

            # Set label, title, and grid colors
            ax.set_xlabel(x_col, color="white")
            ax.set_ylabel(y_col, color="white")
            ax.set_title("Testing Title", color="white")

            # Set tick colors
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')

            # Remove spines or set them to white
            for spine in ax.spines.values():
                spine.set_color("white")

            bar_image_path = "Graphs/TestBarGraph.png"
            fig.savefig(bar_image_path)
            plt.close()
            return bar_image_path

    def display_image_on_frame(self, frame: ctk.CTkFrame, image_path=None):
            if not os.path.exists(image_path):
                print(f"Error: Image file {image_path} not found.")
                return
            image = Image.open(image_path)
            tk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(285, 285))
            label = ctk.CTkLabel(frame, image=tk_image, text="", width=0, height = 0)
            label.image = tk_image  # Keep a reference to avoid garbage collection
            frame.pack_propagate(False) # prevents frame from expanding when image is packed
            label.pack(fill ="none", padx = 0, pady = 0)


    def display_graph(self):
        path = 'dummy.csv'
        graph_image = self.bar_graph(path, "name", "amount")
        
        #to display on frame1
        self.display_image_on_frame(self.frame1, graph_image)
