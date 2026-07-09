# ==========================================
# EV CHARGING STATION ANALYTICS
# Exploratory Data Analysis
# ==========================================


# ==========================================
# IMPORT LIBRARIES
# ==========================================

import pandas as pd
import matplotlib.pyplot as plt
import os


# Create plots folder automatically

os.makedirs("plots", exist_ok=True)



# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv("data/ev_charging_data.csv")



# ==========================================
# DATASET OVERVIEW
# ==========================================

print("\n========== DATA PREVIEW ==========")

print(df.head())


print("\n========== DATA SHAPE ==========")

print(df.shape)


print("\n========== DATA INFORMATION ==========")

print(df.info())


print("\n========== STATISTICAL SUMMARY ==========")

print(df.describe())


print("\n========== COLUMN NAMES ==========")

print(df.columns)



# ==========================================
# DATA QUALITY CHECK
# ==========================================


print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


print("\n========== DUPLICATE ROWS ==========")

print(df.duplicated().sum())



# ==========================================
# BASIC BUSINESS KPI
# ==========================================


print("\n========== BUSINESS KPI ==========")


total_sessions = len(df)

unique_customers = df["Customer_ID"].nunique()

total_revenue = df["Charging_Cost"].sum()

average_cost = df["Charging_Cost"].mean()



print("Total Charging Sessions :", total_sessions)

print("Unique Customers :", unique_customers)

print("Total Revenue :", total_revenue)

print("Average Charging Cost :", average_cost)



# ==========================================
# CATEGORY ANALYSIS
# ==========================================


print("\n========== CITY DISTRIBUTION ==========")

print(df["City"].value_counts())


print("\n========== MANUFACTURER DISTRIBUTION ==========")

print(df["Manufacturer"].value_counts())


print("\n========== VEHICLE DISTRIBUTION ==========")

print(df["Vehicle_Model"].value_counts())


print("\n========== CHARGER TYPE DISTRIBUTION ==========")

print(df["Charger_Type"].value_counts())


print("\n========== PAYMENT DISTRIBUTION ==========")

print(df["Payment_Method"].value_counts())


print("\n========== STATION STATUS ==========")

print(df["Station_Status"].value_counts())



# ==========================================
# BUSINESS ANALYSIS USING GROUPBY
# ==========================================



# Revenue by City

city_revenue = (
    df.groupby("City")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by City")

print(city_revenue)



# Revenue by Manufacturer

manufacturer_revenue = (
    df.groupby("Manufacturer")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\nRevenue by Manufacturer")

print(manufacturer_revenue)



# Average Cost by Charger Type

charger_average_cost = (
    df.groupby("Charger_Type")["Charging_Cost"]
    .mean()
)

print("\nAverage Charging Cost by Charger")

print(charger_average_cost)



# Energy Consumption by Manufacturer

manufacturer_energy = (
    df.groupby("Manufacturer")["Energy_Consumed_kWh"]
    .sum()
    .sort_values(ascending=False)
)

print("\nEnergy Consumption")

print(manufacturer_energy)



# Charging Sessions by City

city_sessions = (
    df.groupby("City")["Session_ID"]
    .count()
)

print("\nCharging Sessions by City")

print(city_sessions)



# Average Duration by Charger Type

average_duration = (
    df.groupby("Charger_Type")["Charging_Duration_Min"]
    .mean()
)

print("\nAverage Charging Duration")

print(average_duration)



# Revenue by Payment Method

payment_revenue = (
    df.groupby("Payment_Method")["Charging_Cost"]
    .sum()
    .sort_values(ascending=False)
)

print("\nPayment Revenue")

print(payment_revenue)



# City Summary Table

city_summary = df.groupby("City").agg(

    Total_Revenue=("Charging_Cost","sum"),

    Average_Energy=("Energy_Consumed_kWh","mean"),

    Average_Duration=("Charging_Duration_Min","mean")

)


print("\nCity Summary")

print(city_summary)
# ==========================================
# VISUALIZATION
# ==========================================


# ==========================================
# 1. Revenue by City
# ==========================================


plt.figure(figsize=(10,6))


bars = plt.bar(
    city_revenue.index,
    city_revenue.values,
    edgecolor="black"
)


plt.title("Revenue by City")

plt.xlabel("City")

plt.ylabel("Revenue (₹)")

plt.xticks(rotation=45)

plt.grid(axis="y")


# Display values on bars

for bar in bars:

    plt.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height(),
        f"{bar.get_height():.0f}",
        ha="center",
        va="bottom"
    )


plt.tight_layout()

plt.savefig("plots/revenue_by_city.png")

plt.show()



# ==========================================
# 2. Charging Sessions by City
# ==========================================


plt.figure(figsize=(10,6))


plt.bar(
    city_sessions.index,
    city_sessions.values,
    edgecolor="black"
)


plt.title("Charging Sessions by City")

plt.xlabel("City")

plt.ylabel("Number of Sessions")

plt.xticks(rotation=45)

plt.grid(axis="y")


plt.tight_layout()

plt.savefig("plots/charging_sessions_by_city.png")

plt.show()



# ==========================================
# 3. Manufacturer Distribution
# ==========================================


manufacturer_distribution = df["Manufacturer"].value_counts()


plt.figure(figsize=(8,5))


plt.bar(
    manufacturer_distribution.index,
    manufacturer_distribution.values,
    edgecolor="black"
)


plt.title("Manufacturer Distribution")

plt.xlabel("Manufacturer")

plt.ylabel("Number of Sessions")


plt.tight_layout()

plt.savefig("plots/manufacturer_distribution.png")

plt.show()



# ==========================================
# 4. Revenue by Manufacturer
# ==========================================


plt.figure(figsize=(8,5))


plt.bar(
    manufacturer_revenue.index,
    manufacturer_revenue.values,
    edgecolor="black"
)


plt.title("Revenue by Manufacturer")

plt.xlabel("Manufacturer")

plt.ylabel("Revenue (₹)")


plt.tight_layout()

plt.savefig("plots/revenue_by_manufacturer.png")

plt.show()



# ==========================================
# 5. Energy Consumption by Manufacturer
# ==========================================


plt.figure(figsize=(8,5))


plt.bar(
    manufacturer_energy.index,
    manufacturer_energy.values,
    edgecolor="black"
)


plt.title("Energy Consumption by Manufacturer")

plt.xlabel("Manufacturer")

plt.ylabel("Energy Consumed (kWh)")


plt.tight_layout()

plt.savefig("plots/energy_consumption.png")

plt.show()



# ==========================================
# 6. Average Charging Cost by Charger Type
# ==========================================


plt.figure(figsize=(6,5))


plt.bar(
    charger_average_cost.index,
    charger_average_cost.values,
    edgecolor="black"
)


plt.title("Average Charging Cost by Charger Type")

plt.xlabel("Charger Type")

plt.ylabel("Average Cost (₹)")


plt.tight_layout()

plt.savefig("plots/average_charging_cost.png")

plt.show()



# ==========================================
# 7. Revenue by Payment Method
# ==========================================


plt.figure(figsize=(8,5))


plt.bar(
    payment_revenue.index,
    payment_revenue.values,
    edgecolor="black"
)


plt.title("Revenue by Payment Method")

plt.xlabel("Payment Method")

plt.ylabel("Revenue (₹)")

plt.xticks(rotation=20)


plt.tight_layout()

plt.savefig("plots/payment_revenue.png")

plt.show()



# ==========================================
# 8. Average Charging Duration
# ==========================================


plt.figure(figsize=(6,5))


plt.bar(
    average_duration.index,
    average_duration.values,
    edgecolor="black"
)


plt.title("Average Charging Duration")

plt.xlabel("Charger Type")

plt.ylabel("Duration (Minutes)")


plt.tight_layout()

plt.savefig("plots/average_duration.png")

plt.show()



# ==========================================
# 9. Charging Cost Distribution
# ==========================================


plt.figure(figsize=(8,5))


plt.hist(
    df["Charging_Cost"],
    bins=20,
    edgecolor="black"
)


plt.title("Charging Cost Distribution")

plt.xlabel("Charging Cost")

plt.ylabel("Frequency")


plt.tight_layout()

plt.savefig("plots/charging_cost_distribution.png")

plt.show()



# ==========================================
# 10. Charging Duration Boxplot
# ==========================================


plt.figure(figsize=(6,5))


plt.boxplot(
    df["Charging_Duration_Min"]
)


plt.title("Charging Duration Distribution")

plt.ylabel("Minutes")


plt.tight_layout()

plt.savefig("plots/charging_duration_boxplot.png")

plt.show()



# ==========================================
# 11. Payment Method Percentage
# ==========================================


payment_distribution = df["Payment_Method"].value_counts()


plt.figure(figsize=(6,6))


plt.pie(
    payment_distribution.values,
    labels=payment_distribution.index,
    autopct="%1.1f%%"
)


plt.title("Payment Method Distribution")


plt.tight_layout()

plt.savefig("plots/payment_distribution.png")

plt.show()



print("\n========== ANALYSIS COMPLETED ==========")

print("All charts saved inside plots folder")