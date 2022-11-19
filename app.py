#Import libraries
import streamlit as st
import pandas as pd


#load in the data
df = pd.read_csv('data/Pakistan - Food Prices_2022.csv')
df = df.dropna()

#rename columns to be all lower case and no spaces
df.columns = df.columns.str.lower().str.replace(' ', '_')

st.title('Pakistan - Commodity Prices Over Time')
st.header('This is a simple app to show the commodity prices over time in Pakistan')
st.write(df)


#add a map of unique City names
st.header('Map of Cities in the dataset')
st.map(df)

st.write("Please filter the data by selecting the commodity and city you want to see")
select_commodity = st.selectbox('Select a commodity item', df['commodity'].unique())
select_city = st.selectbox('Select a city', df['city_name_'].unique())

filtered_df = df[(df['commodity'] == select_commodity) & (df['city_name_'] == select_city)]

#sort the data by date
filtered_df['date'] = pd.to_datetime(filtered_df['date'])
filtered_df = filtered_df.sort_values(by='date')

line_df = filtered_df[['date', 'usd_price']].set_index('date')

#Create a line chart showing the price of food over time
st.header('$USD Price of ' + 'of ' + select_commodity + ' in ' + select_city)

st.line_chart(line_df)

st.write("The filtered data is shown below")
st.write(line_df)


#add a bar chart of times the commodity was reported in the different cities
st.header('Number of times ' + select_commodity + ' was reported in each city')

#group by city and count the number of times the commodity was reported
df_bar = df.groupby(['city_name_', 'commodity']).count().reset_index()
df_bar = df_bar[['city_name_', 'commodity', 'date']]
df_bar = df_bar[df_bar['commodity'] == select_commodity]
df_bar = df_bar.rename(columns={'date': 'count'})
df_bar.drop('commodity', axis=1, inplace=True)
df_bar = df_bar.set_index('city_name_')
st.bar_chart(df_bar)
st.write("The filtered data is shown below")
st.write(df_bar)

## Code for the bar chart
st.code("""
## Code for the bar chart
#group by city and count the number of times the commodity was reported
df_bar = df.groupby(['city_name_', 'commodity']).count().reset_index()
df_bar = df_bar[['city_name_', 'commodity', 'date']]
df_bar = df_bar[df_bar['commodity'] == select_commodity]
df_bar = df_bar.rename(columns={'date': 'count'})
df_bar.drop('commodity', axis=1, inplace=True)
df_bar = df_bar.set_index('city_name_')
st.bar_chart(df_bar)
st.write("The filtered data is shown below")
st.write(df_bar)
""")





