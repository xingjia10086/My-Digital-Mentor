import os
import json
import lark_oapi as lark
from lark_oapi.api.im.v1 import *
from dotenv import load_dotenv

load_dotenv()

FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

lark_client = lark.Client.builder().app_id(FEISHU_APP_ID).app_secret(FEISHU_APP_SECRET).build()

def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    message = data.event.message
    if message.message_type != "text":
        return
        
    sender_id = data.event.sender.sender_id.open_id
    print(f"\n[获取到用户的 Open ID]: {sender_id}")
    
    reply_text = f"这是您的专属推送 ID：\n\n**{sender_id}**\n\n请将这串代码发给星佳的数字后台，以激活您的灵感日历推送功能。"
    
    try:
        req = ReplyMessageRequest.builder() \
            .message_id(message.message_id) \
            .request_body(ReplyMessageRequestBody.builder()
                .content(json.dumps({"text": reply_text}))
                .msg_type("text")
                .build()) \
            .build()
        lark_client.im.v1.message.reply(req)
        print("已回复 ID 给用户。")
    except Exception as e:
        print(f"❌ 飞书接口请求出错: {e}")

if __name__ == "__main__":
    event_handler = lark.EventDispatcherHandler.builder("", "") \
        .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
        .build()
        
    ws_client = lark.ws.Client(
        FEISHU_APP_ID, 
        FEISHU_APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.WARNING 
    )
    
    print("\n[ID 获取助手] 正在运行中...")
    print("请在飞书给机器人发任意一句话，机器人会自动回复您的 ID。")
    ws_client.start()
