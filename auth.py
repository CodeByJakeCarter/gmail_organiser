import os
import google.auth.transport.requests
import google_auth_oauthlib.flow
import googleapiclient.discovery

def authenticate_user():
    """Authenticate the user with OAuth 2.0 and return the credentials."""
    # Define the scopes
    scopes = ["https://www.googleapis.com/auth/userinfo.profile"]

    # Create the flow using the client secrets file
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes)

    # Run the flow to get the credentials
    credentials = flow.run_local_server(port=0)

    return credentials

if __name__ == "__main__":
    # Authenticate the user and get the credentials
    credentials = authenticate_user()

    # Create a service object for the Google API
    service = googleapiclient.discovery.build(
        'oauth2', 'v2', credentials=credentials)

    # Get user info
    user_info = service.userinfo().get().execute()
    # Print the user info
    print("User Info:", user_info)
    # Save the credentials to a file
    with open('token.json', 'w') as token:
        token.write(credentials.to_json())
    print("Credentials saved to token.json")
    # Print the user info
    print("User Info:", user_info)

    