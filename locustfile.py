from locust import HttpUser, task, between
import random
import json
from config import API_KEY

class PublicTransportNavigationUser(HttpUser):
    wait_time = between(5, 10)

    def on_start(self):
        self.client.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Locust Public Transport Test"
        })

    @task
    def get_route(self):
        # Генерация случайных координат вокруг центра Казани
        from_lat, from_lon = 55.796289, 49.108795
        to_lat = from_lat + random.uniform(-0.01, 0.01)
        to_lon = from_lon + random.uniform(-0.01, 0.01)

        body = {
            "locale": "ru_RU",
            "source": {
                "name": "Точка A",
                "point": {"lat": from_lat, "lon": from_lon}
            },
            "target": {
                "name": "Точка B",
                "point": {"lat": to_lat, "lon": to_lon}
            },
            "transport": ["bus", "tram", "minibus"]
        }
        response = self.client.post(
            f"/public_transport/2.0?key={API_KEY}",
            data=json.dumps(body),
            name="Навигация: маршрут A → B"
        )
        if response.status_code == 429:
            print("429 Too Many Requests — делаем паузу")
            self.environment.runner.quit()