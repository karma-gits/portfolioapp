import pickle
import streamlit as st
import requests
import gdown

## Movie Recommendation System
def recommend():
    @st.cache_data()  # cache data for 24 hours
    def load_similarity():
        url = 'https://drive.google.com/file/d/1wwTfZEi3_JWugz_517GFxO1FNNoMvyU4/view?usp=drive_link'
        output = 'similarity.pkl'
        return gdown.download(url, output, quiet=False, fuzzy=True)
    
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
        st.header(f":red[You Selected -\t{title}]", divider="red")
        col1, col2 = st.columns([1/4,3/4])
        with col1:
            st.image(poster_path,use_container_width=True)
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
                st.image(recommended_movie_posters[i],use_container_width=True)
    
    # Webpage 
    movies = pickle.load(open('Recommendation/movie_list.pkl','rb'))
    #similarity = pickle.load(open('similarity.pkl','rb'))
    similarity = pickle.load(open(load_similarity(),'rb'))

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
