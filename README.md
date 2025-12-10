Rationale
===
To show how federated identity can now be used for AWS resources talking to Azure resources.

This uses `sts:GetWebIdentityToken` to get a valid OAuth token to federate to Azure



Deployment Instructions
===
1. Fork repo
2. Create appropriate iam role and app registration in both clouds for CI to run.
3. Give Application.ReadWrtier.OwnedBy to app registration in Azure.
4. Give the app registration in Azure the ability to assign `Reader and Data Access` to the service principal it creates against the resource group this CI works in
5. in the AWS Account enable [Outbound Identity Federation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_outbound_getting_started.html#enable-outbound-federation)
6. Configure OIDC in AWS via https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
7. Give the IAM role you create `AdministratorAccess` or at least enough to
   - Deploy the cloudformation stkac
   - Execute the lambda
7. Create the github secrets:
   - AWS_ROLE_ARN
   - AWS_REGION
   - AZURE_CLIENT_ID
   - AZURE_TENANT_ID
   - AZURE_SUBSCRIPTION_ID
   - AZURE_RESOURCE_GROUP
8. Run github workflow `app-run.yml`