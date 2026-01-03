import json
import paho.mqtt.client as mqtt

MQTT_BROKER = "localhost"
MQTT_TOPIC = "credit/scoring"

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)

def publish_scoring_event(payload: dict):
    client.publish(MQTT_TOPIC, json.dumps(payload))
