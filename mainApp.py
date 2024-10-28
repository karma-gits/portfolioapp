import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from project_house import housePrice
from project_movie import recommend
from project_stock import stockPrice
from tableau import tableau
from LSTM import LSTM_model

st.set_page_config(page_title="Karma - Portfolio🕵️🔍📊", page_icon="images/profile-pic.png", layout="centered")
with open('styles/main.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title container
with st.container():
    col1, col2 = st.columns([1,3])
    with col1:
        st.image('images/profile-pic.png',width=180)
    with col2:
        st.markdown("<h1 style='font-size:60px;font-weight:bold;'>Karma Gurung</h1>",unsafe_allow_html=True)
        st.write('___')
        st.write('Data Science | Data Scientist | Statistical Analysis | Machine Learning | Data Mining/Wrangling | SQL | Python')
    ## address social media
    st.markdown(f"New York City, NY 11378 | karmaguru.work@gmail.com | [linkedin](https://linkedin.com/in/karmag) | [github](https://github.com/karma-gits) | [StockMarketLab-App](https://stockmarketlab.streamlit.app)")

# menu options
with st.container():
    selected = option_menu(
        menu_title=None,
        options=["Projects","Tableau","AboutMe","Contact","LSTM"],
        icons=["archive","window-fullscreen","file-person","person-lines-fill","diagram-2-fill"],
        orientation="horizontal")
#st.write("___")
# About Me
if selected == "AboutMe":
    # Create a button to download the resume
    with open("images/KarmaGurung.pdf", "rb") as file:
        btn = st.download_button(
                label="Download Resume",
                data=file,
                file_name="Karma Gurung Resume.pdf",
                mime="application/pdf")
        
    with st.container():
        ###
        st.success("""
            Recent Master's degree graduate in Data Analytics with a strong foundation in computer science and data science. 
            Proficient in statistical modeling, machine learning, and data manipulation, with hands-on experience in Python 
            and Scikit-Learn for building predictive models and deriving insights from complex datasets. 
            Excellent communicator, capable of conveying technical concepts to both technical and non-technical audiences. 
            Dedicated to leveraging data-driven solutions to drive business growth and facilitate informed decision-making.
            """)

        with st.container():
            st.subheader("Technical Skills")
            st.write("**LANGUAGES:** Utilize Python (Pandas, NumPy, Seaborn) and SQL effectively")
            st.write("**ANALYTICS/DATA VISUALIZATION:** Proficient in Microsoft Excel, Tableau, Matplotlib, and Plotly")
            st.write("**DATA TECHNIQUES:**  Implement Sklearn,TensorFlow, Statistical Modeling, Machine Learning Algorithms, Data Cleaning, Data Manipulation, Hypothesis Testing, A/B Testing, Statistical Analysis, Big Data (Hadoop and Spark)")
            st.write('___')

            st.subheader("Experience")
            st.write("**Data Science Fellow | Feb/2024 - Jul/2024**")
            st.write("**Springboard | Remote**")

            st.write(f" **[● Built a Safety Gear Detection application](https://github.com/karma-gits/springboard/tree/main/Capstone%20Three)**")
            st.write("""
                     - Engineered an AI-driven solution leveraging Python, OpenCV, TensorFlow, and YOLO to monitor construction site safety gear,  enhanced compliance by 30% and minimized inspection time by 40 hours monthly.
                     - Enhanced safety protocols and reduced risk of accidents by 80% through accurate detection and timely notification.""")

            st.write(f" **[● Constructed a Product Recommendation System](https://github.com/karma-gits/springboard/tree/main/capstone%20two)**")
            st.write("""
                     - Developed a product recommendation system using Python, Pandas, Sklearn, and Matplotlib. Analyzed user interactions and historical purchases to train machine learning models, resulting in a 20% improvement in recommendation accuracy.
                     - Enhanced user experience and engagement by 25% through a complete redesign of the app interface. Incorporated user feedback and industry best practices, leading to increased user satisfaction and interaction rates.""")

            st.write(f" **[● Developed Dynamic Pricing Strategy Model](https://github.com/karma-gits/DataScienceGuidedCapstone)**")
            st.write("""
                    -  Created a dynamic pricing strategy model using Python, Pandas, and Sklearn. Conducted competitor analysis and applied data-driven techniques to optimize pricing, aiming for a 5% revenue increase.
                    """)
            
            # StockMarketLab-Awebappforstockmarketanalysisanddecision-making
            st.subheader("Personal Project")
            st.write(f" **[Stock Market Lab - a web app for stock market analysis and decision-making](https://stockmarketlab.streamlit.app)**")
            st.write("""
                    - **Portfolio:** Track holdings, allocation, and performance. 
                    - **News Sentiment Analyzer:** Parse  news articles and analyze sentiment.
                    - **MonteCarlo:** Run Monte Carlo simulations to estimate the value of a stock.
                    - **DCF Model:** Calculate the DCF(Discounted Cash Flow) of a stock.
                    """)
            
            st.write('___')
            # Education
            st.subheader("Education")
            st.write("**MS, Data Analytics**, Western Governors University, Oct 2024")
            st.write("**BS, Computer Science**, Western Governors University, Dec 2023")
            st.write('___')
            # Certifications
            st.subheader("Certifications")
            st.write("**Data Science Certification** - Springboard - Jun 2024")
            st.write("**ITIL Foundation** - PeopleCert - Nov 2023")
            st.write("**Linux Essentials** - LPI - Oct 2023")
            st.write("**Python For Everybody** - University of Michigan - Dec 2022")
            st.write("**Google Data Analytics** - Google Career Certificates - Dec 2022")
            
    st.write('___')

# Projects
if selected == "Projects":
    st.subheader("Three End-to-End Machine Learning Projects")
    selected = st.selectbox("Select a Project",options=["1. Movie Recommendation","2. Stock Prediction (SamllCap Gap-up Strategy) ","3. NYC Housing Price Prediction"],placeholder="Select a ML App project")
    with st.container(border=True):
        if selected == "1. Movie Recommendation":
            st.subheader(":red[1.:movie_camera: Movie Recommendation System :popcorn:] | [Github](https://github.com/karma-gits/portfolioApp)", divider="red")
            st.image('images/movie.png',use_column_width=True)
            st.error("- I cleaned the dataset from kaggle and used the IMDB API to get the movie posters and ratings \n- Then I used sklearn cosine similarity to find the most similar movies to the user's movie.\n- The system takes in a user's movie title and recommends movies that the user might enjoy based on their selected movie.")
            st.subheader(":gray[ 🎞️ 📋 Enter Movie Title to Get Recommendations]",divider="red")
            recommend()
        elif selected == "2. Stock Prediction (SamllCap Gap-up Strategy) ":
            st.subheader(":green[2.:chart_with_upwards_trend: Stock Prediction App 📉] | [Github](https://github.com/karma-gits/portfolioApp)",divider="green")
            st.image('images/stock.png',use_column_width=True)
            st.success("- I developed a machine learning model using Scikit-learn to predict smallcap stock prices and directions.\n- The model was trained on historical data and uses algorithms like Linear Regression, Random Forest Regressor and classification.\n- The outcome shows the potential of machine learning in predicting stock prices and can be applied to day trading strategies called 'Gapup Short', providing valuable insights for smallcap day traders.")
            st.subheader(":gray[ 📈📋 Enter pre-market data to predict]",divider="green")
            stockPrice()
        elif selected == "3. NYC Housing Price Prediction":
            st.subheader(":blue[3.:house: NYC Housing Price Prediction 🏘️] | [Github](https://github.com/karma-gits/portfolioApp)",divider="blue")
            st.image('images/house.png',use_column_width=True)
            st.info("- I used the housing data from kaggle to predict the price of a house in New York City. \n- I used sklearn to train a linear regression model and then used the model to predict the price of a house.")
            st.subheader(":gray[ 🏠 📋 Enter House data to predict]",divider="blue")
            housePrice()    

# LSTM
if selected == "LSTM":
    st.header(":bar_chart: :blue[Deep Learning Project [Demo/Testing]] \n #### :chart_with_upwards_trend: :orange[Testing and still under construction] :chart_with_downwards_trend:",divider='rainbow')
    LSTM_model()         
    
# tableau
if selected == "Tableau":
    st.header(":blue[Tableau Projects] :open_file_folder:",divider='blue')
    tableau()

# Contact
if selected == "Contact":
    st.header(":mailbox: Get In Touch!")
    st.write('___')
    
    github_text = """<a href="https://github.com/karma-gits" style="display: inline-block; text-align: center; vertical-align: middle;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="4em" height="4em" viewBox="0 0 16 16">
                        <path fill="#365E32" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59c.4.07.55-.17.55-.38c0-.19-.01-.82-.01-1.49c-2.01.37-2.53-.49-2.69-.94c-.09-.23-.48-.94-.82-1.13c-.28-.15-.68-.52-.01-.53c.63-.01 1.08.58 1.23.82c.72 1.21 1.87.87 2.33.66c.07-.52.28-.87.51-1.07c-1.78-.2-3.64-.89-3.64-3.95c0-.87.31-1.59.82-2.15c-.08-.2-.36-1.02.08-2.12c0 0 .67-.21 2.2.82c.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82c.44 1.1.16 1.92.08 2.12c.51.56.82 1.27.82 2.15c0 3.07-1.87 3.75-3.65 3.95c.29.25.54.73.54 1.48c0 1.07-.01 1.93-.01 2.2c0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8" />
                        </svg>
                        </a>"""
    linkedin_text = """<a href="https://www.linkedin.com/in/karmag/" style="display: inline-block; text-align: center; vertical-align: middle;">
                       <svg xmlns="http://www.w3.org/2000/svg" width="4em" height="4em" viewBox="0 0 16 16">
                        <path fill="#365E32" d="M0 1.146C0 .513.526 0 1.175 0h13.65C15.474 0 16 .513 16 1.146v13.708c0 .633-.526 1.146-1.175 1.146H1.175C.526 16 0 15.487 0 14.854zm4.943 12.248V6.169H2.542v7.225zm-1.2-8.212c.837 0 1.358-.554 1.358-1.248c-.015-.709-.52-1.248-1.342-1.248S2.4 3.226 2.4 3.934c0 .694.521 1.248 1.327 1.248zm4.908 8.212V9.359c0-.216.016-.432.08-.586c.173-.431.568-.878 1.232-.878c.869 0 1.216.662 1.216 1.634v3.865h2.401V9.25c0-2.22-1.184-3.252-2.764-3.252c-1.274 0-1.845.7-2.165 1.193v.025h-.016l.016-.025V6.169h-2.4c.03.678 0 7.225 0 7.225z" />
                        </svg> </a>"""
    email_text = """<a href="mailto:karmaguru.work@gmail.com" style="display: inline-block; text-align: center; vertical-align: middle;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="4em" height="4em" viewBox="0 0 16 16">
                        <path fill="#365E32" d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0M4 4h8c.143 0 .281.031.409.088L8 9.231L3.591 4.088A.982.982 0 0 1 4 4m-1 7V5l.002-.063l2.932 3.421l-2.9 2.9A.967.967 0 0 1 3 11m9 1H4c-.088 0-.175-.012-.258-.034L6.588 9.12l1.413 1.648L9.414 9.12l2.846 2.846a.967.967 0 0 1-.258.034zm1-1c0 .088-.012.175-.034.258l-2.9-2.9l2.932-3.421L13 5z" />
                        </svg> </a>"""
                                
    
    with st.container():
        st.markdown(github_text + "\t.\t" + linkedin_text + "\t.\t" + email_text,unsafe_allow_html=True)
        
    st.header("#")
    st.write('___')
    
    st.subheader(":postbox: Contact me...",divider='gray')
    with st.container():
        contact_form = """
        <form action="https://formsubmit.co/karmaguru.work@gmail.com" method="POST">
        <input type="text" name="name" placeholder="Your Name" required>
        <input type="email" name="email"  placeholder="Your Email" required>
        <input type="social" name="linkedin" placeholder="Your LinkedIn" optional>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
        </form>
        """
        st.markdown(contact_form, unsafe_allow_html=True)

    
    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    local_css("styles/contact.css")
