# Evo2 embeddings — download

Too large for GitHub, so they live on Google Drive.

> ### 📥 [**Download the embeddings**](https://drive.google.com/drive/folders/1TL1p0ezAXUrGORAoHr7aVtc0YcxE-5ve?usp=drive_link)

Put all three files in this folder:

```
2-data/embeddings/
├── train.npz
├── val.npz
└── test.npz
```

Pre-extracted with Evo2-7b, so the workshop doesn't depend on live API access.
Used from **notebook 02** onward.

## Loading

```python
import numpy as np

d = np.load("2-data/embeddings/train.npz", allow_pickle=True)
X, y = d["embeddings_blocks.26"], d["labels"]
```

`allow_pickle=True` is required — `ids` is an object array.

| Key | Shape | Description |
|---|---|---|
| `embeddings_blocks.26` | (n, 4096) | layer 26 activations |
| `embeddings_blocks.31` | (n, 4096) | layer 31 activations |
| `labels` | (n,) | 1 = coding, 0 = non-coding |
| `ids` | (n,) | window ids |

## Organizers

```bash
export NVIDIA_API_KEY=nvapi-...
python extract_evo2_embeddings.py \
    --processed_dir ./processed --out_dir ./embeddings \
    --target_layers blocks.26 blocks.31
```
