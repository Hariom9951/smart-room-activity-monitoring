import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- CREATE FOLDER ----------------
os.makedirs("plots", exist_ok=True)

# ---------------- LOAD DATA ----------------
chair = pd.read_csv("data/FINAL_DISTANCE_ONLY_13.csv")
bed = pd.read_csv("data/FINAL_FULL_DATASET_13.csv")
kitchen = pd.read_csv("data/KITCHEN_FULL_FINAL.csv")
rack = pd.read_csv("data/KITCHEN_RACK_FINAL.csv")

# ---------------- PREPROCESS ----------------
for df in [chair, bed, kitchen, rack]:
    df.rename(columns={'Time':'timestamp','Distance':'distance'}, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

# ---------------- MERGE ----------------
df = pd.DataFrame()
df['timestamp'] = chair['timestamp']
df['chair_dist'] = chair['distance']
df['bed_dist'] = bed['distance']
df['kitchen_dist'] = kitchen['distance']
df['rack_dist'] = rack['distance']

# ---------------- LABEL ----------------
df['is_chair'] = (df['chair_dist'] < 50).astype(int)
df['is_bed'] = (df['bed_dist'] < 150).astype(int)
df['is_kitchen'] = (df['kitchen_dist'] < 100).astype(int)

def classify(row):
    if row['is_chair'] or row['is_bed']:
        return "Room"
    elif row['is_kitchen']:
        return "Kitchen"
    else:
        return "Outside"

df['location'] = df.apply(classify, axis=1)

# ---------------- TIME ----------------
df = df.sort_values('timestamp')
df['hour'] = df['timestamp'].dt.hour
df['date'] = df['timestamp'].dt.date

df['time_diff'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
df['time_diff'] = df['time_diff'].clip(upper=60)
df['time_hours'] = df['time_diff'] / 3600

# =========================================================
# 🔥 1. ACTIVITY VS HOUR
# =========================================================
activity = df.groupby(['hour','location'])['time_hours'].sum().unstack(fill_value=0)

activity.plot()
plt.title("Activity vs Hour (Hours)")
plt.savefig("plots/activity_vs_hour.png")
plt.close()

# =========================================================
# 🔥 2. ROOM TIME PER DAY
# =========================================================
room_day = df[df['location']=="Room"].groupby(['date','hour'])['time_hours'].sum().unstack(fill_value=0)

room_day.T.plot()
plt.title("Each Day vs Room Time (Hours)")
plt.savefig("plots/room_time_per_day.png")
plt.close()

# =========================================================
# 🔥 3. KITCHEN TIME PER DAY
# =========================================================
kitchen_day = df[df['location']=="Kitchen"].groupby(['date','hour'])['time_hours'].sum().unstack(fill_value=0)

kitchen_day.T.plot()
plt.title("Each Day vs Kitchen Time (Hours)")
plt.savefig("plots/kitchen_time_per_day.png")
plt.close()

# =========================================================
# 🔥 4. OUTSIDE TIME PER DAY
# =========================================================
outside_day = df[df['location']=="Outside"].groupby(['date','hour'])['time_hours'].sum().unstack(fill_value=0)

outside_day.T.plot()
plt.title("Each Day vs Outside Time (Hours)")
plt.savefig("plots/outside_time_per_day.png")
plt.close()

# =========================================================
# 🔥 5. ROOM ENVIRONMENT
# =========================================================
room_env = pd.read_csv("data/FINAL_FULL_DATASET_13.csv")
room_env['Time'] = pd.to_datetime(room_env['Time'])
room_env['hour'] = room_env['Time'].dt.hour
room_env['date'] = room_env['Time'].dt.date

# Temperature
room_env.groupby(['date','hour'])['Temp'].mean().unstack().T.plot()
plt.title("Room Temperature vs Time")
plt.savefig("plots/room_temperature.png")
plt.close()

# Humidity
room_env.groupby(['date','hour'])['Humidity'].mean().unstack().T.plot()
plt.title("Room Humidity vs Time")
plt.savefig("plots/room_humidity.png")
plt.close()

# Light
room_env.groupby(['date','hour'])['Light'].mean().unstack().T.plot()
plt.title("Room Light vs Time")
plt.savefig("plots/room_light.png")
plt.close()

# =========================================================
# 🔥 6. KITCHEN ENVIRONMENT
# =========================================================
kitchen_env = pd.read_csv("data/KITCHEN_FULL_FINAL.csv")
kitchen_env['Time'] = pd.to_datetime(kitchen_env['Time'])
kitchen_env['hour'] = kitchen_env['Time'].dt.hour
kitchen_env['date'] = kitchen_env['Time'].dt.date

# Temperature
kitchen_env.groupby(['date','hour'])['Temp'].mean().unstack().T.plot()
plt.title("Kitchen Temperature vs Time")
plt.savefig("plots/kitchen_temperature.png")
plt.close()

# Humidity
kitchen_env.groupby(['date','hour'])['Humidity'].mean().unstack().T.plot()
plt.title("Kitchen Humidity vs Time")
plt.savefig("plots/kitchen_humidity.png")
plt.close()

# Light
kitchen_env.groupby(['date','hour'])['Light'].mean().unstack().T.plot()
plt.title("Kitchen Light vs Time")
plt.savefig("plots/kitchen_light.png")
plt.close()

print("✅ ALL GRAPHS SAVED SUCCESSFULLY")