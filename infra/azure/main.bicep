extension microsoftgraph

param oidcAudience string
param developerProvidedName string
param ownerApplicationId string
param appName string = 'my-aws-app'
param applicationId string = guid(appName, oidcAudience, developerProvidedName)

// --- GitHub Credentials
resource githubApp 'Microsoft.Graph/applications@beta' = {
  displayName: 'my-aws-app'
  uniqueName: appName
  owners: [

  ]

  resource githubFedAuth 'federatedIdentityCredentials@beta' = {
    name: '${appName}/cognito-federated-credential'
    audiences: [
      oidcAudience
    ]
    issuer: 'https://cognito-identity.amazonaws.com'
    claimsMatchingExpression: {
      languageVersion: 1
      value: 'claims[\'amr\'] eq \'${developerProvidedName}:${oidcAudience}:${applicationId}\''
    }
  }
}
