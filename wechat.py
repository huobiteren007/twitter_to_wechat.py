import tweepy
from wechaty import Wechaty, ScanStatus
from googletrans import Translator
import asyncio

# 您的 Twitter API 凭证
TWITTER_CONSUMER_KEY = 'vQXECxnh2rPUlbq6bEcC20ZFR'
TWITTER_CONSUMER_SECRET = 'ep4YuJkswjTauxT0gahOZFXaGCqaF2kCWrOYN1kpCeh9hJNuam'
TWITTER_ACCESS_TOKEN = '961155312177831937-iqEOV8sYhNTX7xrzPon5afAlMCuk719'
TWITTER_ACCESS_TOKEN_SECRET = 'HaqQfKWfLzhFJiU92Iz98L4id0I9yPj3nBQpD4Ke5GSRe'

# 初始化微信机器人
wechaty = Wechaty()

# 要监控的 Twitter 用户ID
twitter_user_ids = ['@_0xKenny', '@Nu_ethe', '@ouyoung11', '@_0xShark', '@SJ95E', '@hongshen6666', '@kevin_airdrop']

# 初始化 Twitter API
auth = tweepy.OAuth1(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# 初始化 Google Translate
translator = Translator()

# 检查 Twitter 并发送到微信的函数
def check_twitter_and_send_to_wechat():
    for user_id in twitter_user_ids:
        # 获取最新的推文
        tweets = twitter_api.user_timeline(user_id=user_id, count=1)
        latest_tweet = tweets[0].text if tweets else None
        
        if latest_tweet:
            print(f'用户 {user_id} 的最新推文：{latest_tweet}')
            
            # 将推文内容翻译成中文
            translated_tweet = translator.translate(latest_tweet, dest='zh-cn').text
            
            print(f'翻译后的推文：{translated_tweet}')
            
            # 将翻译后的推文内容发送到微信
            wechaty.say(f'用户 {user_id} 的最新推文：\n{translated_tweet}')

# 当收到微信消息时的处理函数
@wechaty.on_message()
async def on_message(message):
    if message.type() == Wechaty.Message.Type.Text:
        text = message.text()
        print('从微信收到消息：', text)
        
        # 如果消息来自微信，将其发布到 Twitter
        # (您需要实现此部分，因为此处省略了发布到 Twitter 的代码)

# 当扫描 QR 码时的处理函数
@wechaty.on_scan()
async def on_scan(qrcode: str, status: ScanStatus):
    print("扫描 QR 码进行登录: {}".format(status))
    print("QR 码: {}".format(qrcode))

# 启动微信机器人的主函数
async def main():
    await wechaty.start()

async def check_twitter_periodically():
    while True:
        check_twitter_and_send_to_wechat()
        await asyncio.sleep(60)  # 在再次检查 Twitter 之前等待 60 秒

if __name__ == '__main__':
    # 在事件循环中启动微信机器人
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_until_complete(check_twitter_periodically())

