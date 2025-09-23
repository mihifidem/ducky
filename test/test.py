import os
import json

ruta_tests = "test"  # tu carpeta donde están los JSON

for archivo in os.listdir(ruta_tests):
    if archivo.endswith(".json"):
        ruta = os.path.join(ruta_tests, archivo)
        try:
            with open(ruta, encoding="utf-8") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] {archivo}: {e}")
        else:
            print(f"[OK] {archivo}")
