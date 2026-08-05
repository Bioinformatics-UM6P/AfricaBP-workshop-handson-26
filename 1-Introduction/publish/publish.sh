#!/usr/bin/env bash
# EEIA — bioAI Workshop
# Author: Généreux Akotenou — PhD student, BioinformaticLabs College of Computing / UM6P
# https://github.com/Genereux-akotenou/EEIA-bioAI-Workshop
# Licensed under the MIT License. See LICENSE at the repo root.
#
# publish.sh — publie la version ÉTUDIANTE (sans solutions) vers le dépôt public.
#
#   Dépôt source (celui-ci)  : tout, y compris les solution/
#   Dépôt public             : la MÊME chose, sans les solution/
#
# Les étudiants reçoivent donc les génomes bruts (2-data/raw/) et les fenêtres
# étiquetées (2-data/processed/) exactement comme ici. Seuls restent dehors :
#   - les solution/          : c'est le but
#   - 1-Introduction/presentation/ : sources LaTeX du diaporama (le PDF part)
#   - 2-data/embeddings/     : fichiers de 100+ Mo, refusés par GitHub, servis
#                              via Drive (voir 2-data/embeddings/README.md)
#   - les secrets et poids   : .env, *.pt
#
# Le dépôt public a son PROPRE historique : rien de l'historique privé n'y passe
# (important — l'ancienne clé NVIDIA est encore dans l'historique d'ici).
#
# Usage
# -----
#   bash 1-Introduction/publish/publish.sh --dry-run      # simulation
#   bash 1-Introduction/publish/publish.sh                # publier
#   bash 1-Introduction/publish/publish.sh -m "Jour 3"    # message de commit
#   bash 1-Introduction/publish/publish.sh --no-raw       # sans les génomes FASTA
#   bash 1-Introduction/publish/publish.sh --no-processed # sans les CSV
#
set -euo pipefail

# ---------------------------------------------------------------- configuration
PUBLIC_REPO="${PUBLIC_REPO:-Genereux-akotenou/EEIA-bioAI-Workshop-project}"
WORK_DIR="${WORK_DIR:-$HOME/.cache/eeia-publish}"
MAX_FILE_MB=95            # GitHub refuse au-delà de 100 Mo

# ce script vit dans <racine>/1-Introduction/publish/ → deux niveaux au-dessus
SRC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLONE_DIR="$WORK_DIR/$(basename "$PUBLIC_REPO")"

DRY_RUN=0
WITH_PROCESSED=1          # par défaut les étudiants ont les mêmes données
WITH_RAW=1
COMMIT_MSG=""

while [ $# -gt 0 ]; do
    case "$1" in
        --dry-run)        DRY_RUN=1 ;;
        --no-processed)   WITH_PROCESSED=0 ;;
        --no-raw)         WITH_RAW=0 ;;
        -m|--message)     COMMIT_MSG="${2:-}"; shift ;;
        -h|--help)        sed -n '7,32p' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "Option inconnue : $1" >&2; exit 2 ;;
    esac
    shift
done

say()  { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m /!\\\033[0m %s\n' "$*" >&2; }
die()  { printf '\033[1;31mERREUR\033[0m %s\n' "$*" >&2; exit 1; }

# ---------------------------------------------------------------- prérequis
command -v git   >/dev/null || die "git est introuvable."
command -v rsync >/dev/null || die "rsync est introuvable."
command -v gh    >/dev/null || warn "gh introuvable : le dépôt public doit déjà exister."

# ---------------------------------------------------------------- dépôt public
mkdir -p "$WORK_DIR"

# En simulation on ne touche à rien de distant : on copie dans un dossier
# temporaire, uniquement pour faire tourner les garde-fous.
if [ "$DRY_RUN" -eq 1 ] && [ ! -d "$CLONE_DIR/.git" ]; then
    CLONE_DIR="$(mktemp -d)"
    say "Simulation dans $CLONE_DIR (aucun dépôt distant créé)"
elif [ ! -d "$CLONE_DIR/.git" ]; then
    if ! git clone "https://github.com/$PUBLIC_REPO.git" "$CLONE_DIR" 2>/dev/null; then
        command -v gh >/dev/null || die "Dépôt $PUBLIC_REPO introuvable et gh absent."
        say "Création du dépôt public $PUBLIC_REPO"
        gh repo create "$PUBLIC_REPO" --public \
           --description "Atelier bioIA — EEIA : version étudiante (sans solutions)" \
           --clone --add-readme >/dev/null
        mv "$(basename "$PUBLIC_REPO")" "$CLONE_DIR" 2>/dev/null || \
            git clone "https://github.com/$PUBLIC_REPO.git" "$CLONE_DIR"
    fi
else
    say "Mise à jour du clone public"
    git -C "$CLONE_DIR" pull --ff-only origin HEAD >/dev/null 2>&1 || true
fi

# ---------------------------------------------------------------- synchronisation
say "Copie de $SRC_ROOT → $CLONE_DIR (hors solutions)"

RSYNC_ARGS=(
    -a --delete
    --exclude '.git/'
    --exclude '.DS_Store'
    --exclude '__pycache__/'
    --exclude '*.pyc'
    --exclude 'solution/'          # <<< le cœur du sujet
    --exclude 'publish/'           # outillage organisateur (ce script)
    --exclude 'presentation/'      # sources LaTeX du diaporama (le PDF, lui, part)
    --exclude '*.pt'               # poids de modèles (teacher_mlp.pt…)
    --exclude '*_partial_*.npy'    # restes d'extraction interrompue
    --exclude '*_checkpoint.json'
    --exclude '.venv/'
    --exclude '.env'
    --exclude '.env.*'
)

[ "$WITH_PROCESSED" -eq 1 ] || RSYNC_ARGS+=( --exclude '2-data/processed/' )
[ "$WITH_RAW"       -eq 1 ] || RSYNC_ARGS+=( --exclude '2-data/raw/' )
# Les .npz font 100+ Mo : jamais sur GitHub. On garde quand même le README,
# c'est lui qui donne le lien Drive aux étudiants.
RSYNC_ARGS+=(
    --include '2-data/embeddings/'
    --include '2-data/embeddings/README.md'
    --exclude '2-data/embeddings/*'
)

# le contenu de l'atelier est à la racine du dépôt (1-Introduction/, 2-data/,
# day1..day5/, README.md, LICENSE) : on synchronise racine → racine.
rsync "${RSYNC_ARGS[@]}" "$SRC_ROOT/" "$CLONE_DIR/"

# ---------------------------------------------------------------- garde-fous
say "Vérifications avant publication"
FAIL=0

if find "$CLONE_DIR" -path "$CLONE_DIR/.git" -prune -o -type d -name solution -print \
     | grep -q .; then
    warn "un dossier solution/ subsiste dans la copie publique"; FAIL=1
fi

if find "$CLONE_DIR" -path "$CLONE_DIR/.git" -prune -o -type f -name '*.pt' -print \
     | grep -q .; then
    warn "un fichier de poids .pt subsiste"; FAIL=1
fi

if find "$CLONE_DIR" -path "$CLONE_DIR/.git" -prune -o \
     \( -type d -name presentation -o -type f -name '*.tex' \) -print | grep -q .; then
    warn "les sources LaTeX du diaporama subsistent dans la copie publique"; FAIL=1
fi

# une vraie clé, pas le placeholder « nvapi-... » de la documentation
KEYFILES=$(grep -rIlE --exclude-dir=.git 'nvapi-[A-Za-z0-9_-]{20,}' "$CLONE_DIR" 2>/dev/null || true)
if [ -n "$KEYFILES" ]; then
    warn "une clé API NVIDIA est présente dans :"
    printf '      %s\n' $KEYFILES >&2
    FAIL=1
fi

BIG=$(find "$CLONE_DIR" -path "$CLONE_DIR/.git" -prune -o -type f \
        -size +${MAX_FILE_MB}M -print 2>/dev/null || true)
if [ -n "$BIG" ]; then
    warn "fichiers au-dessus de ${MAX_FILE_MB} Mo (GitHub les refusera) :"
    printf '      %s\n' $BIG >&2
    FAIL=1
fi

# la version étudiante ne doit pas contenir de code déjà rempli à la place des TODO
if ! grep -rq --exclude-dir=.git 'TODO' "$CLONE_DIR" 2>/dev/null; then
    warn "aucun 'TODO' trouvé : est-ce bien la version étudiante ?"; FAIL=1
fi

[ "$FAIL" -eq 0 ] || die "publication annulée (voir les avertissements ci-dessus)."
say "Contrôles OK"

# ---------------------------------------------------------------- commit + push
if [ "$DRY_RUN" -eq 1 ]; then
    say "--dry-run : rien n'a été copié ni poussé."
    exit 0
fi

cd "$CLONE_DIR"
if [ -z "$(git status --porcelain)" ]; then
    say "Aucun changement à publier."
    exit 0
fi

git status --short | sed 's/^/    /'
SRC_SHA="$(git -C "$SRC_ROOT" rev-parse --short HEAD 2>/dev/null || echo '?')"
[ -n "$COMMIT_MSG" ] || COMMIT_MSG="Mise à jour du matériel étudiant"

git add -A
git commit -m "$COMMIT_MSG" -m "Publié depuis la source $SRC_SHA (sans solutions)." >/dev/null
git push origin HEAD

say "Publié sur https://github.com/$PUBLIC_REPO"
