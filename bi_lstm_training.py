import pandas as pd
import numpy as np
import os
import pickle
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Input
from tensorflow.keras.callbacks import EarlyStopping

# Paths
ROOT_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(ROOT_DIR, "sensor_data.csv")
MODEL_DIR = os.path.join(ROOT_DIR, "ai_model", "saved_model")

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# Load Data
df = pd.read_csv(DATA_PATH)
features = ["temperature", "vibration", "load", "motor_current", "runtime_hours", "ambient_temperature", "temp_rolling_avg", "vib_rolling_avg"]

# Preprocessing
le = LabelEncoder()
df["health_label_encoded"] = le.fit_transform(df["health_label"])
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])

# Save scaler and label encoder
with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
    pickle.dump(scaler, f)
with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
    pickle.dump(le, f)

# Sequence Generation
def create_sequences(data, seq_length):
    X, y_h, y_r = [], [], []
    for crane_id in data["crane_id"].unique():
        crane_data = data[data["crane_id"] == crane_id]
        f_vals, h_vals, r_vals = crane_data[features].values, crane_data["health_label_encoded"].values, crane_data["RUL"].values
        for i in range(len(crane_data) - seq_length):
            X.append(f_vals[i:i+seq_length])
            y_h.append(h_vals[i+seq_length])
            y_r.append(r_vals[i+seq_length])
    return np.array(X), np.array(y_h), np.array(y_r)

SEQ_LENGTH = 10
X, y_health, y_rul = create_sequences(df, SEQ_LENGTH)
X_train, X_test, y_h_train, y_h_test, y_r_train, y_r_test = train_test_split(X, y_health, y_rul, test_size=0.2, random_state=42)

# Multi-output Bi-LSTM
input_layer = Input(shape=(SEQ_LENGTH, len(features)))
lstm_1 = Bidirectional(LSTM(64, return_sequences=True))(input_layer)
lstm_2 = Bidirectional(LSTM(32))(lstm_1)
dense_1 = Dense(32, activation='relu')(lstm_2)
health_out = Dense(len(le.classes_), activation='softmax', name='health')(dense_1)
rul_out = Dense(1, activation='linear', name='rul')(dense_1)

model = Model(inputs=input_layer, outputs=[health_out, rul_out])
model.compile(optimizer='adam', loss={'health': 'sparse_categorical_crossentropy', 'rul': 'mse'}, metrics={'health': 'accuracy', 'rul': 'mae'})

print("Training Bi-LSTM...")
model.fit(X_train, {'health': y_h_train, 'rul': y_r_train}, epochs=10, batch_size=32, validation_split=0.1, verbose=1)
model.save(os.path.join(MODEL_DIR, "bi_lstm_crane.h5"))

# Autoencoder
normal_data = df[df["health_label"] == "Normal"][features].values
ae_input = Input(shape=(len(features),))
encoded = Dense(8, activation='relu')(Dense(4, activation='relu')(Dense(8, activation='relu')(ae_input))) # Sequential layout
autoencoder = Model(ae_input, Dense(len(features), activation='linear')(Dense(8, activation='relu')(Dense(4, activation='relu')(Dense(8, activation='relu')(ae_input))))) # Fixed
# Simplified AE definition
ae_input = Input(shape=(len(features),))
e = Dense(8, activation='relu')(ae_input)
e = Dense(4, activation='relu')(e)
d = Dense(8, activation='relu')(e)
d = Dense(len(features), activation='linear')(d)
autoencoder = Model(ae_input, d)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.fit(normal_data, normal_data, epochs=20, batch_size=16, verbose=0)
autoencoder.save(os.path.join(MODEL_DIR, "autoencoder.h5"))

reconstructions = autoencoder.predict(normal_data)
mse = np.mean(np.power(normal_data - reconstructions, 2), axis=1)
threshold = np.percentile(mse, 99)
with open(os.path.join(MODEL_DIR, "anomaly_threshold.pkl"), "wb") as f:
    pickle.dump(threshold, f)

print("[DONE] Training complete. Models saved in ai_model/saved_model/")
