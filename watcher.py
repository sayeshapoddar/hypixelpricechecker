import os
import time
import requests
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()

API_KEY = os.getenv("HYPIXEL_API_KEY")
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

TARGET_PRICE = int(os.getenv("TARGET_PRICE", "40000"))      # coins
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "5"))      # seconds


def get_soulflow_price() -> float:
    """
    Fetches the current SOULFLOW sell price from the Hypixel SkyBlock Bazaar API.
    """
    if not API_KEY:
        raise RuntimeError("HYPIXEL_API_KEY is not set. See README for setup.")

    resp = requests.get(
        "https://api.hypixel.net/skyblock/bazaar",
        params={"key": API_KEY},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()

    if not data.get("success", False):
        raise RuntimeError(f"Hypixel API returned an error: {data}")

    try:
        return data["products"]["SOULFLOW"]["quick_status"]["sellPrice"]
    except KeyError as exc:
        raise RuntimeError("SOULFLOW price not found in API response.") from exc


def send_discord_alert(price: float) -> None:
    """
    Sends an alert to a Discord channel via webhook.
    """
    if not DISCORD_WEBHOOK:
        print(f"[ALERT] SOULFLOW just hit {price:.0f} coins! (no webhook set)")
        return

    payload = {"content": f":bell: SOULFLOW just hit **{price:.0f}** coins!"}
    try:
        resp = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        resp.raise_for_status()
        print("Discord alert sent.")
    except Exception as e:
        print("Failed to send Discord alert:", e)


def main() -> None:
    """
    Continuously watches the SOULFLOW price and alerts when it crosses the target.
    """
    if not API_KEY:
        print("Error: HYPIXEL_API_KEY is not set. Set it in your environment or .env file.")
        return

    print("Watching SOULFLOW price...")
    print(f"Target price: {TARGET_PRICE} coins")
    print(f"Check interval: {CHECK_INTERVAL} seconds\n")

    alerted = False

    while True:
        try:
            price = get_soulflow_price()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{now}] Current sell price: {price:.2f}")

            if price >= TARGET_PRICE and not alerted:
                print("Threshold reached!")
                send_discord_alert(price)
                alerted = True
            elif price < TARGET_PRICE:
                alerted = False

        except Exception as e:
            print("Error fetching price:", e)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
