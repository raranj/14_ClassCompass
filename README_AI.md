
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

ClassCompass uses Qwen/Qwen3-0.6B from Hugging Face because it can run locally without a paid API. We originally used Qwen3-4B but it took too long to load and required too much storage. The smaller model was better for our local setup because it used fewer resources while still extracting assignment information.

## AI Architecture

The syllabus extractor is connected directly to the Django application. The user enters syllabus text and Django sends it to the local Qwen model. The model generates JSON which is then parsed and displayed on the webpage.

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
Qwen3-0.6B
     |
     v
JSON Parsing
     |
     v
Extracted Assignment
     |
     v
ClassCompass Webpage
```

## Evaluation

We tested the AI with five different syllabus inputs to see how well it extracted assignment information. The model performed well on structured text and unstructured paragraphs. It also handled missing information without making up values.

| Test | Result                                 | Inference Time |
|---|----------------------------------------|---|
| CS 225 - Basic Extraction | Correct                                | 13.432 seconds |
| ECE 391 - Multiple Assignments | Correctly extracted MP1 only           | 16.138 seconds |
| MATH 241 - Missing Hours | Correct                                | 11.462 seconds |
| CS 410 - Unstructured Text | Correct                                | 9.496 seconds |
| ASTRO 350 - No Assignment | Correctly returned no assignment found | Not recorded |

## Failure Analysis

One issue we faced was that Qwen kept generating reasoning text instead of returning JSON. This caused the output to get cut off and the application returned an HTTP 422 error.

The model also only extracts one assignment at a time because the current prompt is designed for a single assignment.

## Improvements Made

We disabled Qwen's thinking mode because the model was using its output tokens on reasoning instead of generating JSON. After adding `enable_thinking=False` the model successfully returned structured assignment information.

We also updated the extraction prompt to better recognize estimated hours. In a later test the model correctly extracted 8 hours from the ECE 391 syllabus.

## Future Improvements

We plan to improve the extractor so it can process multiple assignments from one syllabus. We also want to improve accuracy because the smaller model sometimes misses information. The current system displays the extracted information for students to review before using it in their calendar.

