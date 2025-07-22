import os
from dotenv import load_dotenv
load_dotenv()

WECHAT_APPID = os.getenv("WECHAT_APPID")
WECHAT_SECRET = os.getenv("WECHAT_SECRET")
WECHAT_TOKEN = os.getenv("WECHAT_TOKEN")

# 公众号消息推送URL: http://<你的服务器>/wechat/callback
