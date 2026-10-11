# VidMind Accuracy & Grounding Evaluation Framework

VidMind treats empirical accuracy as an engineered, measurable system characteristic rather than an abstract marketing claim.

---

## 1. Grounding Principles & Hallucination Prevention
1. **Rule 1 — Evidence before Generation**: Models are strictly forbidden from generating answers without retrieved evidence context.
2. **Sufficiency Gate**: If retrieval similarity or token overlap falls below confidence thresholds, the system explicitly returns:
   > *"Not enough evidence in the video to answer this confidently."*
3. **Citation Verification**: Every generated statement is cross-checked against source segment timestamps. Unsubstantiated claims are pruned before presentation.

---

## 2. Evaluation Metrics

| Metric | Target | Measurement Method |
| :--- | :--- | :--- |
| **Word Error Rate (WER)** | < 8% | Comparison of Whisper output against golden transcript fixtures |
| **Evidence Support Rate** | > 95% | Proportion of factual claims backed by valid segment citations |
| **Unsupported Claim Rate**| < 3% | Claims lacking matching transcript evidence |
| **Timestamp Precision** | ± 3.0s | Alignment between cited timestamp and spoken utterance |
| **Retrieval Recall@5** | > 90% | Relevant segments retrieved in top 5 search candidates |

---

## 3. Golden Dataset Benchmark

Golden test fixtures are stored in `tests/golden/`:
- `tests/golden/sample001.json`: Synthetic lecture covering factual assertions and out-of-scope queries.
- Automated tests in `backend/tests/evaluation/test_accuracy.py` run against these fixtures to verify accuracy thresholds.
