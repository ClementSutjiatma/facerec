//Provides anonymous log on to AWS services
function AnonLog() {
  // Configure the credentials provider to use your identity pool
  AWS.config.region = 'us-east-1'; // Region
  AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:168a0483-7bf7-45b2-af68-9452dbe8d488',
  });
  // Make the call to obtain credentials
  AWS.config.credentials.get(function () {
    // Credentials will be available when this function is called.
    //var accessKeyId = AWS.config.credentials.accessKeyId;
    //var secretAccessKey = AWS.config.credentials.secretAccessKey;
    var accessKeyId = 'AKIAJY5FGYFDHNQTZMTA';
    var secretAccessKey = '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';
    var sessionToken = AWS.config.credentials.sessionToken;
  });
}
