import os
import time
from typing import Optional
from dataclasses import dataclass
import boto3
import json
from botocore.exceptions import ClientError


# Create Bedrock prompt struct for the request to invoke.
@dataclass
class BedrockBody:
    prompt: str
    max_tokens_to_sample: int
    temperature: float
    top_p: float
    anthropic_version: str = "bedrock-2023-05-31"

    def to_dict(self):
        return {
            "messages": [{"role": "user", "content": self.prompt}],
            "max_tokens": self.max_tokens_to_sample,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "anthropic_version": self.anthropic_version,
        }


# Create a struct to handle the items from the cache.
@dataclass
class CacheItem:
    log_group_arn: str
    summary: str
    timestamp: int


# We can get responses from DynamoDB cache, this makes the widget load much faster.
def get_summary_cache(log_group_arn: str) -> Optional[CacheItem]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["cache_name"])

    try:
        response = table.get_item(Key={"log_group_arn": log_group_arn})
    except ClientError as e:
        return e.response["Error"]["Message"]

    if "Item" in response:
        return CacheItem(**response["Item"])
    else:
        return None


# If the summary is not in the cache, we should put it in after doing the fetch_analysis
def put_summary(log_group_arn: str, summary: str) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["cache_name"])

    timestamp = int(time.time())
    table.put_item(
        Item={
            "log_group_arn": log_group_arn,
            "summary": summary,
            "timestamp": timestamp,
        }
    )


# Format the response from Bedrock because we only care about the completion section here.
def response_format(response_string: str) -> str:
    try:
        json_response = json.loads(response_string)
    except json.JSONDecodeError as e:
        raise e

    content = json_response["content"][0].get("text", "")
    return content.replace("\n", "<br />")


# Call on Bedrock API for summary of data.
def bedrock_analyze(result_string: str) -> str:
    body = BedrockBody(
        prompt=f"Please create some insights on the following log string.{result_string}",
        max_tokens_to_sample=1000,
        temperature=0,
        top_p=1,
    )

    blob_body = bytes(json.dumps(body.to_dict()), "utf-8")

    bedrock_client = boto3.client("bedrock-runtime")

    bedrock_resp = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=blob_body,
        contentType="application/json",
    )

    response_blob = bedrock_resp["body"].read()
    response_string = response_blob.decode("utf-8")

    response_string_formatted = response_format(response_string)

    return response_string_formatted


# Function to return most recent log stream from log_group. This way we do not have to keep updating the stream to
# analyze
def recent_log_stream(log_group_arn: str) -> str:
    logs_client = boto3.client("logs")

    response = logs_client.describe_log_streams(
        logGroupIdentifier=log_group_arn, orderBy='LastEventTime'
    )

    log_streams = response.get("logStreams", [])
    if log_streams:
        recent_stream_name = log_streams[0]["logStreamName"]
        return recent_stream_name
    else:
        raise Exception("No log streams found for the given log group ARN.")


# Fetch analysis string from bedrock
def fetch_analysis(log_group_arn: str) -> str:
    logs_client = boto3.client("logs")

    log_stream_name = recent_log_stream(log_group_arn)

    response = logs_client.get_log_events(
        logGroupIdentifier=log_group_arn, logStreamName=log_stream_name, limit=50
    )

    events = response.get("events", [])
    if not events:
        raise Exception("Unable to pull any events from the log.")

    result_string = "\n".join(
        [f"[{event['timestamp']}] {event['message']}" for event in events]
    )
    analysis = bedrock_analyze(result_string)
    put_summary(log_group_arn, analysis)
    return analysis


def lambda_handler(event: dict, context: dict) -> str:
   message = 'Hello {} !'.format(event['key1'])
   return {
       'message' : message
   }
    # if event.get("describe"):
    #     docs = """## Python Bedrock Analysis
    #     This is a widget where we will use Bedrock to analyze a CloudWatch Log Group, then return the output summary.
    #     ### Widget parameters
    #     Param | Description
    #     ---|---
    #     **log_group_arn** | The ARN of the log group to summarize

    #     ### Example Parameters
    #     ``` yaml
    #     log_group_arn: arn:aws:logs:$REGION:$ACCOUNTID:log-group:/log/GroupName
    #     ```
    #     """
    #     return docs

    # log_group_arn = event["widgetContext"]["params"].get("log_group_arn")
    # print(f"The log group arn is: {log_group_arn}")

    # if not log_group_arn:
    #     return "Missing 'log_group_arn' parameter in the request payload."
        
    # # Encode log group name for use in deep links
    # encoded_log_group_name = log_group_arn.replace("/", "$252F")

    # # Create deeplinks
    # overview_deeplink = f"https://console.aws.amazon.com/cloudwatch/home#logsV2:log-groups/log-group/{encoded_log_group_name}"
    # insights_deeplink = f"https://console.aws.amazon.com/cloudwatch/home#logsV2:logs-insights$3FqueryDetail$3D~(end~0~start~-3600~timeType~'RELATIVE~unit~'seconds~editorString~'~isLiveTail~false~queryId~'~source~(~'{encoded_log_group_name}))"
    # tail_deeplink = f"https://console.aws.amazon.com/cloudwatch/home#logsV2:live-tail$3FlogGroupArns$3D~(~'{encoded_log_group_name})"

    # # Get time for cache check
    # timestamp_now = int(time.time())

    # # Initializing string for insertion into f string html
    # payload_string = '{"retry":"true"}'

    # cache_item = get_summary_cache(log_group_arn)
    # if (
    #     cache_item
    #     and timestamp_now - cache_item.timestamp < 30 * 60
    #     and "retry" not in event
    # ):
    #     html = f"""
    #     <h2>Log Group Summary</h2>
    #     <p>{cache_item.summary}</p>
    #     <a class="btn btn-primary">Fetch a new Summary</a>
    #     <cwdb-action action="call" endpoint="{context.invoked_function_arn}">
    #         {payload_string}
    #     </cwdb-action>
    #     <a class="btn btn-primary" href="{overview_deeplink}">Log Group Overview</a>
    #     <a class="btn btn-primary" href="{insights_deeplink}">View in Logs Insights</a>
    #     <a class="btn btn-primary" href="{tail_deeplink}">Tail Log</a>
    #     """
    #     return html
    # else:
    #     analysis = fetch_analysis(log_group_arn)
    #     html = f"""
    #     <h2>Log Group Summary</h2>
    #     <p>{analysis}</p>
    #     <a class="btn btn-primary">Fetch a new Summary</a>
    #     <cwdb-action action="call" endpoint="{context.invoked_function_arn}">
    #         {payload_string}
    #     </cwdb-action>
    #     <a class="btn btn-primary" href="{overview_deeplink}">Log Group Overview</a>
    #     <a class="btn btn-primary" href="{insights_deeplink}">View in Logs Insights</a>
    #     <a class="btn btn-primary" href="{tail_deeplink}">Tail Log</a>
    #     """
    #     return html