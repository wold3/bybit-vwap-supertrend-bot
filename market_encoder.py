import torch
import torch.nn as nn


class MarketEncoder(nn.Module):

    def __init__(self, input_dim=5, d_model=64):

        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(input_dim, d_model),
            nn.ReLU(),
            nn.Linear(d_model, d_model)
        )

    def forward(self, x):
        return self.net(x)
