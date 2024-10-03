import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Helper functions for data manipulation and visualization
def rentals_in_date_range(df, start_date, end_date):
    """Calculate total rentals within the user-defined date range."""
    filtered_df = df[(df['dteday_x'] >= start_date) & (df['dteday_x'] <= end_date)]
    return filtered_df.groupby('dteday_x')['cnt_x'].sum().reset_index()

def rentals_workday_vs_holiday(df):
    """Compare rentals between workdays and holidays."""
    return df.groupby('workingday_x')['cnt_x'].sum().reset_index()

def seasonal_rentals_by_user_type(df):
    """Compare seasonal rentals by user type (Casual vs Registered)."""
    total_casual_users = df.groupby('season_x')['casual_x'].sum().reset_index(name='Casual Users')
    total_registered_users = df.groupby('season_x')['registered_x'].sum().reset_index(name='Registered Users')
    total_rentals = pd.merge(total_casual_users, total_registered_users, on='season_x')
    total_rentals['Casual Users'] /= 10
    total_rentals['Registered Users'] /= 10

    return total_rentals
    

# Load dataset and convert date column
all_df = pd.read_csv("https://raw.githubusercontent.com/naufalkiky/submision_dicoding/refs/heads/main/dashboard/all_data.csv")
all_df["dteday_x"] = pd.to_datetime(all_df["dteday_x"])

# Sidebar for date range selection and logo
with st.sidebar:
    st.title("Rizky Achmad Naufal")
    st.image("https://raw.githubusercontent.com/naufalkiky/submision_dicoding/refs/heads/main/dashboard/streamlit-seeklogo.svg")

    min_date = all_df["dteday_x"].min()
    max_date = all_df["dteday_x"].max()
    
    # Date range input
    start_date, end_date = st.date_input(
        'Rentang Waktu', min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
# Filter data based on selected date range
filtered_df = all_df[(all_df['dteday_x'] >= pd.to_datetime(start_date)) & (all_df['dteday_x'] <= pd.to_datetime(end_date))]

st.header('Bike Sharing Dashboard :sparkles:')

# penyewaan sepeda per Date Range (Line Chart)
st.subheader('Total Rentals in Selected Date Range')
rentals_per_day = rentals_in_date_range(all_df, start_date, end_date)

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x='dteday_x', y='cnt_x', data=rentals_per_day, ax=ax)
plt.title("Total Rentals Over Time", fontsize=15)
plt.xlabel("Date")
plt.ylabel("Number of Rentals")
plt.xticks(rotation=45)
st.pyplot(fig)

# penyewaan sepeda di Workdays vs Holidays (Box Plot)
st.subheader('Comparison of Rentals on Working Days vs Holidays')
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x='workingday_x', y='cnt_x', data=filtered_df, palette='pastel')
plt.title("Rentals on Working Days vs Holidays", fontsize=15)
plt.xlabel("Holiday, Working Day")
plt.ylabel("Number of Rentals")
st.pyplot(fig)

# Penyewaan sepeda permusim berdasarkan tipe user (Bar Plot)
st.subheader('Seasonal Rentals by User Type')
user_type = seasonal_rentals_by_user_type(filtered_df)

fig, ax = plt.subplots(figsize=(10, 5))
user_type_melted = pd.melt(user_type, id_vars=['season_x'], value_vars=['Casual Users', 'Registered Users'])

sns.barplot(x='season_x', y='value', hue='variable', data=user_type_melted, ax=ax)
plt.title("Rentals per Season by User Type", fontsize=15)
plt.ylabel("Number of Rentals")
plt.xlabel("Season")
st.pyplot(fig)

