from dataclasses import dataclass
import json
import boto3

import logging


@dataclass
class AnthropicBedrockBody:
    prompt: str
    max_tokens_to_sample: int
    temperature: float
    top_p: float
    anthropic_version: str = "bedrock-2023-05-31"
    modelId = "anthropic.claude-3-haiku-20240307-v1:0"

    def to_dict(self):
        return {
            "messages": [
                {
                    "role": "user",
                    "content": f"Please create some insights on the following log string.{self.prompt}",
                }
            ],
            "max_tokens": self.max_tokens_to_sample,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "anthropic_version": self.anthropic_version,
        }

    def bedrock_analyze(self) -> str:
        blob_body = bytes(json.dumps(self.to_dict()), "utf-8")
        logging.debug(blob_body)
        bedrock_client = boto3.client("bedrock-runtime")

        bedrock_resp = bedrock_client.invoke_model(
            modelId=self.modelId,
            body=blob_body,
            contentType="application/json",
        )

        response_blob = bedrock_resp["body"].read()
        response_string = response_blob.decode("utf-8")
        try:
            json_response = json.loads(response_string)
        except json.JSONDecodeError as e:
            raise e

        content = json_response["content"][0].get("text", "")
        return content.replace("\n", "<br />")


@dataclass
class AmazonTitantBedrockBody:
    prompt: str
    max_tokens_to_sample: int
    temperature: float
    top_p: float

    def to_dict(self):
        return {
            "messages": [{"role": "user", "content": self.prompt}],
            "max_tokens": self.max_tokens_to_sample,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "anthropic_version": self.anthropic_version,
        }
