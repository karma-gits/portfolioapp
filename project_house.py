import pickle
import streamlit as st
import pandas as pd


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