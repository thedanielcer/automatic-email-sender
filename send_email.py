import os
import requests

def get_email_addresses(test=False):
    recipient_env_key = "TEST_RECIPIENT_EMAIL" if test else "RECIPIENT_EMAIL"
    cc_env_key = "TEST_CC_EMAIL" if test else "CC_EMAIL"

    recipient_email = os.getenv(recipient_env_key)
    cc_email = os.getenv(cc_env_key)

    if not recipient_email:
        raise ValueError(f"{recipient_env_key} is not set")

    if not cc_email:
        raise ValueError(f"{cc_env_key} is not set")

    return recipient_email, cc_email

def send_email(subject, body, access_token, base_url, test=False):
    recipient_email, cc_email = get_email_addresses(test)

    endpoint = "/me/sendMail"
    full_url = base_url + endpoint

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": recipient_email
                    }
                }
            ],
            "ccRecipients": [
                {
                    "emailAddress": {
                        "address": cc_email
                    }
                }
            ]
        }
    }

    response = requests.post(full_url, headers=headers, json=body)

    if response.status_code == 202:
        print("Email sent successfully")
    else:
        raise RuntimeError("Could not send automatic email")
