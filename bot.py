import tweepy
from wechaty import Wechaty, ScanStatus, Message
from googletrans import Translator
import asyncio

# 您的 Twitter API 凭证
TWITTER_CONSUMER_KEY = 'vQXECxnh2rPUlbq6bEcC20ZFR'
TWITTER_CONSUMER_SECRET = 'ep4YuJkswjTauxT0gahOZFXaGCqaF2kCWrOYN1kpCeh9hJNuam'
TWITTER_ACCESS_TOKEN = '961155312177831937-iqEOV8sYhNTX7xrzPon5afAlMCuk719'
TWITTER_ACCESS_TOKEN_SECRET = 'HaqQfKWfLzhFJiU92Iz98L4id0I9yPj3nBQpD4Ke5GSRe'

# 要监控的 Twitter 用户ID
twitter_user_ids = ['@_0xKenny', '@Nu_ethe', '@ouyoung11', '@_0xShark', '@SJ95E', '@hongshen6666', '@kevin_airdrop']

# 初始化 Twitter API
auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# 初始化 Google Translate
translator = Translator()

# 创建微信机器人实例
wechaty = Wechaty()

# 当扫描 QR 码时的处理函数
@wechaty.on_scan()
async def on_scan(qrcode: str, status: ScanStatus):
    print("扫描 QR 码进行登录: {}".format(status))
    print("QR 码: {}".format(qrcode))

# 当收到微信消息时的处理函数
@wechaty.on_message()
async def on_message(message: Message):
    if message.type() == Message.Type.Text:
        text = message.text()
        print('从微信收到消息：', text)

# 检查 Twitter 并发送到微信的函数
async def check_twitter_and_send_to_wechat():
    for user_id in twitter_user_ids:
        # 获取最新的推文
        tweets = twitter_api.user_timeline(screen_name=user_id, count=1)
        latest_tweet = tweets[0].text if tweets else None
        
        if latest_tweet:
            print(f'用户 {user_id} 的最新推文：{latest_tweet}')
            
            # 将推文内容翻译成中文
            translated_tweet = translator.translate(latest_tweet, dest='zh-cn').text
            
            print(f'翻译后的推文：{translated_tweet}')
            
            # 将翻译后的推文内容发送到微信
            await wechaty.say(f'用户 {user_id} 的最新推文：\n{translated_tweet}')

# 主函数
async def main():
    await wechaty.start()

    # 检查 Twitter 并发送到微信
    while True:
        await check_twitter_and_send_to_wechat()
        await asyncio.sleep(60)  # 每隔 60 秒检查一次 Twitter

if __name__ == '__main__':
    asyncio.run(main())

