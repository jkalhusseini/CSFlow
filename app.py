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


st.title("CSFlow Computation")

uploaded_file = st.file_uploader("Insert CSV File Here!")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    SubPlot = make_subplots(rows = 1, cols = 4,
    y_title= "Flow Rate", x_title="", subplot_titles= ("Age", "BMI", "Months", "FOHR")   
                     )

    SubPlot.update_layout(showlegend = False, title = "", plot_bgcolor = 'white')

    SubPlot.update_xaxes(showline = True, linecolor = 'black', linewidth = 1.5, ticks = "outside", showgrid = True, gridcolor = "lightgray", gridwidth = .5)
    SubPlot.update_yaxes(showline = True, linecolor = 'black', linewidth = 1.5, ticks = "inside", showgrid = True, gridcolor = "lightgray", gridwidth = .5)

    SubPlot.append_trace(go.Scatter(x = df['Age'], y = df["FR"], mode = "markers", marker = dict(color = "red")), row = 1, col = 1)
    SubPlot.append_trace(go.Scatter(x = df['BMI'], y = df["FR"], mode = "markers", marker = dict(color = "green")), row = 1, col = 2)
    SubPlot.append_trace(go.Scatter(x = df['Months'], y = df["FR"], mode = "markers", marker = dict(color = "orange")), row = 1, col = 3)
    SubPlot.append_trace(go.Scatter(x = df['FOHR'], y = df["FR"], mode = "markers", marker = dict(color = "purple")), row = 1, col =4)

    SubPlot.update_traces(marker = dict(size = 8, line = dict(width = .75, color = "black")))

    st.plotly_chart(SubPlot)




    Plot3D = px.scatter_3d(df, x = "FOHR", y = "Age", z = "FR", color = "Etiology")
    Plot3D.update_traces(marker_size = 5, opacity = 0.75)

    st.plotly_chart(Plot3D)



    pca = PCA()
    features = ["FR", "BMI", "FOHR", "Age", "Months"]
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

else: st.warning("Bro where's the file???")


