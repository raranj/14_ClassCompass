
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
