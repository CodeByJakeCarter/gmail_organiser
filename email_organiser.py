from auth import authenticate_user
from extract_senders import extract_unique_senders


service = authenticate_user()
# Extract unique senders
extract_unique_senders(service)

print("Unique senders extracted successfully.")