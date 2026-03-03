# Medical NER with LoRA Fine-Tuning

A weekend project exploring parameter-efficient fine-tuning for medical named entity recognition. I wanted to see if LoRA could work well on medical text without needing to retrain entire models.

## What This Does

Extracts medical entities (conditions, medications, procedures, anatomy) from clinical notes using a fine-tuned DistilBERT model with LoRA adapters.

**Example:**
```
Input: "Patient with hypertension, started on lisinopril 10mg daily."

Output:
- CONDITION: hypertension
- MEDICATION: lisinopril
```

## Results

On a test set of 200 clinical notes:
- F1: 96.88%
- Training time: ~2 minutes on T4 GPU
- Trainable params: 597K (0.89% of full model)

The F1 score was surprisingly high - I'm using weak supervision for labeling so I'd take this with a grain of salt. Need to validate on proper benchmark datasets.

## How It Works

1. **Data**: AGBonnet/augmented-clinical-notes (30K synthetic clinical notes)
2. **Labeling**: Weak supervision with regex patterns (not ideal, but good enough for experimentation)
3. **Model**: DistilBERT-base-uncased
4. **Adapter**: LoRA (rank=32, alpha=64)
5. **Task**: Token classification with BIO tagging

## Setup

```bash
# Clone and install
git clone https://github.com/yourusername/medical-ner-lora.git
cd medical-ner-lora
pip install -r requirements.txt
```

## Usage

### Fine-Tuning

Open `notebooks/01_fine_tuning_lora.ipynb` in Google Colab (recommended) or Jupyter:
- Works on free Colab T4 GPU
- Takes ~2 minutes to train
- Saves LoRA adapters to `medical_ner_finetuning/model/`

### Inference

Open `notebooks/02_inference_demo.ipynb` to:
- Load the fine-tuned model
- Run predictions on new clinical notes
- Extract and visualize entities

### Scripts

```bash
# Generate ICD-10 mappings from dataset
python scripts/generate_icd_mappings.py

# Evaluate saved model
python scripts/evaluate_model.py
```

## Project Structure

```
medical-ner-lora/
├── notebooks/
│   ├── 01_fine_tuning_lora.ipynb      # Training notebook
│   └── 02_inference_demo.ipynb        # Inference + demo
├── scripts/
│   ├── generate_icd_mappings.py       # Extract conditions from 30K notes
│   └── evaluate_model.py              # Quick model evaluation
├── data/
│   ├── icd_mapping.json               # 50 medical conditions → ICD-10 codes
│   └── critical_conditions.json       # 20 critical conditions
├── requirements.txt
├── LICENSE
└── README.md
```

## What I Learned

### What Worked Well
- **LoRA is fast**: Training in 2 minutes vs hours for full fine-tuning
- **Small adapter size**: 2.3 MB vs 268 MB for full model
- **Good F1 score**: 96.9% on test set (though see limitations below)

### Challenges & Limitations
- **Weak supervision labels**: Using regex patterns isn't perfect. Entities get missed and there are false positives.
- **Synthetic data**: AGBonnet dataset is augmented/synthetic. Real clinical notes would be messier.
- **No proper benchmark**: Should test on i2b2 or n2c2 datasets to see actual performance.
- **Subword tokenization issues**: Had to handle DistilBERT's WordPiece tokens carefully to merge entities properly.
- **High F1 might be misleading**: Model might be overfitting to the regex patterns used for labeling.

## Future Improvements

- [ ] Evaluate on real benchmark (i2b2/n2c2 2009 dataset)
- [ ] Try other base models (BioBERT, ClinicalBERT)
- [ ] Experiment with different LoRA ranks
- [ ] Add relation extraction (e.g., medication → condition links)
- [ ] Handle negation and uncertainty ("no fever", "possible pneumonia")
- [ ] Try active learning to improve labels

## Technical Details

### LoRA Configuration
```python
LoraConfig(
    r=32,              # Rank
    lora_alpha=64,     # Scaling factor
    lora_dropout=0.1,
    target_modules=["q_lin", "v_lin"],  # Only adapt query/value
    bias="none"
)
```

### Training Hyperparameters
```python
learning_rate = 2e-3   # Higher LR works better for LoRA
epochs = 10
batch_size = 16
weight_decay = 0.01
```

### Why These Settings?
- **High learning rate (2e-3)**: LoRA adapters can handle aggressive learning rates
- **Rank 32**: Balance between capacity and efficiency
- **Alpha 64**: Strong adaptation signal (alpha/rank = 2.0)

## References

- LoRA paper: [Hu et al., 2021](https://arxiv.org/abs/2106.09685)
- Dataset: [AGBonnet/augmented-clinical-notes](https://huggingface.co/datasets/AGBonnet/augmented-clinical-notes)
- PEFT library: [Hugging Face PEFT](https://github.com/huggingface/peft)

## License

MIT License - see [LICENSE](LICENSE)

---

**Note**: This is an educational project. Not validated for clinical use.
