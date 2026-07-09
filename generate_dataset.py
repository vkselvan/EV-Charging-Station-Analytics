import pandas as pd
import numpy as np

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

charger_types = ["AC", "DC Fast"]

connector_types = [
    "Type 2",
    "CCS2"
]

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
    f"C{np.random.randint(1001,1101)}"
    for _ in range(NUM_RECORDS)
]

station_ids = [
    f"ST{np.random.randint(101,111)}"
    for _ in range(NUM_RECORDS)
]

# ======================================================
# GENERATE VEHICLE DETAILS
# ======================================================

manufacturers = []
vehicle_models = []
battery_capacities = []

manufacturer_list = list(vehicle_data.keys())

for i in range(NUM_RECORDS):

    manufacturer = np.random.choice(manufacturer_list)

    model = np.random.choice(
        list(vehicle_data[manufacturer].keys())
    )

    battery = vehicle_data[manufacturer][model]

    manufacturers.append(manufacturer)
    vehicle_models.append(model)
    battery_capacities.append(battery)

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
# CHARGING DETAILS
# ======================================================

charging_duration = np.random.randint(
    20,
    181,
    NUM_RECORDS
)

energy_consumed = np.round(
    np.random.uniform(
        10,
        60,
        NUM_RECORDS
    ),
    2
)

charging_cost = np.round(
    energy_consumed * RATE_PER_KWH,
    2
)

# ======================================================
# BATTERY DETAILS
# ======================================================

battery_before = np.random.randint(
    10,
    81,
    NUM_RECORDS
)

battery_after = np.random.randint(
    80,
    101,
    NUM_RECORDS
)

# ======================================================
# DATE & TIME
# ======================================================

start_time = pd.date_range(
    start="2025-01-01",
    periods=NUM_RECORDS,
    freq="h"
)

end_time = (
    start_time +
    pd.to_timedelta(
        charging_duration,
        unit="m"
    )
)

# ======================================================
# DAY TYPE
# ======================================================

day_type = np.where(
    start_time.dayofweek < 5,
    "Weekday",
    "Weekend"
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

    "Charger_Type": np.random.choice(
        charger_types,
        NUM_RECORDS
    ),

    "Connector_Type": np.random.choice(
        connector_types,
        NUM_RECORDS
    ),

    "Start_Time": start_time,

    "End_Time": end_time,

    "Charging_Duration_Min": charging_duration,

    "Energy_Consumed_kWh": energy_consumed,

    "Charging_Cost": charging_cost,

    "Weather": np.random.choice(
        weather_conditions,
        NUM_RECORDS
    ),

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
# SAVE DATASET
# ======================================================

df.to_csv(
    "data/ev_charging_data.csv",
    index=False
)

# ======================================================
# OUTPUT
# ======================================================

print("\nFirst 5 Records\n")

print(df.head())

print("\nDataset Shape")

print(df.shape)

print("\nDataset Info")

print(df.info())

print("\nDataset Generated Successfully!")

print("\nSaved to : data/ev_charging_data.csv")