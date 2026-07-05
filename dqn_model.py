import torch
import torch.nn as nn


class DQN(nn.Module):
    """
    Deep Q Network
    Input:
        price
        sma
        momentum
        volatility
        trend
        market_score
    Output:
        0 = HOLD
        1 = BUY
        2 = SELL
    """

    def __init__(
        self,
        input_size=6,
        hidden_size=128,
        output_size=3,
    ):
        super().__init__()

        self.net = nn.Sequential(

            nn.Linear(input_size, hidden_size),
            nn.ReLU(),

            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),

            nn.Linear(hidden_size, 64),
            nn.ReLU(),

            nn.Linear(64, output_size)

        )

    def forward(self, x):

        if x.dim() == 1:
            x = x.unsqueeze(0)

        y = self.net(x)

        return y.squeeze(0)
