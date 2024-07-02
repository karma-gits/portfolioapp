import pickle
import streamlit as st
import requests
import pandas as pd

## Movie Recommendation System
def recommend():
    # Fetch selected movie datas
    def movie_data(movie):
        movie_id = movies[movies['title'] == movie].movie_id.values[0]
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f155b8d67d9c5853348a9f37105ba012&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path =  ("https://image.tmdb.org/t/p/w500/" + data['poster_path'])
        movie_overview = data['overview']
        release_date = data['release_date']
        vote_average = data['vote_average']
        genreslist = data['genres']
        genres = ', '.join([genre['name'] for genre in genreslist])
        
        return poster_path,movie_overview, release_date,vote_average,genres

    # Fetch only posters path
    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=f155b8d67d9c5853348a9f37105ba012&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        return ("https://image.tmdb.org/t/p/w500/" + poster_path)
        
    def recommend(movie,num):
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:num+1]:
            # fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names,recommended_movie_posters

    # Query movie   
    def query_movie(title):
        
        #selected movie infos
        poster_path,movie_overview, release_date,vote_average,genres = movie_data(title)
        ## Display info of selected Movie
        st.header(f":red[You {title}]", divider="red")
        col1, col2 = st.columns([1/4,3/4])
        with col1:
            st.image(poster_path,use_column_width=True)
        with col2:
            st.write("**Title** :",title)
            st.write("**Overview** : ",movie_overview)
            st.write("**Genres** : ",genres)
            st.write("**Ratings** :",round(vote_average,1))
            st.write('**Release date** :',release_date)
            
        st.header(f':red[Your Top {num_recommendations} Recommendations:]', divider="red")
        recommended_movie_names, recommended_movie_posters = recommend(title,num_recommendations)
        num_columns = min(len(recommended_movie_names), 8)
        cols = st.columns(num_columns)
        
        #display movie recommendations
        for i in range(num_columns):
            with cols[i]:
                st.write(recommended_movie_names[i])
                st.image(recommended_movie_posters[i],use_column_width=True)
    
    # Webpage 
    movies = pickle.load(open('Recommendation/movie_list.pkl','rb'))
    similarity = pickle.load(open('Recommendation/similarity.pkl','rb'))

#    # Movie list
    movie_list = movies['title'].values    
    selected_movie = st.selectbox("Select/Type a Movie Title",movie_list)
    num_recommendations = st.slider('No. of Recommendations', 1, 8, 4)
    
    with st.container():
        # Display recommendation
            try:
                query_movie(selected_movie) 
            except:
                st.error("No Recommendation Found. Please select a different movie.")

 
    st.write('___')

## House Price Prediction
def housePrice():
    

    ##style 
    #st.markdown("<h1 style='text-align: center; font-size: 50px;'>NYC House Price Prediction</h1>", unsafe_allow_html=True)

    # load the model
    priceModel = pickle.load(open('housePrice\priceModel.pkl','rb'))

    # Create a dropdown menu to select the neighbourhood

    neighbourhoods = ['Astoria','Battery Park', 'Baychester', 'Bedford Stuyvesant', 'Briarwood',
           'Brooklyn Heights', 'Canarsie', 'Carnegie Hill', 'Flushing',
           'Forest Hills', 'Gravesend', 'Heartland Village', 'Hollis',
           'Jackson Heights', 'Jamaica Estates', 'Middle Village', 'Midtown',
           'Mill Basin', 'Oakland Gardens', 'Park Slope', 'Rego Park',
           'Richmond Hill', 'Riverdale', 'Rosebank', 'Spuyten Duyvil', 'Stapleton',
           'Turtle Bay', 'Upper East Side', 'Williamsbridge', 'Windsor Terrace']
    airconditions =['Cooling only', 'Heating & Cooling', 'Heating only', 'No']


    def user_options():
        neighbourhood_select = st.selectbox("Select a Neighbourhood", neighbourhoods)
        year_build = st.slider("Select Built Year", 1844, 2022, 1960)
        
        col1,col2 = st.columns([1,1])
        with col1:
            beds = st.number_input("Select Bedrooms", 0, 7, 2)
            baths = st.number_input("Select Bathrooms", 1, 6, 1)
            
        with col2:
            airCondition_select = st.selectbox("Select a Heating/Cooling Options", airconditions)
            area = st.text_input("Enter Area (Sqft)", value="1200")


        neighbourhoods_mask = [1 if neighbourhood == neighbourhood_select else 0 for neighbourhood in neighbourhoods]
        neighbourhood_df = pd.DataFrame([neighbourhoods_mask], columns=neighbourhoods)

        ac_mask = [1 if aircondition == airCondition_select else 0 for aircondition in airconditions]
        ac_df = pd.DataFrame([ac_mask],columns=airconditions )

        user_data = {
            'Year Built' : year_build,
            'Beds': beds,
            'Baths': baths,
            'Area': area
        }
        df1 = pd.DataFrame(user_data, index=[0])
        final_data =pd.concat([df1,neighbourhood_df,ac_df],axis=1).reset_index(drop=True)
        tag = f"Build in {year_build} | {neighbourhood_select} | {area}sqft | {beds}Bedroom | {baths}Bathroom"
        return final_data,tag

    user_data,tag = user_options()

    predicted_price = priceModel.predict(user_data)
    st.header(":blue[:moneybag: Predicted Price]",divider='blue')
    if predicted_price >0:
        st.subheader(tag)
        st.info(f"${int(predicted_price[0]):,}")
    else:
        st.error(tag, icon="🚨")
        st.error(f"${int(predicted_price[0]):,}")
        st.error("Invalid input. Please Try Again...")
    st.markdown('---')


# Stock Price Prediction
def stockPrice():
    #st.header(":green[:chart_with_upwards_trend: Stock Prediction :chart_with_upwards_trend:]",divider="green")
    
    # load the model
    modelOpenPush = pickle.load(open('Stocks\modelOpenPush.pkl','rb'))
    modelHodDrop = pickle.load(open('Stocks\modelHodDrop.pkl','rb'))
    modelEodVolume = pickle.load(open('Stocks\modelEodVolume.pkl','rb'))
    modelClosedRed = pickle.load(open('Stocks\modelClosedRed.pkl','rb'))
    
  
    # Create a dropdown menu to select the stock
    allColumns = ['open', 'gap', 'hod', 'low', 'close', 'eodVolume', 'pmVolume', 'floatShares', 'marketCap', 'openPush', 'hodToClose', 'closedRed']
    X = ['open', 'gap', 'pmVolume', 'floatShares', 'marketCap']
    
    def user_options():
        col1, col2 = st.columns([1,1])
        with col1:
            marketCap = st.number_input("Enter Market Cap in Millions", 0.00, 10000.00, 35.00)
            floatShares = st.number_input("Enter Float Shares in Millions", 0.00, 1000.0, 10.0)
        with col2:
            openPrice = st.number_input("Enter Open Price", 1.0, 25.00, 3.50)
            gap = st.number_input("Enter Gap", 15.00, 100.00, 42.28)
            volume = st.number_input("Enter Volume", 200000, 10000000, 2154000)
        
            
        user_data = {
            'open' : openPrice,
            'gap': gap,
            'pmVolume': volume,
            'floatShares': floatShares*1000000,
            'marketCap': marketCap*1000000
        }
        return pd.DataFrame(user_data, index=[0])
    finaldf = user_options()
    
    ## Prediction
    
    predicted_openpush = modelOpenPush.predict(finaldf)
    predicted_hodtoclose = modelHodDrop.predict(finaldf)       
    predicted_eodvolume = modelEodVolume.predict(finaldf)
    predicted_closedred =  modelClosedRed.predict(finaldf)
    predicted_closedred = ['Yes' if predicted_closedred[0] == 1 else 'No' ]
    
    priceOpen = finaldf.open
    priceHod = priceOpen*(1+predicted_openpush[0]/100)
    priceClose = priceHod*(1-abs(predicted_hodtoclose[0]/100))
    pricePattern = pd.DataFrame({
            'index': [0,1,2],
            'price': [float(priceOpen),float(priceHod),float(priceClose)]
        })    
    
    ## Display
    st.header(":green[:chart_with_upwards_trend: Prediction :chart_with_upwards_trend:]",divider="green")
    
    with st.container():
        #st.dataframe(finaldf)
        col1, col2 = st.columns([1,1])
        with col1:
            st.text(f"Open Push : {float(predicted_openpush[0]):.2f}%")
            st.text(f"Hod to Close : {float(predicted_hodtoclose[0]):.2f}%")
            st.text(f"Eod Volume : {int(predicted_eodvolume[0]):,}")
            st.text(f"Closed Red : {predicted_closedred[0]}")
        with col2:
            st.text(f"Hod Around : ${float(priceHod):.2f}")
            st.text(f"Close Around : ${float(priceClose):.2f}")
    

        st.subheader("Predcted Price Pattern")
        st.line_chart(pricePattern,y='price', use_container_width= True)
    
    st.markdown('---')
    
# CV Resume
def resume():
    
    st.header("Technical Skills")
    st.write("**LANGUAGES:** Utilize Python (Pandas, NumPy, Seaborn) and SQL effectively")
    st.write("**ANALYTICS/DATA VISUALIZATION:** Proficient in Microsoft Excel, Tableau, Matplotlib, and Plotly")
    st.write("**DATA TECHNIQUES:** Apply Sklearn (sklearn), TensorFlow, Statistical Modeling, Machine Learning Algorithms,Data Cleaning, Data Manipulation, and Hypothesis Testing")
    st.write('___')
    
    st.header("Experience")
    st.subheader("**Data Science Fellow | March/2024 – Present**")
    st.subheader("**Springboard | Remote**")

    st.subheader(f" [● Built a Safety Gear Detection application](https://github.com/karma-gits/springboard/tree/main/Capstone%20Three)")
    st.write("""
             - Utilized Python, OpenCV, TensorFlow, and YOLO to develop a system that detects and tracks various types of safety gear in construction sites with high accuracy.
             - Enhanced safety protocols and reduced risk of accidents by 80% through accurate detection and timely notification.""")
    
    st.subheader(f" [● Constructed a Product Recommendation System](https://github.com/karma-gits/springboard/tree/main/capstone%20two)") 
    st.write("""
             -  Used Python, Pandas, Sklearn, and Matplotlib to devise a system that recommends relevant items based on user interactions and historical purchase data.
             - Enhanced user experience and engagement.""")

    st.subheader(f" [● Developed Dynamic Pricing Strategy Model](https://github.com/karma-gits/DataScienceGuidedCapstone)")
    st.write("""
            -  Created a model using data-driven techniques in Python, Pandas, and Sklearn to optimize pricing based on competitor analysis.
            -  Aimed for a +5% revenue increase.""")

    st.write('___')
    
    # Education
    st.header("Education")
    st.write("**Data Science Certification**, Springboard, Jun2024")
    st.write("**BS, Computer Science**, Western Governors University, Dec 2023")

    st.header("Certifications")
    st.write("**ITIL Foundation** - PeopleCert - Nov 2023")
    st.write("**Linux Essentials** - LPI - Oct 2023")
    st.write("**Python For Everybody** - University of Michigan - Dec 2022")
    st.write("**Google Data Analytics** - Google Career Certificates - Dec 2022")