# 🚀 Deployment Guide

This guide explains how to deploy the PDF Bot to various hosting platforms.

## Render.com (Free Tier) Deployment

### Prerequisites

1. **GitHub Repository**: Your code should be pushed to GitHub
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Telegram Bot Token**: Get from [@BotFather](https://t.me/botfather)

### Step-by-Step Deployment

#### 1. Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Choose your repository

#### 2. Configure Build Settings

```
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

#### 3. Environment Variables

Add these environment variables in Render:

```
BOT_TOKEN=your_telegram_bot_token_here
ADMIN_IDS=123456789,987654321
SUPPORT_USERNAME=YourSupportUsername
WEBHOOK_URL=https://your-app-name.onrender.com
WEBHOOK_PATH=/webhook
PORT=10000
USE_WEBHOOK=true
```

**Important**: Replace `your-app-name` with your actual Render app name.

#### 4. Advanced Settings

- **Instance Type**: Free
- **Region**: Choose closest to your users
- **Health Check Path**: `/` (root path)
- **Auto-Deploy**: Enable for automatic updates

#### 5. Deploy

Click **"Create Web Service"** and wait for deployment to complete.

#### 6. Update Webhook URL

After deployment, update the `WEBHOOK_URL` environment variable with your actual Render URL:
- Go to your Render service dashboard
- Copy the URL (e.g., `https://pdf-bot-xyz.onrender.com`)
- Update the `WEBHOOK_URL` environment variable
- Redeploy the service

### How It Works

- **Webhook Mode**: The bot uses webhooks instead of polling, which is perfect for serverless platforms
- **Health Check**: The `/` endpoint keeps the service alive on Render's free tier
- **Auto-Scaling**: Render automatically manages the service lifecycle

### Troubleshooting

#### Service Keeps Stopping

1. Check if `USE_WEBHOOK=true` is set
2. Verify `WEBHOOK_URL` is correct
3. Ensure the health check endpoint is responding

#### Webhook Not Working

1. Check Render logs for errors
2. Verify `BOT_TOKEN` is correct
3. Test the webhook URL manually: `https://your-app.onrender.com/webhook`

#### Bot Not Responding

1. Check Telegram BotFather for webhook info: `/setwebhook`
2. Remove webhook if needed: `/setwebhook` (without URL)
3. Check Render service status

### Local Development

For local development, set `USE_WEBHOOK=false` to use polling mode:

```bash
USE_WEBHOOK=false python main.py
```

### Cost Optimization

- **Free Tier**: 750 hours/month, auto-sleep after 15 minutes of inactivity
- **Usage**: Monitor your usage in Render dashboard
- **Scaling**: Upgrade to paid plans if needed

### Security Notes

- Never commit `.env` files to Git
- Use environment variables for all sensitive data
- Regularly rotate your bot token if compromised

## Other Hosting Options

### Railway

```bash
# Similar setup to Render
# Use the same environment variables
```

### Heroku

```bash
# Procfile: web: python main.py
# Use the same environment variables
```

### VPS (DigitalOcean, Linode, etc.)

```bash
# Use polling mode for dedicated servers
# Set USE_WEBHOOK=false
# Use systemd or screen to keep it running
```

## Support

If you encounter issues:
1. Check the logs in your hosting platform
2. Verify all environment variables are set correctly
3. Test locally first with `USE_WEBHOOK=false`
