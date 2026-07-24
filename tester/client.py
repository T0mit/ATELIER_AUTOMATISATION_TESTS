import requests
import time
import urllib3

# Désactive les avertissements visuels dans la console concernant SSL non vérifié
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class APIClient:
    def __init__(self, base_url="https://api.quotable.io", timeout=4.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def request(self, method, endpoint, params=None, headers=None, max_retries=1):
        """
        Exécute une requête avec mesure de latence, gestion des erreurs et 1 retry.
        """
        url = f"{self.base_url}{endpoint}"
        attempts = 0
        
        while attempts <= max_retries:
            start_time = time.perf_counter()
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                    verify=False  # <--- IGNORER L'EXPIRATION DU CERTIFICAT SSL
                )
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                
                # En cas de 429 (Rate Limit) ou 5xx, retry après une pause de 1 sec
                if response.status_code in [429, 500, 502, 503, 504] and attempts < max_retries:
                    attempts += 1
                    time.sleep(1.0)
                    continue

                return {
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                    "headers": dict(response.headers),
                    "json": self._safe_json(response),
                    "error": None
                }

            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                latency_ms = round((time.perf_counter() - start_time) * 1000, 2)
                if attempts < max_retries:
                    attempts += 1
                    time.sleep(1.0)
                    continue
                
                return {
                    "status_code": 0,
                    "latency_ms": latency_ms,
                    "headers": {},
                    "json": None,
                    "error": str(e)
                }

    def _safe_json(self, response):
        try:
            return response.json()
        except Exception:
            return None
