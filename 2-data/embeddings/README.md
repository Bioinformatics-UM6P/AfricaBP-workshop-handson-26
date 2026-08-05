# Workshop data — download instructions

The datasets for this workshop are **not stored in this repository**. Genome FASTA
files and Evo2 activation dumps run to several hundred megabytes, which would make
the repo slow to clone and push (GitHub also rejects any single file over 100 MB).

Everything lives on Google Drive instead. Download it once, drop it into the
folders below, and the notebooks will find it.

> ### 📥 [**Download the workshop data from Google Drive**](https://drive.google.com/drive/folders/1TL1p0ezAXUrGORAoHr7aVtc0YcxE-5ve?usp=drive_link)

If you hit a permission screen, make sure you're signed in to Google and ask the
organizer to grant access.

---

## What you need

### 1. Evo2 embeddings → `2-data/embeddings/`

Pre-extracted by the organizer, so the workshop never depends on live NVIDIA NIM
API availability or quota. Used from **notebook 02** (teacher classifier) onward.

| File | Size | md5 |
|---|---|---|
| `train.npz` | 187.6 MB | `f29b5eca1b386bbe7b4e0129a9437e3b` |
| `val_partial_blocks.26.npy` | 15.6 MB | `6303d760d1087e20c735882afef813ec` |
| `val_partial_blocks.31.npy` | 15.6 MB | `f12bd4721c3c73c830e36a1b207ef246` |
| `val_checkpoint.json` | <1 KB | `61ac13f9b6b84fe7c68739e58f9fdda2` |

**`train.npz` contents** — 4000 windows, Evo2-7b, mean-pooled per window:

| Array | Shape | dtype | Notes |
|---|---|---|---|
| `embeddings_blocks.26` | (4000, 4096) | float32 | layer 26 activations |
| `embeddings_blocks.31` | (4000, 4096) | float32 | layer 31 (last block) |
| `embeddings` | (4000, 4096) | float32 | duplicate of `blocks.26` — kept for backwards compat |
| `labels` | (4000,) | int64 | 1 = coding (CDS), 0 = non-coding |
| `ids` | (4000,) | object | window ids matching `processed/train.csv` |
| `layers` | (2,) | <U9 | `['blocks.26', 'blocks.31']` |

Load it with:

```python
import numpy as np
d = np.load("2-data/embeddings/train.npz", allow_pickle=True)   # allow_pickle needed for `ids`
X, y = d["embeddings_blocks.26"], d["labels"]
```

Two things to know:

- `allow_pickle=True` is required — `ids` is an object array of strings.
- The `val_partial_*` files are **partial**. Extraction stopped at index 250 of
  1000 (see `val_checkpoint.json`), so they cover only the first 250 validation
  windows. Use `processed/val.csv` if you need the full validation split.

### 2. Processed windows → `2-data/processed/`

Labeled 200 bp coding/non-coding windows built from the raw genomes by
`build_dataset.py`. Used from **notebook 01** (k-mer and CNN baselines).

| File | Size | md5 |
|---|---|---|
| `train.csv` | 15.6 MB | `3e20158fe4fac68e445f92706b0f1d62` |
| `val.csv` | 2.7 MB | `2f21a3940e967c709ce97ed9cdbafa2b` |
| `test.csv` | 4.6 MB | `8040adc409cf00b1fd48bd40022d6f1f` |

Columns: `id, split, organism, seqid, start, end, strand, label, sequence`
(`label`: 1 = coding/CDS window, 0 = non-coding/intergenic).

### 3. Raw genomes → `2-data/raw/` *(optional)*

Bacterial genome FASTA + matching GFF3 annotations, ~168 MB total.

| Split | Genomes | Size |
|---|---|---|
| `raw/train/` | 20 | 125 MB |
| `raw/val/` | 4 | 25 MB |
| `raw/test/` | 5 | 18 MB |

**Only needed if you want to rebuild the dataset from scratch.** If you just want
to follow the notebooks, skip this and grab `processed/` instead — it's a tenth
of the size.

---

## Where the files go

```
2-data/
├── embeddings/
│   ├── README.md                     ← this file (the only part in git)
│   ├── train.npz
│   ├── val_partial_blocks.26.npy
│   ├── val_partial_blocks.31.npy
│   └── val_checkpoint.json
├── processed/
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
└── raw/                              ← optional
    ├── train/   (20 × .fasta + .gff)
    ├── val/     (4 × .fasta + .gff)
    └── test/    (5 × .fasta + .gff)
```

Notebooks resolve paths relative to the repo root, so keep these exact names.

## Verify your download

```bash
cd 2-data
md5 embeddings/train.npz processed/*.csv     # macOS
md5sum embeddings/train.npz processed/*.csv  # Linux
```

Compare against the tables above. A mismatch usually means Google Drive served an
HTML "file too large to scan" warning page instead of the real file — check the
file size, and if it's a few kilobytes, download it through the browser rather
than with `wget`/`curl`.

---

## Regenerating the data (organizers only)

Students don't need this. Both scripts live in `2-data/`:

```bash
# raw genomes -> labeled windows
python build_dataset.py \
    --raw_dir ./raw --out_dir ./processed \
    --window 200 --stride 200 --max_per_class_per_genome 4000

# labeled windows -> Evo2 embeddings (needs an NVIDIA NIM API key)
export NVIDIA_API_KEY=nvapi-...
python extract_evo2_embeddings.py \
    --processed_dir ./processed --out_dir ./embeddings \
    --max_per_split train=4000 val=1000 test=1000 \
    --target_layers blocks.26 blocks.31
```

Get a key at <https://build.nvidia.com/arc/evo2-7b-forward/modelcard>.
Never commit it — `.env` and `*api_key*` are gitignored.
