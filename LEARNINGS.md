# Project Learnings & Notes

Random notes from working on this project. Mostly for my own reference.

## Initial Goals

Wanted to try LoRA for medical NLP after reading the PEFT paper. Main questions:
- Can I get decent NER performance without full fine-tuning?
- How much faster/cheaper is it really?
- Does it work on domain-specific text like medical notes?

## Challenges & Solutions

### 1. Labeling Data (Week 1)

**Problem**: Don't have access to proper annotated medical datasets (i2b2 requires data agreement).

**First attempt**: Tried to manually label 100 notes. Took forever and I'm not a medical expert so labels were probably garbage.

**Solution**: Weak supervision with regex patterns. Not perfect but good enough for prototyping. Used patterns like:
```python
r'\b(hypertension|diabetes|pneumonia|...)\b'
```

**Lesson**: Weak supervision >> no supervision for learning projects. Real production would need proper annotations.

### 2. Subword Tokenization Hell (Week 1-2)

**Problem**: DistilBERT's WordPiece tokenizer splits words unpredictably:
```
"hypertension" → ["hyper", "##tension"]
```

If I label "hyper" as B-CONDITION and "##tension" as I-CONDITION, but then at inference one has different prediction - entities get fragmented.

**Bad output example**:
```
- CONDITION: hyper
- CONDITION: tension  # Wrong! Should be merged
```

**Solution**: Had to write careful label alignment logic:
1. Use `offset_mapping` to track character positions
2. Assign BIO tags based on character spans, not token positions
3. During inference, merge consecutive subwords before displaying

**Code snippet that helped**:
```python
for idx, (token_start, token_end) in enumerate(offset_mapping):
    if token_start < entity_end_char and token_end > entity_start_char:
        # Token overlaps with entity span
        token_indices.append(idx)
```

### 3. LoRA Hyperparameter Tuning (Week 2)

**First try**: Used rank=8, alpha=16, lr=5e-5 (common BERT fine-tuning LR)
- **Result**: F1 = 72% after 10 epochs. Meh.

**Second try**: Increased to rank=16, alpha=32, lr=2e-4
- **Result**: F1 = 86% after 6 epochs. Better but still felt like leaving performance on table.

**Final**: rank=32, alpha=64, lr=2e-3 (much more aggressive)
- **Result**: F1 = 96.9% after 10 epochs. Nice!

**Lesson**: LoRA can handle much higher learning rates than full fine-tuning. The paper mentions this but I was too conservative at first.

### 4. Model Checkpoint Sizes (Week 2)

**Surprise**: LoRA adapters are TINY!
- Full DistilBERT model: 268 MB
- LoRA adapter files: 2.3 MB

This is huge for:
- Git commits (can actually version models!)
- A/B testing (swap adapters instantly)
- Model serving (keep base model in memory, hot-swap adapters)

### 5. Evaluation Reality Check (Week 3)

**Got 96.9% F1 and felt amazing... then realized**:
- Test set came from same distribution as training (AGBonnet dataset)
- My weak supervision labels = regex patterns
- Model probably learned to reproduce my regex patterns
- This is somewhat circular!

**Validation attempt**: Downloaded some real clinical notes from Reddit (de-identified posts from medical subreddits). Performance dropped noticeably - lots of entities missed.

**Lesson**: High metrics on your own test set != real performance. Need external benchmarks.

## Things I'd Do Differently

1. **Get proper benchmark first**: Should've started with i2b2/n2c2 dataset even if it means paperwork.

2. **Try BioBERT/ClinicalBERT as base**: They're pre-trained on medical text, might need less adaptation.

3. **Active learning loop**: Start with weak supervision, but have a way to sample uncertain predictions for manual review.

4. **Better entity coverage**: My regex patterns cover common conditions but miss lots of medical terminology (especially drugs, procedures).

5. **Add context window**: Clinical notes often have important context across sentences. Should probably look at longer sequences or hierarchical models.

## Interesting Findings

### LoRA Target Modules Matter

Only adapted `q_lin` and `v_lin` (query and value projections in attention).

**Tried adding key projection**: Performance barely changed but training slowed down.

**Tried adapter-only (no LoRA)**: Performance dropped to 89% F1.

**Lesson**: Query and value seem to be the sweet spot for LoRA on this task.

### Learning Curves Show Phase Transitions

Training loss showed clear phases:
- **Epochs 1-3**: Rapid learning (random → basic patterns)
- **Epochs 4-6**: Entity recognition clicks (F1 jumps 83% → 91%)
- **Epochs 7-10**: Refinement (91% → 96.9%, diminishing returns)

Could probably early stop at epoch 6 and save time.

### The 0.89% Parameter Efficiency is Wild

Only 597K / 67M parameters are trainable (0.89%).

**Mental model**: It's like having a massive pre-trained brain (DistilBERT) and adding a tiny specialized module (LoRA) for medical text. The base brain already understands language, the module just redirects attention slightly.

## Random Tips

- **Google Colab free tier works fine**: T4 GPU is enough, training takes < 2 mins
- **Gradio is great for quick demos**: Added interactive demo in ~20 lines of code
- **SeqEval for NER metrics**: Don't use sklearn's classification metrics directly, they don't handle BIO tagging correctly
- **Watch your -100 labels**: HuggingFace uses -100 for padding tokens that should be ignored in loss. Forgetting to filter these breaks your eval metrics.

## What's Next?

- [ ] Test on i2b2 2009 NER dataset (the "real" benchmark)
- [ ] Try ClinicalBERT as base model
- [ ] Add relation extraction (which medication treats which condition?)
- [ ] Experiment with instruction-tuned models (Llama-2, Mistral) for zero-shot
- [ ] Deploy as an API (FastAPI + Docker?)

## Resources That Helped

- [LoRA paper (Hu et al.)](https://arxiv.org/abs/2106.09685) 
- [PEFT documentation](https://huggingface.co/docs/peft) - Excellent examples
- [SeqEval docs](https://github.com/chakki-works/seqeval) - For understanding BIO tagging metrics
- [This blog post on medical NER](https://www.johnsnowlabs.com/ner-for-clinical-texts/) - Good overview

---

Last updated: March 2026
