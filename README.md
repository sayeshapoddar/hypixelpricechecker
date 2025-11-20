# Soulflow Price Watcher

A small Python script that watches the SOULFLOW sell price on the Hypixel SkyBlock Bazaar and notifies you (optionally via Discord webhook) when it crosses a target price. 

Features

- Polls the Hypixel SkyBlock Bazaar API on a fixed interval
- Prints live SOULFLOW sell prices to the console
- Sends a Discord webhook alert when the price hits or exceeds your target
- Target price and polling interval configurable via environment variables

Requirements

- Python 3.8+
- A Hypixel API key
- (Optional) A Discord webhook URL

Install dependencies:

```bash
pip install -r requirements.txt
