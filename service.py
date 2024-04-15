
import bentoml
from bentoml.io import JSON
import numpy as np

model_ref = bentoml.sklearn.get('stroke_prediction:latest')
dv = model_ref.custom_objects['dicVectorizer']

model_runner = model_ref.to_runner()

svc = bentoml.Service('stroke_prediction', runners=[model_runner])

@svc.api(input= JSON.from_sample({
      "gender": "Male",
      "age": 74.0,
      "hypertension": 1,
      "heart_disease": 1,
      "ever_married": Yes,
      "work_type": "Private",
      "residence_type": "Rural",
      "smoking_status": "never smoked",
      "obese": False,
      "diabetes": False
        }), output= JSON())

def classify(application_data):
    vector = dv.transform(application_data)
    prediction = model_runner.predict_proba.run(vector)
    # np.format_float_positional returns a string
    round_predict = float(np.format_float_positional(prediction[:,1], precision=2))

    if round_predict < 0.10:
        return 'Stroke Risk: LOW'
    elif (round_predict => 0.10) & (round_predict =< 0.15):
        return 'Stroke Risk: MODERATE'
    else:
        return 'Stroke Risk: HIGH'
