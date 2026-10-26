import pandas as pd
import numpy as np
from pathlib import Path

# ======================================================
# EV CHARGING STATION DATASET GENERATOR
# ======================================================

print("=" * 60)
print("EV CHARGING STATION DATASET GENERATOR")
print("=" * 60)

# ======================================================
# CONFIGURATION
# ======================================================

NUM_RECORDS = 1000
RATE_PER_KWH = 18
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)

# ======================================================
# MASTER DATA
# ======================================================

city_state = {
    "Chennai": "Tamil Nadu",
    "Coimbatore": "Tamil Nadu",
    "Bangalore": "Karnataka",
    "Hyderabad": "Telangana",
    "Mumbai": "Maharashtra",
    "Pune": "Maharashtra",
    "Delhi": "Delhi",
    "Kochi": "Kerala"
}

vehicle_data = {
    "Tata": {
        "Nexon EV": 30,
        "Punch EV": 35,
        "Tiago EV": 24
    },
    "MG": {
        "ZS EV": 50,
        "Comet EV": 17
    },
    "Hyundai": {
        "Kona Electric": 39,
        "Ioniq 5": 72
    },
    "Mahindra": {
        "XUV400": 40,
        "BE 6": 59
    },
    "BYD": {
        "Atto 3": 60,
        "Seal EV": 82
    }
}

# Simplified connector mapping for this synthetic dataset.
# This is a modelling assumption, not a complete compatibility database.
charger_config = {
    "AC": {
        "connector": "Type 2",
        "power_kw": 7.4
    },
    "DC Fast": {
        "connector": "CCS2",
        "power_kw": 50.0
    }
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking"
]

weather_conditions = [
    "Sunny",
    "Cloudy",
    "Rainy"
]

# Status is the station's recorded status at session start.
station_status = [
    "Available",
    "Busy",
    "Maintenance"
]

# ======================================================
# GENERATE IDS
# ======================================================

session_ids = [
    f"S{i:05d}"
    for i in range(1, NUM_RECORDS + 1)
]

customer_ids = [
    f"C{i:04d}"
    for i in np.random.randint(1001, 1101, NUM_RECORDS)
]

station_ids = [
    f"ST{i:03d}"
    for i in np.random.randint(101, 111, NUM_RECORDS)
]

# ======================================================
# GENERATE VEHICLE DETAILS
# ======================================================

manufacturers = []
vehicle_models = []
battery_capacities = []

manufacturer_list = list(vehicle_data.keys())

for _ in range(NUM_RECORDS):
    manufacturer = np.random.choice(manufacturer_list)

    model = np.random.choice(
        list(vehicle_data[manufacturer].keys())
    )

    battery_capacity = vehicle_data[manufacturer][model]

    manufacturers.append(manufacturer)
    vehicle_models.append(model)
    battery_capacities.append(battery_capacity)

battery_capacities = np.array(battery_capacities, dtype=float)

# ======================================================
# CITY & STATE
# ======================================================

cities = np.random.choice(
    list(city_state.keys()),
    NUM_RECORDS
)

states = [
    city_state[city]
    for city in cities
]

# ======================================================
# CHARGER DETAILS
# ======================================================

charger_types = np.random.choice(
    ["AC", "DC Fast"],
    NUM_RECORDS,
    p=[0.60, 0.40]
)

connector_types = [
    charger_config[charger]["connector"]
    for charger in charger_types
]

charger_power_kw = np.array([
    charger_config[charger]["power_kw"]
    for charger in charger_types
])

# ======================================================
# BATTERY DETAILS
# ======================================================

# Generate the initial battery percentage.
battery_before = np.random.randint(
    10,
    71,
    NUM_RECORDS
)

# Generate a target percentage above the initial percentage.
battery_after = np.array([
    np.random.randint(before + 1, 101)
    for before in battery_before
])

# Energy added to the vehicle battery.
energy_added = (
    battery_capacities
    * (battery_after - battery_before)
    / 100
)

# Assume 90% charging efficiency.
# Energy drawn from the station is higher than energy added
# to the vehicle battery due to charging losses.
CHARGING_EFFICIENCY = 0.90

energy_consumed = np.round(
    energy_added / CHARGING_EFFICIENCY,
    2
)

# ======================================================
# CHARGING DURATION
# ======================================================

# Approximate average charging power using charger rating.
# Actual charging power varies with vehicle and battery conditions.
charging_duration = np.ceil(
    energy_consumed / charger_power_kw * 60
).astype(int)

# Add a small amount of time for simplified charging overhead.
charging_duration += np.random.randint(
    3,
    11,
    NUM_RECORDS
)

# Minimum duration of 10 minutes for this synthetic model.
charging_duration = np.maximum(
    charging_duration,
    10
)

# ======================================================
# CHARGING COST
# ======================================================

charging_cost = np.round(
    energy_consumed * RATE_PER_KWH,
    2
)

# ======================================================
# DATE & TIME
# ======================================================

# Generate sessions over a full year to support monthly analysis.
start_time = pd.to_datetime(
    np.random.choice(
        pd.date_range(
            start="2025-01-01",
            end="2025-12-31 23:00:00",
            freq="h"
        ),
        NUM_RECORDS,
        replace=True
    )
).sort_values()

start_time = pd.Series(start_time).reset_index(drop=True)

end_time = (
    start_time
    + pd.to_timedelta(charging_duration, unit="m")
)

# ======================================================
# DAY TYPE
# ======================================================

day_type = np.where(
    start_time.dt.dayofweek < 5,
    "Weekday",
    "Weekend"
)

# ======================================================
# WEATHER
# ======================================================

weather = np.random.choice(
    weather_conditions,
    NUM_RECORDS,
    p=[0.50, 0.30, 0.20]
)

# ======================================================
# CREATE DATAFRAME
# ======================================================

df = pd.DataFrame({
    "Session_ID": session_ids,
    "Customer_ID": customer_ids,
    "Station_ID": station_ids,
    "City": cities,
    "State": states,
    "Manufacturer": manufacturers,
    "Vehicle_Model": vehicle_models,
    "Battery_Capacity_kWh": battery_capacities,
    "Battery_%_Before": battery_before,
    "Battery_%_After": battery_after,
    "Charger_Type": charger_types,
    "Connector_Type": connector_types,
    "Start_Time": start_time,
    "End_Time": end_time,
    "Charging_Duration_Min": charging_duration,
    "Energy_Consumed_kWh": energy_consumed,
    "Charging_Cost": charging_cost,
    "Weather": weather,
    "Day_Type": day_type,
    "Payment_Method": np.random.choice(
        payment_methods,
        NUM_RECORDS
    ),
    "Station_Status": np.random.choice(
        station_status,
        NUM_RECORDS
    )
})

# ======================================================
# DATA QUALITY CHECKS
# ======================================================

assert df["Session_ID"].is_unique, "Duplicate session IDs found."

assert df["Battery_%_Before"].between(0, 100).all()
assert df["Battery_%_After"].between(0, 100).all()

assert (
    df["Battery_%_After"] > df["Battery_%_Before"]
).all(), "Battery percentage should increase."

assert (df["Energy_Consumed_kWh"] > 0).all()
assert (df["Charging_Cost"] >= 0).all()
assert (df["Charging_Duration_Min"] > 0).all()

assert (
    df["End_Time"] > df["Start_Time"]
).all()

assert (
    df["City"].map(city_state) == df["State"]
).all(), "City and state mismatch."

# ======================================================
# SAVE DATASET
# ======================================================

# Save to the DATA folder beside this Python file.
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "DATA"

DATA_DIR.mkdir(parents=True, exist_ok=True)

output_file = DATA_DIR / "ev_charging_data.csv"

df.to_csv(output_file, index=False)

# ======================================================
# OUTPUT
# ======================================================

print("\nFirst 5 Records\n")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nDataset Information")
df.info()

print("\nMissing Values")
print(df.isnull().sum())

print("\nData Quality Checks: PASSED")

print("\nTotal Revenue:", round(df["Charging_Cost"].sum(), 2))
print("Total Energy Consumed:", round(df["Energy_Consumed_kWh"].sum(), 2), "kWh")
print("Average Charging Cost:", round(df["Charging_Cost"].mean(), 2))

print(f"\nDataset Generated Successfully!")
print(f"Saved to: {output_file}")