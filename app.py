import streamlit as st
import pandas as pd
import plotly.express as px
from forecasting.predictor import SalesPredictor
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt

st.set_page_config(page_title="📈 Enterprise Sales Forecasting", layout="wide")

st.title("📊 Enterprise Sales Forecasting Dashboard")
st.write("Forecast future sales with advanced models, KPIs, scenarios, and interactive analytics")

# Sidebar controls
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload your sales CSV", type=["csv"])
model_choice = st.sidebar.selectbox("Choose forecasting model", ["Linear Regression", "Prophet (advanced)", "ARIMA (advanced)"])
horizon = st.sidebar.slider("Forecast horizon (days)", 1, 180, 30)
scenario_factor = st.sidebar.slider("Promotion impact (%)", -20, 50, 0)

# Load data
if uploaded_file:
    data = pd.read_csv(uploaded_file, parse_dates=["date"])
else:
    data = pd.read_csv("data/sales.csv", parse_dates=["date"])

# KPIs
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Average Sales", f"{data['sales'].mean():.2f}")
col2.metric("Max Sales", f"{data['sales'].max():.2f}")
col3.metric("Min Sales", f"{data['sales'].min():.2f}")
growth_rate = ((data['sales'].iloc[-1] - data['sales'].iloc[0]) / data['sales'].iloc[0]) * 100
col4.metric("Growth Rate", f"{growth_rate:.2f}%")

# Forecasting
predictor = SalesPredictor()
date_input = st.date_input("Select a forecast start date")
if date_input:
    future_dates = pd.date_range(start=date_input, periods=horizon)

    # y = forecast values
    y = [predictor.forecast(str(d.date())) for d in future_dates]

    # Z = adjusted forecast values
    forecast_df = pd.DataFrame({"date": future_dates, "y": y})
    forecast_df["Z"] = forecast_df["y"] * (1 + scenario_factor/100)

    # 📈 Forecast Overview
    st.header("📈 Forecast Overview")
    # Rename sales column to 'y' so chart uses y="y"
    data = data.rename(columns={"sales": "y"})
    fig = px.line(data, x="date", y="y", title="Sales Forecasting")
    fig.add_scatter(x=future_dates, y=forecast_df["y"], mode="lines+markers", name="Forecast (y)")
    st.plotly_chart(fig, use_container_width=True,
                    config={"displaylogo": False, "modeBarButtonsToRemove": ["toImage", "resetScale2d"]})

    # 🔍 Trend Analysis
    st.header("🔍 Trend Analysis")
    try:
        data = data.set_index("date")
        result = seasonal_decompose(data["y"], model="additive", period=30)

        fig_trend, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12,8), sharex=True)
        result.observed.plot(ax=ax1, title="Observed")
        result.trend.plot(ax=ax2, title="Trend")
        result.seasonal.plot(ax=ax3, title="Seasonality")
        result.resid.plot(ax=ax4, title="Residuals")
        st.pyplot(fig_trend)
    except Exception as e:
        st.warning("Trend analysis requires enough data points. Please upload a longer dataset.")

    # 📊 Scenario Analysis
    st.header("📊 Scenario Analysis")
    fig2 = px.line(forecast_df, x="date", y="Z", title="Scenario Forecast (Z with promotion impact)")
    st.plotly_chart(fig2, use_container_width=True,
                    config={"displaylogo": False, "modeBarButtonsToRemove": ["toImage", "resetScale2d"]})

    # ⚖️ Model Comparison
    st.header("⚖️ Model Comparison")
    st.write("Model comparison with accuracy metrics (MAPE, RMSE) will be added here.")
