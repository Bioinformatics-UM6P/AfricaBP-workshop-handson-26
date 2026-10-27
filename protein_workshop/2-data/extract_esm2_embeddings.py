#!/usr/bin/env python3
"""
Extract ESM2 embeddings for protein sequences.
ESSM2 is Meta's protein language model.
"""

import argparse
import numpy as np
import pandas as pd
import torch
from pathlib import Path
from tqdm import tqdm
from Bio import SeqIO
from io import StringIO
import esm

# ESM2 model options
ESM2_MODELS = {
    "esm2_t6_8M_UR50D": 320,      # 8M parameters, 320 dim
    "esm2_t12_35M_UR50D": 480,    # 35M parameters, 480 dim
    "esm2_t30_150M_UR50D": 640,   # 150M parameters, 640 dim
    "esm2_t33_650M_UR50D": 1280,  # 650M parameters, 1280 dim
    "esm2_t36_3B_UR50D": 2560,    # 3B parameters, 2560 dim
}

def load_esm2_model(model_name="esm2_t12_35M_UR50D", device="cuda"):
    """Load ESM2 model and alphabet."""
    print(f"Loading ESM2 model: {model_name}")
    print(f"Device: {device}")
    
    model, alphabet = esm.pretrained.load_model_and_alphabet(model_name)
    model = model.to(device).eval()
    batch_converter = alphabet.get_batch_converter()
    
    hidden_dim = model.embed_dim
    n_layers = model.num_layers
    print(f"  hidden_dim={hidden_dim} | n_layers={n_layers}")
    
    return model, batch_converter, hidden_dim, n_layers

def extract_embeddings(sequences, model, batch_converter, device="cuda",
                       batch_size=8, n_layers=12, pooling="mean", max_seq_length=1024):
    """Extract ESM2 embeddings."""
    model = model.to(device).eval()
    all_embs = []
    
    # Use last layer by default
    repr_layer = n_layers
    
    for start in tqdm(range(0, len(sequences), batch_size), desc="Extracting"):
        batch = sequences[start : start + batch_size]
        
        # Truncate sequences to max length
        batch = [seq[:max_seq_length] for seq in batch]
        
        # Prepare batch data
        batch_labels = [f"seq_{i}" for i in range(len(batch))]
        batch_strs = batch
        data = list(zip(batch_labels, batch_strs))
        
        batch_tokens = batch_converter(data)[2].to(device)
        
        with torch.no_grad():
            if pooling == "mean":
                # Extract mean of all layers
                results = model(batch_tokens, repr_layers=[repr_layer])
                token_representations = results["representations"][repr_layer]
                
                # Remove batch and cls tokens (first and last)
                token_representations = token_representations[:, 1:-1, :]
                
                # Mean pooling
                emb = token_representations.mean(dim=1)
            else:
                # Use CLS token (first token)
                results = model(batch_tokens, repr_layers=[repr_layer])
                token_representations = results["representations"][repr_layer]
                emb = token_representations[:, 0, :]
        
        all_embs.append(emb.cpu().float().numpy())
    
    return np.concatenate(all_embs, axis=0)

def process_fasta_file(fasta_path, model, batch_converter, output_dir,
                        class_name, device="cuda", max_samples=None, n_layers=12):
    """Process a single FASTA file."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse FASTA
    sequences = []
    ids = []
    with open(fasta_path) as f:
        for record in SeqIO.parse(f, "fasta"):
            # Clean sequence: remove '*' (stop codon) and other non-standard chars
            seq = str(record.seq).replace('*', '').replace('X', '').replace('B', '').replace('Z', '').replace('J', '').replace('O', '').replace('U', '')
            sequences.append(seq)
            ids.append(record.id)
    
    # Subsample if needed
    if max_samples is not None and len(sequences) > max_samples:
        print(f"Subsampling to {max_samples} samples")
        indices = np.random.choice(len(sequences), max_samples, replace=False)
        sequences = [sequences[i] for i in indices]
        ids = [ids[i] for i in indices]
    
    print(f"[{class_name}] Processing {len(sequences)} sequences...")
    
    # Extract embeddings
    embeddings = extract_embeddings(sequences, model, batch_converter, device, n_layers=n_layers)
    
    # Save
    npz_path = output_dir / f"{class_name}.npz"
    np.savez(
        npz_path,
        embeddings=embeddings,
        ids=np.array(ids),
        class_name=class_name
    )
    
    print(f"[{class_name}] Saved to {npz_path}")
    print(f"  Shape: {embeddings.shape}")

def main():
    parser = argparse.ArgumentParser(description="Extract ESM2 embeddings for protein sequences")
    parser.add_argument("--raw_dir", default="protein_workshop/2-data/raw",
                        help="Path to raw FASTA files directory")
    parser.add_argument("--out_dir", default="protein_workshop/2-data/embeddings",
                        help="Path to output embeddings directory")
    parser.add_argument("--model", default="esm2_t12_35M_UR50D",
                        choices=list(ESM2_MODELS.keys()),
                        help="ESM2 model to use")
    parser.add_argument("--max_samples", type=int, default=None,
                        help="Max samples per class (None for all)")
    parser.add_argument("--device", default="cuda",
                        help="Device to use (cuda or cpu)")
    
    args = parser.parse_args()
    
    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    
    # Load model
    model, batch_converter, hidden_dim, n_layers = load_esm2_model(args.model, args.device)
    
    # Process each FASTA file
    fasta_files = sorted(raw_dir.glob("*.fas"))
    
    for fasta_path in fasta_files:
        class_name = fasta_path.stem
        process_fasta_file(fasta_path, model, batch_converter, out_dir,
                          class_name, args.device, args.max_samples, n_layers)
    
    print("\nDone!")

if __name__ == "__main__":
    main()

