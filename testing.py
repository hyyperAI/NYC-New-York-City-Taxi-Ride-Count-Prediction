# import pandas as pd
# from datetime import datetime,timedelta
# x=pd.date_range(start='1/1/2018', periods=8)
# dates_list=[]
# def date_range(selected_date):
#     dates_list=[item.strftime("%Y/%m/%d") for item in  pd.date_range(pd.Timestamp(selected_date)-pd.offsets.Day(3),freq='D',periods=4)]
#     future_dates=[item for item in pd.date_range(start=pd.Timestamp(selected_date)+pd.offsets.Day(1),freq='D',periods=3)]
#     for item in future_dates:
#         dates_list.append(item.strftime('%Y/%m/%d'))
#     print(dates_list)
# date_range("2023/1/02")