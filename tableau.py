import streamlit as st

def tableau():
    # display table of tableau projects    
    with st.container(height=750,border=True):
        for project_name, project_info in tableau_projects.items():
            with st.container(border=True):
                st.markdown(project_info["name"], unsafe_allow_html=True)
                st.image(project_info["image"], caption=project_info["caption"], use_column_width=True)
                st.info(project_info["info"])

# dictionary of tableau projects
tableau_projects = {
        # project Churn
        "project_churn":{"name" :''' <h3 style='text-align: center;'>Churn Analysis Dashboard ☎️ | 🖥️ <em>  <a href="https://public.tableau.com/views/TelecommunicationsChurnAnalysis_17220110829400/TelecommunicationsChurnAnalysisDashboard?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"> Tableau</a> | <a href="https://github.com/karma-gits">Github</a></h3>''',
                "image" : "images/fulls/05.jpg",
                "caption" : "Telecommunications Churn Analysis Dashboard",
                "info" : "- The Telecommunications Churn Analysis Dashboard aims to uncover insights into customer churn patterns through extensive data cleaning and exploratory analysis using Python. \n- The dashboard visualizes churn metrics across demographic segments, service usage patterns, and reasons for churn, helping stakeholders identify key factors affecting customer retention."
                },
        #project uber
        "project_uber":{"name" :''' <h3 style='text-align: center;'>Uber Black and Lyft Black 🚕 | 🖥️ <em>  <a href="https://public.tableau.com/app/profile/karma.tabs/viz/NYC-UberBlackandLyftBlack/Dashboard1"> Tableau</a> | <a href="https://github.com/karma-gits">Github</a></h3>''',
                "image" : "images/fulls/04.jpg",
                "caption" : "NYC - Uber Black and Lyft Black",
                "info" : "- Developed a dashboard using NYC open data to help Uber Black and Lyft Black drivers identify peak demand areas and times. \n- Cleaned and processed data with Python, using proxy calculations to differentiate black car rides from UberX. \n- Highlighted busy neighborhoods and optimal trip times for long rides, aiding drivers in maximizing their earnings."
                },
        #project fhv
        "project_fhv":{"name" :''' <h3 style='text-align: center;'>FHV NYC 2023 🚕 | 🖥️ <em>  <a href="https://public.tableau.com/app/profile/karma.tabs/viz/FHV-NYC2023/FHV-NYC-Dashboard"> Tableau</a> | <a href="https://github.com/karma-gits/vin_decoder">Github</a></h3>''',
                "image" : "images/fulls/01.jpg",
                "caption" : "FHV NYC 2023",
                "info" : "- I used Python to scrape large amounts of data, which took 18 hours to complete. \n- The data from FHV was then analyzed and cleaned using SQL and Excel. \n- The ultimate goal was to visualize the insights gained from the data using Tableau, allowing for a deeper understanding and presentation of the findings."
                },
        #project Airbnb
        "project_airbnb":{"name" :''' <h3 style='text-align: center;'> AirBnB NYC 2022 🏠  |  🖥️ <em><a href="https://public.tableau.com/app/profile/karma.tabs/viz/Airbnb_Dashboard_16733188991360/Dashboard1">Tableau</a></em></h3>''',
                "image" : "images/fulls/02.jpg",
                "caption" : "AirBnB NYC 2022",
                "info" : "-   utilized SQL to extract and query the Airbnb data, and then worked with Excel to analyze and clean the datasets. \n- The ultimate goal was to leverage Tableau to create informative and interactive visualizations, providing insights into Airbnb trends and patterns"
                },
        # project vechicle
        "project_vechicle":{ "name" :''' <h3 style='text-align: center;'> All New EV Models - 2023 🔋  |  🖥️ <em><a href="https://public.tableau.com/views/NewElectricVehicleModelinU_S_for2023/Dashboard">Tableau</a> | <a href="https://github.com/karma-gits/webScrapeCar">Github</a></em></h3>''',
                "image" : "images/fulls/03.jpg",
                "caption" : "Every New EV Models - 2023",
                "info" : "- I scraped the data from the website using Python. \n- The scraped data was then used to create interactive and informative visualizations with Tableau. \n- The goal was to gain insights and understand trends and patterns from the scraped data.  "
                }
        }