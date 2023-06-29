import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import plotly.express as px
page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb736");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

df = pd.read_pickle('SharkTank')
st.markdown("<h1 style='text-align: center; color: red;'>Shark Tank EDA</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3, gap='large')
with col1:
    st.write('Total Number of Participating Brands :' + " " + str(len(df['Brand'].unique())))
with col2:
    st.write('Total Number of Episodes in Season 1:' + " " + str(len(df['Episode Number'].unique())))
with col3:
    st.write('Total Number of Participating Sharks:' + " " + str(len((df.columns[7:14]))))
col4, col5, col6 = st.columns(3, gap='large')
with col4:
    st.write(('Total Amount Investment in Season 1:₹{} Lakhs'.format(df.iloc[:, 4].sum())))
with col5:
    st.write(('Total Debt in Season 1 :₹{} Lakhs'.format(df.iloc[:, 5].sum())))
st.markdown('**:blue[Top 10 Invested Brands]**')
x = df.groupby(['Brand'], as_index=False)['Investment Amount (In Lakhs INR) '].sum().nlargest(10,
                                                                                              columns='Investment Amount (In Lakhs INR) ')
fig = px.bar(x, x='Brand', y='Investment Amount (In Lakhs INR) ')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)
st.markdown('**:green[Top 10 Debt Brands]**')
x = df.groupby(['Brand'], as_index=False)['Debt (In lakhs INR)'].sum().sort_values(by='Debt (In lakhs INR)',
                                                                                   ascending=False).head(10)
fig = px.bar(x, x='Brand', y='Debt (In lakhs INR)')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)
st.markdown('**:orange[Highest Equity Brand]**')
df['Equity'] = df['Equity'].str.replace('%', '').astype(float)
x = df.groupby('Brand', as_index=False)['Equity'].sum().sort_values(by='Equity', ascending=False).head(10)
fig = px.bar(x, x='Brand', y='Equity')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)
st.markdown('**:violet[Investment By Each Sharks]**')
sharks = df.columns[7:14]
company = []
for i in sharks:
    company.append(len(df[df[i] == 'Y']['Brand'].value_counts().index))
x = pd.DataFrame([sharks, company]).T
x.columns = ['Name', 'Number']
fig = px.pie(x, values='Number', names='Name')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)
st.markdown('**:red[Ratio of Investment Compaines of Season 1]**')
df['Invested']=np.where(df['Investment Amount (In Lakhs INR) ']>0,'Invested','Not Invested')
x=df.groupby('Invested',as_index=False)['Invested'].value_counts()
fig=px.pie(x,values='count',names='Invested')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)
st.header('Ratio of Investment by Each Shark in Brands')
select=st.selectbox('Select Shark Name',sharks)
x=df[select].value_counts().reset_index().rename(columns={select:'Invested'})
fig=px.pie(x,values='count',names='Invested')
fig.update_layout(
    {
        'height': 500,
        'width': 800
    }
)
st.plotly_chart(fig)

