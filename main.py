from app.UI  import UIDesign
from app.api import UrlCall
from app.data import Data
import time
import streamlit as st
import pandas as pd
from datetime import date

from PIL import Image
st.set_page_config(layout="wide")
hero=Image.open("./utilis/background/practice.jpg")
csv_data=pd.read_csv("daily_agg.csv")

# background_image()
st.title("NYC Taxi Ridership Prediction")

st.markdown('''This app uses the services and analysis developed by the ATS Data Analysis team to provide a prediction of the total number of trips on any given day in NYC. The data source is the publically available NYC Trips data. The data is cleaned, parsed, and transformed using Azure Databricks to easily extract the necessary features for ML training. Then the Azure ML Studio is used to train the model on data from the duration of 01/01/2009 to 31/12/2022. The endpoint API is deployed on Azure Services and can be accessed through a server link. This web app is deployed using Azure Web Application ready to provide trends and predictions based on the necessary inputs. ''')
st.image('./static/purpose2.webp')
st.write("You can try the prediction model below yourself. Adjust parameters according to your need.")
col1, col2, col3 = st.columns(3)
with col1:
  pickup_location = st.selectbox("Pickup Borough", ["Manhattan","Bronx", "Brooklyn", "EWR",  "Queens", "Staten Island" ])
with col2:
  selected_date = st.date_input("Date in the future", date(2023, 1, 1))
year = int(selected_date.year)
month = int(selected_date.month)
day = int(selected_date.day)
selected_day = selected_date.strftime("%A")[0:3]

with col3:
  taxi_type = st.selectbox("Select a taxi", ["Green Taxi", "Yellow Taxi", "High Volume For-Hire Vehicle"])

#  -------------------------------------
data=Data(csv_data,selected_date=selected_date,selected_day=selected_day,taxi=taxi_type,location=pickup_location)
api_call=UrlCall(url='http://ff8b8ccf-0dfb-48f0-b6f3-5e7954b6d1c6.eastus.azurecontainer.io/score',headers={'Content-Type':'application/json'})

ui=UIDesign()
result=[]
# ui.hero_img(text="this that",subtitle="this is subtitle",image2=hero)

if st.button("Use AI to predict"):
    progress_text = "Prediction in progress. Please wait."

    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1, text=progress_text)


    time.sleep(1)
    date_list=data.date_range()   # date range to be return

    data.previous_values()  # should give reault as the name

    for item in date_list:
      api_parameter=data.api_parameters(single_date_to_predict=item) 
      # api required parameters  
      
      api_result=api_call.url_call(data=api_parameter) # give result to url call
      
      api_result=data.clean_result(api_result) # clean the result
      
      result.append(api_result) # result list contain all the predicitve values
      
      days=f"{day}/{month}/{year}" 
      
      listing=[days,pickup_location,taxi_type]
       
    header,subtitle=ui.result_display(result=result[3],description=listing)


    df=data.create_df(results=result) # give dataframe for showing on graphs

    my_bar.empty()
    
    fig,bar_trace=ui.graphs_st(chart_data=df) # for line chart and bar chart
    st.plotly_chart(fig)
    st.plotly_chart(bar_trace) 