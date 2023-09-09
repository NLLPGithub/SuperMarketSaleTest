import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='Supermarket Sale Dashboard',page_icon=':bar_chart:',layout='wide')

df=pd.read_csv('supermarket_sales.csv')

st.sidebar.header('Please filter here')

product=st.sidebar.multiselect("Select product line: ",
                      options=df['Productline'].unique(),
                      default=df['Productline'].unique()[:5]
                      )

city=st.sidebar.multiselect("Select City: ",
                      options=df['City'].unique(),
                      default=df['City'].unique()[:5])

customertype=st.sidebar.multiselect("Select Customer type : ",
                      options=df['Customertype'].unique(),
                      default=df['Customertype'].unique()[:5])

paymentmethod=st.sidebar.multiselect("Select Payment methods : ",
                      options=df['Payment'].unique(),
                      default=df['Payment'].unique()[:5])

st.title(":bar_chart:  Supermarket Sales Dashbord for Q1 2019")
st.markdown('##')

total_sale=df['Total'].sum()
product_num=df['Productline'].nunique()


left_col,right_col=st.columns(2)

with left_col:
    st.subheader('Total Sales')
    st.subheader(f"US $ {total_sale}")
    
with right_col:
    st.subheader('Number of Product line')
    st.subheader(f"{product_num}")
    
    
df_select=df.query('City==@city and Customertype==@customertype and Productline==@product and Payment==@paymentmethod')

sale_by_product=(df_select.groupby('Productline')['Total'].sum().sort_values(ascending=False))

fig_product_sales =px.bar(
    sale_by_product,
    x=sale_by_product.values,
    y=sale_by_product.index,
    orientation='h',
    title='Sales by product line'
)

sale_city_pie= px.pie(df_select,values='Total',names='City',title='Sales of City')

sale_by_customertype=(df_select.groupby('Customertype')['Total'].sum().sort_values(ascending=False))

fig_custype_sales =px.bar(
    sale_by_customertype,
    x=sale_by_customertype.index,
    y=sale_by_customertype.values,
    title='Sales by Customer Types'
)

a_col,b_col,c_col=st.columns(3)

a_col.plotly_chart(fig_product_sales,use_container_width=True)
c_col.plotly_chart(fig_custype_sales,use_container_width=True)
b_col.plotly_chart(sale_city_pie,use_container_width=True)

#  ---

l_col,r_col,z_col=st.columns(3)

df1=df.query('City==@city')
vv=df1.groupby('City')['Total'].sum()
fig=px.line(df,x=vv.index, y=vv.values, title='Sales by City')
r_col.plotly_chart(fig,use_container_width=True)


fig2=px.scatter(df,x='Total',y='Productline', title='Sales by Product line')

l_col.plotly_chart(fig2,use_container_width=True)

sale_payment_pie= px.pie(df_select,values='Total',names='Payment',title='Sales by Payment Method')
z_col.plotly_chart(sale_payment_pie,use_container_width=True)

#

