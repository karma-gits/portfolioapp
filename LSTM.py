import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from sklearn.metrics import mean_absolute_error, mean_squared_error

def LSTM_model():
    def get_stock_data(ticker):
        try:
            security = yf.Ticker(ticker)
            data = security.history(period='2y', interval='1d')[['Open', 'High', 'Low', 'Close']]
            return data
        except Exception as e:
            st.error(f"Failed to fetch data: {str(e)}")
            return None

    def prepare_data(data):
        data.index = pd.to_datetime(data.index)
        data.index = data.index.date
        data = pd.DataFrame(data.values, index=pd.to_datetime(data.index), columns=data.columns)
        data = data.asfreq('B').fillna(method='ffill')
        return data

    def create_dataset(data, time_step=1):
        dataX, dataY = [], []
        for i in range(len(data) - time_step - 1):
            a = data[i:(i + time_step), 0]
            dataX.append(a)
            dataY.append(data[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def lstm_forecasting(data, time_step=20):
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

        # Create the dataset
        X, y = create_dataset(scaled_data, time_step)
        X = X.reshape(X.shape[0], X.shape[1], 1)

        # Split into training and testing sets
        train_size = int(len(X) * 0.8)
        X_train, y_train = X[:train_size], y[:train_size]
        X_test, y_test = X[train_size:], y[train_size:]

        # Build LSTM Model
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=50, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mean_squared_error')

        # Fit the model
        model.fit(X_train, y_train, epochs=50, batch_size=32) 
        model.fit(X_train, y_train, epochs=50, batch_size=32)  # Repeat the training process to avoid overfitting

        # Predict on training and testing data
        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)

        # Inverse transform the predictions
        train_predict = scaler.inverse_transform(train_predict)
        test_predict = scaler.inverse_transform(test_predict)

        # Prepare the forecast DataFrame with date index
        train_predict_index = data.index[time_step:time_step + len(train_predict)]
        test_predict_index = data.index[time_step + len(train_predict) + 1:time_step + len(train_predict) + 1 + len(test_predict)]

        forecast_df = pd.DataFrame({
            'Actual': data['Close'],
            'Train Prediction': pd.Series(train_predict.flatten(), index=train_predict_index),
            'Test Prediction': pd.Series(test_predict.flatten(), index=test_predict_index)
        })

        # Calculate metrics
        actual_close = data['Close'][train_predict_index.append(test_predict_index)]
        predictions = pd.Series(np.concatenate((train_predict.flatten(), test_predict.flatten())), index=actual_close.index)

        mae = mean_absolute_error(actual_close, predictions)
        mse = mean_squared_error(actual_close, predictions)
        rmse = np.sqrt(mse)

        metrics = {'MAE': mae, 'MSE': mse, 'RMSE': rmse}

        # Predict for the next n days
        predict_days = 20
        last_data = scaled_data[-time_step:]  # Get last `time_step` data
        future_predictions = []

        for _ in range(predict_days):  # Predict n future days
            x_input = last_data.reshape(1, time_step, 1)
            next_prediction = model.predict(x_input)  # Make a prediction
            future_predictions.append(next_prediction[0][0])  # Store the predicted value
            last_data = np.append(last_data, next_prediction)[1:]  # Update the input for the next prediction

        # Inverse transform future predictions
        future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

        # Create future dates
        last_date = data.index[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=predict_days, freq='B')  # Business days only
        future_df = pd.DataFrame(future_predictions, index=future_dates, columns=['Future Prediction'])

        #new
        # Calculate prediction intervals based on the model's accuracy on test data
        error = actual_close[test_predict_index] - predictions[test_predict_index]
        std_dev = np.std(error)  # Standard deviation of the errors
        margin_of_error = 1.96 * std_dev  # 1.96 for 95% confidence interval

        # Calculate upper and lower bounds for future predictions
        lower_bounds = future_predictions - margin_of_error
        upper_bounds = future_predictions + margin_of_error

        # Add bounds to the DataFrame
        future_df['Lower Bound'] = lower_bounds
        future_df['Upper Bound'] = upper_bounds

        return forecast_df, metrics, future_df

    #st.header(":bar_chart: Time Series Analysis with LSTM")
    ticker = st.text_input("Enter the ticker symbol of the stock you want to analyze").upper()

    if ticker:
        data = get_stock_data(ticker)

        if data is not None and not data.empty:
            data = prepare_data(data)
            st.subheader(f"{ticker} Stock Price Fetched for 2 years")
            st.dataframe(data,height=300)

            # Create a figure and axis using matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            # Plot the 'Close' prices
            sns.lineplot(data['Close'],ax=ax)
            # Set y-axis limit to start above zero, you can adjust the lower limit as needed
            y_min = data['Close'].min()  # Get the minimum value from the Close prices
            y_min_adjusted = y_min if y_min > 0 else 0  # Ensure it starts above zero if all are positive
            ax.set_ylim(bottom=y_min_adjusted*.95)  # Set the y-axis limit to the adjusted minimum value
            # Set labels and title if necessary
            ax.set_xlabel('Date')
            ax.set_ylabel('Price')
            ax.set_title(f'{ticker} Stock Price Over Time')
            # Use the matplotlib figure in Streamlit
            st.pyplot(fig,use_container_width=True)

            submmitted = st.button("Train and Predict",type="primary",use_container_width=True)
            if submmitted:
                st.subheader("LSTM Model Training and Prediction")
                with st.spinner("Training The Model... \n This may take a few minutes..."):

                    forecast_df,metrics, future_df = lstm_forecasting(data)
                    #st.dataframe(forecast_df)
                    # Display metrics
                    st.subheader("Evaluation Metrics")
                    st.write(metrics)
                    # Display future predictions
                    #st.subheader("Future Predictions for Next 20 Days")
                    #st.dataframe(future_df)
                    # Create a figure with two subplots
                    plt.figure(figsize=(10, 10))
                    # First subplot: Full predictions
                    plt.subplot(2, 1, 1)  # 2 rows, 1 column, first subplot
                    plt.plot(forecast_df['Actual'], label='Actual Data', color='orange')
                    plt.plot(forecast_df['Train Prediction'], label='Train Prediction', color='blue')
                    plt.plot(forecast_df['Test Prediction'], label='Test Prediction', color='green')
                    plt.plot(future_df['Future Prediction'], label='Future Prediction', color='red', linestyle='--')  # Future predictions
                    # the confidence intervals
                    #plt.fill_between(future_df.index, future_df['Lower Bound'], future_df['Upper Bound'], color='red', alpha=0.3, label='95% CI')
                    plt.title('Actual, Train, Test, and Future Predictions')
                    plt.xlabel('Date')
                    plt.ylabel('Stock Price')
                    plt.legend()
                    #plt.xlim(forecast_df['Train Prediction'].index[500], future_df.index[-1])
                    # Second subplot: Future predictions only
                    plt.subplot(2, 1, 2)  # 2 rows, 1 column, second subplot
                    plt.plot(future_df['Future Prediction'], label='Future Prediction', color='red', linestyle='--')  # Future predictions
                    #plt.fill_between(future_df.index, future_df['Lower Bound'], future_df['Upper Bound'], color='red', alpha=0.3, label='95% CI')
                    plt.title('Forecast For Next 20 Days')
                    plt.xlabel('Date')
                    plt.ylabel('Stock Price')
                    plt.legend()
                    # Adjust layout
                    plt.suptitle(f'{ticker} Stock LSTM Model Predictions', fontsize=16)
                    plt.tight_layout()
                    st.pyplot(plt)
        else:
            st.error("No data available for the entered ticker symbol.")
    else:
        st.info("Please enter a valid ticker symbol to get started.")
    
#if __name__ == "__main__":
#    main()