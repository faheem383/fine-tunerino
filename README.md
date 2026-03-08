# Fine-Tunerino

A GPT-2 fine-tuning notebook that teaches a pre-trained language model new knowledge from custom PDF documents. This is the **local development starting point** for the MLOps capstone project.

## What It Does

1. **Extracts text** from PDF files in `data/pdfs/`
2. **Tokenizes** the text using the GPT-2 tokenizer
3. **Fine-tunes** the pre-trained GPT-2 model on your documents
4. **Generates text** using the fine-tuned model

## Quick Start

### 1. Set up the environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### 2. Add your training data

Place PDF files in the `data/pdfs/` folder. A sample `declaration.pdf` is included.

### 3. Run the notebook

```bash
jupyter notebook main.ipynb
```

Run all cells in order. Training takes a few minutes on CPU, faster on GPU.

## Project Structure

```
fine-tunerino/
├── main.ipynb          # Training notebook (run this)
├── requirements.txt    # Python dependencies
└── data/
    └── pdfs/
        └── declaration.pdf   # Sample training document
```

## How It Maps to MLOps

This notebook is the prototype for an automated pipeline on Azure:

| Notebook Step | MLOps Stage | Azure Service |
|---|---|---|
| Extract PDF text | Data Pre-processing | AKS Pod (CPU) |
| Tokenize & prepare | Data Pipeline | AKS Pod (CPU) |
| Configure training | Experiment Config | AML Workspace |
| Fine-tune model | Model Training | AKS Pod (GPU/CPU) |
| Generate text | Model Serving | AKS Inference Endpoint |

## Tips

- **Documents must be in English** (GPT-2 was trained on English text)
- **Don't ask questions** - start the sentence: use `"Declaration: X is"` instead of `"Who is X?"`
- **Small datasets need more epochs** - increase `num_train_epochs` to 20+ and `learning_rate` to 2e-4 to force memorization

## Dependencies

Key libraries: `transformers`, `torch`, `datasets`, `pypdf`, `accelerate`

See `requirements.txt` for the full list.
