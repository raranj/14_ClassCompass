# Evaluation Prompt Catalog

Total unique prompts: 25

| Prompt ID | Prompt Type | Actual Prompt |
|---|---|---|
| AH1 | ambiguity_handling | A student says, "Schedule my study session for next Friday." What information should you clarify before scheduling? |
| AH2 | ambiguity_handling | A user asks, "Which model is best?" Explain what you need to clarify. |
| AH3 | ambiguity_handling | A student says, "I need more time for my project." Respond helpfully without making assumptions. |
| AH4 | ambiguity_handling | A user says, "Remind me before the exam." What information is missing? |
| AH5 | ambiguity_handling | A student asks, "Will I pass this course?" What information would help estimate this? |
| CL1 | classification | Classify the sentiment as positive, negative, or neutral: "The lecture was clear and helpful." |
| CL2 | classification | Classify this request as academic, administrative, or personal: "I need to change my course registration." |
| CL3 | classification | Classify the urgency as low, medium, or high: "My assignment is due in three weeks." |
| CL4 | classification | Classify this statement as a fact, opinion, or prediction: "I think the next exam will be difficult." |
| CL5 | classification | Classify this activity as review, practice, or new learning: "I am solving additional problems on a topic I already learned." |
| RE1 | reasoning_estimation | A student studies 2 hours per day for 5 days and then 3 hours on Saturday. How many hours did they study? |
| RE2 | reasoning_estimation | A project has 4 tasks requiring 2, 3, 5, and 4 hours. If 2 hours of work are completed each day, how many full days are needed? |
| RE3 | reasoning_estimation | A class has 80 students. If 25% miss a lecture, how many students attended? |
| RE4 | reasoning_estimation | A model processes 120 tokens in 6 seconds. What is its throughput in tokens per second? |
| RE5 | reasoning_estimation | A student has 12 hours available and 4 assignments requiring 2, 3, 4, and 5 hours. Can all assignments be completed? |
| SE1 | structured_extraction | Extract the name, date, and location from: "Maya has a biology exam on November 12 in Lincoln Hall." Return JSON only. |
| SE2 | structured_extraction | Extract the task and deadline from: "Submit the database project by Friday at 5 PM." Return JSON only. |
| SE3 | structured_extraction | Extract the course, credits, and instructor from: "CS 124 is a 3-credit course taught by Professor Lee." Return JSON only. |
| SE4 | structured_extraction | Extract the product, quantity, and unit price from: "I bought 2 notebooks for $6 each." Return JSON only. |
| SE5 | structured_extraction | Extract all events and their dates from: "The workshop is on March 3, and the final presentation is on March 10." Return JSON only. |
| SU1 | summarization | Summarize in exactly two bullet points: "Students must complete weekly readings, submit homework every Thursday, attend discussion sections, and complete a final project during the last two weeks." |
| SU2 | summarization | Summarize in one sentence: "Model A was fastest, Model B was most accurate, and Model C used the least memory." |
| SU3 | summarization | Summarize the action items: "Finish the interface by Monday, test the API on Tuesday, and fix critical bugs before Friday." |
| SU4 | summarization | Summarize in no more than 40 words: "Quizzes account for 15% of the grade, midterms for 40%, and the cumulative final for 45%." |
| SU5 | summarization | Summarize the cause and result: "The server received too many simultaneous requests, causing slow responses and timeouts. The team added caching and rate limiting, reducing timeouts." |