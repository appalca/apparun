import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

os.environ["APPARUN_IMPACT_MODELS_DIR"] = os.path.join(DATA_DIR, "impact_models")
