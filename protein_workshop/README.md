# Protein Classification Workshop

This workshop focuses on **protein classification** using knowledge distillation with ESM2 as the teacher model.

## Overview

- **Teacher Model**: ESM2 (Meta's protein language model)
- **Task**: 8-class plant transcription factor classification
- **Student Models**: Various lightweight architectures
- **Goal**: Distill knowledge from ESM2 to efficient student models

## Protein Classes (8 balanced classes)

Selected transcription factor families with balanced sample sizes:

- **GRF** (1876 sequences)
- **E2F__DP** (1781 sequences)
- **DBB** (1651 sequences)
- **CPP** (1612 sequences)
- **GeBP** (1564 sequences)
- **BES1** (1549 sequences)
- **CAMTA** (1343 sequences)
- **BBR-BPC** (1256 sequences)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the notebook:
```bash
jupyter notebook protein_classification_esm2.ipynb
```

## Structure

```
protein_workshop/
├── 2-data/
│   ├── raw/              # Downloaded FASTA files
│   ├── processed/        # Train/val/test splits
│   ├── embeddings/       # ESM2 embeddings
│   └── models/           # Saved models
├── assets/               # Images and diagrams
├── protein_classification_esm2.ipynb  # Main notebook
└── requirements.txt
```

## Large Files

Due to GitHub's file size limit (100 MB), the following large files are stored in Google Drive:

- `protein_workshop/2-data/processed/train.npz` (117.94 MB)
- `protein_workshop/2-data/embeddings/*` (all embedding files)

Download them from: https://drive.google.com/drive/folders/1Rnv2CWg1Xp31y8cIGn49s7SejHqf4oWD

## ESM2 Models

Available ESM2 models (from Meta):

- `esm2_t6_8M_UR50D`: 8M parameters, 320 dim
- `esm2_t12_35M_UR50D`: 35M parameters, 480 dim (default)
- `esm2_t30_150M_UR50D`: 150M parameters, 640 dim
- `esm2_t33_650M_UR50D`: 650M parameters, 1280 dim
- `esm2_t36_3B_UR50D`: 3B parameters, 2560 dim
