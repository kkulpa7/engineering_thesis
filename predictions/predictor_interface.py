import torch
import torch.nn as nn
from tqdm import tqdm

from predictions.result_predictor_model import ResultPredictorModel


INPUT_SIZE = 1
HIDDEN_SIZE = 32
OUTPUT_SIZE = 1


class PredictorInterface:

    def __init__(self, filename=None):
        self.model = ResultPredictorModel(INPUT_SIZE, HIDDEN_SIZE, OUTPUT_SIZE)
        if filename:
            self.model.load_state_dict(torch.load(filename))

    def train_model(self, data, num_epochs):
        optimizer = torch.optim.Adam(self.model.parameters())
        loss_fn = nn.MSELoss()

        training_data = [(sequence[:-1], sequence[1:]) for sequence in data]

        progress_bar = tqdm(total=num_epochs * len(training_data))
        results = []
        for epoch in range(num_epochs):
            for input_sequence, target in training_data:
                input_sequence = torch.Tensor(input_sequence).view(len(input_sequence), 1, -1)
                target = torch.Tensor(target).view(len(target), 1, -1)

                # Forward pass
                output = self.model(input_sequence)
                results.append(int(output[-1].item()) == int(target[-1].item()))
                loss = loss_fn(output, target)

                # Backward pass
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                progress_bar.set_description(f'Epoch [{epoch + 1}/{num_epochs}] - acc: {sum(results) / len(results) * 100:.2f}%%')
                progress_bar.update()

    def test_model(self, data):
        test_data = [(sequence[:-1], sequence[-1]) for sequence in data]
        results = []

        for input_sequence, target in test_data:
            result = self.predict(input_sequence)
            results.append(result == target)

        print(f'Accuracy: {sum(results) / len(results) * 100:.2f}%')

    def save_model(self, filename):
        torch.save(self.model.state_dict(), filename)

    def predict(self, input_sequence):
        data = torch.Tensor(input_sequence).view(len(input_sequence), 1, -1)
        output = self.model(data)
        return int(output[-1].item())
