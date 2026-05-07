import argparse
import sys
import os
from dotenv import load_dotenv
from get_access_token import get_access_token
from send_email import send_email
from get_email_body import get_email_body

MS_GRAPH_BASE_URL = "https://graph.microsoft.com/v1.0"
ENV_PATH = ".env"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test",
        action="store_true",
        help="send the email to the test recipient and cc addresses"
    )
    return parser.parse_args()

def main():
    args = parse_args()
    load_dotenv(ENV_PATH)
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    SCOPES = ["User.Read", "Mail.ReadWrite", "Mail.Send"]

    try:
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET, SCOPES)
        body, subject = get_email_body()

        send_email(subject, body, access_token, MS_GRAPH_BASE_URL, test=args.test)

        sys.exit(0)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
