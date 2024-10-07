
# Woot Deals Notifier

This Python script fetches live deals from Woot using their API and sends deal updates to a Discord webhook if there are any changes. The script can be set up to run at regular intervals using `cron` or other job scheduling tools.

## Prerequisites

- Python 3.x
- `requests` module (Install it via `pip install requests`)

## Setup

1. Clone the repository or download the Python script.
2. Install the required dependencies:

   ```bash
   pip install requests
   ```

3. Add your Woot API key and Discord webhook URL to the script.

## Usage

### Adding API Key and Webhook

In the Python script (`woot_deals.py`), replace the placeholders for the API key and webhook URL:

```python
API_KEY = 'your-woot-api-key-here'
DISCORD_WEBHOOK_URL = 'your-discord-webhook-url-here'
```

### Running the Script

You can run the script manually by executing:

```bash
python3 woot_deals.py
```

Alternatively, make the script executable and run it directly:

```bash
chmod +x woot_deals.py
./woot_deals.py
```

### Automating with Cron

To run the script automatically at regular intervals, add a cron job:

1. Open the crontab editor:

   ```bash
   crontab -e
   ```

2. Add a line to schedule the script. For example, to run the script every 30 minutes:

   ```bash
   */30 * * * * /usr/bin/python3 /path/to/woot_deals.py
   ```

3. Save and exit. The script will now run automatically based on the schedule.

## Customization

- You can modify the `fetch_woot_deals()` function to fetch deals from specific categories by changing the `feedname` parameter (e.g., `Computers`, `Tools`, `Electronics`, etc.).
- The script is set to only send notifications when there are changes in the available deals.

## License

This project is licensed under the MIT License.
