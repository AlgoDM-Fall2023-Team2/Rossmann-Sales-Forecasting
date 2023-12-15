import streamlit as st
import pandas as pd
import json
import plotly.express as px


# page headings
st.set_page_config(layout="wide", page_title="INFO7374: Algorithmic Digital Marketing")
st.title("Rossmann Sales Prediction")
st.header("INFO7374: Final Project")
st.subheader("Team 2: Adit Bhosale, Sowmya Chatti, Vasundhara Sharma")

# initializing variables
store_type, store_id, flag_weekly_monthly = None, None, None
button_view_sales = None

with open("data/store_mappings.json", 'r') as file:
    store_dict = json.load(file)

col_store_type, col_store_id, col_radio = st.columns((2, 2, 1))

with col_store_type:
    store_type = st.selectbox(label='Select the Store Type', placeholder="Store Type", index=None, options=store_dict.keys())
with col_store_id:
    if store_type:
        store_id = st.selectbox(label='Select the Store ID', placeholder="Store ID", index=None, options=store_dict[store_type])
with col_radio:
    if store_id:
        flag_weekly_monthly = st.radio("See weekly or monthly sales", options=['Weekly', 'Monthly'], horizontal=True, index=None)


if flag_weekly_monthly:
    col_space_1, col_space_2, col_space_3 = st.columns((2, 2, 1))
    with col_space_3:
        button_view_sales = st.button("View Sales", key=1001, use_container_width=True)

    # display past sales data
if button_view_sales:
    df = pd.read_csv("data/train.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df = df[df['Store'] == store_id]
    df = df[['Date', 'Sales']]
    df = df.set_index('Date', drop=False)
    if flag_weekly_monthly == "Weekly":
        df = df.resample('W').mean(numeric_only=True)
        #st.line_chart(data=df, color="#54007d")
        fig = px.line(df, x=df.index.values, y="Sales")
        fig.update_layout(
            title=f'Weekly Sales of Store ID: {store_id}',
            xaxis_title='Date',
            yaxis_title='Sales in USD',
        )
    else:
        df = df.resample('M').mean(numeric_only=True)
        #st.line_chart(data=df, color="#54007d")

        fig = px.line(df, x=df.index.values, y="Sales")
        fig.update_layout(
            title=f'Monthly Sales of Store ID: {store_id}',
            xaxis_title='Date',
            yaxis_title='Sales in USD',
        )
    fig.update_traces(marker_color='rgb(158,202,225)')
    st.plotly_chart(fig, use_container_width=True)

