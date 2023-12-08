import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
import pandas as pd
import streamlit as st
from PIL import Image

#  bold color

image=Image.open("./utilis/background/practice.jpg")
class UIDesign:
    def __init__(self) -> None:
        pass

    def back_ground(self,image):
         # Resize the image
        resized_img = image.resize((100, 100))

        # Convert the resized image to base64
        encoded_image = base64.b64encode(resized_img.tobytes()).decode()

        # Embed the HTML code in Streamlit app
        markdown=f"""
            <style>
                [data-testid="stAppViewContainer"] {{
                    background: url(data:image/{resized_img};base64,{base64.b64encode(open(resized_img, "rb").read()).decode()});
                    background-size: cover;
                    background-repeat: no-repeat;
                }}
                [data-testid="stHeader"] {{
                    visibility: hidden;
                }}
            </style>
            """
        return markdown


    def result_display(self,result,description):
        header_markdown = f"""
            
            <div class="hero-text234">
            <strong><h>{result}</h></strong>
            </div>
        """
        subtitle_markdown = f"""
           
        
            <style>
                mark {{
                    background-color: white;
                    color: black;
                }}
                #popup {{
                text-align: center;
                font-size: 25px; /* Adjust the font size as needed */
                margin-top: 10px;
                margin-left:%;
                position: relative;
                margin-top:150px;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 750px;
                height: 250px;
                box-shadow: 0 0 50px 1px rgba(0, 0, 0, 0.5);
                padding-top: 30px
                }}
                .hero-text234 h{{
                    font-size: 70px; /* Adjust the font size as needed */
                    
                    
                }}
            </style>

            <div id="popup">
                <div style="margin-top: 25px;">
                    <p style="font-size: 20px;">
                        Total Number of Trips Expected on
                        <mark ><strong><span style="color: black;">{description[0]}</span></strong></mark>
                        from
                        <mark ><strong><span style="color: black;">{description[1]}</span></strong></mark>
                        for
                        <mark ><strong><span style="color: black;">{description[2]}</span></strong></mark>
                    </p>
                </div>
                <div class="hero-text234">
                    <strong>
                        <h>{result}</h>
                    </strong>
                </div>
            </div>


        """
        # st.markdown(header_markdown, unsafe_allow_html=True)
        st.markdown(subtitle_markdown, unsafe_allow_html=True)
        
        return header_markdown,subtitle_markdown
    
    def footer(self):
        # Custom footer
        footer_html = """
            <style>
            #MainMenu{
                visivility:hidden;
            }
            footer{
            visibility:visible;
            }
            footer:after{
                content: By Usman Sajid  @ 2023: ATS;
                display:block;
                position:relative;
                color:tomato;
                padding:5px;
                top:3px;
            }
            </style>
           
        """
        # Display the footer
        st.markdown(footer_html, unsafe_allow_html=True)

        
        
       
    def graphs_st(self,chart_data,selected_year):
        """Showing graphs of dates and their respective results."""
        #  plot the line chart based on previous years value.
        costom_hover_data=[selected_year,'2020','2021','2022']
        fig = px.line(chart_data, x='Date', y=['Predicted_Values', '2020', '2021', '2022'], markers=True, title="Graph of Dates and Results")
        fig.update_traces(hovertemplate=('Date: %{x}<br>' +'Result: %{y}<br>'))

        chart_data['Color'] = chart_data['Percentage'].apply(lambda x: 'Positive Change' if x > 0 else "Negative Change")

    # Plot the bar chart with color based on the "Color" column
        bar_trace = px.bar(
            chart_data,
            x="Date",
            y='Percentage',
            title=f"Taxi ride percentage of 2022 VS {selected_year}",
            color='Color',
        )
        return fig,bar_trace

        

            
            
