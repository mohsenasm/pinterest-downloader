# Pinterest Downloader Bot

This bot intregrates [pinterest-downloader](limkokhole/pinterest-downloader) into Telegram messager. Users can share the pin url with this bot to download the content.


## Fair Use Information

Please respect the rights of the image right holders that you download. Also read Pinterest's [Terms of Service](https://policy.pinterest.com/en/terms-of-service), especially the [copy-right part](https://policy.pinterest.com/en/copyright).

The creator of this script takes no responsibility for misuse by any user.

## Deployment

1. Create a file named `secret.env` with the following env:

```env
BOT_ADMIN_ID="your_telegram_chat_id"
WEBHOOK_BASE_URL="https://the_url"
BOT_SECRET="..."
LOG_VIEWER_USERNAME="..."
LOG_VIEWER_PASSWORD="..."
```

2. Create `docker-compose.yml` like the provided `docker-compose.example.yml`.

3. `docker-compose up --build -d`