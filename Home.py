import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import timedelta
from models.sarimax import train_arima
import plotly.graph_objects as go


# page headings
st.set_page_config(layout="wide", page_title="INFO7374: Algorithmic Digital Marketing")
st.title("Rossmann Sales Prediction")
st.header("INFO7374: Final Project")
st.subheader("Team 2: Adit Bhosale, Sowmya Chatti, Vasundhara Sharma")

