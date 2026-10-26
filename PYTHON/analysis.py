# ======================================================
# EV CHARGING STATION ANALYTICS
# Exploratory Data Analysis
# ======================================================

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ======================================================
# PROJECT PATHS
# ======================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_DIR / "DATA" / "ev_charging_data.csv"

PLOTS_DIR = PROJECT_DIR / "plots"
PLOTS_DIR.mkdir(parents=True, exist_ok=True)

# ======================================================
# LOAD DATASET
# ======================================================

print("=" * 60)
print("EV CHARGING STATION ANALYTICS")
print("=" * 60)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Run generate_dataset.py first."
    )

df = pd.read_csv(DATA_FILE)

# Convert date columns to datetime.
df["Start_Time"] = pd.to_datetime(
    df["Start_Time"], errors="coerce"
)

df["End_Time"] = pd.to_datetime(
    df["End_Time"], errors="coerce"
)

# ======================================================
# DATASET OVERVIEW
# ======================================================

print("\n========== DATA PREVIEW ==========")
print(df.head())

print("\n========== DATA SHAPE ==========")
print(df.shape)

print("\n========== DATA INFORMATION ==========")
df.info()

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe(include="all").T)

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# ======================================================
# DATA QUALITY CHECKS
# ======================================================

print("\n========== MISSING VALUES ==========")
missing_values = df.isnull().sum()
print(missing_values)

print("\n========== DUPLICATE ROWS ==========")
print(df.duplicated().sum())

print("\n========== DUPLICATE SESSION IDS ==========")
print(df["Session_ID"].duplicated().sum())

print("\n========== INVALID BATTERY PERCENTAGES ==========")

invalid_battery = (
    ~df["Battery_%_Before"].between(0, 100)
    | ~df["Battery_%_After"].between(0, 100)
    | (
        df["Battery_%_After"]
        <= df["Battery_%_Before"]
    )
)

print("Invalid battery records:", invalid_battery.sum())

print("\n========== INVALID ENERGY VALUES ==========")

print(
    "Zero or negative energy records:",
    (df["Energy_Consumed_kWh"] <= 0).sum()
)

print("\n========== INVALID CHARGING COST ==========")

print(
    "Negative cost records:",
    (df["Charging_Cost"] < 0).sum()
)

print("\n========== DURATION VALIDATION ==========")

actual_duration = (
    df["End_Time"] - df["Start_Time"]
).dt.total_seconds() / 60

duration_mismatch = (
    actual_duration - df["Charging_Duration_Min"]
).abs() > 0.01

print("Duration mismatch records:", duration_mismatch.sum())

# ======================================================
# BUSINESS KPIs
# ======================================================

print("\n========== BUSINESS KPI ==========")

total_sessions = len(df)

unique_customers = df["Customer_ID"].nunique()

unique_stations = df["Station_ID"].nunique()

total_revenue = df["Charging_Cost"].sum()

average_cost = df["Charging_Cost"].mean()

total_energy = df["Energy_Consumed_kWh"].sum()

average_duration = df["Charging_Duration_Min"].mean()

print("Total Charging Sessions:", total_sessions)
print("Unique Customers:", unique_customers)
print("Unique Stations:", unique_stations)
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Average Charging Cost: ₹{average_cost:,.2f}")
print(f"Total Energy Consumed: {total_energy:,.2f} kWh")
print(f"Average Charging Duration: {average_duration:.2f} minutes")

# ======================================================
# CATEGORY ANALYSIS
# ======================================================

categories = [
    "City",
    "Manufacturer",
    "Vehicle_Model",
    "Charger_Type",
    "Payment_Method",
    "Station_Status"
]

for column in categories:
    print(f"\n========== {column.upper()} DISTRIBUTION ==========")
    print(df[column].value_counts())

# ======================================================
# BUSINESS ANALYSIS USING GROUPBY
# ======================================================

# Revenue by City
city_revenue = (
    df.groupby("City")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== REVENUE BY CITY ==========")
print(city_revenue.round(2))

# Revenue by Manufacturer
manufacturer_revenue = (
    df.groupby("Manufacturer")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== REVENUE BY MANUFACTURER ==========")
print(manufacturer_revenue.round(2))

# Average Cost by Charger Type
charger_average_cost = (
    df.groupby("Charger_Type")["Charging_Cost"]
    .mean()
    .sort_values(ascending=False)
)

print("\n========== AVERAGE COST BY CHARGER ==========")
print(charger_average_cost.round(2))

# Energy Consumption by Manufacturer
manufacturer_energy = (
    df.groupby("Manufacturer")["Energy_Consumed_kWh"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== ENERGY BY MANUFACTURER ==========")
print(manufacturer_energy.round(2))

# Charging Sessions by City
city_sessions = (
    df.groupby("City")["Session_ID"]
    .nunique()
    .sort_values(ascending=False)
)

print("\n========== SESSIONS BY CITY ==========")
print(city_sessions)

# Average Duration by Charger Type
average_duration_by_charger = (
    df.groupby("Charger_Type")["Charging_Duration_Min"]
    .mean()
)

print("\n========== AVERAGE DURATION BY CHARGER ==========")
print(average_duration_by_charger.round(2))

# Revenue by Payment Method
payment_revenue = (
    df.groupby("Payment_Method")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\n========== REVENUE BY PAYMENT METHOD ==========")
print(payment_revenue.round(2))

# City Summary
city_summary = df.groupby("City").agg(
    Total_Sessions=("Session_ID", "nunique"),
    Total_Revenue=("Charging_Cost", "sum"),
    Average_Energy=("Energy_Consumed_kWh", "mean"),
    Average_Duration=("Charging_Duration_Min", "mean")
).sort_values("Total_Revenue", ascending=False)

print("\n========== CITY SUMMARY ==========")
print(city_summary.round(2))

# Monthly Revenue
monthly_revenue = (
    df.set_index("Start_Time")["Charging_Cost"]
    .resample("MS")
    .sum()
)

print("\n========== MONTHLY REVENUE ==========")
print(monthly_revenue.round(2))

# ======================================================
# VISUALIZATION HELPER
# ======================================================

def save_chart(filename):
    """Save the current chart and display it."""
    plt.tight_layout()
    plt.savefig(
        PLOTS_DIR / filename,
        dpi=150,
        bbox_inches="tight"
    )
    plt.show()
    plt.close()

# ======================================================
# 1. REVENUE BY CITY
# ======================================================

plt.figure(figsize=(10, 6))

bars = plt.bar(
    city_revenue.index,
    city_revenue.values,
    edgecolor="black"
)

plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)

for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"₹{bar.get_height():,.0f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

save_chart("revenue_by_city.png")

# ======================================================
# 2. CHARGING SESSIONS BY CITY
# ======================================================

plt.figure(figsize=(10, 6))

plt.bar(
    city_sessions.index,
    city_sessions.values,
    edgecolor="black"
)

plt.title("Charging Sessions by City")
plt.xlabel("City")
plt.ylabel("Number of Sessions")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)

save_chart("charging_sessions_by_city.png")

# ======================================================
# 3. MANUFACTURER DISTRIBUTION
# ======================================================

manufacturer_distribution = df["Manufacturer"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    manufacturer_distribution.index,
    manufacturer_distribution.values,
    edgecolor="black"
)

plt.title("Manufacturer Distribution")
plt.xlabel("Manufacturer")
plt.ylabel("Number of Sessions")

save_chart("manufacturer_distribution.png")

# ======================================================
# 4. REVENUE BY MANUFACTURER
# ======================================================

plt.figure(figsize=(8, 5))

plt.bar(
    manufacturer_revenue.index,
    manufacturer_revenue.values,
    edgecolor="black"
)

plt.title("Revenue by Manufacturer")
plt.xlabel("Manufacturer")
plt.ylabel("Revenue (₹)")

save_chart("revenue_by_manufacturer.png")

# ======================================================
# 5. ENERGY CONSUMPTION BY MANUFACTURER
# ======================================================

plt.figure(figsize=(8, 5))

plt.bar(
    manufacturer_energy.index,
    manufacturer_energy.values,
    edgecolor="black"
)

plt.title("Energy Consumption by Manufacturer")
plt.xlabel("Manufacturer")
plt.ylabel("Energy Consumed (kWh)")

save_chart("energy_consumption.png")

# ======================================================
# 6. AVERAGE COST BY CHARGER TYPE
# ======================================================

plt.figure(figsize=(6, 5))

plt.bar(
    charger_average_cost.index,
    charger_average_cost.values,
    edgecolor="black"
)

plt.title("Average Charging Cost by Charger Type")
plt.xlabel("Charger Type")
plt.ylabel("Average Cost (₹)")

save_chart("average_charging_cost.png")

# ======================================================
# 7. REVENUE BY PAYMENT METHOD
# ======================================================

plt.figure(figsize=(8, 5))

plt.bar(
    payment_revenue.index,
    payment_revenue.values,
    edgecolor="black"
)

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=20)

save_chart("payment_revenue.png")

# ======================================================
# 8. AVERAGE CHARGING DURATION
# ======================================================

plt.figure(figsize=(6, 5))

plt.bar(
    average_duration_by_charger.index,
    average_duration_by_charger.values,
    edgecolor="black"
)

plt.title("Average Charging Duration by Charger Type")
plt.xlabel("Charger Type")
plt.ylabel("Duration (Minutes)")

save_chart("average_duration.png")

# ======================================================
# 9. CHARGING COST DISTRIBUTION
# ======================================================

plt.figure(figsize=(8, 5))

plt.hist(
    df["Charging_Cost"],
    bins=20,
    edgecolor="black"
)

plt.title("Charging Cost Distribution")
plt.xlabel("Charging Cost (₹)")
plt.ylabel("Frequency")

save_chart("charging_cost_distribution.png")

# ======================================================
# 10. CHARGING DURATION BOXPLOT
# ======================================================

plt.figure(figsize=(6, 5))

plt.boxplot(
    df["Charging_Duration_Min"]
)

plt.title("Charging Duration Distribution")
plt.ylabel("Minutes")

save_chart("charging_duration_boxplot.png")

# ======================================================
# 11. PAYMENT METHOD PERCENTAGE
# ======================================================

payment_distribution = df["Payment_Method"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    payment_distribution.values,
    labels=payment_distribution.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Payment Method Distribution")

save_chart("payment_distribution.png")

# ======================================================
# 12. MONTHLY REVENUE TREND
# ======================================================

plt.figure(figsize=(10, 5))

plt.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Charging Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

save_chart("monthly_revenue.png")

# ======================================================
# EXPORT SUMMARY TABLES
# ======================================================

city_summary.to_csv(
    PLOTS_DIR / "city_summary.csv"
)

monthly_revenue.to_csv(
    PLOTS_DIR / "monthly_revenue.csv",
    header=["Revenue"]
)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print(f"Dataset loaded from: {DATA_FILE}")
print(f"Charts and summaries saved to: {PLOTS_DIR}")