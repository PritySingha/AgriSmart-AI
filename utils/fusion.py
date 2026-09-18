from utils.cnn_model import predict_plant_image
from utils.sensor_model import predict_sensor_data


def fusion_prediction(
    image,
    soil_moisture,
    soil_temperature,
    soil_ph,
    humidity,
    air_temperature,
    solar_radiation
):

    image_result = predict_plant_image(image)

    sensor_result = predict_sensor_data(
        soil_moisture=soil_moisture,
        soil_temperature=soil_temperature,
        soil_ph=soil_ph,
        humidity=humidity,
        air_temperature=air_temperature,
        solar_radiation=solar_radiation
    )

    return {
        "image_analysis": image_result,
        "sensor_analysis": sensor_result
    }