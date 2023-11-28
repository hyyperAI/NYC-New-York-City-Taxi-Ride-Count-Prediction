import streamlit as st
from datetime import date
import urllib.request
import base64
import json
import os
import ssl
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import time

df=pd.read_csv("daily_agg.csv")
image = Image.open('purpose2.webp')

dates_list=[]
def date_range(selected_date):
    """use for getting 3 days of future and past dates """
    dates_list=[item.strftime("%Y/%m/%d") for item in  pd.date_range(pd.Timestamp(selected_date)-pd.offsets.Day(3),freq='D',periods=5)]
    future_dates=[item for item in pd.date_range(start=pd.Timestamp(selected_date)+pd.offsets.Day(2),freq='D',periods=2)]
    # print(dates_list)
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

def workday_con(workday):
  """conditions for checking season and workday"""
  if selected_day  in ["Mon","Tue","Wed","Thu","Fri"]:
    workday=1
    return workday
  else:
    workday=0
    return workday
  
def selected_season_con(month):
  if month in [12, 1, 2]:
    season="Winter"
    return season
  elif month in [3, 4, 5]:
    season="Spring"
    return season
  elif month in [6, 7, 8]:
    season="Summer"
    return season
  elif month in [9, 10, 11]:
    season="Autumn"
    return season

#  PREVIOUS YEARS DATA (2021,2022)
def previous_dates(dates:list,taxi_type,pickup_location):
  """if you want to show graphs of dates that are present in df"""
  previous_RC_list={}
  
  previ=["2021","2022"]
  for previous_year in previ:
    single_year_data=[]
    for single_date in dates:
      month1 = str(single_date[5:7])
      day1=str(single_date[8:])
      conditions = {
              "PickupBorough": pickup_location,
              "RideType": taxi_type,
              "Date":f"{day1}/{month1}/{previous_year}"
    }
      condition_mask = (df[list(conditions.keys())] == list(conditions.values())).all(axis=1)
      # print(f"{day1}/{month1}/{previous_year}")
      RC_for_previous_year = (df.RideCount[condition_mask])
      single_year_data.append(int(RC_for_previous_year))
    previous_RC_list[previous_year]=single_year_data
  return previous_RC_list

def checking_results(result:int):
    if result < 0:
      result=0
    elif result >= 0:
      pass
    return result
  


def background_image():
  side_bg="nycbackheroimg.webp"
  side_bg="nycbackheroimg.png"
  side_bg_ext = 'webp'
  side_bg="nycbackheroimg.png"
  side_bg_ext = 'webp'
  img = Image.open("nycbackheroimg.png")
  st.image(
        side_bg,
        caption="NYC PREDICTION",
        use_column_width='auto',  # Adjust as needed
        # width=(1000,100),
        
    )
  # Resize the image
  # resized_img = img.resize((100, 100))

  # # Convert the resized image to base64
  # encoded_image = base64.b64encode(resized_img.tobytes()).decode()



def banner(text):
   # Set the background color and text for the banner
  banner_style = """
      <style>
          .banner {
              text-align: center;
              display: table-cell;
              vertical-align: middle;
              padding: 20px;
              background-color: #3498db;  /* Set your desired background color */
              color: white;  /* Set the text color */
              text-align: center;
              font-size: 24px;
              font-weight: bold;
              border-radius: 10px;
          }
      </style>
  """
  st.markdown(f'{banner_style}<div class="banner">{text}</div>', unsafe_allow_html=True)
    
def percentage(past_values,predicted_values):
   percen_list = [round(((predict_value - past_value) / past_value) * 100, 3) for past_value,predict_value in zip(past_values,predicted_values)]
   return percen_list
    
   
def graphs_st(dates: list, results, past_data: dict):
    """Showing graphs of dates and their respective results."""
    data_2021=past_data["2021"]
    data_2022=past_data["2022"]
    # Convert dates to strings
    percentage_values=percentage(data_2022,results)
    # Check if the lengths of 'dates' and 'results' lists match
    if len(dates) != len(results):
        st.write("Error: The 'dates' and 'results' lists must have the same length.")
    else:
        try:
            chart_data = pd.DataFrame({
                "Date": dates,
                "Predicted_Values": results,
                "2021": data_2021,
                "2022": data_2022,
                "Percentage":percentage_values
            })
            fig = px.line(chart_data, x='Date', y=['Predicted_Values', '2021', '2022'],markers=True, title="Graph of Dates and Results",hover_data={'Date': False} )
            chart_data['Color'] = chart_data['Percentage'].apply(lambda x: 'Positive Change' if x < 0 else "Negative Change")

# Plot the bar chart with color based on the "Color" column
            bar_trace = px.bar(
                chart_data,
                x="Date",
                y='Percentage',
                title="NYC Taxi-Ride count percentage",
                color='Color',
            )
            st.plotly_chart(fig)
            st.plotly_chart(bar_trace)
            
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
  content: " By Usman at Advanced Telecom Services (atsailab.com) © 2023."
  }

  div[class="block-container css-1y4p8pa e1g8pov64"]{

  }
    </style>
    """



st.markdown(custom_css, unsafe_allow_html=True)

# background_image()
st.title("NYC Taxi Ridership Prediction")

st.markdown('''This app uses the services and analysis developed by the ATS Data Analysis team to provide a prediction of the total number of trips on any given day in NYC. The data source is the publically available NYC Trips data. The data is cleaned, parsed, and transformed using Azure Databricks to easily extract the necessary features for ML training. Then the Azure ML Studio is used to train the model on data from the duration of 01/01/2009 to 31/12/2022. The endpoint API is deployed on Azure Services and can be accessed through a server link. This web app is deployed using Azure Web Application ready to provide trends and predictions based on the necessary inputs. ''')
st.image(image)
# st.write("Adjust parameters according to your need.")
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

all_result=[]
dates_to_predict=None
button_press=0

if st.button("Use AI to predict"):
    progress_text = "Prediction in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    
    button_press+=1
    dates_to_predict=date_range(str(selected_date))
    prev_year_csv_data=previous_dates(dates_to_predict,taxi_type,pickup_location)
    workday=None
    for item in dates_to_predict:
      year1 = int(item[:4])
      month1 = int(item[5:7])
      day1=int(item[9:])
      workday=workday_con(workday=workday)
      season=selected_season_con(month=month1)
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
    my_bar.empty()
    st.markdown(f"Total Number of Trips Expected on {day}/{month}/{year} from {pickup_location} for {taxi_type}.")
    st.title(f"{all_result[3]}")
    graphs_st(dates=dates_to_predict, results=all_result,past_data=prev_year_csv_data)
