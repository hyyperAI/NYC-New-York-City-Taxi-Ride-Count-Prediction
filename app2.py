import streamlit as st
from datetime import date
import requests
import urllib.request
import json
import os
import ssl
import pandas as pd
from time import sleep
import matplotlib.pyplot as plt
from bokeh.plotting import figure
import numpy as np
import altair as alt

df=pd.read_csv("daily_agg.csv")

def dark_theme():
  custom_css = """
  <style>
  body {
      background-color: #222;
      color: #fff;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"] {
      background-color: #222;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"] {
      background-color: #222;
  }
  div[data-baseweb="avatar"] {
    background-color: #222;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"] {
    background-color: #222;
  }
    </style>
    """
  st.markdown(custom_css, unsafe_allow_html=True)

dates_list=[]
def date_range(selected_date):
    """use for getting 3 days of future and past dates """
    dates_list=[item.strftime("%Y/%m/%d") for item in  pd.date_range(pd.Timestamp(selected_date)-pd.offsets.Day(2),freq='D',periods=3)]
    future_dates=[item for item in pd.date_range(start=pd.Timestamp(selected_date)+pd.offsets.Day(1),freq='D',periods=3)]
    for item in future_dates:
        dates_list.append(item.strftime('%Y/%m/%d'))
    return dates_list

def url_call(data,year,month,day):
    """use to call url for our project"""
    body = str.encode(json.dumps(data))
    url = 'http://ff8b8ccf-0dfb-48f0-b6f3-5e7954b6d1c6.eastus.azurecontainer.io/score'
    headers = {'Content-Type':'application/json'}
    req = urllib.request.Request(url, body, headers)
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read())
        return result

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        st.write("The request failed with status code: " + str(error.code))
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

def allowSelfSignedHttps(allowed):
    """ allow to connect azure using env variable """
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context
allowSelfSignedHttps(True) 

def conditions(season,workday):
  """conditions for checking season and workday"""
  if day  in ["Mon","Tues","Wed","Thur","Fri"]:
    workday=1
  else:
    workday=0
  if month in [12, 1, 2]:
    season="Winter"
  elif month in [3, 4, 5]:
    season="Spring"
  elif month in [6, 7, 8]:
    season="Summer"
  elif month in [9, 10, 11]:
    season="Autumn"

#  PREVIOUS YEARS DATA (2021,2022)
def previous_dates():
  """if you want to show graphs of dates that are present in df"""
  previous_RC_list={}
  previ=["2021","2022"]
  for previous_year in previ:
    conditions = {
            "PickupBorough": pickup_location,
            "RideType": taxi_type, 
            "Date":str(f"{year}\{month}\{day}")
  }
    condition_mask = (df[list(conditions.keys())] == list(conditions.values())).all(axis=1)
    RC_for_previous_year = (df.RideCount[condition_mask])
    print(f'hello {(RC_for_previous_year)}')
    previous_RC_list[previous_year]=RC_for_previous_year
  plt.figure(figsize=(10, 6))
  fig, ax = plt.subplots()
  ax.bar(previ,['20','300'])
  ax.set_xlabel("Pickup Borough")
  ax.set_ylabel("Ride Count")
  ax.set_title("Previous Year Data")
  plt.show()
  st.pyplot(fig)

def checking_results(result:int):
    if result < 0:
      result=0
    elif result >= 0:
      pass
    return result
    
      

def graphs_st(dates:list,results):
  """ showing graphs of dates and their respective results """
  date = [str(single_date) for single_date in dates]  
  if len(dates) != len(results):
        st.write("Error: The 'dates' and 'results' lists must have the same length.")
  else:
        try:
            date = [str(single_date) for single_date in dates]
            chart_data = pd.DataFrame(
                {
                    "Date": date,
                    "Results": results,
                }
            )

            # Altair chart for better and visualization
            st.subheader("Dates and Results for NYC taxi prediction")
            st.markdown("This chart shows the relationship between dates and results.")
            st.write("Date Range:", min(date), "to", max(date))
            st.write("Results Range:", min(results), "to", max(results))

            chart = alt.Chart(chart_data).mark_line().encode(
                x='Date',
                y='Results:Q',
                tooltip=['Date', 'Results:Q']
            )+ alt.Chart(chart_data).mark_point().encode(
                x='Date:T',
                y='Results:Q'
            ).interactive()

            st.altair_chart(chart, use_container_width=True)

        except ValueError as e:
            st.write(f"An error occurred: {e}")

custom_css = """
  <style>
  body {
      background-color: #222;
      color: #fff;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"] {
      background-color: #222;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"] {
      background-color: #222;
  }
  div[data-baseweb="avatar"] {
    background-color: #222;
  }
  div[data-baseweb="avatar"][data-baseweb="avatar"][data-baseweb="avatar"] {
    background-color: #222;
  }

  footer:after{
  content: " By Usman @ 2023"
  }
    </style>
    """
st.markdown('<div class="stFooter">MADE BY USMAN</div>', unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

st.title("NYC (New York City) Taxi Ride Count Prediction")

st.markdown('''

This app uses the services and analysis developed by the ATS Data Analysis team to provide a prediction of the total number of trips on any given day in NYC. 
The data source is the publically available NYC Trips data. The data is cleaned, parsed, and transformed using Azure Databricks to easily extract the necessary features for ML training. Then the Azure ML Studio is used to train the model on data from the duration of 01/01/2021 to 31/12/2022. The endpoint API is deployed on Azure Services and can be accessed through a server link. This web app is deployed using Azure Web Application ready to provide trends and predictions based on the necessary inputs. 
The inputs required for this prediction are:
- The Trip Origin Borough 
- The Date for the Prediction
- The Ride Type 
This prediction model enables taxi and for-hire-vehicle dispatching services with an estimate of the daily number of trips originating at a given borough in NYC on any given day. The City of New York can use this information to better manage its fleet and more accurately meet demand. This helps them reduce wait times, have a lower number of idle vehicles, less wasted resources, and mitigate their negative contribution to traffic and the environment. 

You can try the prediction model below yourself.
''')

st.write("You can adjust some parameters according to your need, ")
pickup_location = st.selectbox("Pickup Borough", ["Manhattan","Bronx", "Brooklyn", "EWR",  "Queens", "Staten Island" ])

selected_date = st.date_input("Date in the future", date(2023, 1, 1))
year = int(selected_date.year)
month = int(selected_date.month)
day = int(selected_date.day)

selected_day = selected_date.strftime("%A")[0:3]


taxi_type = st.selectbox("Select a taxi", ["Green Taxi", "Yellow Taxi", "High Volume For-Hire Vehicle"])

#  -------------------------------------

all_result=[]
dates_to_predict=None
button_press=0

if st.button("Use AI to predict"):
    button_press+=1
    dates_to_predict=date_range(str(selected_date))
    for item in dates_to_predict:
      year1 = item[:4]
      month1 = item[5:7]
      day1=item[9:]
      workday=0
      season=""
      conditions(season=season,workday=workday)
      data =  {
      "Inputs": {
        "data": [
          {
            "PickupBorough": pickup_location, 
            "RideType": taxi_type, 
            "Year": year1, 
            "Month": month1,
            "Day": day1, 
            "Season": season, 
            "DayOfWeek": selected_day, 
            "Workday": workday
          }
        ]
      },
      "GlobalParameters": 1.0
    }
      result = url_call(data=data,year=year1,month=month1,day=day1)
      result=int(round(result["Results"][0]))
      result=checking_results(result)
      all_result.append(result)
    st.title(f" {all_result[2]}")
    graphs_st(dates=dates_to_predict,results=all_result)


 