# Automatic Email Sender

Small Python utility that sends a weekly parking request email through Microsoft
Graph.

The program calculates the next Monday through Thursday, removes any global
Mexico public holidays returned by the Nager.Date API, formats a Spanish email
with those parking dates and vehicle details, then sends it from the signed-in
Microsoft account.

## Requirements

- Python 3.12 or newer
- [uv](https://docs.astral.sh/uv/)
- A Microsoft app registration for a personal Microsoft account
- Microsoft Graph permissions for:
  - `User.Read`
  - `Mail.ReadWrite`
  - `Mail.Send`

## Setup

Install/sync the project dependencies with uv:

```bash
uv sync
```

Create a `.env` file in the project root:

```env
CLIENT_ID=your_microsoft_app_client_id
CLIENT_SECRET=your_microsoft_app_client_secret
RECIPIENT_EMAIL=production_recipient@example.com
CC_EMAIL=production_cc@example.com
TEST_RECIPIENT_EMAIL=daniel.gonzalez.5@hotmail.com
TEST_CC_EMAIL=mar_cervantesg@yahoo.com
VEHICLE_MODEL=your_vehicle_model
VEHICLE_COLOR=your_vehicle_color
VEHICLE_PLATES=your_vehicle_plates
```

The first successful run will add a `refresh_token` entry to `.env` so later
runs can request new access tokens without going through the browser flow again.

## Run

Run the email sender with uv:

```bash
uv run main.py
```

To send the same email to the test recipient and CC addresses instead, use:

```bash
uv run main.py --test
```

On the first run, the program prints a Microsoft authorization URL. Open that
URL in a browser, sign in, approve the requested permissions, and copy the full
redirected URL back into the terminal when prompted:

```text
Full URL:
```

If the email is accepted by Microsoft Graph, the program prints:

```text
Email sent successfully
```

## Scheduled Job

`run_email_job.sh` is a convenience wrapper intended for cron or another
scheduler. It:

- changes into this project directory
- runs `uv run main.py`
- appends output to `log.txt`
- sends a success or failure notification to the configured ntfy topic

Run it manually with:

```bash
./run_email_job.sh
```

If you move the project or install `uv` somewhere else, update `BASE_DIR` and
`UV_BIN` inside `run_email_job.sh`.

## Project Structure

- `main.py` loads environment variables, gets an access token, builds the email,
  and sends it.
- `get_access_token.py` handles Microsoft authentication and stores refresh
  tokens in `.env`.
- `get_email_body.py` calculates parking dates and formats the subject/body.
- `send_email.py` sends the message through Microsoft Graph.
- `run_email_job.sh` runs the job and writes logs/notifications.

## Notes

- `.env` and `log.txt` are intentionally ignored by git.
- The ntfy topic is currently hard-coded in `run_email_job.sh`.
- The redirect URI used for Microsoft login is `http://localhost:8000`; make
  sure the app registration allows that redirect URI.
