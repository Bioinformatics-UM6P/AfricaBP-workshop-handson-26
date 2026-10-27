# AfricaBP: bioAI Workshop · Atelier pratique 2026

**De l'ADN aux modèles**: trois jours pour aller d'un génome bactérien brut
jusqu'à un classifieur minuscule distillé depuis un modèle de fondation génomique.

<!-- Auteur : Généreux Akotenou: PhD student, BioinformaticLabs College of Computing / UM6P
· [dépôt GitHub](https://github.com/Bioinformatics-UM6P/AfricaBP-workshop-handson-26) -->

<div align="center">

### 🎓 &nbsp;DÉPÔT DU CODE ÉTUDIANT&nbsp; 🎓

<a href="https://github.com/Bioinformatics-UM6P/AfricaBP-workshop-handson-26">
<img src="https://img.shields.io/badge/GitHub-AfricaBP--workshop--handson--26-2ea44f?style=for-the-badge&logo=github&logoColor=white" alt="Dépôt étudiant">
</a>

**👉 &nbsp;<https://github.com/Bioinformatics-UM6P/AfricaBP-workshop-handson-26>&nbsp; 👈**

```bash
git clone https://github.com/Bioinformatics-UM6P/AfricaBP-workshop-handson-26.git
```

*C'est le dépôt à cloner pour suivre l'atelier.*
*Les embeddings Evo2 se téléchargent séparément —*
*voir [`2-data/embeddings/README.md`](2-data/embeddings/README.md).*

</div>

---

## 1. Commencez par lire le guide

**Avant d'ouvrir le moindre notebook**, lisez [`1-Introduction/guide.md`](1-Introduction/guide.md).
Il pose le contexte biologique, la tâche à résoudre (codant vs non-codant), le déroulé de
l'atelier et ce qui est attendu comme livrable. Les notebooks supposent que vous l'avez lu.

La présentation d'ouverture est dans [`1-Introduction/presentation`](1-Introduction/presentation)
(ouvrez-la simplement dans un navigateur).

## 2. Préparez l'environnement Jupyter

<!-- Toutes les commandes ci-dessous se lancent **depuis ce dossier `AfricaBP-workshop-handson-26/`**.
Python **3.10 ou plus récent** est requis. -->

### Option A: `venv` (recommandée, aucune installation supplémentaire)

```bash
# 1. créer l'environnement
python3 -m venv .venv

# 2. l'activer
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows (PowerShell)

# 3. installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 4. enregistrer l'environnement comme noyau Jupyter
python -m ipykernel install --user --name africabp-handson --display-name "(africabp-handson)"
```

### Option B: `conda`

```bash
conda create -n africabp-handson python=3.11 -y
conda activate africabp-handson
pip install -r requirements.txt
python -m ipykernel install --user --name africabp-handson --display-name "(africabp-handson)"
```

### Lancer Jupyter

```bash
jupyter lab        # ou : jupyter notebook
```

Dans chaque notebook, sélectionnez le noyau **«(africabp-handson) »**
(menu *Kernel → Change Kernel*). Si vous ne le voyez pas, relancez l'étape
`ipykernel install` puis rechargez la page.

### Vérifier que tout fonctionne

```bash
python -c "import numpy, pandas, sklearn, torch, matplotlib; print('OK', torch.__version__)"
```

### Dépendances

| Paquet | À quoi il sert |
| --- | --- |
| `numpy`, `pandas` | manipulation des séquences et des splits CSV |
| `scikit-learn` | régression logistique, métriques, PCA |
| `torch` | CNN one-hot, tête MLP du teacher, student distillé, SAE |
| `matplotlib` | tous les graphiques |
| `umap-learn` | projection 2D optionnelle des embeddings (`plot_embedding_space(method="umap")`) |
| `requests` | appels à l'API NVIDIA NIM pour Evo2 (Lab 2) |
| `tqdm` | barres de progression lors de l'extraction d'embeddings |
| `jupyter`, `ipykernel` | exécution des notebooks |

> **CPU suffit.** Aucun GPU n'est nécessaire : les embeddings Evo2 sont pré-calculés et
> fournis, et tous les modèles entraînés pendant l'atelier sont petits.

## 3. Déroulé de l'atelier

| Dossier | Notebook | Contenu |
| --- | --- | --- |
| `1-Introduction/` | `guide.md`, `presentation.html` | contexte, biologie, organisation |
| `2-data/` | `build_dataset.py`, `extract_evo2_embeddings.py` | scripts fournis + données `raw/` et `processed/` |
| `lab1/` | `00_biology_intro_and_data_setup.ipynb` | ADN codant vs non-codant, des FASTA/GFF aux fenêtres étiquetées |
| `lab1/` | `01_kmer_and_cnn_baselines.ipynb` | k-mers + régression logistique, one-hot + CNN |
| `lab2/` | `02_evo2_embeddings_and_classifier.ipynb` | embeddings Evo2 + tête MLP (le « teacher ») |
| `lab3/` | `03_knowledge_distillation.ipynb` | distillation du teacher vers un student minuscule |
| `lab4/` | `04_compression_analysis_and_wrapup.ipynb` | compromis précision / taille / latence, bilan |
| `lab5/` | `bonus_sparse_autoencoder_interpretability.ipynb` | piste bonus : autoencodeurs parcimonieux |
| `labBonus/` | `protein_classification_esm2.ipynb` | extension protéines : embeddings ESM2 + classifieur |

Répartition sur les trois jours : **Jour 1** → Lab 0–1 · **Jour 2** → Lab 2–3 ·
**Jour 3** → Lab 4–5 + présentations. Le `labBonus/` est en libre accès.

Suivez l'ordre des labs : chaque notebook réutilise les chiffres ou les modèles du
précédent, et le graphique final du Lab 4 rassemble tout.

## 4. Comment travailler dans les notebooks

- Chaque notebook commence par une cellule **« Votre identité »** : double-cliquez dessus
  et complétez nom, binôme et date avant de commencer.
- Les cellules à compléter sont marquées `# TODO :`: remplacez les `...` par votre code.
- Chaque dossier `labN/` contient un sous-dossier `src/` avec le code d'infrastructure
  déjà écrit (chargement des données, métriques, graphiques) : à utiliser tel quel.
- Un sous-dossier `solution/` accompagne chaque lab avec la version corrigée complète.
  **Essayez d'abord par vous-même**: la solution est là pour se débloquer, pas pour
  démarrer.

## 5. Licence

Code sous licence **MIT** (voir [`LICENSE`](../LICENSE) à la racine du dépôt).
Si vous réutilisez ce matériel pédagogique, merci de citer l'auteur.
