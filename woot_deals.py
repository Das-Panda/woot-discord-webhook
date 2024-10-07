
import requests
import json
import os

# Add your Woot API key here
API_KEY = 'your-woot-api-key-here'

# Woot API URL
WOOT_API_URL = "https://developer.woot.com/feed/{feedname}"

# Add your Discord webhook URL here
DISCORD_WEBHOOK_URL = 'your-discord-webhook-url-here'

# Path to save the previous deals data
DEALS_FILE = 'previous_deals.json'

# Fetch the deals from a specific category
def fetch_woot_deals(feedname="All"):
    headers = {
        'x-api-key': API_KEY,
    }
    try:
        response = requests.get(WOOT_API_URL.format(feedname=feedname), headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch deals: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Woot deals: {e}")
        return None

# Send a message to Discord
def send_to_discord(content):
    data = {
        "content": content
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Message sent to Discord successfully.")
        else:
            print(f"Failed to send message to Discord: {response.status_code}")
    except Exception as e:
        print(f"Error sending message to Discord: {e}")

# Format deal data for Discord
def format_deal(deal):
    return f"**{deal['Title']}**\nPrice: ${deal['SalePrice']['Minimum']}\n[Link]({deal['Url']})\n"

# Save deals to file
def save_deals(deals):
    with open(DEALS_FILE, 'w') as f:
        json.dump(deals, f)

# Load deals from file
def load_previous_deals():
    if os.path.exists(DEALS_FILE):
        with open(DEALS_FILE, 'r') as f:
            return json.load(f)
    return None

# Compare deals to see if there are changes
def deals_changed(new_deals, old_deals):
    if old_deals is None:
        return True  # If there are no previous deals, consider it as changed
    
    old_ids = {deal['OfferId'] for deal in old_deals['Items']}
    new_ids = {deal['OfferId'] for deal in new_deals['Items']}

    return new_ids != old_ids

# Main function
def main():
    # Fetch new deals from the 'All' category
    new_deals = fetch_woot_deals(feedname="All")
    
    if new_deals and 'Items' in new_deals:
        # Load previous deals
        previous_deals = load_previous_deals()

        # Check if deals have changed
        if deals_changed(new_deals, previous_deals):
            print("Deals have changed. Sending notifications...")
            # Notify only if there are changes
            for deal in new_deals['Items']:
                if not deal['IsSoldOut']:
                    formatted_deal = format_deal(deal)
                    send_to_discord(formatted_deal)

            # Save the new deals as the latest
            save_deals(new_deals)
        else:
            print("No changes in deals.")
    else:
        print("No deals available or API failed.")

if __name__ == "__main__":
    main()
