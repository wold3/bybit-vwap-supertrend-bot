import torch
import torch.nn as nn


class WorldModel(nn.Module):

    def __init__(self, input_dim=5, latent_dim=32):

        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )

        self.transition = nn.GRU(latent_dim, latent_dim, batch_first=True)

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )

    def encode(self, x):
        return self.encoder(x)

    def predict(self, z_seq):
        out, _ = self.transition(z_seq)
        return self.decoder(out)
