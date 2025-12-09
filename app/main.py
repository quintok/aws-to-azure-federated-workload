import json
import os
from typing import List

import boto3
from azure.identity import ClientAssertionCredential
from azure.core.exceptions import ClientAuthenticationError


# Environment configuration
AZURE_TENANT_ID = os.environ["ENTRA_TENANT_ID"]
AZURE_CLIENT_ID = os.environ["ENTRA_CLIENT_ID"]

AZURE_SCOPES: List[str] = ["https://management.azure.com/.default"]
FEDERATED_TOKEN_AUDIENCE = "api://AzureADTokenExchange"
STS_TOKEN_DURATION = 300
STS_SIGNING_ALGORITHM = "RS256"

_sts = boto3.client("sts")

def _get_assertion() -> str:
    resp = _sts.get_web_identity_token(
        Audience=[FEDERATED_TOKEN_AUDIENCE],
        DurationSeconds=STS_TOKEN_DURATION,
        SigningAlgorithm=STS_SIGNING_ALGORITHM,
    )
    return resp["WebIdentityToken"]

_credential = ClientAssertionCredential(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_CLIENT_ID,
    func=_get_assertion,
)


def lambda_handler(event, context):
    """Acquire an Azure access token using the AWS-issued web identity token."""
    try:
        token = _credential.get_token(*AZURE_SCOPES)
        body = {
            "scopes": AZURE_SCOPES,
            "expires_on": token.expires_on,
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except (ClientAuthenticationError) as exc:
        return {"statusCode": 401, "body": json.dumps({"error": str(exc)})}
    except Exception as exc:  # pylint: disable=broad-except
        return {"statusCode": 500, "body": json.dumps({"error": str(exc)})}