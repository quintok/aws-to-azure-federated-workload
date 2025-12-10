import json
import os
from typing import List

import boto3
from azure.identity import ClientAssertionCredential
from azure.mgmt.storage import StorageManagementClient

# Environment configuration
AZURE_TENANT_ID = os.environ["ENTRA_TENANT_ID"]
AZURE_CLIENT_ID = os.environ["ENTRA_CLIENT_ID"]
SUBSCRIPTION_ID = os.environ["AZURE_SUBSCRIPTION_ID"]

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
    storage_client = StorageManagementClient(_credential, SUBSCRIPTION_ID)
    accounts = storage_client.storage_accounts.list()
    storageAccounts = []
    for account in accounts:
        storageAccounts.append({
            "name": account.name,
            "resource_group": account.id.split('/')[4],
            "location": account.location,
            "kind": account.kind,
            "sku": account.sku.name
        })

    return {"statusCode": 200, "body": json.dumps(storageAccounts)}