from network import DokuNet, inputs, answers

import numpy as np
import torch

checkpoint = torch.load('./history/model.pt')
model = DokuNet()
model.load_state_dict(checkpoint['model_state_dict'])

inp = answers[142].reshape(9,9)
pred = model(torch.tensor(inputs[142]).reshape(1, 81).float())
processed_pred = (torch.argmax(pred[0], dim=-1) + 1).reshape(9,9).numpy()

print("input: ")
print()
print(inp)



print()
print()

print("output: ")
print()

print(processed_pred)

print()

match = 0

for r in range(9):
    for c in range(9):
        if processed_pred[r,c] == inp[r,c]:
            match += 1


print("{} / 81".format(match))