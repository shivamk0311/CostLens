def calculate_cost(model, prompt_tokens, completion_tokens):
    
    pricing = {
        "gpt-4o-mini" : {
            "input" : 0.15 /1_000_000,
            "output": 0.60 /1_000_000
        },
        "gpt-4o" : {
            "input" : 2.50 /1_000_000,
            "output": 10.00 /1_000_000
        },
    }

    if model not in pricing:
        raise ValueError(f"Unsupported model for pricing: {model}")

    model_pricing = pricing[model]

    if model_pricing is None:
        return 0.0

    input_cost = model_pricing["input"] * prompt_tokens
    output_cost = model_pricing["output"] * completion_tokens

    return round(input_cost + output_cost, 6)
