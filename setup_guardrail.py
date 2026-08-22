#!/usr/bin/env python3

import json
from pathlib import Path

import boto3

REGION = "us-east-1"
CONFIG_PATH = Path("agentcore_config.json")
GUARDRAIL_NAME = "support-chatbot-guardrail"

bedrock = boto3.client("bedrock", region_name=REGION)

filters = [
    {
        "type": "PROMPT_ATTACK",
        "inputStrength": "HIGH",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
    {
        "type": "HATE",
        "inputStrength": "MEDIUM",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
    {
        "type": "INSULTS",
        "inputStrength": "MEDIUM",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
    {
        "type": "SEXUAL",
        "inputStrength": "MEDIUM",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
    {
        "type": "VIOLENCE",
        "inputStrength": "MEDIUM",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
    {
        "type": "MISCONDUCT",
        "inputStrength": "MEDIUM",
        "outputStrength": "NONE",
        "inputAction": "BLOCK",
        "outputAction": "NONE",
        "inputEnabled": True,
        "outputEnabled": False,
    },
]

response = bedrock.create_guardrail(
    name=GUARDRAIL_NAME,
    description="Input protection for the Customer Support Chatbot.",
    blockedInputMessaging=(
        "I can't process that request. Please rephrase it as a legitimate "
        "customer-support question."
    ),
    blockedOutputsMessaging="I can't provide that response.",
    contentPolicyConfig={
        "filtersConfig": filters,
        "tierConfig": {"tierName": "CLASSIC"},
    },
)

guardrail_id = response["guardrailId"]

version_response = bedrock.create_guardrail_version(
    guardrailIdentifier=guardrail_id,
    description="Submission-ready customer support guardrail",
)

config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

config.update({
    "guardrail_name": GUARDRAIL_NAME,
    "guardrail_id": guardrail_id,
    "guardrail_arn": response["guardrailArn"],
    "guardrail_version": version_response["version"],
})

CONFIG_PATH.write_text(
    json.dumps(config, indent=2) + "\n",
    encoding="utf-8",
)

print("Guardrail created successfully.")
print("id:", guardrail_id)
print("arn:", response["guardrailArn"])
print("version:", version_response["version"])
print("Saved to agentcore_config.json.")
