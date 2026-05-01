import pandas as pd
import numpy as np
import pickle

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

# ENVIRONMENT (from room dataset)
df['Temp'] = bed['Temp']
df['Humidity'] = bed['Humidity']
df['Light'] = bed['Light']

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

# ---------------- TIME FEATURES ----------------
df['hour'] = df['timestamp'].dt.hour
df['minute'] = df['timestamp'].dt.minute

df['sin_time'] = np.sin(2*np.pi*(df['hour'] + df['minute']/60)/24)
df['cos_time'] = np.cos(2*np.pi*(df['hour'] + df['minute']/60)/24)

# ---------------- ENVIRONMENT MODEL ----------------
X_env = df[['sin_time','cos_time']]

temp_model = RandomForestRegressor()
hum_model = RandomForestRegressor()
light_model = RandomForestRegressor()

temp_model.fit(X_env, df['Temp'])
hum_model.fit(X_env, df['Humidity'])
light_model.fit(X_env, df['Light'])

# ---------------- MAIN MODEL ----------------
features = ['sin_time','cos_time','Temp','Humidity','Light']
X = df[features]

le = LabelEncoder()
y = le.fit_transform(df['location'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=10),
    "Random Forest": RandomForestClassifier(n_estimators=100, class_weight='balanced'),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=100)
}

trained_models = {}
model_scores = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    
    trained_models[name] = model
    model_scores[name] = acc
    
    print(f"{name} Accuracy: {acc}")

# ---------------- ROOM MODEL ----------------
room_df = df[df['location']=="Room"].copy()

def room_type(row):
    if row['is_bed']:
        return "Bed"
    elif row['is_chair']:
        return "Chair"
    else:
        return "Unknown"

room_df['room_type'] = room_df.apply(room_type, axis=1)

X_room = room_df[features]
y_room = room_df['room_type']

le_room = LabelEncoder()
y_room_enc = le_room.fit_transform(y_room)

room_model = RandomForestClassifier()
room_model.fit(X_room, y_room_enc)

# ---------------- SAVE ----------------
with open("models/all_models.pkl", "wb") as f:
    pickle.dump((
        trained_models,
        le,
        model_scores,
        room_model,
        le_room,
        temp_model,
        hum_model,
        light_model
    ), f)

print("✅ Training Complete")