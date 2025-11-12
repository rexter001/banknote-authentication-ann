# Banknote Authentication - ANN

This repository contains a Jupyter notebook `Banknote_Authentication_ANN.ipynb` that trains a simple Artificial Neural Network (ANN) to classify banknotes as genuine or forged using the UCI Banknote Authentication dataset.

Contents
- `Banknote_Authentication_ANN.ipynb` - Notebook with data loading, exploration, preprocessing, model training, evaluation, and model saving.

How to run locally
1. Create a virtual environment (recommended):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Place the dataset CSV in the same folder and open the notebook in Jupyter or VS Code.

Notes
- The notebook includes Colab-specific helpers (e.g., `files.upload()`). Remove or adapt these if running locally.
- If the notebook saves a Keras model (`.h5`), you may need h5py installed.
