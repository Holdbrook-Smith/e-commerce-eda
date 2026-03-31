import streamlit as st
import pandas as pd
#import altair as alt
#import seaborn as sns
#import os
import plotly.express as px
import datetime as dt
#import matplotlib.pyplot as plt
tab1,tab2 = st.tabs(["E-C EDA","OVERVIEW"])
with tab1:
    st.set_page_config(page_title='E-commerce shop',layout="wide")
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
    
    st.subheader("Product Performance")
    fig = px.bar(category_df,x = "category", y = "quantity",text=['${:,.2f}'.format(x) for x in category_df["quantity"]],template = "seaborn")
    fig.update_layout(width=1400,height=600,autosize=False)           
    st.plotly_chart(fig,use_container_width=False)


        
    
    st.header("Regional Purchasing Power")
        
    
    # Aggregate quantities by region
    region_df = df2.groupby('region', as_index=False)['quantity'].sum()
    
    # Create pie chart
    fig = px.pie(
        region_df,
        values="quantity",
        names="region",
        hole=0.5,               # Donut chart
        title="Regional Purchasing Power"
    )
    
    # Update layout and styling
    fig.update_traces(textposition="outside", textinfo="percent+label")
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Display in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    #st.plotly_chart(fig,use_container_width=False,height = 600,width = 1400)
    #tree based on category,region and payment_method
    st.subheader("Heirachiel Map")
    fig3 = px.treemap(df2,path = ["region","category","payment_method"],values = "quantity", hover_data=["quantity"],
                     color = "payment_method")
    fig3.update_layout(width=1000,height=600,autosize=False)
    st.plotly_chart(fig3,use_container_width = False)
    #quantity vrs profit_margin
    #col1,col2 = st.columns(2)
    #with col1:
    #    pfm = df2.groupby("quantity")["profit_margin"].value_counts().reset_index(name="count")
    #    st.line_chart(pfm)
    #with col2
    #    pfm1 = df2.groupby("category")["profit_margin"].value_counts().reset_index(name="count")
    #    st.bar_chart(pfm1,x="category",y="profit_margin")
    st.subheader("Profit Margin")
    df2["month"] = df2["order_date"].dt.to_period("M")
    plots = pd.DataFrame(df2.groupby(df2["month"].dt.strftime("%Y:%b"))["profit_margin"].sum()).reset_index()
    figure = px.line(plots,x = "month",y = "profit_margin", labels = {"profit_margin:amount"},height = 500, width = 1000, template = "gridon")
    figure.update_layout(width=1400,height=600,autosize=False)
    st.plotly_chart(figure,use_container_width=False)
        
with tab2:
    st.header("OVERVIEW AND EXPLANATION OF THE EDA")
    st.write("This project focuses on performing an Exploratory Data Analysis" \
    "on an e-commerce dataset to uncover meaningful insights into customer and product behaviour," \
    "sales trends, and product performance.")

    st.write("The goal of this analysis is to understand key patterns such as" \
    "purchasing habits, revenue distribution, factors influencing sales, time analysis per product performance" \
    "and more. By analysing these trends, the project aims to support data-driven decision making" \
    "that can improve customer experince, optimised product offerings, and increase in business performance.")

    st.write("Various data visualisation techniques and statistical summaries " \
    "were used to explore the dataset,identify patterns, detect anomalies and highlight key " \
    "business insights")

    st.subheader("PRODUCT PERFORMANCE :bar_chart:")
    st.write("The very first bar plot distribution shows the perfomance of various " \
    "products by displaying from the top-selling products by their categories and the revenue each category generates, " \
    "The leading most purchased product category being Electronics, followed by Fashion " \
    "and with the least purchased product category being Grocery")
    
    st.subheader("REGIONAL PURCHASING POWER")
    st.write("The regional purchasing power is a pie chart that shows the " \
    "proportions of purchasing among the various regions, the chart explains" \
    " the purchasing density as related to the other regions ")

    st.subheader("HEIRACHIAL TREE MAP")
    st.write("This treemap visualizes the hierarchical structure of product categories, " \
    "allowing us to quickly identify which categories and subcategories contribute the most to overall sales. Larger blocks indicate higher revenue contribution, " \
    "making it easy to spot top-performing segments.")

    st.subheader("PROFIT MARGIN :chart_with_upwards_trend:")
    st.write("The profit margin shows the amount of profit made over time" \
    "begining from 2023 December to 2025 September, highlighting how efficiently revenue is converted into profit. Higher margins indicate more profitable areas of the business, " \
    "while lower margins may signal higher costs or pricing inefficiencies. ")

    st.subheader("NOTE :mag:")
    st.write("In this interactive dashboard an option has been " \
    "provided where users can upload their own specific data for the dashboard to make analysis " \
    "there is also a calender to help users make analysis within a specific time range " \
    "and also there is the sidebar that can help users make analysis solely on a specific region or compare certain specific regions at ease")



