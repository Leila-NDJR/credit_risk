import sys
import os

# Ajoute le dossier parent au chemin de recherche de Python
# On remonte de DEUX niveaux pour arriver à la racine du projet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import paho.mqtt.client as mqtt

from api.database.session import SessionLocal
from api.database.models import ScoringEvent

MQTT_BROKER = "localhost"
MQTT_TOPIC = "credit/scoring"


def on_connect(client, userdata, flags, rc):
    print("MQTT connected")
    client.subscribe(MQTT_TOPIC)


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())
    print("Received:", payload)

    db = SessionLocal()
    try:
        event = ScoringEvent(
            probability_default=payload["probability_default"],
            decision=payload["decision"],
            features=payload["features"],
            shap_values=payload["top_shap_features"]
        )
        db.add(event)
        db.commit()
    except Exception as e:
        db.rollback()
        print("DB error:", e)
    finally:
        db.close()


def start_consumer():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_forever()


if __name__ == "__main__":
    start_consumer()
