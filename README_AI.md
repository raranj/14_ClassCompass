
# ClassCompass Workflow

## Data Input

ClassCompass allows authenticated students to submit syllabi for AI to extract assignments and other events/deadlines.
The frontend sends the text as a JSON POST request to /api/extract-syllabus/.

For example:

{
  "syllabus": "CS 225: MP1 is due September 5, 2026. Estimated time: 6 hours."
}

The endpoint processes the text and returns structured assignment information. Students review the extracted information before adding it to the app's calendar.

## Preprocessing

The Django view checks that the submitted text is a nonempty string and enforces an input length limit.
The text is stripped of surrounding whitespace and inserted into a structured prompt containing instructions and examples.

The Hugging Face tokenizer converts the prompt into model input tokens, with a maximum input length of 2048 tokens.
The model is instructed to return the following JSON fields:

- course
- assignment
- due_date
- estimated_hours

Dates use YYYY-MM-DD format, estimated workload uses hours, and missing information is represented by null.

## Safety Guardrails

The application requires authentication for the extraction endpoint and uses CSRF protection for browser requests.
The submitted syllabus is treated as untrusted data rather than instructions to the model.
Input length limits and output token limits prevent excessively large inference requests.

The generated response is parsed and validated to ensure it contains the required fields with the expected data types.
If the response cannot be parsed or fails validation, the application returns an error instead of treating the output as reliable assignment information.
The model does not automatically save extracted deadlines. Students can review and correct any results before using them.

## AI Model Selection

ClassCompass uses Qwen3-0.6B from Hugging Face because it can run locally without requiring a paid API. We originally chose Qwen3-4B because it performed well in our earlier assignments. However, the model took too long to load and required more storage than our local computer could handle. We switched to Qwen3-0.6B because it was smaller and could still extract assignment information.

We used Qwen3-0.6B because it was one of the models we tested in our earlier assignments. We originally wanted to use Qwen3-4B because it had better evaluation results but it required too much memory for our local setup. We switched to Qwen3-0.6B because it was smaller and could run locally. Our A9 tests showed that it could still extract assignment information correctly even though it sometimes missed details.

Our main goal was to have a model that could correctly identify assignment information and return it in JSON format. We also wanted the response time to be reasonable because students would be using the feature directly through the website.

### Previous Model Testing (A6)

In A6 we tested 15 Hugging Face models to compare their performance. Qwen3-4B achieved 100% field accuracy and 100% strict JSON compliance for our extraction tests. It performed just as well as some larger models such as Qwen2.5-14B. This showed us that using a larger model did not always improve the results.

We originally selected Qwen3-4B because it gave us accurate results without requiring as many resources as the larger models. However, it was still too large for our local setup during A9.

We also tested Qwen3-0.6B in A6 and it achieved 81.25% field accuracy with an average latency of 5.71 seconds. It returned valid JSON but had 0% strict JSON compliance. We switched to this model for A9 because it required fewer resources and could run on our local computer. We improved its JSON output by disabling thinking mode and changing the extraction prompt.

### Model Performance and Latency (A7)

In A7 we compared models based on quality and latency. Mistral-7B had the highest average quality score of 9.97/10 while Qwen3-4B scored 9.92/10. Qwen2-1.5B scored 8.99/10 but had a lower latency of 2.61 seconds.

These results showed us that model size was not the only factor that mattered. A smaller model could still perform well while responding faster. We also tested Qwen3-0.6B in A7 but did not have a quality score for it, so we could not directly compare its accuracy with the other models.

We chose Qwen3-0.6B for A9 because the larger model was difficult to run locally. The smaller model worked with our available hardware and our tests showed that it could still return useful assignment information. The quality scores from A7 were based on model self-evaluation, so we also needed to test the actual outputs in ClassCompass.

### A8 Integration

In A8 we worked with retrieval techniques to find relevant information from documents. For A9 we used direct extraction instead because students enter syllabus text and the model processes it directly. We did not need a separate retrieval system because our current feature works with shorter syllabus inputs. If we expand the feature to support longer syllabi or multiple documents then retrieval or chunking could help us find the relevant assignment information before sending it to the model.

## AI Architecture

The syllabus extractor is connected directly to our Django application. Students enter syllabus text through the webpage and the text is sent to the Django backend. The backend validates the input before passing it to the local Qwen model.

The model generates the assignment information in JSON format. The response is then parsed and returned to the webpage so the student can review the extracted information.

```text
Student Input
     |
     v
Django View
     |
     v
Input Validation
     |
     v
Prompt Construction
     |
     v
Qwen3-0.6B
     |
     v
JSON Parsing and Validation
     |
     v
Extracted Assignment
     |
     v
ClassCompass Webpage
```

The AI processing is handled by `process_syllabus_extraction()` in `courses/ai_prototype.py`. The Django view handles the request and sends the results back to the frontend.

## Evaluation

We tested Qwen3-0.6B using five different syllabus inputs because we wanted to see how well the model handled different situations. The tests included structured assignments and unstructured syllabus text. We also tested missing information and a syllabus without any assignments.

The model was able to return structured information for the valid assignments. It also handled missing estimated hours without making up a value. The first CS 225 test missed the estimated hours but the extraction worked after we updated the prompt.

Test 1 - CS 225:
CS 225 - Data Structures
Fall 2026
Instructor: Dr. Smith

Course Assignments:
Machine Problem 1 (MP1)
Due Date: September 15, 2026
Estimated Completion Time: 6 hours

Students must submit their completed MP1 assignment on the course website before 11:59 PM.


Test 2 - ECE 391:
ECE 391 - Computer Systems Engineering
Fall 2026

Assignment Schedule:
MP1: System Calls - Due September 10, 2026 - Estimated 8 hours
MP2: File Systems - Due September 24, 2026 - Estimated 12 hours
MP3: Processes and Threads - Due October 15, 2026 - Estimated 15 hours

All assignments must be submitted before 11:59 PM.


Test 3 - MATH 241:
MATH 241 - Calculus III
Fall 2026
Instructor: Professor Johnson

Homework Assignment 4
Due Date: October 18, 2026

Complete textbook problems from Chapter 12 and submit your solutions through the course portal.


Test 4 - CS 410:
Welcome to CS410! This semester we will explore information retrieval, search engines, and document ranking. Please remember that the first programming project, called Search Engine Implementation, should be uploaded by October 21, 2026. Students typically need around 10 hours to finish the implementation. Late submissions will receive a penalty.


Test 5 - ASTRO 350:
ASTRO 350 - Fall 2026
Instructor: Dr. Williams
Office Hours: Monday and Wednesday, 2 PM - 4 PM

Course Description:
This course covers stars, galaxies, cosmology, and the evolution of the universe. Students are expected to attend lectures and participate in classroom discussions.

No assignments or deadlines are listed in this section.

| Test Input | Expected Behavior | Actual Output | Quality Notes | Latency                                                                                                                                                                                                                                                |
|---|---|---|---|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CS 225 - Basic Extraction | Extract MP1 with September 15 due date and 6 hours | Correctly extracted all four fields after prompt improvement | Initially missed estimated hours but correctly returned 6 after updating the prompt | 12.363s                                                                                                                                                                                                                                                |
| ECE 391 - Multiple Assignments | Extract MP1 with September 10 due date and 8 hours | Extracted MP1 with the correct information | Correct for MP1 but did not extract the other assignments | 16.138s                                                                                                                                                                                                                                                |
| MATH 241 - Missing Hours | Extract Homework 4 and leave estimated hours empty | Correctly returned missing estimated hours | Correct because the syllabus did not provide an estimate | 11.462s                                                                                                                                                                                                                                                |
| CS 410 - Unstructured Text | Extract Search Engine Implementation with October 21 due date and 10 hours | Correctly extracted all fields | Correct even though the information was written as a paragraph | 9.496s                                                                                                                                                                                                                                                 |
| ASTRO 350 - No Assignment | Return an error without inventing information | Returned "No assignment found in syllabus" | Correctly handled the missing assignment | Not recorded |

For Astro 350 test, it returned valid JSON but did not identify an assignment. The application returned HTTP 422 because the assignment field was null. The inference time was not displayed because the request ended with an error response.

The successful tests returned the expected JSON structure because the output included the course name, assignment name, due date and estimated hours. Missing information was returned as null instead of making up a value. The ECE 391 test returned valid information but only extracted one assignment because the current model is designed for single assignment extraction.

The tests showed that the model could handle different syllabus formats. It also showed that the model sometimes missed information even when the syllabus provided it.

The inference time for the four recorded tests ranged from 9.496 to 16.138 seconds. This was reasonable for our local testing, although the response time could still be improved.

## Failure Analysis

### Failure 1: Invalid JSON Output

One issue we faced was that Qwen3-0.6B kept generating reasoning text instead of returning JSON. The model was using its output tokens on the thinking process and the response was getting cut off before it could generate the assignment information.

This caused the JSON parser to fail and Django returned an HTTP 422 error. The model was recognizing the information in the syllabus but it was not returning it in the correct format.

### Failure 2: Missing Estimated Hours

The first CS 225 test returned the correct assignment and due date but did not extract the estimated hours. The syllabus included an estimate of 6 hours but the model returned "Not found."

This showed that the smaller model could miss information even when it was clearly provided. We updated the prompt to explain how estimated hours should be extracted and later tested the extraction again.

### Limitation: Multiple Assignments

The ECE 391 syllabus contained multiple assignments but the model only extracted MP1. This happened because our current prompt is designed to extract one assignment at a time.

The feature works for individual assignment extraction but it cannot create a complete assignment schedule from one syllabus yet.

## Improvements Made

### Disabling Thinking Mode

We added `enable_thinking=False` because the model was generating reasoning text instead of the JSON output. Before this change the model returned an HTTP 422 error because the generated response could not be parsed.

After disabling thinking mode the model returned structured JSON that Django could process. The first successful extraction took 13.432 seconds and generated 51 tokens. This fixed the main problem that was preventing the AI feature from working through the webpage.

### Improving the Extraction Prompt

The first CS 225 test missed the estimated hours even though the syllabus included 6 hours. We updated the prompt because the model needed clearer instructions for extracting workload estimates. After the change the model correctly extracted all four fields. The inference time also decreased from 13.432 seconds to 12.363 seconds in our test.

We also updated the system prompt because the model initially missed the estimated hours in our CS 225 test. The new prompt gives clearer instructions for identifying estimated time and converting it into hours.

After the prompt changes we successfully extracted estimated hours in later tests. The ECE 391 test returned 8 hours and the CS 410 test returned 10 hours. We also tested MATH 241 without an estimated workload and the model correctly returned a missing value.

These changes improved the reliability of the extraction process without requiring a larger model.

## Future Improvements

We want to improve the extractor so it can process multiple assignments from one syllabus because students usually have several deadlines in the same course. The current model only extracts one assignment at a time.

We also want to improve extraction accuracy because the smaller model can still miss information. A stronger model could help with more complicated syllabus formats but we would need to consider the additional memory and processing requirements.

The current feature allows students to review the AI results before using them in their calendar. This is important because the extracted information should be checked before students rely on it for their schedules.