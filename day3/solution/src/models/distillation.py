# EEIA — bioAI Workshop
# Author: Généreux Akotenou — PhD student, BioinformaticLabs College of Computing / UM6P
# https://github.com/Genereux-akotenou/EEIA-bioAI-Workshop
# Licensed under the MIT License. See LICENSE at the repo root.

"""
distillation.py — teacher (embedding Evo2 gelé + MLPHead) -> student minuscule (MLP sur
k-mers), via cibles douces + température (perte hybride).
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


def distillation_loss(student_logits, teacher_logits, labels,
                       temperature: float = 4.0, alpha: float = 0.5):
    """Perte hybride = alpha * CE sur étiquettes dures + (1 - alpha) * KD sur cibles douces.

    alpha=1.0 est un entraînement supervisé classique (pas de distillation) ;
    alpha=0.0 est une pure imitation des cibles douces du teacher.
    """
    hard_loss = F.binary_cross_entropy_with_logits(student_logits, labels.float())

    t_soft = torch.sigmoid(teacher_logits / temperature)
    s_soft = torch.sigmoid(student_logits / temperature)
    soft_loss = F.binary_cross_entropy(s_soft, t_soft) * (temperature ** 2)

    return alpha * hard_loss + (1 - alpha) * soft_loss


def train_student(student, teacher_logits, inputs, labels, epochs=20, lr=1e-3,
                   temperature=4.0, alpha=0.5, device="cpu", batch_size=256,
                   log_every=10):
    """inputs: tenseur déjà transformé en caractéristiques pour le student (vecteurs
    k-mer ou fenêtres one-hot). teacher_logits: précalculés une fois, dans le même ordre
    que inputs."""
    student = student.to(device)
    optimizer = torch.optim.Adam(student.parameters(), lr=lr)

    n = inputs.shape[0]
    history = {"loss": [], "accuracy": []}

    for epoch in range(epochs):
        perm = torch.randperm(n)
        epoch_loss = 0.0
        epoch_correct = 0
        for start in range(0, n, batch_size):
            idx = perm[start:start + batch_size]
            x = inputs[idx].to(device)
            y = labels[idx].to(device)
            t_logits = teacher_logits[idx].to(device)

            optimizer.zero_grad()
            s_logits = student(x)
            loss = distillation_loss(s_logits, t_logits, y, temperature, alpha)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(idx)
            epoch_correct += ((s_logits > 0).float() == y).sum().item()

        avg_loss = epoch_loss / n
        history["loss"].append(avg_loss)
        history["accuracy"].append(epoch_correct / n)

        if log_every and ((epoch + 1) % log_every == 0 or epoch == 0
                          or epoch == epochs - 1):
            print(f"epoch {epoch + 1:3d}/{epochs} | loss={avg_loss:.4f} "
                  f"| acc={epoch_correct / n:.4f}")

    return student, history
