import pickle
import streamlit as st
import pandas as pd
import gdown

# Stock Price Prediction
def stockPrice(): 
    # load the model
    @st.cache_data(ttl=86400)  
    def load_model_open_push():
        return gdown.download('https://drive.google.com/file/d/1dPjOLBWbObLbbteTWMXgZIHRhvh4W51P/view?usp=sharing', 'modelOpenPush.pkl', quiet=False, fuzzy=True)

    @st.cache_data(ttl=86400)  
    def load_model_hod_drop():
        return gdown.download('https://drive.google.com/file/d/1SnzI6e08oaeYAdKmQy7HoTtBRwl8VA0O/view?usp=sharing', 'modelHodDrop.pkl', quiet=False, fuzzy=True)

    @st.cache_data(ttl=86400)  
    def load_model_eod_volume():
        return gdown.download('https://drive.google.com/file/d/1VwvaznLuTofoQgindflTuRviKv8SeAyN/view?usp=sharing', 'modelEodVolume.pkl', quiet=False, fuzzy=True)

    @st.cache_data(ttl=86400)  
    def load_model_closed_red():
        return gdown.download('https://drive.google.com/file/d/1QXqhMei10ld337tJCutSVsOEMIPQeUF-/view?usp=sharing', 'modelClosedRed.pkl', quiet=False, fuzzy=True)
  
    # Create a dropdown menu to select the stock
    allColumns = ['open', 'gap', 'hod', 'low', 'close', 'eodVolume', 'pmVolume', 'floatShares', 'marketCap', 'openPush', 'hodToClose', 'closedRed']
    X = ['open', 'gap', 'pmVolume', 'floatShares', 'marketCap']
    
    def user_options():
        col1, col2 = st.columns([1,1])
        with col1:
            marketCap = st.number_input("Enter Market Cap in Millions", 1.00, 10000.00, 35.00)
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
    #user df
    finaldf = user_options()
    
    modelOpenPush = pickle.load(open(load_model_open_push(),'rb'))
    modelHodDrop = pickle.load(open(load_model_hod_drop(),'rb'))
    modelEodVolume = pickle.load(open(load_model_eod_volume(),'rb'))
    modelClosedRed = pickle.load(open(load_model_closed_red(),'rb'))
    
    ## Prediction
    try:
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
        st.header(":green[:chart_with_upwards_trend: Prediction :chart_with_downwards_trend:]",divider="green")

        with st.container():
            #st.dataframe(finaldf)
            if predicted_openpush >0:
                st.text(f"Open Push : around HOD ${float(priceHod):.2f} ({float(predicted_openpush[0]):.2f}%)")
                #st.text(f"Close Around : ${float(priceClose):.2f}")
                st.text(f"HOD to Close : close around  ${float(priceClose):.2f} ({float(predicted_hodtoclose[0]):.2f}%)")
            else:
                st.subheader(":red[Open Push : **Most Likely No Push**] :chart_with_downwards_trend:")

            st.warning(f"Closed Red : {predicted_closedred[0]}")
            st.warning(f"EOD Volume : {int(predicted_eodvolume[0]/1000000):,.2f}M")


            st.subheader("Predcted Price Pattern")
            st.line_chart(pricePattern,y='price', use_container_width= True)
    except:
        st.error("Invalid Input")
    st.markdown('---')