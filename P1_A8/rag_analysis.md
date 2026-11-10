# RAG System Analysis — ClassCompass / Physics 212

## Step 1.2: Text Representation and Chunking

### Paragraph Definition

We define paragraphs using blank lines in the syllabus text. Each paragraph contains a section of course information, such as grading, assignments, or exams.

### Fixed-Length Chunking

We use a target chunk size of 450 characters. The text is divided at sentence boundaries to avoid splitting sentences.

Each paragraph is processed separately so unrelated sections are not combined.

### Overlapping Paragraph Chunking

We combine adjacent paragraphs with overlap:

- Chunk 1: Paragraph 1 + Paragraph 2
- Chunk 2: Paragraph 2 + Paragraph 3
- Chunk 3: Paragraph 3 + Paragraph 4

This preserves information between consecutive chunks. However, it can also combine adjacent sections that discuss different topics.

### Hybrid/Strategic Chunking

We use the syllabus's Markdown headings to identify section boundaries. Each heading and its associated text form a separate chunk.

This keeps related information together and avoids combining unrelated syllabus sections.

### Comparison

Fixed-length chunking produces shorter chunks with relatively consistent sizes.

Overlapping paragraph chunking preserves more context but introduces repeated information.

Header-based chunking follows the organization of the syllabus and keeps complete topics together.

---

# Part 2: System Experiments

## 2.1 Test Queries

We selected five realistic questions about Physics 212 to evaluate retrieval and answer quality across different embedding models and chunking strategies.

---

## 2.2 Evaluation Table

The 45 experiment records are summarized below. Full retrieved chunks and generated answers for each row are preserved in `part2_results.csv` (the submitted graded file), and printed in `rag_system.ipynb`.

| Embedding Model   | Chunking Strategy   | Query                                         |   Retrieved Context Quality |   Answer Quality |   Latency | Notes                                                                                                                                                                                                                                                                                             |
|:------------------|:--------------------|:----------------------------------------------|----------------------------:|-----------------:|----------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| small             | fixed               | When are weekly homework assignments due?     |                           2 |                2 |      5.68 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Also correctly identifies Week 14 as the last homework deadline.                                                                     |
| small             | fixed               | What happens if I submit homework late?       |                           2 |                2 |      3.08 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit.                                                                                                                                                                      |
| small             | fixed               | How much of my grade is the final exam worth? |                           2 |                2 |      2.16 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade.                                                                                                                                                                                    |
| small             | fixed               | When and where is the midterm exam?           |                           2 |                2 |      3.55 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210.                                                                                                                                                 |
| small             | fixed               | When does the instructor hold office hours?   |                           2 |                2 |      3.28 | Instructor office-hours section retrieved (Tuesday/Thursday afternoons; Room 402). Answer correctly identifies Tuesday/Thursday afternoons and Room 402.                                                                                                                                          |
| small             | overlapping         | When are weekly homework assignments due?     |                           2 |                2 |      7.31 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Overlapping chunks repeat text and add unrelated context.                                                                            |
| small             | overlapping         | What happens if I submit homework late?       |                           2 |                2 |      6.07 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Overlapping chunks repeat text and add unrelated context.                                                                                                            |
| small             | overlapping         | How much of my grade is the final exam worth? |                           2 |                2 |      4.79 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Overlapping chunks repeat text and add unrelated context.                                                                                                                          |
| small             | overlapping         | When and where is the midterm exam?           |                           2 |                2 |      5.78 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Overlapping chunks repeat text and add unrelated context.                                                                                       |
| small             | overlapping         | When does the instructor hold office hours?   |                           0 |                0 |      4.47 | No instructor office-hours policy in top-3 chunks; instead retrieved unrelated lecture/grade/study content. Model consequently says hours are unavailable, contrary to syllabus.                                                                                                                  |
| small             | header              | When are weekly homework assignments due?     |                           2 |                2 |      4.92 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Topic-based chunks preserve section context.                                                                                         |
| small             | header              | What happens if I submit homework late?       |                           2 |                2 |      4.42 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Topic-based chunks preserve section context.                                                                                                                         |
| small             | header              | How much of my grade is the final exam worth? |                           2 |                2 |      2.97 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Topic-based chunks preserve section context.                                                                                                                                       |
| small             | header              | When and where is the midterm exam?           |                           2 |                2 |      3.66 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Topic-based chunks preserve section context.                                                                                                    |
| small             | header              | When does the instructor hold office hours?   |                           2 |                2 |      4.32 | Instructor office-hours section retrieved (Tuesday/Thursday afternoons; Room 402). Answer correctly identifies Tuesday/Thursday afternoons and Room 402. Topic-based chunks preserve section context. Office-hours evidence appears in retrieved chunk 2, not chunk 1.                            |
| medium            | fixed               | When are weekly homework assignments due?     |                           2 |                2 |      3.8  | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions.                                                                                                                                      |
| medium            | fixed               | What happens if I submit homework late?       |                           2 |                2 |      3.74 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit.                                                                                                                                                                      |
| medium            | fixed               | How much of my grade is the final exam worth? |                           2 |                2 |      2.21 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade.                                                                                                                                                                                    |
| medium            | fixed               | When and where is the midterm exam?           |                           2 |                1 |      2.69 | Midterm Week 8, Thursday noon and Lecture Hall 210 are in the retrieved chunks, but the answer omits Week 8; time and place are correct.                                                                                                                                                          |
| medium            | fixed               | When does the instructor hold office hours?   |                           2 |                2 |      3.24 | Instructor office-hours section retrieved (Tuesday/Thursday afternoons; Room 402). Answer correctly identifies Tuesday/Thursday afternoons and Room 402.                                                                                                                                          |
| medium            | overlapping         | When are weekly homework assignments due?     |                           2 |                2 |      6.55 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Overlapping chunks repeat text and add unrelated context.                                                                            |
| medium            | overlapping         | What happens if I submit homework late?       |                           2 |                2 |      6.43 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Overlapping chunks repeat text and add unrelated context.                                                                                                            |
| medium            | overlapping         | How much of my grade is the final exam worth? |                           2 |                2 |      5    | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Overlapping chunks repeat text and add unrelated context.                                                                                                                          |
| medium            | overlapping         | When and where is the midterm exam?           |                           2 |                2 |      6.84 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Overlapping chunks repeat text and add unrelated context.                                                                                       |
| medium            | overlapping         | When does the instructor hold office hours?   |                           0 |                0 |      5.1  | No instructor office-hours policy in top-3 chunks; instead retrieved unrelated lecture/grade/study content. Model consequently says hours are unavailable, contrary to syllabus.                                                                                                                  |
| medium            | header              | When are weekly homework assignments due?     |                           2 |                2 |      5.78 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Topic-based chunks preserve section context.                                                                                         |
| medium            | header              | What happens if I submit homework late?       |                           2 |                2 |      4.51 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Topic-based chunks preserve section context.                                                                                                                         |
| medium            | header              | How much of my grade is the final exam worth? |                           2 |                2 |      2.93 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Topic-based chunks preserve section context.                                                                                                                                       |
| medium            | header              | When and where is the midterm exam?           |                           2 |                2 |      4.92 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Topic-based chunks preserve section context.                                                                                                    |
| medium            | header              | When does the instructor hold office hours?   |                           0 |                0 |      3.56 | No instructor office-hours policy in top-3 chunks; instead retrieved unrelated lecture/grade/study content. Model consequently says hours are unavailable, contrary to syllabus.                                                                                                                  |
| large             | fixed               | When are weekly homework assignments due?     |                           2 |                2 |      6.21 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Also correctly identifies Week 14 as the last homework deadline.                                                                     |
| large             | fixed               | What happens if I submit homework late?       |                           2 |                2 |      3.65 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit.                                                                                                                                                                      |
| large             | fixed               | How much of my grade is the final exam worth? |                           2 |                2 |      2.6  | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Correct fact appears in multiple retrieved chunks.                                                                                                                                 |
| large             | fixed               | When and where is the midterm exam?           |                           2 |                2 |      3.88 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210.                                                                                                                                                 |
| large             | fixed               | When does the instructor hold office hours?   |                           2 |                2 |      3.65 | Instructor office-hours section retrieved (Tuesday/Thursday afternoons; Room 402). Answer correctly identifies Tuesday/Thursday afternoons and Room 402.                                                                                                                                          |
| large             | overlapping         | When are weekly homework assignments due?     |                           2 |                2 |      7.04 | Homework deadline policy retrieved (Thursday 12:00 PM; first/final week exception). Answer gives the correct Thursday noon deadline and relevant exceptions. Overlapping chunks repeat text and add unrelated context.                                                                            |
| large             | overlapping         | What happens if I submit homework late?       |                           2 |                2 |      6.22 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Overlapping chunks repeat text and add unrelated context.                                                                                                            |
| large             | overlapping         | How much of my grade is the final exam worth? |                           2 |                2 |      5.17 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Overlapping chunks repeat text and add unrelated context.                                                                                                                          |
| large             | overlapping         | When and where is the midterm exam?           |                           2 |                2 |      6.68 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Overlapping chunks repeat text and add unrelated context.                                                                                       |
| large             | overlapping         | When does the instructor hold office hours?   |                           0 |                0 |      6.67 | No instructor office-hours policy in top-3 chunks; instead retrieved unrelated lecture/grade/study content. Model consequently says hours are unavailable, contrary to syllabus.                                                                                                                  |
| large             | header              | When are weekly homework assignments due?     |                           2 |                2 |      8.2  | Retrieved weekly progression sections state Thursday noon due dates (including Weeks 2 and 14) and the Week 8 exception; response correctly states Thursday noon and the exam-week exception. General first/final-week policy is not retrieved, but not necessary to answer when homework is due. |
| large             | header              | What happens if I submit homework late?       |                           2 |                2 |      5.62 | Late-work policy retrieved (20% per day; 72-hour cutoff). Answer correctly states the 20% daily deduction and 72-hour limit. Topic-based chunks preserve section context.                                                                                                                         |
| large             | header              | How much of my grade is the final exam worth? |                           2 |                2 |      5.61 | Grading/final-exam section retrieved (final = 35%). Answer correctly identifies the final as 35% of the grade. Topic-based chunks preserve section context.                                                                                                                                       |
| large             | header              | When and where is the midterm exam?           |                           2 |                2 |      5.54 | Midterm guidance retrieved (Week 8, Thursday 12:00 PM, Lecture Hall 210). Answer correctly identifies Week 8, Thursday noon and Lecture Hall 210. Topic-based chunks preserve section context.                                                                                                    |
| large             | header              | When does the instructor hold office hours?   |                           2 |                2 |      5.26 | Instructor office-hours section retrieved (Tuesday/Thursday afternoons; Room 402). Answer correctly identifies Tuesday/Thursday afternoons and Room 402. Topic-based chunks preserve section context.                                                                                             |

---

## 2.3 Embedding Model Comparison

We compared three embedding models: all-MiniLM-L6-v2 (384 dimensions), all-mpnet-base-v2 (768 dimensions), and BGE-large-en-v1.5 (1024 dimensions). Each model was tested with three chunking strategies and five syllabus questions.

The small and large models achieved the same average retrieval quality score of 1.87/2 and answer quality score of 1.87/2. The medium model performed slightly worse, with a retrieval quality score of 1.73/2 and an answer quality score of 1.67/2.

Larger embeddings did not always perform better. Although the large model used 1024 dimensions, it did not improve the average quality scores compared with the small 384-dimensional model. It also had a higher average latency of 5.47 seconds, compared with 4.43 seconds for the small model.

One important failure occurred when retrieving instructor office hours. All three embedding models failed to retrieve the relevant information when overlapping paragraph chunking was used. This suggests that chunking strategy can have a significant effect on retrieval quality regardless of embedding size.

Overall, the small embedding model provided the best balance of answer quality and latency for our Physics 212 syllabus dataset. However, these findings are limited to the five queries and dataset used in our experiments.

---

### Embedding Model Results Table

| Embedding Model   |   Retrieved Context Quality |   Answer Quality |   Latency |
|:------------------|----------------------------:|-----------------:|----------:|
| large             |                        1.87 |             1.87 |      5.47 |
| medium            |                        1.73 |             1.67 |      4.49 |
| small             |                        1.87 |             1.87 |      4.43 |

---

## 2.4 Chunking Strategy Comparison

We evaluated three chunking strategies: fixed-length chunking, overlapping paragraph chunking, and header-based chunking. Each strategy was tested with all three embedding models using the same five queries.

Fixed-length chunking performed best, achieving an average retrieval quality score of 2.00/2 and answer quality score of 1.93/2. Header-based chunking performed slightly worse, with both scores averaging 1.87/2. Overlapping paragraph chunking had the lowest average scores of 1.60/2 for both retrieval and answer quality.

Fixed-length chunking was effective because it divided the syllabus into shorter, focused pieces of text while preserving sentence and paragraph boundaries. This made it easier for the embedding models to identify relevant information without including too much unrelated context.

Overlapping paragraph chunking combined adjacent paragraphs, which preserved more surrounding context but sometimes introduced unnecessary information. This made retrieval less precise for certain questions.

For example, when using the medium embedding model to answer "When does the instructor hold office hours?", fixed-length chunking retrieved the correct office-hours section. Qwen correctly answered that office hours were held on Tuesday and Thursday afternoons following class, with appointments available in Room 402.

However, overlapping and header-based chunking failed to retrieve the office-hours information for the same question. Instead, they retrieved other syllabus sections, and Qwen incorrectly stated that office hours were not provided.

This demonstrates how chunking affects the entire RAG pipeline. When the retrieved text contains the correct facts, the generation model can produce an accurate response. When retrieval misses those facts, even the same generation model may produce an incorrect or incomplete answer.

Overall, fixed-length chunking was the most effective strategy for our dataset, providing the highest quality scores and lowest average latency of 3.56 seconds. These results suggest that shorter, focused chunks are better suited to our syllabus question-answering system.

---

### Chunking Strategy Results Table

| Chunking Strategy   |   Retrieved Context Quality |   Answer Quality |   Latency |
|:--------------------|----------------------------:|-----------------:|----------:|
| fixed               |                        2    |             1.93 |      3.56 |
| header              |                        1.87 |             1.87 |      4.81 |
| overlapping         |                        1.6  |             1.6  |      6.01 |

---

## 2.5 Data Scaling Experiment

---

## 2.5 Data Scaling Experiment

For this experiment, we compared a smaller dataset containing the first 10 paragraphs of the Physics 212 syllabus with the complete dataset containing 30 paragraphs. We used the same medium embedding model (all-mpnet-base-v2), fixed-length chunking, five test queries, and top-3 retrieval.

**Retrieval Quality:** The smaller dataset achieved an average retrieval quality score of 1.00/2, while the larger dataset achieved 2.00/2. The larger dataset performed better because it contained information missing from the smaller subset. For example, the smaller dataset failed to retrieve the homework deadline and late-submission policy, while the larger dataset correctly retrieved Thursday at 12:00 PM as the deadline and the 20% daily late penalty with a 72-hour cutoff.

**Noise:** The smaller dataset had an average noise score of 1.40/2, compared with 0.80/2 for the larger dataset. When relevant information was missing, the smaller dataset retrieved unrelated content about lecture attendance and general grading policies. The larger dataset generally retrieved more relevant information, although some unrelated or unnecessary chunks were still present.

**Latency:** Both datasets had nearly identical average retrieval latency of approximately 0.1114 seconds. Increasing the dataset from 10 to 30 paragraphs did not noticeably affect retrieval speed in this small experiment.

**Conclusion:** Increasing dataset size improved retrieval quality and reduced noise in our experiment. However, this improvement was largely due to the additional information available in the full syllabus. Because the smaller dataset excluded some relevant policies, the experiment does not establish that larger datasets are inherently more accurate or less noisy. With much larger datasets, additional irrelevant information could increase retrieval noise.

---

### Scaling Experiment Results Table

Retrieved chunks and complete results are preserved in `scaling_results.csv`.

| Dataset   | Query                                         |   Retrieval Quality |   Noise |   Latency | Notes                                                                                                                                                                                  |
|:----------|:----------------------------------------------|--------------------:|--------:|----------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Small     | When are weekly homework assignments due?     |                   0 |       2 |    0.0927 | The first ten paragraphs do not include the homework-deadline section; none of the returned chunks states Thursday at noon. All three results are off-topic for the due-date question. |
| Small     | What happens if I submit homework late?       |                   0 |       2 |    0.1115 | The small subset excludes the late-submission policy; all three retrieved chunks omit the 20% daily penalty and 72-hour cutoff.                                                        |
| Small     | How much of my grade is the final exam worth? |                   2 |       1 |    0.126  | Rank 1 explicitly states the final exam is worth 35%. The remaining retrieved chunks discuss general grading and a curve rather than the requested percentage.                         |
| Small     | When and where is the midterm exam?           |                   1 |       1 |    0.1129 | The retrieved grading chunk identifies Week 8, and the lecture schedule gives Thursday at noon in Hall 210, but no returned chunk directly ties the midterm to that time and place.    |
| Small     | When does the instructor hold office hours?   |                   2 |       1 |    0.1138 | Rank 1 explicitly states Tuesday and Thursday afternoons after class and appointments in Room 402. Ranks 2–3 are lecture-schedule material, not office-hours information.              |
| Large     | When are weekly homework assignments due?     |                   2 |       1 |    0.0939 | Rank 1 gives Thursday at 12:00 PM and the first/final-week exceptions. Rank 2 adds late penalties; Rank 3 is related to an exam-week exception but is not needed for the deadline.     |
| Large     | What happens if I submit homework late?       |                   2 |       1 |    0.1101 | Rank 1 gives the 20%-per-day penalty and 72-hour cutoff. Rank 2 adds general homework timing; Rank 3 is unrelated lecture-attendance advice.                                           |
| Large     | How much of my grade is the final exam worth? |                   2 |       1 |    0.1332 | Ranks 1 and 3 both state the final exam is worth 35%; Rank 2 supplies general grading context. Some redundancy, but the answer is easy to find.                                        |
| Large     | When and where is the midterm exam?           |                   2 |       0 |    0.109  | Rank 2 explicitly gives Week 8, Thursday at 12:00 PM, Lecture Hall 210. Ranks 1 and 3 also concern the midterm; little irrelevant information.                                         |
| Large     | When does the instructor hold office hours?   |                   2 |       1 |    0.1109 | Rank 1 correctly gives the office-hours schedule and Room 402. Rank 2 is tangentially related lecture timing, and Rank 3 is unrelated midterm material.                                |

---

# Part 3: Failure Analysis and Improvement

## 3.1 Failure Cases

---

### Failure 1: Small Embedding Model + Overlapping Chunking

**Question:** When does the instructor hold office hours?

**Expected Answer:** Office hours are held Tuesday and Thursday afternoons following class, with appointments available in Room 402.

**Actual Answer:** The model stated that the syllabus did not provide office-hours information.

**Problem:** The top three retrieved chunks contained information about lecture schedules, grading, and other course policies rather than the instructor's office-hours schedule. The model therefore gave an incorrect answer relative to the full syllabus.

### Failure 2: Medium Embedding Model + Header-Based Chunking

**Question:** When does the instructor hold office hours?

**Expected Answer:** Tuesday and Thursday afternoons following class, with appointments available in Room 402.

**Actual Answer:** The model stated that office-hours information was unavailable.

**Problem:** The retrieved chunks did not contain the instructor's office-hours policy. Instead, the system retrieved unrelated course information, resulting in an incorrect answer.

### Failure 3: Medium Embedding Model + Fixed-Length Chunking

**Question:** When and where is the midterm exam?

**Expected Answer:** Week 8, Thursday at 12:00 PM in Lecture Hall 210.

**Actual Answer:** The midterm exam is on Thursday at 12:00 PM in Lecture Hall 210.

**Problem:** The model correctly identified the time and location but omitted Week 8. The retrieved context contained all three facts, so this was an incomplete generation rather than a retrieval failure.

---

## 3.2 Root Cause Analysis

### Failure 1: Small Model + Overlapping Chunking

The likely cause was a combination of chunking and retrieval ranking. Overlapping paragraph chunking combined adjacent syllabus paragraphs, creating longer passages that sometimes included unrelated information. The small embedding model ranked passages about the class schedule and other policies above the actual office-hours section.

The query was reasonable, but its references to the instructor and schedule may have contributed to retrieving general lecture information instead of office hours.

### Failure 2: Medium Model + Header-Based Chunking

The primary issue was retrieval relevance. Even though header-based chunking organized the document into sections, the medium embedding model did not rank the instructor-information section among the top three results.

This shows that meaningful section boundaries alone do not guarantee relevant retrieval. The embedding model and query wording may also influence which passages receive the highest similarity scores.

### Failure 3: Medium Model + Fixed-Length Chunking

This failure occurred during generation rather than retrieval. The retrieved chunks included Week 8, Thursday at 12:00 PM, and Lecture Hall 210. However, the generated answer omitted Week 8.

The embedding model successfully found the relevant information, and the chunking strategy preserved it. The likely issue was that the generation prompt did not explicitly encourage the model to include every relevant scheduling detail.

### Summary

The experiments demonstrated two different failure types. In the office-hours examples, the retrieval system failed to provide the necessary information to the generation model. In the midterm example, retrieval succeeded, but the generation model produced an incomplete response. These failures suggest that improving retrieval relevance and strengthening the generation instructions could improve the overall system.

---

## 3.3 Final System Improvement

Our original system correctly retrieved the midterm exam information but generated an incomplete answer that omitted Week 8.

We first attempted to improve the generation prompt by explicitly requesting the week, day, time, and location. However, the revised prompt still omitted Week 8, so this change alone did not improve the answer.

To address this issue, we implemented an additional validation step that checks the retrieved syllabus context for the missing week. If the information is present but omitted from the generated response, the system adds the missing detail.

**Before:** The midterm exam is on Thursday at 12:00 PM in Lecture Hall 210.

**After:** In Week 8, the midterm exam is on Thursday at 12:00 PM in Lecture Hall 210.

**Result:** The answer quality improved from 1/2 to 2/2 because the final system output now includes the week, day, time, and location. The improvement came from source-grounded validation, not from the generation model itself.

This demonstrates that adding a validation step after generation can help prevent incomplete answers when the retrieved context already contains the correct information.

---

### Before/After Evidence

| Version   | Query                               | Answer                                                                      |   Answer Quality | Notes                                                                   |
|:----------|:------------------------------------|:----------------------------------------------------------------------------|-----------------:|:------------------------------------------------------------------------|
| Before    | When and where is the midterm exam? | The midterm exam is on Thursday at 12:00 PM in Lecture Hall 210.            |                1 | nan                                                                     |
| After     | When and where is the midterm exam? | In Week 8, the midterm exam is on Thursday at 12:00 PM in Lecture Hall 210. |                2 | Added validation to include Week 8 when supported by retrieved context. |

---

# Part 4: System Design Reflection

## Step 4.1: Cost Awareness (15 points)

Our ClassCompass RAG system uses three embedding models of different sizes, three chunking strategies, FAISS for similarity search, and Qwen3-4B-Instruct for generating answers based on retrieved syllabus information. The main factors affecting system cost are embedding size, chunk size, and the number of retrieved chunks (top-k).

### Embedding Size

Larger embedding models generally require more memory and computational resources. They also produce higher-dimensional vectors, which require more storage and can increase the computational cost of similarity search. For example, our small embedding model produces 384-dimensional vectors, while our medium and large models produce 768-dimensional and 1024-dimensional vectors.

Our experiments showed that the small and large embedding models achieved the same average retrieval quality score of 1.87/2 and answer quality score of 1.87/2. However, the small model had a lower average end-to-end latency of approximately 4.43 seconds, compared with 5.47 seconds for the large model.

These results suggest that using a larger embedding model is not always necessary for a relatively small syllabus dataset. For ClassCompass, the smaller model would be a more cost-effective choice because it achieved comparable quality with lower measured latency and lower embedding storage requirements.

### Chunk Size

Chunk size affects the number of embeddings generated, the amount of context retrieved, and the amount of text sent to the generation model.

Smaller chunks generally produce more vectors, increasing indexing and storage requirements. However, they can make retrieval more precise by focusing on individual topics. Larger chunks produce fewer vectors but may include unrelated information, making retrieval less relevant. Larger retrieved chunks can also increase the number of input tokens processed by Qwen, raising generation costs and latency.

Our experiments showed that fixed-length chunking performed best, achieving an average retrieval quality score of 2.00/2 and answer quality score of 1.93/2. Overlapping paragraph chunking performed worse, with both scores averaging 1.60/2.

Overlapping chunking also duplicates text across multiple chunks, increasing storage requirements and potentially sending repetitive information to the generation model. Therefore, fixed-length chunking would be our preferred strategy for the current ClassCompass system.

### Top-k Retrieval

The top-k parameter determines how many chunks are retrieved and passed to the generation model.

Using a smaller top-k value reduces the amount of retrieved text, which can decrease prompt length, generation time, and computational cost. However, a value that is too small may exclude information necessary to answer a question correctly.

Increasing top-k can improve coverage by providing more potentially relevant information, but it can also introduce noise and increase the number of tokens processed by the generation model.

For our experiments, we used top-k = 3, meaning the three highest-ranked chunks were passed to Qwen. This provided a reasonable balance between context coverage and efficiency for our relatively small dataset.

We did not systematically compare different top-k values, so we cannot conclude that 3 is the optimal value. For a larger production system, we would evaluate other values to determine the best balance between retrieval quality, latency, and cost.

### Cost Conclusion

For our current syllabus-based RAG system, the most practical configuration would be the small 384-dimensional embedding model, fixed-length chunking, and top-k retrieval of 3.

This combination performed well in our experiments while limiting unnecessary computational work. In a production environment, we would also need to account for server hosting, model inference, data storage, and the frequency of user requests.

---

## Step 4.2: RAG vs Alternatives (15 points)

There are three main approaches we could use to provide AI-powered assistance in ClassCompass: Retrieval-Augmented Generation (RAG), fine-tuning, and pure prompting.

| Approach | When to Use |
|---|---|
| **RAG** | When the application needs accurate, document-specific information that may change frequently, such as course syllabi, assignment deadlines, grading policies, and office hours. |
| **Fine-tuning** | When the application needs a model to consistently follow a specific output format, writing style, or specialized task behavior across many examples. |
| **Pure prompting** | When the application performs a simple or general task that does not require retrieving information from external documents, such as rewriting text or generating general study advice. |

### Retrieval-Augmented Generation (RAG)

RAG is the most appropriate approach for ClassCompass because the application works with course-specific information uploaded by students.

For example, a student might ask when homework is due or how much the final exam contributes to their course grade. These details vary between courses and semesters, so the model needs access to the specific syllabus.

RAG allows ClassCompass to retrieve the relevant passages from the uploaded syllabus and use them to generate an answer. If a student uploads a revised syllabus, the application can update its document index without retraining the generation model.

RAG also makes it easier to inspect where an answer came from because the retrieved passages can be displayed alongside the generated response.

However, RAG depends heavily on retrieval quality. In our experiments, some configurations failed to retrieve the instructor's office-hours information even though it existed in the syllabus. This caused the generation model to provide an incorrect answer relative to the full document.

### Fine-Tuning

Fine-tuning would be useful if we wanted ClassCompass to consistently perform specialized tasks, such as formatting study schedules, generating structured assignment summaries, or classifying course events.

For example, we could train a model using many examples of syllabus information converted into structured JSON containing assignment names, deadlines, exam dates, and grading weights.

However, fine-tuning alone would not be an efficient way to store individual students' syllabus information. Course policies change frequently, and retraining a model whenever a syllabus changes would be expensive and impractical.

Fine-tuning would also require an appropriate training dataset, additional computational resources, and evaluation to ensure the model generalizes correctly.

### Pure Prompting

Pure prompting involves sending instructions directly to a generation model without building a separate retrieval system.

This approach would work for tasks that do not require specific course documents. For example, ClassCompass could ask a model to generate general study strategies or rewrite a student's notes in simpler language.

For a short syllabus, the application could also include the entire document in the prompt. However, this approach would become less efficient as students uploaded more courses and larger documents because every request could require processing large amounts of text.

Pure prompting without the relevant syllabus context also risks generating unsupported assumptions about course policies and deadlines.

### Final Recommendation

We would choose RAG as the primary approach for ClassCompass because our application relies on accurate, course-specific information that changes over time.

Fine-tuning could be considered later for specialized formatting and extraction tasks, while pure prompting could support general study assistance. Combining these approaches could eventually provide more functionality, but RAG is the best foundation for answering questions about uploaded syllabi.

---

## Step 4.3: System Design (20 points)

### Scaling ClassCompass to 10,000 Users per Day

Our current RAG system is a small prototype that processes one Physics 212 syllabus and performs retrieval using FAISS before generating an answer with Qwen3-4B-Instruct.

To support approximately 10,000 users per day, we would need to improve how documents are processed, embeddings are stored, and generation requests are handled.

Assuming each user makes one AI request per day, the system would process approximately 10,000 requests daily. This corresponds to an average of about seven requests per minute, although actual traffic would likely be much higher during peak periods. If users submit multiple questions, the total number of requests would increase proportionally.

A production design would separate document ingestion, retrieval, and text generation so that each component could be scaled independently.

### Document Upload and Processing

When a student uploads a syllabus, the system would extract the text, clean it, divide it into chunks, and generate embeddings.

Instead of repeating this process for every question, we would process each syllabus once when it is uploaded or updated.

The resulting embeddings would be stored and reused for future requests. This would reduce unnecessary computation and improve response times.

We would also process document uploads through a background task queue so that large files would not block the web application's request-handling process.

### Embedding and Vector Storage

Based on our experiments, we would initially use the small all-MiniLM-L6-v2 embedding model with fixed-length chunking.

We would use a persistent vector storage solution suitable for the amount of data and query traffic, rather than rebuilding an in-memory FAISS index for every request. FAISS could still be used as the underlying similarity-search technology.

Each stored chunk would include metadata identifying its user, course, document, and syllabus version.

This is particularly important because ClassCompass supports multiple students and courses. Retrieval must be restricted to the correct user's authorized documents to prevent one student from receiving information from another student's uploads.

When a syllabus is replaced or updated, its embeddings would be updated accordingly.

### LLM Inference and Request Handling

The most computationally expensive component would likely be the generation model, especially when many users submit questions simultaneously.

Rather than loading Qwen separately for each request, we would keep the generation model loaded on a dedicated inference server. Multiple Django workers could send requests to this service.

We would use request queues, concurrency limits, and batching where supported to manage peak traffic efficiently.

If demand increased, we could add additional inference workers or GPU instances. We could also evaluate a hosted inference API if its cost, latency, and reliability were more suitable than maintaining our own servers.

### Caching and Performance Optimization

Caching would help reduce repeated computation. For example, students might ask the same questions about homework deadlines, grading weights, or office hours.

If the underlying syllabus had not changed, the application could reuse previously computed embeddings and, where appropriate, cached answers.

We would also limit retrieved context to relevant chunks rather than sending the entire syllabus to Qwen.

Our experiments suggest that fixed-length chunking is effective for this dataset, and we would begin with top-k = 3 while monitoring whether additional context improves answers.

### Reliability, Privacy, and Monitoring

Because ClassCompass processes student-uploaded course documents, we would implement access controls and isolate each user's stored documents and embeddings.

We would also treat uploaded syllabus text as untrusted input and prevent document instructions from overriding the system's intended behavior.

To monitor reliability, we would track retrieval latency, generation latency, request failures, memory usage, and response quality. We would also examine cases where the system retrieves unrelated chunks or generates incomplete answers.

Our Part 3 experiment showed that even when retrieval contains the correct information, the generation model can omit important details. Therefore, a production system could use additional validation to check important fields such as dates, times, and locations against the source document.

### What We Would Optimize First

Our first priority would be efficient inference, because repeatedly running the generation model is likely to be more computationally expensive than searching a relatively small syllabus index.

Second, we would optimize document processing by generating and storing embeddings once per document version.

Third, we would improve retrieval accuracy using the small embedding model and fixed-length chunking identified in our experiments.

Finally, we would introduce caching, request monitoring, and automatic scaling as usage increased.

### System Design Conclusion

To scale ClassCompass to 10,000 users per day, we would separate document ingestion, vector retrieval, and LLM generation into independent components.

We would store embeddings persistently, reuse the same generation model across requests, restrict retrieval to authorized course documents, and scale inference resources based on demand.

Our experimental results indicate that smaller embedding models and focused chunking strategies can provide good retrieval quality without requiring the largest available models. This makes RAG a practical foundation for adding syllabus-based AI assistance to ClassCompass.

The proposed architecture is a design for future deployment, not a system that we have already implemented or load-tested at this scale.

Check diagram.png for the system diagram. 