from .predict import Predictor

def run_zero_shot(mix_file_path, query_file_path):
    pred = Predictor()
    pred.setup()
    prediction_path = pred.predict(mix_file = mix_file_path, query_file= query_file_path)
    return prediction_path

