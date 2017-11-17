import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('55oQ//W4iTixbQHuP2zUOSAtNrZPEPhNTv2eNUZ8L+Plf2t8X5L9UDWmA0nTQV5hi6jHtEyYCHFhkPqk0KarDFsoin1HWOXBOcIzb30/1O6eYHHOG1y/EFe7TvIPZA1C6KXLXR1H8jQ7c1kLpwqNjwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0d6b9ac72dc370da661c4c6c34a59de4')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
