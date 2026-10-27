# P1-A7: Multi-Model AI Systems
## System Design, Cost Analysis, and Routing Strategy

## 1. Part 1: Model Size Selection and Benchmarking

### 1.1 Model Size Categories

I evaluated 15 instruction-tuned language models across five parameter-size categories. Each category contains three models.

| Model Category | Parameter Range | Models |
|---|---|---|
| Ultra-Light | Less than 1B | SmolLM2-360M-Instruct, Qwen2.5-0.5B-Instruct, Qwen3-0.6B |
| Small | 1B to less than 3B | Qwen2.5-1.5B-Instruct, SmolLM2-1.7B-Instruct, Qwen2-1.5B-Instruct |
| Medium | 3B to less than 7B | Qwen2.5-3B-Instruct, Qwen3-4B-Instruct-2507, Phi-3.5-mini-instruct |
| Large | 7B to less than 13B | Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, Falcon3-7B-Instruct |
| Very Large | 13B and above | Qwen2.5-14B-Instruct, Qwen3-14B, DeepSeek-R1-Distill-Qwen-14B |

The model categories let me compare whether increasing parameter count improves output quality and whether those improvements justify additional latency and hosting costs.

### 1.2 Prompt Types and Evaluation Prompts

The benchmark uses five prompt categories that represent different tasks a course-planning and study-assistance application such as ClassCompass may need to perform.

| Prompt Type | Purpose | Prompt IDs |
|---|---|---|
| Structured extraction | Extract deadlines, course names, assignments, and other fields from unstructured text | SE1-SE5 |
| Classification | Categorize academic tasks, materials, or student requests | CL1-CL5 |
| Summarization | Condense course materials and instructions into useful summaries | SU1-SU5 |
| reasoning_estimation | Use provided information to answer questions or help plan academic work | RE1-RE5 |
| Ambiguity handling | Identify missing information, avoid unsupported assumptions, and ask clarifying questions | AH1-AH5 |

Five prompts were designed for each category, giving 25 unique prompts. Each of the 15 models was evaluated against the same prompt set, for 375 model-prompt combinations.

The prompts are intended to reflect realistic inputs rather than only testing general knowledge. For example, a structured extraction prompt may ask a model to identify assignment names, due dates, and point values from a syllabus excerpt. An ambiguity-handling prompt may omit a deadline or provide conflicting dates and check whether the model acknowledges the uncertainty.

The full prompt texts, benchmark outputs, and scaling simulations are recorded in `multi_model_system.ipynb`. The prompt catalog is also available in `prompt_documentation.md`.

### 1.3 Evaluation Metrics

Each response was evaluated using four criteria on a 1-10 scale.

| Metric | Description |
|---|---|
| Instruction adherence | Whether the model followed the requested task and constraints |
| Accuracy | Whether the response correctly reflected the provided information and avoided unsupported claims |
| Clarity | Whether the response was understandable and useful |
| Structure | Whether the response followed the requested format and was organized appropriately |

The overall quality score is the average of the four metric scores:

`quality_score = (instruction_adherence + accuracy + clarity + structure) / 4`

Latency, measured in seconds, and throughput, measured in generated tokens per second, were also recorded. These performance metrics help compare models that produce similarly useful outputs but have different response times.

### 1.4 Benchmark Results and Analysis

The benchmark results show that Mistral-7B-Instruct-v0.3 achieved the highest recorded average quality score, at 9.97/10. Qwen3-4B-Instruct-2507 followed at 9.92, while Qwen3-14B achieved 9.87 and Falcon3-7B-Instruct achieved 9.85.

| Model | Average Quality | Latency (seconds) | Throughput (tokens/sec) | Scored Responses |
|---|---:|---:|---:|---:|
| Mistral-7B-Instruct-v0.3 | 9.97 | 6.21 | 13.88 | 25 |
| Qwen3-4B-Instruct-2507 | 9.92 | 8.15 | 10.98 | 25 |
| Qwen3-14B | 9.87 | 9.63 | 9.05 | 25 |
| Falcon3-7B-Instruct | 9.85 | 5.76 | 14.67 | 25 |
| Phi-3.5-mini-instruct | 9.75 | 9.12 | 16.90 | 24 |
| Qwen2.5-7B-Instruct | 9.40 | 6.70 | 14.36 | 24 |
| Qwen2.5-14B-Instruct | 9.29 | 9.43 | 8.72 | 25 |
| Qwen2.5-3B-Instruct | 9.26 | 6.91 | 11.90 | 24 |
| Qwen2-1.5B-Instruct | 8.99 | 2.61 | 25.05 | 25 |
| Qwen2.5-1.5B-Instruct | 8.98 | 3.74 | 24.77 | 25 |
| Qwen2.5-0.5B-Instruct | 8.05 | 3.62 | 30.39 | 25 |
| SmolLM2-1.7B-Instruct | 6.31 | 1.95 | 27.70 | 25 |
| SmolLM2-360M-Instruct | 5.00 | 2.41 | 25.34 | 16 |
| DeepSeek-R1-Distill-Qwen-14B | Not scored | 29.67 | 8.63 | 0 |
| Qwen3-0.6B | Not scored | 10.05 | 23.60 | 0 |

**Which model category produced the best outputs?**

The Large category had the highest mean quality among the scored models, at approximately 9.74/10. Its three models were Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, and Falcon3-7B-Instruct. The Medium category followed at approximately 9.64/10.

These category averages should be interpreted cautiously because some models have missing evaluation scores. In particular, the Ultra-Light category has only two models with available scores, and SmolLM2-360M-Instruct was scored on only 16 of its 25 responses.

**Did larger models always perform better?**

No. Parameter count alone did not determine quality. Qwen3-4B achieved a 9.92 average quality score, exceeding Qwen2.5-14B at 9.29. Mistral-7B also outperformed the tested 14B models with available scores. Smaller models such as Qwen2-1.5B produced useful responses with lower latency and higher throughput.

This suggests that model architecture, training, instruction tuning, and task fit can matter as much as model size. The results do not establish that every smaller model is better than every larger model, but they show that increasing parameter count does not guarantee better results.

**Which model gave the best balance between speed and output quality?**

Qwen2-1.5B-Instruct was a strong speed-quality choice. It achieved an average quality score of 8.99, a latency of 2.61 seconds, and a throughput of 25.05 tokens per second. It produced a higher quality score than Qwen2.5-0.5B while remaining substantially faster than the highest-scoring 7B models in this benchmark.

Mistral-7B-Instruct-v0.3 is the stronger choice when output quality is the primary objective. Qwen2-1.5B-Instruct is a reasonable default for frequent, straightforward requests where response time and compute costs matter.

**Evaluation limitations:** DeepSeek-R1-Distill-Qwen-14B and Qwen3-0.6B have no scored responses in the current results, so their quality cannot be ranked. SmolLM2-360M-Instruct's score is based on 16 responses, not all 25. These gaps should be reported rather than replaced with invented scores. Latency and throughput are benchmark observations and may differ on other hardware or under concurrent production traffic.

The quality comparisons use available evaluation scores only. Models with missing scores are excluded from quality rankings, and averages based on fewer than 25 responses may not be directly comparable with fully scored models.

---

## 2. Part 2: Cost Comparison and Infrastructure Planning

### 2.1 Estimated Token Usage

For the scaling simulation, I assume that each daily active user makes one AI request per day and that each request generates an average of 500 tokens. This provides a consistent baseline for comparing traffic levels.

The estimate represents generated tokens, not the total of input and output tokens. Actual usage will vary by feature: a short classification request may use fewer tokens, while syllabus summarization or study-plan generation may use more.

### 2.2 Total Daily Token Load

The total daily token load is calculated as:

`Daily token load = Daily active users × 500 generated tokens`

| Traffic Category | Daily Active Users | Assumed Tokens per User | Total Daily Token Load |
|---|---:|---:|---:|
| Prototype | 1,000 | 500 | 500,000 |
| Early Startup | 10,000 | 500 | 5,000,000 |
| Growing Product | 100,000 | 500 | 50,000,000 |
| Large Platform | 1,000,000 | 500 | 500,000,000 |
| Mass Consumer App | 10,000,000 | 500 | 5,000,000,000 |
| Global Platform | 100,000,000 | 500 | 50,000,000,000 |

### 2.3 Local Hosting Cost Assumptions

For the local-hosting estimate, I assume a cloud GPU machine with 16 vCPUs, 64 GB of RAM, and a GPU. As a pricing reference, an AWS g5.4xlarge has 16 vCPUs and 64 GiB of RAM. The example on-demand price used here is $1.62 per hour, or $38.88 for 24 hours. Actual costs vary by provider, region, and purchasing arrangement.

Pricing reference: [AWS EC2 G5 instance specifications](https://aws.amazon.com/ec2/instance-types/accelerated-computing/) and [G5 instance pricing](https://www.economize.cloud/resources/aws/pricing/ec2/family/g5/).

The machine-cost estimate uses:

- Cost per machine per day: `$1.62 × 24 = $38.88`
- Assumed usable capacity: 60% of measured benchmark throughput, leaving capacity for variation and overhead
- Estimated daily capacity per machine: `tokens/sec × 86,400 × 0.60`
- Machines required: `ceiling(daily token load / estimated daily machine capacity)`
- Total daily hosting cost: `machines required × $38.88`

For example, Qwen2-1.5B-Instruct achieved 25.05 tokens per second in the benchmark. Its estimated daily capacity under this assumption is:

`25.05 × 86,400 × 0.60 = 1,298,592 tokens/day`

The resulting estimates are:

| Traffic Category | Daily Token Load | Estimated Machines for Qwen2-1.5B | Estimated Daily Local Cost |
|---|---:|---:|---:|
| Prototype | 500,000 | 1 | $38.88 |
| Early Startup | 5,000,000 | 4 | $155.52 |
| Growing Product | 50,000,000 | 39 | $1,516.32 |
| Large Platform | 500,000,000 | 386 | $15,007.68 |
| Mass Consumer App | 5,000,000,000 | 3,851 | $149,726.88 |
| Global Platform | 50,000,000,000 | 38,504 | $1,497,035.52 |

These figures are simplified capacity estimates, not production deployment guarantees. They extrapolate benchmark throughput to daily capacity and do not model batching gains, queueing, concurrent requests, memory limits, autoscaling delays, redundancy, or multiple models sharing a machine. The full notebook should calculate machine requirements separately for all 15 models using their measured throughput.
The complete local-hosting simulation covers all 15 models across all six traffic levels, producing 90 model-traffic combinations. The calculations use each model's measured throughput and the same machine-cost and utilization assumptions.

### 2.4 Hugging Face Inference API Cost Assumptions

Hugging Face Inference Providers routes requests to supported inference providers and bills according to the selected provider's pricing. Therefore, the API price is not a universal fixed rate for every model.

For a consistent classroom comparison, I use an **assumed rate of $0.03 per 1,000 generated tokens**. This is a modeling assumption, not a claim about the current price of a particular hosted model. A production estimate should replace it with the actual rate for the selected model and provider.

Pricing reference: [Hugging Face Inference Providers pricing and billing](https://huggingface.co/docs/inference-providers/pricing).

The calculation is:

`Estimated API cost = (daily token load / 1,000) × $0.03`

For this comparison, the API provider manages the inference machines. Therefore, the number of customer-managed API inference machines is zero; the API cost represents the assumed usage charge. This does not mean the provider uses no infrastructure.

| Traffic Category | Daily Token Load | Assumed API Cost per 1,000 Tokens | Estimated Daily API Cost |
|---|---:|---:|---:|
| Prototype | 500,000 | $0.03 | $15 |
| Early Startup | 5,000,000 | $0.03 | $150 |
| Growing Product | 50,000,000 | $0.03 | $1,500 |
| Large Platform | 500,000,000 | $0.03 | $15,000 |
| Mass Consumer App | 5,000,000,000 | $0.03 | $150,000 |
| Global Platform | 50,000,000,000 | $0.03 | $1,500,000 |

For the full 90-row comparison, the notebook should use each local model's measured throughput for local machine calculations. The API calculation should use the selected rate assumption consistently unless model-specific provider prices are available. The closest available hosted instruction model should be recorded for each local model rather than assuming every model is offered by every provider.
The complete API cost simulation also contains 90 model-traffic combinations. Because the $0.03 per 1,000 generated tokens rate is hypothetical, these figures support a consistent comparison rather than a prediction of actual provider charges.

### 2.5 Local Hosting vs. API Analysis

**At what scale is local hosting cheaper?**

Using the Qwen2-1.5B example and the assumptions above, local hosting becomes slightly cheaper at the Mass Consumer App scale. The estimate is approximately $149,726.88 per day locally compared with $150,000 per day through the assumed API rate.

The difference is very small, so it should not be treated as a universal break-even point. A different model throughput, API provider, token rate, hardware price, or utilization rate can change the result.

**At what scale is API usage cheaper?**

API usage is cheaper for the Prototype, Early Startup, Growing Product, and Large Platform categories under this example. It avoids the cost of maintaining a dedicated inference fleet when request volume is relatively low. It also reduces the operational work of provisioning GPUs, monitoring capacity, and scaling machines.

**When would I switch the architecture?**

I would start with a hosted inference API because the initial traffic is relatively low and the application can avoid managing GPU infrastructure. I would measure actual usage, latency, quality, and monthly spending before moving any workload to local hosting.

As traffic increases, I would compare the actual API bill against a revised local-hosting estimate. If frequent, predictable requests make dedicated hosting cheaper, I would consider moving those requests to a local model. I would keep an API fallback for requests that require stronger reasoning or when local capacity is unavailable.

The decision should consider more than token cost. Privacy requirements, reliability, deployment effort, model availability, response latency, and the quality of the generated study plans all affect the final architecture.

---

## 3. Part 3: Multi-Model Routing Strategy

### 3.1 Routing Architecture

I propose a hybrid architecture for ClassCompass that uses a fast local model for routine tasks and a stronger hosted model for requests that require more detailed reasoning or better handling of complex instructions.

The router evaluates the task type, prompt length, ambiguity, recent latency, and available capacity before choosing a model. It should not automatically send every request to the largest model. Instead, it should use the least expensive model that meets the task's quality requirements.

The proposed architecture is:

1. Receive the user's request.
2. Identify the task type and estimate its complexity.
3. Check whether required information is missing or contradictory.
4. Select a local model or a hosted model based on task requirements and system load.
5. Validate the response format and check for missing required fields.
6. Return the response or ask the user for clarification.
7. Record latency, token usage, routing choice, and quality signals for future evaluation.

### 3.2 Five Scenarios and Routing Strategies

| Scenario | Routing Strategy | Local Model | Hosted Hugging Face Model | Expected Benefit |
|---|---|---|---|---|
| Normal operation | Send straightforward classification, short summaries, and routine study-planning requests to the local model. | Qwen2-1.5B-Instruct | Mistral-7B-Instruct-v0.3, if available through the selected provider | Lower routine latency and reduced dependence on API calls |
| Peak usage before exams | Keep simple requests on the local model. Route only complex or queued requests to the hosted model when local utilization passes a threshold. | Qwen2.5-0.5B-Instruct for simple requests; Qwen2-1.5B-Instruct for standard requests | Mistral-7B-Instruct-v0.3, or a comparable supported hosted instruction model | Preserves responsiveness during demand spikes |
| Complex or ambiguous syllabus | Use a stronger model for conflicting deadlines, complicated instructions, or requests that require reasoning across several pieces of course information. Ask for clarification if key information is missing. | Qwen2-1.5B-Instruct for initial parsing | Mistral-7B-Instruct-v0.3, or a comparable supported hosted instruction model | Improves handling of difficult requests and reduces unsupported assumptions |
| Cost optimization | Route frequent, repetitive tasks to the local model. Use the hosted model only when the local response fails validation or the task requires stronger reasoning. | Qwen2.5-0.5B-Instruct for simple tasks; Qwen2-1.5B-Instruct for standard tasks | A supported hosted instruction model used selectively | Controls API spending while retaining a higher-quality option |
| Local system overload or failure | Detect high latency, failed requests, or unavailable local capacity. Send requests to the hosted model if the provider is available; otherwise return a clear retry message. | Qwen2-1.5B-Instruct when healthy | Mistral-7B-Instruct-v0.3, or a comparable supported hosted instruction model | Improves resilience and avoids leaving requests indefinitely queued |

Hosted model names are proposed choices and must be checked against the provider's current availability before implementation. The benchmark's local throughput measurements do not guarantee identical performance on the hosted provider.

### 3.3 Routing Conditions

The router can use the following conditions:

- **Task type:** Classification and short extraction tasks generally use a smaller model. Multi-step reasoning can use a stronger model.
- **Prompt length:** Very long syllabus excerpts may need preprocessing or chunking before model selection.
- **Ambiguity:** Missing or contradictory dates should trigger clarification rather than confident guessing.
- **Response validation:** Structured extraction results should be checked for required fields and valid formats before being returned.
- **System load:** High local utilization or increasing queue time can trigger hosted inference.
- **Cost budget:** Hosted calls should be limited by a daily or monthly budget.
- **Model health:** Repeated timeouts or failures should trigger a fallback to another available route.

Thresholds should be selected using load testing rather than assumed to be optimal. For example, the system could initially consider routing away from a local model when utilization exceeds 80% or when its measured response time exceeds a defined service target, then tune those thresholds using actual traffic.

### 3.4 How the Strategy Improves Latency

The strategy improves latency by keeping routine requests on a small, locally available model instead of sending every request through a hosted endpoint. This avoids network round trips for those requests and reduces unnecessary use of larger models.

During peak usage, routing simple requests to the smaller model prevents all requests from competing for the same inference capacity. Requests that require more reasoning can use the hosted model when the local queue becomes too long.

The system should monitor end-to-end latency, including preprocessing, queueing, inference, validation, and network time. A faster token-generation rate alone does not guarantee a faster complete response.

### 3.5 How the Strategy Reduces Cost

The strategy reduces cost by avoiding hosted inference for tasks that a smaller local model can complete adequately. This is especially useful for repeated operations such as classification and basic extraction.

A hosted call is justified when its expected improvement in output quality is worth the additional usage cost. The system can also cache results for identical, non-personal inputs when safe and appropriate, reducing repeated inference.

Local hosting is not automatically cheaper. The cost model must account for GPU rental, machine utilization, redundancy, maintenance, and the capacity needed to serve concurrent requests. API pricing must be checked for the specific provider and model.

### 3.6 How the Strategy Maintains Output Quality

The strategy maintains quality by assigning tasks according to difficulty and validating responses before presenting them to users.

For structured extraction, the system should check that required fields exist and that dates or point values follow the expected format. For summaries, it should ensure that important course instructions are retained. For ambiguous requests, it should ask the user to clarify rather than invent missing information.

If a local response fails validation or does not meet a defined quality threshold, the router can retry with a stronger hosted model. Repeated failures should be logged so the team can improve prompts, adjust routing thresholds, or reconsider the selected model.

The router should also be evaluated against the same 25 prompts used in the benchmark. Useful measurements include average quality score, percentage of valid structured outputs, latency, hosted-model call rate, and estimated cost per request. This makes it possible to determine whether routing actually improves the balance between quality, speed, and cost.

## 4. Conclusion

The benchmark indicates that the highest-scoring model is not necessarily the best default for every request. Mistral-7B-Instruct-v0.3 achieved the highest recorded quality score, while Qwen2-1.5B-Instruct offered a strong combination of response time, throughput, and quality.

For ClassCompass, a hybrid architecture is a reasonable starting point: use a smaller local model for routine tasks, route more difficult requests to a stronger hosted model, and validate outputs before returning them. The cost comparison suggests that the best hosting decision depends on traffic volume, measured model throughput, and the actual price of the selected inference provider.

The next step is to test the routing strategy under simulated concurrent traffic and replace the illustrative pricing assumptions with provider-specific costs before making a production deployment decision.