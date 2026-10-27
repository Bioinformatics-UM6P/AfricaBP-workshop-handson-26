<h1 align="center">🧬 AI & Biologie: Entrainement d'un model de classification d'ADN & Introduction a la distillation de model</h1>

<p align="center">
  <img src="https://img.shields.io/badge/LAB_0-Kickoff-64748b?style=for-the-badge" alt="Lab 0"/>
  <img src="https://img.shields.io/badge/LAB_1-Biologie%20%2B%20Baselines-5eead4?style=for-the-badge&labelColor=0d1526" alt="Lab 1"/>
  <img src="https://img.shields.io/badge/LAB_2-Embeddings%20Evo2-818cf8?style=for-the-badge&labelColor=0d1526" alt="Lab 2"/>
  <img src="https://img.shields.io/badge/LAB_3-Distillation-f472b6?style=for-the-badge&labelColor=0d1526" alt="Lab 3"/>
  <img src="https://img.shields.io/badge/LAB_4-Efficacité-fbbf24?style=for-the-badge&labelColor=0d1526" alt="Lab 4"/>
  <img src="https://img.shields.io/badge/LAB_5-Bonus%20%2B%20Demos-a78bfa?style=for-the-badge&labelColor=0d1526" alt="Lab 5"/>
  <img src="https://img.shields.io/badge/LAB-Bonus%20Prot%C3%A9ines-94a3b8?style=for-the-badge&labelColor=0d1526" alt="Lab Bonus"/>
</p>

<br>
<a href="presentation.html">
  <div align="center" style="height:10em;display:flex;align-items:center;justify-content:center;background:linear-gradient(90deg,#5eead4,#818cf8);border-radius:12px;margin:1.2em 0;">
    <span style="font-size:1.6em;font-weight:800;color:#04101a;letter-spacing:.06em;">
      🎬 PRÉSENTATION
    </span>
  </div>
</a>
<br>

## 🗺️ Vue d'ensemble

L'atelier dure **trois jours** et se découpe en **labs** :

| | Jour | Lab | Thème | Notebook |
|---|---|---|---|---|
| 🟦 | 1 | **0** | Kickoff & préparation des données | `presentation` |
| 🟩 | 1 | **1** | Biologie + baselines | `00_biology_intro...` · `01_kmer_and_cnn...` |
| 🟪 | 2 | **2** | Embeddings Evo2 | `02_evo2_embeddings...` |
| 🟥 | 2 | **3** | Distillation | `03_knowledge_distillation...` |
| 🟨 | 3 | **4** | Analyse d'efficacité | `04_compression_analysis...` |
| 🟧 | 3 | **5** | Bonus + présentations | `bonus_sparse_autoencoder...` |
| ⬜ | — | **Bonus** | Extension protéines (ESM2) | `labBonus/protein_classification_esm2...` |

**Progression du pipeline :** `🟩🟩🟩🟩🟩`
<br>
<br>

## 📁 Anatomie d'un dossier de lab

```text
AfricaBP-workshop-handson-26/
  lab1/  📗 Biologie + baselines
    ├── <notebooks>.ipynb   ← incomplet : des TODO à remplir, guidés étape par étape
    ├── src/                ← copie locale des modules dont ce lab a besoin — également
    │                          incomplète là où le TODO est l'objectif pédagogique du lab
    └── solution/           ← clone complet : notebooks + src entièrement remplis
  lab2/ 
  …
```

<table width="100%"><tr><td bgcolor="#f3f4f6">

### 🎯 Objectif & méthode de travail

Chaque lab suit le même rythme :

1. 📢 **Nous annonçons l'objectif du lab** - ce qu'on construit et pourquoi (voir le tableau *Vue d'ensemble* ci-dessus).
2. ⬆️ **Nous mettons à jour le dépôt GitHub** avec le nouveau matériel (`labN/` : notebooks + `src/` à compléter).
3. ⬇️ **Vous récupérez le matériel du lab** avec une seule commande (voir ci-dessous).
4. ✍️ **Vous complétez les objectifs** — les `# TODO` des notebooks et de `src/`, guidés étape par étape.
5. 🙋 **Nous passons entre les groupes** — posez toutes vos questions, on est là pour ça.

#### 📥 Récupérer le matériel

**La toute première fois** (cloner le dépôt) :

```bash
git clone https://github.com/Bioinformatics-UM6P/AfricaBP-workshop-handson-26.git
cd AfricaBP-workshop-handson-26
```

**À chaque nouveau lab** (récupérer le nouveau matériel) :

```bash
cd AfricaBP-workshop-handson-26
git pull origin main
```

> ⚠️ Travaillez dans un dossier à vous (ex. `mon_travail/`) ou gardez une copie de vos
> réponses — un `git pull` peut entrer en conflit avec des fichiers que vous avez modifiés.
> En cas de souci, **appelez-nous**, on règle ça ensemble.

</td></tr></table>
<br>

<!-- ******************************** -->
<!-- ******************************** -->
<div align="center">
  <img src="./assets/img1.png" alt="Illustration" width="200">
</div>
<table width="100%"><tr><td bgcolor="#f3f4f6">

## 🟩 Lab 1: Biologie + baselines → [`../lab1/`](../lab1/)

- 📓 [`00_biology_intro_and_data_setup.ipynb`](../lab1/00_biology_intro_and_data_setup.ipynb) : dogme central, FASTA/GFF bruts, d'où viennent les étiquettes.
- 📓 [`01_kmer_and_cnn_baselines.ipynb`](../lab1/01_kmer_and_cnn_baselines.ipynb) : k-mer + régression logistique, one-hot + CNN.
- 📓 `src/` : `data.py` (complet) · `featurize.py` + `models/baselines.py` + `eval.py` (**incomplet**).

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #f59e0b;background:#fff8e6;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🏁 Checkpoint</h4>

  <p style="margin:.3rem 0;">
    Chaque groupe doit reporter les métriques suivantes pour <strong>les deux baselines</strong> :
  </p>

  <ul style="margin:.4rem 0 0 1.2rem;">
    <li><strong>Accuracy</strong></li>
    <li><strong>F1-score</strong></li>
    <li><strong>Nombre de paramètres</strong></li>
    <li><strong>Latence d'inférence</strong></li>
  </ul>
</div>

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #22c55e;background:#f0fdf4;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🔓 Solution</h4>

  <p style="margin:0;">
    La solution complète <strong>(notebooks + code source)</strong> n'est pas fournie dans cette version.
    Elle sera partagée avec vous après le checkpoint.
  </p>
  <!--
  <p style="margin-top:.6rem;">
    📂 <a href="../lab1/solution/"><code>../lab1/solution/</code></a>
  </p>
  -->
</div>
</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br>
<br>


<!-- ******************************** -->
<!-- ******************************** -->
<div align="center">
  <img src="./assets/img2.png" alt="Illustration" width="200">
</div>

<table width="100%"><tr><td bgcolor="#f3f4f6">

## 🟪 Lab 2 : Embeddings Evo2 → [`../lab2/`](../lab2/)

- 📓 [`02_evo2_embeddings_and_classifier.ipynb`](../lab2/02_evo2_embeddings_and_classifier.ipynb):  charger les embeddings pré-calculés, entraîner la tête MLP, visualisation PCA/UMAP.
- 📓 `src/` : `embeddings.py` + `eval.py` (complets) · `models/classifier_heads.py` + `viz.py` (**incomplet**).

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #8b5cf6;background:#f5f3ff;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🏁 Checkpoint</h4>

  <p style="margin:0;">
    Le classifieur <strong>Evo2</strong> doit obtenir de meilleures performances que les
    <strong>deux baselines du Lab&nbsp;1</strong>.
  </p>
</div>

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #22c55e;background:#f0fdf4;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🔓 Solution</h4>

  <p style="margin:0;">
    La solution complète <strong>(notebooks + code source)</strong> sera partagée avec vous après le checkpoint.
  </p>

  <!--
  <p style="margin-top:.6rem;">
    📂 <a href="../lab2/solution/"><code>../lab2/solution/</code></a>
  </p>
  -->
</div>

</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br><br>



<!-- ******************************** -->
<!-- ******************************** -->
<div align="center">
  <img src="./assets/img3.png" alt="Illustration" width="200">
</div>

<table width="100%"><tr><td bgcolor="#f3f4f6">

## 🟥 Lab 3 : Distillation de connaissances → [`../lab3/`](../lab3/)

- 📓 [`03_knowledge_distillation.ipynb`](../lab3/03_knowledge_distillation.ipynb) : INtroduction a la distaillation - teacher → student.
- 📓 `src/` : `data.py`, `embeddings.py`, `featurize.py`, `models/classifier_heads.py`, `eval.py` (complets, portés) · `models/distillation.py` (**incomplet**).

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #ef4444;background:#fef2f2;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🏁 Checkpoint</h4>

  <p style="margin:0;">
    Le modèle <strong>Student</strong> doit récupérer l'essentiel des performances du
    <strong>Teacher</strong> tout en étant significativement plus léger et plus rapide.
  </p>
</div>

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #22c55e;background:#f0fdf4;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🔓 Solution</h4>

  <p style="margin:0;">
    La solution complète <strong>(notebooks + code source)</strong> sera partagée avec vous après le checkpoint.
  </p>

  <!--
  <p style="margin-top:.6rem;">
    📂 <a href="../lab3/solution/"><code>../lab3/solution/</code></a>
  </p>
  -->
</div>
</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br><br>


<!-- ******************************** -->
<!-- ******************************** -->
<div align="center">
  <img src="./assets/img4.png" alt="Illustration" width="200">
</div>

<table width="100%"><tr><td bgcolor="#f3f4f6">

## 🟨 Lab 4 : Analyse de compression → [`../lab4/`](../lab4/)

- 📓 [`04_compression_analysis_and_wrapup.ipynb`](../lab4/04_compression_analysis_and_wrapup.ipynb) : un seul graphique, tous les modèles construits pendant l'atelier.
- 📓 `src/` : `viz.py` (**incomplet**, uniquement `plot_efficiency_tradeoff`).

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #eab308;background:#fefce8;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🏁 Checkpoint</h4>

  <p style="margin:0;">
    Produire le graphique d'efficacité comparant l'ensemble des modèles :
  </p>

  <ul style="margin:.5rem 0 0 1.2rem;">
    <li>Baselines</li>
    <li>Teacher</li>
    <li>Student</li>
  </ul>
</div>

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #22c55e;background:#f0fdf4;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🔓 Solution</h4>

  <p style="margin:0;">
    La solution complète <strong>(notebooks + code source, avec des chiffres d'exemple)</strong> sera partagée avec vous après le checkpoint.
  </p>

  <!--
  <p style="margin-top:.6rem;">
    📂 <a href="../lab4/solution/"><code>../lab4/solution/</code></a>
  </p>
  -->
</div>
</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br><br>


<!-- ******************************** -->
<!-- ******************************** -->
<div align="center">
  <img src="./assets/img5.png" alt="Illustration" width="200">
</div>

<table width="100%"><tr><td bgcolor="#f3f4f6">

## 🟧 Lab 5 : Piste bonus + présentations → [`../lab5/`](../lab5/)

- 📓 [`bonus_sparse_autoencoder_interpretability.ipynb`](../lab5/bonus_sparse_autoencoder_interpretability.ipynb) — groupes optionnels/avancés.
- 📓 `src/` : `data.py`, `featurize.py`, `embeddings.py` (complets, portés) · `models/sae.py` + `viz.py` (**incomplet**).

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #f97316;background:#fff7ed;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🎤 Présentations finales</h4>

  <ul style="margin:0 0 0 1.2rem;">
    <li>Chaque groupe présente les résultats de son pipeline principal.</li>
    <li>Les groupes ayant réalisé la piste bonus présentent également leurs analyses SAE.</li>
  </ul>
</div>

<div style="margin:1rem 0;padding:1rem 1.25rem;border-left:5px solid #22c55e;background:#f0fdf4;border-radius:6px;">
  <h4 style="margin:0 0 .6rem 0;">🔓 Solution</h4>

  <p style="margin:0;">
    La solution complète <strong>(notebooks + code source)</strong> sera partagée avec vous après les présentations.
  </p>

  <!--
  <p style="margin-top:.6rem;">
    📂 <a href="../lab5/solution/"><code>../lab5/solution/</code></a>
  </p>
  -->
</div>
</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br><br>



<!-- ******************************** -->
<!-- ******************************** -->
<table width="100%"><tr><td bgcolor="#f3f4f6">

## ⬜ Lab Bonus : Extension protéines (ESM2) → [`../labBonus/`](../labBonus/)

- 📓 [`protein_classification_esm2.ipynb`](../labBonus/protein_classification_esm2.ipynb) : le même pipeline appliqué aux protéines — embeddings ESM2 + classifieur sur 8 familles de facteurs de transcription végétaux.
- 📖 Détails et prérequis dans [`../labBonus/README.md`](../labBonus/README.md).

</td></tr></table>
<div style="height:0.5em; width: 100%; background: #ddd;"></div>
<br><br>
