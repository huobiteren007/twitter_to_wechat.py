import tweepy
import asyncio
from googletrans import Translator
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode

# Your Twitter API credentials
TWITTER_CONSUMER_KEY = 'vQXECxnh2rPUlbq6bEcC20ZFR'
TWITTER_CONSUMER_SECRET = 'ep4YuJkswjTauxT0gahOZFXaGCqaF2kCWrOYN1kpCeh9hJNuam'
TWITTER_ACCESS_TOKEN = '961155312177831937-iqEOV8sYhNTX7xrzPon5afAlMCuk719'
TWITTER_ACCESS_TOKEN_SECRET = 'HaqQfKWfLzhFJiU92Iz98L4id0I9yPj3nBQpD4Ke5GSRe'

# Your Telegram API token
TELEGRAM_API_TOKEN = '6701897229:AAEhXuCZj39J__f9vthuKdFIuCXq_0sUtU0'

# Telegram chat ID where you want to send the messages
TELEGRAM_CHAT_ID = 'ChatBot'

# Twitter user IDs to monitor
twitter_user_ids = ['@_0xKenny', '@Nu_ethe', '@ouyoung11', '@_0xShark', '@SJ95E', '@hongshen6666', '@kevin_airdrop']

# Initialize Twitter API
auth = tweepy.OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Initialize Google Translate
translator = Translator()

# Initialize Telegram bot and dispatcher
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


# Function to check Twitter and send to Telegram
async def check_twitter_and_send_to_telegram():
    for user_id in twitter_user_ids:
        # Get the latest tweet
        tweets = twitter_api.user_timeline(screen_name=user_id, count=1)
        latest_tweet = tweets[0].text if tweets else None
        
        if latest_tweet:
            print(f'Latest tweet from user {user_id}: {latest_tweet}')
            
            # Translate the tweet content to Chinese
            translated_tweet = translator.translate(latest_tweet, dest='zh-cn').text
            
            print(f'Translated tweet: {translated_tweet}')
            
            # Send the translated tweet content to Telegram
            await bot.send_message(TELEGRAM_CHAT_ID, f'Latest tweet from user {user_id}:\n{translated_tweet}', parse_mode=ParseMode.HTML)


# Main function
async def main():
    # Start the Telegram bot
    await bot.delete_webhook()
    await dp.start_polling()


# Periodically check Twitter and send to Telegram
async def check_twitter_periodically():
    while True:
        await check_twitter_and_send_to_telegram()
        await asyncio.sleep(60)  # Wait 60 seconds before checking Twitter again


if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(check_twitter_periodically())


