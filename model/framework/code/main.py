# N. gonorrhoeae antibiotic activity predictor (Chemprop D-MPNN ensemble).
#
# Source model: jackievaleri/ngonorrhoeae_abx_ml_discovery (Anahtar et al.,
# Sci. Transl. Med. 2026, scitranslmed.ads4699). This wraps the "Round 2"
# model (FINALbayHO11152022), trained on Pharmakon + Internal-37K + the first
# round of experimental validation hits. It is the authors' designated
# quick-start model and the one that surfaced compound A1, which was tested in
# the in vivo mouse vaginal infection model. It is a 50-checkpoint ensemble
# (5 folds x 10 models) trained with Chemprop v1.5.1 on RDKit-2D-normalized
# features and --no_features_scaling.
#
# Checkpoints are NOT committed to git. They live under ../../checkpoints/
# (fold_*/model_*/model.pt) and are fetched at runtime from S3 via eosvc.

import os
import csv
import sys
import tempfile

import numpy as np
from ersilia_pack_utils.core import read_smiles, write_out

from chemprop.args import PredictArgs
from chemprop.train import make_predictions
from chemprop.features import get_features_generator

# rdkit_2d_normalized descriptor length (descriptastorus); used as a fallback
# row width when the very first molecule is itself unparseable.
N_FEATURES = 200

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# current file directory
root = os.path.dirname(os.path.abspath(__file__))

# ensemble checkpoint directory (resolved relative to this file, never hardcoded)
CHECKPOINT_DIR = os.path.abspath(os.path.join(root, "..", "..", "checkpoints"))


def compute_features(smiles_list):
    """Pre-compute RDKit-2D-normalized features (one row per input SMILES).

    The model was trained with --features_path (a saved .npz), and chemprop
    requires the same feature *source* at prediction time, so we reproduce the
    authors' save_features step in-process rather than using --features_generator.
    Unparseable SMILES get a zero row; chemprop flags them as "Invalid SMILES"
    and ignores those rows, so the placeholder values never reach the model.
    """
    generator = get_features_generator("rdkit_2d_normalized")
    rows = []
    width = None
    for smi in smiles_list:
        try:
            feats = np.asarray(generator(smi), dtype=float)
            width = width or len(feats)
            rows.append(feats)
        except Exception:
            rows.append(None)
    width = width or N_FEATURES
    rows = [r if r is not None else np.zeros(width) for r in rows]
    return np.asarray(rows, dtype=float)


def my_model(smiles_list):
    """Run the Chemprop ensemble and return one activity probability per SMILES.

    Mirrors the chemprop_predict CLI the authors used (rdkit_2d_normalized
    features supplied via --features_path, --no_features_scaling). Invalid /
    unparseable SMILES come back as NaN, in input order.
    """
    features = compute_features(smiles_list)

    with tempfile.TemporaryDirectory() as tmp:
        in_csv = os.path.join(tmp, "input.csv")
        preds_csv = os.path.join(tmp, "preds.csv")
        feats_npz = os.path.join(tmp, "features.npz")

        with open(in_csv, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["smiles"])
            for smi in smiles_list:
                writer.writerow([smi])
        np.savez(feats_npz, features=features)

        args = PredictArgs().parse_args([
            "--test_path", in_csv,
            "--preds_path", preds_csv,
            "--checkpoint_dir", CHECKPOINT_DIR,
            "--smiles_columns", "smiles",
            "--features_path", feats_npz,
            "--no_features_scaling",
            "--num_workers", "0",
        ])
        # return_invalid_smiles (default True) keeps output aligned 1:1 with input
        make_predictions(args)

        with open(preds_csv, "r", newline="") as f:
            rows = list(csv.DictReader(f))

    # the single non-smiles column holds the predicted "hit" probability
    target_col = [c for c in rows[0].keys() if c != "smiles"][0]
    outputs = []
    for row in rows:
        try:
            val = float(row[target_col])
        except (ValueError, TypeError):
            val = float("nan")  # "Invalid SMILES" -> NaN (clipped by write_out)
        outputs.append([val])
    return outputs


# read SMILES from .csv/.bin file, assuming one column with header
_, smiles_list = read_smiles(input_file)

# run model
outputs = my_model(smiles_list)

# check input and output have the same length
assert len(smiles_list) == len(outputs)

# write output
header = ["activity_score"]
write_out(outputs, header, output_file, np.float32)
