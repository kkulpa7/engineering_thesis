import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theis_project.settings')

import django
django.setup()

from predictions.predictor_interface import PredictorInterface
from pigeons.models import Pigeon

def train_model(epochs=10):
    interface = PredictorInterface()

    data = []
    for pigeon in Pigeon.objects.all():
        pigeon_results = list(pigeon.result_set.values_list("place", flat=True))
        if len(pigeon_results) < 3:
            continue
        data.append(pigeon_results)
    interface.train_model(data, epochs)
    interface.test_model(data)

    interface.save_model('results_model.pth')

# def predict_result(pigeon):
#    pigeon_results = list(pigeon.result_set.values_list("place", flat=True))
#    interface = PredictorInterface('results_model.pth')
#    return interface.predict(pigeon_results)

# train model with data from database
train_model(epochs=10)
# predict result for pigeon with id PL-10314
# print(predict_result(Pigeon.objects.get(number="PL-10314")))
