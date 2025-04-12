import googleapiclient.errors
from email.utils import parseaddr
from collections import Counter


def extract_unique_senders(service, after=None, before=None):
    query = ""
    if after:
        query += f"after:{after} "
    if before:
        query += f"before:{before} "

    message_ids = []
    try:
        # Fetch the initial batch of messages
        response = service.users().messages().list(
            userId='me',
            q=query
        ).execute()
        if 'messages' in response:
            message_ids.extend(response['messages'])

        # Handle pagination
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId='me',
                q=query,
                pageToken=page_token
            ).execute()
            if 'messages' in response:
                message_ids.extend(response['messages'])
    except googleapiclient.errors.HttpError as error:
        print(f'An error occurred: {error}')
        return Counter()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return {}

    # Extract senders
    sender_counts = Counter()
    for msg in message_ids:
        try:
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From']
            ).execute()
            headers = message['payload']['headers']
            for header in headers:
                if header['name'] == 'From':
                    raw_sender = header['value']
                    email_address = parseaddr(raw_sender)[1]
                    sender_counts[email_address] += 1
                    break
        except googleapiclient.errors.HttpError as error:
            print(f"Failed to fetch message {msg['id']}: {error}")
        except Exception as e:
            print(f"An unexpected error occurred while processing message {msg['id']}: {e}")

    with open("unique_senders.txt", "w") as f:
        for sender, count in sender_counts.most_common():
            f.write(f"{sender} - {count}\n")
    print(f"Unique senders extracted and saved to unique_senders.txt")

    return sender_counts
