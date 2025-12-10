
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

resource sp 'Microsoft.Graph/servicePrincipals@beta' = {
  appId: myAwsApp.appId
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(appName, 'Storage Reader')
  scope: resourceGroup()
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', 'c12c1c16-33a1-487b-954d-41c89c60f349') // Reader and Data Access
    principalId: sp.id
  }
}

output appId string = myAwsApp.appId
