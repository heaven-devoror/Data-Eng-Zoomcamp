from prefect.blocks.notifications import SlackWebhook

slack_webhook_block = SlackWebhook.load("slack-notification")
slack_webhook_block.notify("Hello from Prefect!")
