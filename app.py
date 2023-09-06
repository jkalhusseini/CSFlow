import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
import statistics
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from sklearn.decomposition import PCA
import time






st.title("CSFlow Computation")

with st.sidebar:
    options = st.multiselect(
        'How would you like to analyze the data?',
        ['PCA','Histogram','3D Scatter', 'PCA Matrix']
    )

st.subheader("Data Cleaning:")
uploaded_file = st.file_uploader("Insert CSV File Here!")
st.caption("After uploading your CSV, ensure the columns are labeled appropriately below.")
st.caption("Flow rate = FR, Age @ enrollment = Age, Months since shunt = Months, FOHR = FOHR, and Etiology labeled as either NTD, OTHER, or IVH")

df = pd.read_csv(uploaded_file)

st.dataframe(df)



if st.button("Process Data"):
    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.success('Done!')





    hist_values = px.histogram(
        df, x = "PC Flow Rate (mL/hr)", 
        #nbins = 150,
        title = "Histogram of Flow Rate Distributions",
        color = "Etiology",
        #text_auto = True,
        #y_title = "Count",
        #x_title = "Flow Rate",
        )
    
    hist_values = px.histogram(
    df, x = "Etiology", 
    #nbins = 150,
    title = "Histogram of Etiology Distributions",
    color = "PC Flow Rate (mL/hr)",
    #text_auto = True,
    #y_title = "Count",
    #x_title = "Flow Rate",
    )
    

    st.plotly_chart(hist_values)
        

    SubPlot = make_subplots(rows = 1, cols = 4,
    y_title= "Flow Rate", x_title="", subplot_titles= ("Age @ Enrollment(y)", "BMI", "Months btwn shunt placement and PC shunt", "FOHR")   
                    )

    SubPlot.update_layout(showlegend = False, title = "", plot_bgcolor = 'white')

    SubPlot.update_xaxes(showline = True, linecolor = 'black', linewidth = 1.5, ticks = "outside", showgrid = True, gridcolor = "lightgray", gridwidth = .5)
    SubPlot.update_yaxes(showline = True, linecolor = 'black', linewidth = 1.5, ticks = "inside", showgrid = True, gridcolor = "lightgray", gridwidth = .5)

    SubPlot.append_trace(go.Scatter(x = df['Age @ Enrollment(y)'], y = df["PC Flow Rate (mL/hr)"], mode = "markers", marker = dict(color = "red")), row = 1, col = 1)
    SubPlot.append_trace(go.Scatter(x = df['BMI'], y = df["PC Flow Rate (mL/hr)"], mode = "markers", marker = dict(color = "green")), row = 1, col = 2)
    SubPlot.append_trace(go.Scatter(x = df['Months btwn shunt placement and PC shunt'], y = df["PC Flow Rate (mL/hr)"], mode = "markers", marker = dict(color = "orange")), row = 1, col = 3)
    SubPlot.append_trace(go.Scatter(x = df['FOHR'], y = df["PC Flow Rate (mL/hr)"], mode = "markers", marker = dict(color = "purple")), row = 1, col =4)

    SubPlot.update_traces(marker = dict(size = 8, line = dict(width = .75, color = "black")))

    st.plotly_chart(SubPlot)



   
    Plot3D = px.scatter_3d(df, x = "FOHR", y = "Age @ Enrollment(y)", z = "PC Flow Rate (mL/hr)", color = "Etiology")
    Plot3D.update_traces(marker_size = 5, opacity = 0.75)

    st.plotly_chart(Plot3D)



    pca = PCA()
    features = ["PC Flow Rate (mL/hr)", "BMI", "FOHR", "Age @ Enrollment(y)", "Months btwn shunt placement and PC shunt"]
    components = pca.fit_transform(df[features])
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig = px.scatter_matrix(
    components,
    labels=labels,
    dimensions=range(5),
        color=df["Etiology"]
    )
    fig.update_traces(diagonal_visible=False, showupperhalf = False )
    fig.update_traces(marker_size = 4.5
                )
    
    st.plotly_chart(fig)



