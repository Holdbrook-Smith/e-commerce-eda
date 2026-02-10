import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
#import os
import plotly.express as px
import datetime as dt
import matplotlib.pyplot as plt
tab1,tab2 = st.tabs(["E-C EDA","OVERVIEW"])
with tab1:

    st.set_page_config(page_title='E-commerce shop',layout = 'wide')

    st.title("Holdbrook's E-commerce EDA")
    fl = st.file_uploader(":file_folder: upload file")
    if fl is not None:
        filename=fl.name
        st.write(filename)
        df=pd.read_csv(filename)
    else:
        df=pd.read_csv("ecommerce_sales_port.csv")

    col1,col2 = st.columns((2))
#converting to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])
#getting the start and end date
    startdate = pd.to_datetime(df["order_date"]).min()
    enddate = pd.to_datetime(df["order_date"]).max()
#getting column date to filter the data due to date
    with col1:
        d1 = pd.to_datetime(st.date_input("Start Date",startdate))
    with col2:
        d2 = pd.to_datetime(st.date_input("End Date",enddate))

    df = df[
    (df["order_date"] >= d1) &
    (df["order_date"] <= d2)
    ].copy()

#creating a sidebar for area select

    st.sidebar.header("Choose your location")
    region = st.sidebar.multiselect("Pick your region",df["region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["region"].isin(region)]
    category_df = df2.groupby('category', as_index=False)['quantity'].sum()
    with col1:
        st.subheader("Quantity purchased")
        fig = px.bar(category_df,x = "category", y = "quantity", text = ['${:,.2f}'.format(x) for x in category_df["quantity"]],
                    template = "seaborn")
	figure2.update_layout(width=1400,height=600,autosize=False)
        st.plotly_chart(figure2,use_container_width= False, height = 200)
    with col2:
        st.header("Regional Purchasing Power")
        region_df = df2.groupby('region', as_index=False)['quantity'].sum()
        fig = px.pie(region_df, values = "quantity", names = "region", hole = 0.5)
        fig.update_traces(textposition = "outside")
	figure.update_layout(width=1400,height=600,autosize=False)
        st.plotly_chart(figure,use_container_width= False,height = 200)
    #tree based on category,region and payment_method
    st.subheader("Heirachiel Map")
    fig3 = px.treemap(df2,path = ["region","category","payment_method"],values = "quantity", hover_data=["quantity"],
                     color = "payment_method")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3,use_container_width= False)
    #quantity vrs profit_margin
    #col1,col2 = st.columns(2)
    #with col1:
    #    pfm = df2.groupby("quantity")["profit_margin"].value_counts().reset_index(name="count")
    #    st.line_chart(pfm)
    #with col2:
    #    pfm1 = df2.groupby("category")["profit_margin"].value_counts().reset_index(name="count")
    #    st.bar_chart(pfm1,x="category",y="profit_margin")
    st.subheader("Profit Made Over Time")
    df2["month"] = df2["order_date"].dt.to_period("M")
    plots = pd.DataFrame(df2.groupby(df2["month"].dt.strftime("%Y:%b"))["profit_margin"].sum()).reset_index()
    figure = px.line(plots,x = "month",y = "profit_margin", labels = {"profit_margin:amount"},height = 500, width = 1000, template = "gridon")
	st.plotly_chart(figure,use_container_width = False)
        








