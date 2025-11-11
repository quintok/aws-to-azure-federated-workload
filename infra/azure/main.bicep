extension microsoftgraph

param oidcAudience string
param subject string
param appName string = 'my-aws-app'

// --- GitHub Credentials
resource githubApp 'Microsoft.Graph/applications@beta' = {
  displayName: 'my-aws-app'
  uniqueName: appName

  resource githubFedAuth 'federatedIdentityCredentials@beta' = {
    name: '${appName}/cognito-federated-credential'
    audiences: [
      oidcAudience
    ]
    issuer: 'https://cognito-identity.amazonaws.com'
    subject: subject
  }
}
