import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict

def load_dataframes(uploaded_files: List) -> Dict[str, pd.DataFrame]:
    """
    Loads CSV or Excel files into Pandas DataFrames.

    Args:
        uploaded_files: A list of uploaded file objects from Streamlit's file_uploader.

    Returns:
        A dictionary where keys are file names and values are the corresponding DataFrames.
    """
    dataframes = {}
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f"Unsupported file type: {uploaded_file.name}")
                continue  # Skip to the next file
            dataframes[uploaded_file.name] = df
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {e}")
    return dataframes

def plot_data(data: pd.DataFrame, x_axis: str, y_axis: str, plot_title: str, plot_type: str = "Line Plot") -> go.Figure:
    """
    Plots the data based on user selections using Plotly.  Returns the Plotly figure.

    Args:
        data: The Pandas DataFrame containing the data to plot.
        x_axis: The column name for the x-axis.
        y_axis: The column name for the y-axis.
        plot_title: Title of the plot
        plot_type: The type of plot to create ("Line Plot" or "Scatter Plot").

    Returns:
        A Plotly Figure object.
    """
    if plot_type == "Line Plot":
        fig = go.Figure(data=go.Scatter(x=data[x_axis], y=data[y_axis], mode='lines'))
    elif plot_type == "Scatter Plot":
        fig = go.Figure(data=go.Scatter(x=data[x_axis], y=data[y_axis], mode='markers'))
    else:
        st.error(f"Unsupported plot type: {plot_type}")
        return go.Figure()  # Return an empty figure to avoid errors

    fig.update_layout(
        title=plot_title,
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font_color="#FFFFFF",
        xaxis=dict(gridcolor="#4a4a4a", zerolinecolor="#4a4a4a"),
        yaxis=dict(gridcolor="#4a4a4a", zerolinecolor="#4a4a4a"),
    )
    return fig

def main():
    """
    Main function to run the Streamlit app.
    """
    # Set page configuration
    st.set_page_config(
        page_title="NFR-25 DAQ Interface",
        page_icon="NFR",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar
    st.sidebar.title("Navigation")
    st.sidebar.write("Use the sidebar to navigate the app.")

    # File uploader in the sidebar for multiple files
    uploaded_files = st.sidebar.file_uploader("Upload your data files", type=["csv", "xlsx"], accept_multiple_files=True)

    # Main content
    st.title("NFR 25 DAQ Interface")
    st.write("Northwestern Formula Racing's DAQ data analysis tool. Upload your data using the sidebar.")

    if uploaded_files:
        # Load all uploaded files into dataframes
        dataframes = load_dataframes(uploaded_files)

        # Combine all dataframes into one for column selection
        combined_data = pd.concat(dataframes.values(), ignore_index=True)
        available_columns = combined_data.columns

        # Allow user to select the number of plots
        num_plots = st.sidebar.selectbox("Number of Plots", [1, 2, 3, 4], index=1)  # default 2

        st.write("File uploaded successfully!")
        st.write("Preview of the data:")
        for name, df in dataframes.items():
            st.write(name)
            st.dataframe(df)

        plot_configs = []  # List to store plot configurations
        show_plots = False #flag

        # Create a 2x2 grid for plot input
        cols = st.columns(2)
        rows = [cols[i % 2] for i in range(num_plots)]

        for i in range(num_plots):
            with rows[i]:
                st.subheader(f"Plot {i + 1}")
                # Use a unique key for each selectbox
                file_name_key = f"file_name_{i}"
                x_axis_key = f"x_axis_{i}"
                y_axis_key = f"y_axis_{i}"
                plot_type_key = f"plot_type_{i}"

                file_name = st.selectbox(f"Select Data Source for Plot {i + 1}", list(dataframes.keys()), key=file_name_key)
                df = dataframes[file_name]
                x_axis = st.selectbox(f"Select X-axis variable for Plot {i + 1}", df.columns, key=x_axis_key)
                y_axis = st.selectbox(f"Select Y-axis variable for Plot {i + 1}", df.columns, key=y_axis_key)
                plot_type = st.selectbox(f"Select Plot Type for Plot {i + 1}", ["Line Plot", "Scatter Plot"], key=plot_type_key)

                plot_configs.append({
                    "file_name": file_name,
                    "x_axis": x_axis,
                    "y_axis": y_axis,
                    "plot_type": plot_type,
                    "df": df, #store df
                    "title": f"{file_name} - {y_axis} vs {x_axis}"
                })

        # Generate Plots Button
        if st.button("Generate Plots"):
            show_plots = True #set flag

        if show_plots:
             # Create a 2x2 grid for displaying the plots
            plot_cols = st.columns(2)
            plot_rows = [plot_cols[i % 2] for i in range(num_plots)]
            for i, config in enumerate(plot_configs):
                with plot_rows[i]:
                    fig = plot_data(config["df"], config["x_axis"], config["y_axis"], config["title"], config["plot_type"])
                    st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Please upload a file to get started.")

        # Add a map of Northwestern University with a pin on Ford Design Center
        st.title("Welcome to Northwestern Formula Racing")
        ford_design_center_coords = [42.056459, -87.675267]
        st.map(pd.DataFrame([{"lat": ford_design_center_coords[0], "lon": ford_design_center_coords[1]}]), color="#4E2A84", zoom=14)

if __name__ == "__main__":
    main()
