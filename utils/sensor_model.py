import joblib
import pandas as pd


CLASSIFIER_PATH = "models/irrigation_classifier.pkl"
REGRESSOR_PATH = "models/irrigation_regressor.pkl"
FEATURES_PATH = "models/irrigation_features.pkl"


classifier = joblib.load(CLASSIFIER_PATH)
regressor = joblib.load(REGRESSOR_PATH)
features = joblib.load(FEATURES_PATH)


def predict_sensor_data(
    soil_moisture,
    soil_temperature,
    soil_ph,
    humidity,
    air_temperature,
    solar_radiation
):

    input_data = pd.DataFrame([{
        'Soil_Moisture_pct': soil_moisture,
        'Soil_Temperature_C': soil_temperature,
        'Soil_pH': soil_ph,
        'Humidity_pct': humidity,
        'Air_Temperature_C': air_temperature,
        'Solar_Radiation_W_m2': solar_radiation
    }])

    irrigation_prediction = classifier.predict(input_data)[0]

    irrigation_probability = classifier.predict_proba(input_data)[0][1]

    if irrigation_prediction == 1:
        recommended_liters = regressor.predict(input_data)[0]
        recommended_liters = max(0, float(recommended_liters))
    else:
        recommended_liters = 0.0

    return {
        "irrigation_needed": int(irrigation_prediction),

        "irrigation_probability":
            float(irrigation_probability),

        "recommended_irrigation_liters":
            float(max(0, recommended_liters)),

        "sensor_readings": {
            "soil_moisture_pct": float(soil_moisture),
            "soil_temperature_c": float(soil_temperature),
            "soil_ph": float(soil_ph),
            "humidity_pct": float(humidity),
            "air_temperature_c": float(air_temperature),
            "solar_radiation_w_m2": float(solar_radiation)
        }
    }