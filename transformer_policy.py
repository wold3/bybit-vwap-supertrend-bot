import torch
import torch.nn as nn


class TransformerPolicy(nn.Module):

    def __init__(self, input_dim=5, d_model=64, nhead=4):

        super().__init__()

        self.embedding = nn.Linear(input_dim, d_model)

        self.encoder = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=nhead,
                batch_first=True
            ),
            num_layers=2
        )

        self.head = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Linear(32, 3)
        )

    def forward(self, x):

        x = self.embedding(x)
        x = self.encoder(x)
        x = x[:, -1, :]

        return self.head(x)
