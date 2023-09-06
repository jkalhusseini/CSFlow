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
import plotly.graph_objects as go
#from mitosheet.streamlit.v1 import spreadsheet


#st.set_page_config(layout="wide")



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
#spreadsheet(df)


if st.button("Process Data"):
    with st.spinner('Wait for it...'):
        time.sleep(1)
    st.success('Done!')


    hist_values = px.histogram(
    df, x = "FR", 
    #nbins = 150,
    title = "Histogram of Flow Rate Distributions",
    color = "Sex",
    #text_auto = True,
    #y_title = "Count",
    #x_title = "Flow Rate",
    )
    
    hist_values2 = px.histogram(
    df, x = "Etiology", 
    #nbins = 150,
    title = "Histogram of Etiology Distributions",
    color = "Sex",
    #text_auto = True,
    #y_title = "Count",
    #x_title = "Flow Rate",
    )
    

    st.plotly_chart(hist_values, use_container_width=True)
    st.plotly_chart(hist_values2, use_container_width=True)
        

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

    st.plotly_chart(SubPlot, use_container_width=True)



   
    Plot3D = px.scatter_3d(df, x = "FOHR", y = "Age", z = "FR", color = "Sex")
    Plot3D.update_traces(marker_size = 5, opacity = 0.75)

    st.plotly_chart(Plot3D, use_container_width=True)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'surface'}, {'type': 'surface'}]])
    fig.add_trace(
    go.Surface(x=df['FOHR'], y=df["Age"], z=df["FR"], colorscale='Viridis', showscale=False),
    row=1, col=1)

    fig.add_trace(
        go.Surface(x=df['Months'], y=df['FR'], z=df['FOHR'], colorscale='RdBu', showscale=False),
        row=1, col=2)


    fig.update_layout(
        title_text='3D subplots with different colorscales',
        height=800,
        width=800
    )

    st.plotly_chart(fig, use_container_width = True)

    pca = PCA()
    features = ["FR", "BMI", "FOHR", "Age", "Months"]
    components = pca.fit_transform(df[features])
    labels = {
        str(i): f"PC {i+1} ({var:.1f}%)"
        for i, var in enumerate(pca.explained_variance_ratio_ * 100)
    }

    fig1 = px.scatter_matrix(
    components,
    labels=labels,
    dimensions=range(5),
        color=df["Etiology"]
    )
    fig1.update_traces(diagonal_visible=False, showupperhalf = False )
    fig1.update_traces(marker_size = 4.5
                )
    
    st.plotly_chart(fig1, use_container_width=True)



