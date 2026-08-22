import boto3


def apply_input_guardrail(config, text):
    guardrail_id = config.get("guardrail_id")
    guardrail_version = config.get("guardrail_version")

    if not guardrail_id or not guardrail_version:
        return {
            "blocked": False,
            "action": "NONE",
            "message": None,
        }

    runtime = boto3.client(
        "bedrock-runtime",
        region_name=config.get("region", "us-east-1"),
    )

    response = runtime.apply_guardrail(
        guardrailIdentifier=guardrail_id,
        guardrailVersion=str(guardrail_version),
        source="INPUT",
        content=[
            {
                "text": {
                    "text": text,
                    "qualifiers": ["guard_content"],
                }
            }
        ],
        outputScope="FULL",
    )

    blocked = response.get("action") == "GUARDRAIL_INTERVENED"

    message = None
    if blocked:
        outputs = response.get("outputs") or []
        if outputs:
            message = outputs[0].get("text")

        if not message:
            message = (
                "I can't process that request. "
                "Please rephrase it as a legitimate customer-support question."
            )

    return {
        "blocked": blocked,
        "action": response.get("action", "NONE"),
        "message": message,
        "assessments": response.get("assessments", []),
    }
