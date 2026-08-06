# EEIA — bioAI Workshop
# Author: Généreux Akotenou — PhD student, BioinformaticLabs College of Computing / UM6P
# https://github.com/Genereux-akotenou/EEIA-bioAI-Workshop
# Licensed under the MIT License. See LICENSE at the repo root.

"""
sae.py — autoencodeur parcimonieux Top-K minimal pour la piste bonus d'interprétabilité.
Entraîné sans aucune étiquette sur des activations Evo2 brutes (data/autoencoder/).

Volontairement minuscule : c'est un artefact pédagogique, pas la version à l'échelle
recherche.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TopKSparseAutoencoder(nn.Module):
    """Dictionnaire surcomplet (d_hidden > d_in) avec une contrainte stricte de parcimonie
    top-k : chaque vecteur d'activation est expliqué par exactement k « caractéristiques »."""

    def __init__(self, d_in: int, d_hidden: int, k: int):
        super().__init__()
        self.k = k
        W = F.normalize(0.1 * torch.randn(d_in, d_hidden), dim=0)
        self.W = nn.Parameter(W)
        self.b_enc = nn.Parameter(torch.zeros(d_hidden))
        self.b_dec = nn.Parameter(torch.zeros(d_in))

    def encode(self, x):
        f = F.relu(x @ self.W + self.b_enc)
        values, indices = torch.topk(f, self.k, dim=-1)
        sparse_f = torch.zeros_like(f)
        return sparse_f.scatter_(-1, indices, values)

    def decode(self, f):
        return f @ self.W.T + self.b_dec

    def forward(self, x):
        f = self.encode(x)
        return self.decode(f), f


def train_sae(sae, activations: torch.Tensor, epochs=10, lr=2e-4,
              batch_size=512, device="cpu", log_every=1):
    """activations: tenseur (N, d_in), déjà chargé/sous-échantillonné en mémoire — prévu
    pour quelques milliers à dizaines de milliers de vecteurs, pas le dump complet
    multi-Go."""
    sae = sae.to(device)
    optimizer = torch.optim.Adam(sae.parameters(), lr=lr)
    n = activations.shape[0]
    history = {"recon_loss": [], "alive_frac": [], "explained_var": []}

    var_x = activations.var().item()          # pour la variance expliquée

    for epoch in range(epochs):
        perm = torch.randperm(n)
        epoch_loss = 0.0
        used = torch.zeros(sae.W.shape[1], dtype=torch.bool)   # caractéristiques vues
        for start in range(0, n, batch_size):
            x = activations[perm[start:start + batch_size]].to(device)
            optimizer.zero_grad()
            x_hat, f = sae(x)
            loss = F.mse_loss(x_hat, x)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * x.shape[0]
            used |= (f > 0).any(dim=0).cpu()

        recon = epoch_loss / n
        alive = used.float().mean().item()          # part du dictionnaire réellement utilisée
        ev = 1.0 - recon / var_x if var_x > 0 else float("nan")
        history["recon_loss"].append(recon)
        history["alive_frac"].append(alive)
        history["explained_var"].append(ev)

        if log_every and ((epoch + 1) % log_every == 0 or epoch == 0
                          or epoch == epochs - 1):
            print(f"epoch {epoch + 1:3d}/{epochs} | recon_loss={recon:.4f} "
                  f"| variance expliquée={ev:6.1%} "
                  f"| caractéristiques vivantes={alive:5.1%}")

    return sae, history
