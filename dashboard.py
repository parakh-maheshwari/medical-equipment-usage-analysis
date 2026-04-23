import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Medical Equipment Dashboard", layout="centered")

st.title("🏥 Medical Equipment Usage Dashboard")

# Load data
df = pd.read_csv("medical_equipment_usage.csv")

# Cleaning
df['usage_start_time'] = df['usage_start_time'].astype(str).str.replace('.', ':', regex=False)
df['usage_end_time'] = df['usage_end_time'].astype(str).str.replace('.', ':', regex=False)

df['usage_start_time'] = pd.to_datetime(df['usage_start_time'], dayfirst=True)
df['usage_end_time'] = pd.to_datetime(df['usage_end_time'], dayfirst=True)

# Features
df['usage_duration'] = (df['usage_end_time'] - df['usage_start_time']).dt.total_seconds() / 3600
df['total_cost'] = df['usage_duration'] * df['cost_per_hour']
df['hour'] = df['usage_start_time'].dt.hour

# ------------------ FILTERS ------------------
st.sidebar.header("🔍 Filters")

equipment = st.sidebar.multiselect(
    "Equipment",
    df['equipment_name'].unique(),
    default=df['equipment_name'].unique()
)

department = st.sidebar.multiselect(
    "Department",
    df['department'].unique(),
    default=df['department'].unique()
)

shift = st.sidebar.multiselect(
    "Shift",
    df['shift'].unique(),
    default=df['shift'].unique()
)

filtered_df = df[
    (df['equipment_name'].isin(equipment)) &
    (df['department'].isin(department)) &
    (df['shift'].isin(shift))
]

# ------------------ KPIs ------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records", len(filtered_df))
col2.metric("Total Hours", round(filtered_df['usage_duration'].sum(), 1))
col3.metric("Avg Duration", round(filtered_df['usage_duration'].mean(), 1))
col4.metric("Total Cost", round(filtered_df['total_cost'].sum(), 0))

# ------------------ ROW 1 (GLOBAL VIEW) ------------------
st.subheader("📊 Overall Trends")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    sns.countplot(x='equipment_name', data=filtered_df, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    sns.countplot(x='department', data=filtered_df, ax=ax)
    st.pyplot(fig)

# ------------------ ROW 2 ------------------
col3, col4 = st.columns(2)

with col3:
    fig, ax = plt.subplots()
    sns.countplot(x='shift', data=filtered_df, ax=ax)
    st.pyplot(fig)

with col4:
    fig, ax = plt.subplots()
    sns.countplot(x='hour', data=filtered_df, ax=ax)
    st.pyplot(fig)

# ------------------ ROW 3 ------------------
st.subheader("💰 Cost Analysis")

col5, col6 = st.columns(2)

with col5:
    cost_data = filtered_df.groupby('equipment_name')['total_cost'].sum()
    fig, ax = plt.subplots()
    cost_data.plot(kind='bar', ax=ax)
    st.pyplot(fig)

with col6:
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['total_cost'], bins=20, ax=ax)
    st.pyplot(fig)

# ------------------ ROW 4 ------------------
st.subheader("⚙️ Operational Insights")

col7, col8 = st.columns(2)

with col7:
    fig, ax = plt.subplots()
    sns.countplot(x='maintenance_required', hue='breakdown', data=filtered_df, ax=ax)
    st.pyplot(fig)

with col8:
    top_eq = filtered_df.groupby('equipment_name')['usage_duration'].sum().sort_values(ascending=False)
    st.write("Top Equipment by Usage")
    st.dataframe(top_eq)