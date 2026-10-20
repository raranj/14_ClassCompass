## Data Input
In terms of data input, the user data is captured kept in JSON format.

## Preprocessing

For the preprocessing, we formatted the data into
a prompt layout, then used the Hugging Face tokenizer to change the raw text into a 
tensor format the PyTorch model can understand. 

## Safety Guardrails
To protect against and avoid there being too 
much input data, we set a token cap and truncation limit.
For the output, by setting a limit to the output length, we avoid generating infinitely long text
 by accident. We also disabled gradient tracking to protect the system from
memory exhaustion. To avoid broken outputs, we made functions extract_json and is_strict_json to ensure the output
is in JSON and not some other format.

