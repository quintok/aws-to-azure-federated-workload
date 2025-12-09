extension microsoftgraph

param subject string
param issuer string
param appName string = 'my-aws-app'

// --- GitHub Credentials
resource myAwsApp 'Microsoft.Graph/applications@beta' = {
  displayName: 'my-aws-app'
  uniqueName: appName

  resource awsFedAuth 'federatedIdentityCredentials@beta' = {
    name: '${appName}/sts-federated-credential'
    audiences: [
      'api://AzureADTokenExchange'
    ]
    issuer: issuer
    subject: subject
  }
}

output appId string = myAwsApp.appId
