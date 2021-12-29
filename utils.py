import os

from linebot import LineBotApi, WebhookParser
from linebot.models import *


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_main_menu_message(reply_token):
    line_bot_api = LineBotApi(channel_access_token)
    Carousel_template = TemplateSendMessage(
        alt_text='Carousel template',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1585738917085.jpg',
                    title='增刪備忘錄功能',
                    text='不管是代辦事項、幹話或遺言...都能放喔!當然也可以刪',
                    actions=[
                        MessageTemplateAction(
                            label='增加項目指令',
                            text='解說: 增加項目，可一次添加多項，\nex: 增 吃飯, 增 吃飯 睡覺'
                        ),
                        MessageTemplateAction(
                            label='刪除項目指令',
                            text='解說: 刪除對應編號的項目，\n可一次刪除多項或全部，\nex: 刪 1, 刪 1 2, 刪 *'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/dmVCLQx.jpg',
                    title='改查備忘錄功能',
                    text='改動及查詢備忘錄說明',
                    actions=[
                        MessageTemplateAction(
                            label='更新項目指令',
                            text='解說: 更新一個指定項目，\nex: 改 吃飯 睡覺'
                        ),
                        MessageTemplateAction(
                            label='查詢項目指令',
                            text='解說: 列出所有項目，\nex: 查'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/AZPqkrE.jpeg',
                    title='查看日出落時間功能',
                    text='某天作者coding到日出所想到的功能',
                    actions=[
                        MessageTemplateAction(
                            label='今明兩天的日出時間',
                            text='日出'
                        ),
                        MessageTemplateAction(
                            label='今明兩天的日落時間',
                            text='日落'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://i.imgur.com/V3Etxtb.jpg',
                    title='我是哪這是誰?',
                    text='程式碼甚麼的能動就好',
                    actions=[
                        MessageTemplateAction(
                            label='查看FSM',
                            text='FSM'
                        ),
                        MessageTemplateAction(
                            label='LINE說不塞這欄就吃error',
                            text='還說不能傳空訊息'
                        )
                    ]
                ),
            ]
        )
    )
    line_bot_api.reply_message(reply_token, Carousel_template)



def send_image_url(reply_token, img_url):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, 
                               ImageSendMessage(original_content_url=img_url,preview_image_url=img_url))

"""
def send_button_message(id, text, buttons):
    pass
"""
