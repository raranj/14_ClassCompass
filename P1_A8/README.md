# Assignment 8

## Project Overview

This project evaluates a Retrieval-Augmented Generation (RAG) pipeline for ClassCompass. The experiment uses a Physics 212 syllabus as a knowledge base to answer student questions about homework, exams, grading, and office hours.

The pipeline loads syllabus text, divides it into chunks, embeds those chunks, retrieves the most similar passages with FAISS, and sends the retrieved context to a language model to generate an answer.

## Contents

| File | Description |
|---|---|
| `rag_system.ipynb` | RAG implementation, retrieval and generation tests, experiments, comparisons, failure analysis, and system design reflection. |
| `rag_analysis.md` | Written experiment analysis, evaluation tables, failure cases, and system design discussion. |
| `physics_212_syllabus.txt` | Source document used as the RAG knowledge base. |
| `part2_results.csv` | Evaluated results for 45 experiments, including retrieved chunks, answers, quality ratings, latency, and notes. |
| `scaling_results.csv` | Evaluated comparison of the first 10 paragraphs and the full syllabus, including retrieved chunks and ratings. |
| `part3_before_after_fixed.csv` | Saved before-and-after results for the Part 3 validation-based improvement. |
| `requirements.txt` | Python package dependencies. |

Install the dependencies with:

```bash
pip install -r requirements.txt
```

The notebook also contains package installation cells for Colab.

## How to Run

1. Open `rag_system.ipynb` in **Google Colab**.
2. Select **Runtime → Change runtime type** and enable a GPU if available.
3. Upload `physics_212_syllabus.txt` into Colab's working directory. The notebook looks for this relative filename and can prompt for an upload if it is missing.
4. Upload the evaluated CSV files to the same directory **using these exact names**:
   - `part2_results.csv`
   - `scaling_results.csv`
   - `part3_before_after_fixed.csv`
5. Run the installation and Part 1 cells to load the syllabus and create the retrieval pipeline.
6. For reviewing the supplied experiment results, **skip the Part 2 experiment-generation and scaling-generation loops**. Those cells write to `part2_results.csv` and `scaling_results.csv`, and rerunning them can replace the manually evaluated files. Continue with the cells that load the CSVs and calculate comparison tables.
7. Run the Part 3 demonstration and validation cells if you want to reproduce the before/after improvement. The final validation cell writes `part3_before_after_fixed.csv`.
8. Read `rag_analysis.md` for the written interpretation of results and system design reflection.

## Models and Experiment Setup

**Embedding models:**

- Small: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- Medium: `sentence-transformers/all-mpnet-base-v2` (768 dimensions)
- Large: `BAAI/bge-large-en-v1.5` (1024 dimensions)

**Generation model:** `Qwen/Qwen3-4B-Instruct-2507`, used consistently across the model comparisons.

**Chunking strategies:**

- Sentence-aware fixed-length chunking
- Overlapping adjacent-paragraph chunking
- Header-based strategic chunking

**Retrieval:** FAISS similarity search using normalized vectors; top-k = 3 for the main experiments.
