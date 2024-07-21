import telebot
from datetime import datetime, timedelta
import re
from get_calendar import add_calendar_event, get_calendar_events, get_calendar_events_tomorrow
from ai_reply import ai_reply
from get_weather import get_weather
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Init telebot
TOKEN = "6932276342:AAHxx6fRfeUbro6CePLsJMrH0cTs61yqlFQ"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# Global variables to share between functions
NewEventCache = {
    "name": None,
    "start_date": None,
    "location": None,
    "description": None
}

EndSentenceStr = "喵"
player_choose = "cute"

# Util function to clean multi-line strings for /start and /help descriptions
def strip_str(str):
    s = str.strip()
    s = "\n".join([line.strip() for line in s.split("\n")])
    return s

@bot.message_handler(commands=["help"])
def handle_helpsend_help(message):
    help_msg = """
    嗨！你可以跟AI醬ヽ(=^・ω・^=)丿這樣互動喔～ 
    /help : 顯示所有指令、使用說明
    /createSchedule : 排程行程
    /displayToday : 顯示今日所有行程
    /displayTomorrow : 顯示明日所有行程
    /displayWeek : 顯示一週行程
    /displayMonth : 顯示一個月內所有 upcoming 行程
    /settings : Chatbot 設定
    /mode：選擇秘書類型
    """.format(custom_ending=EndSentenceStr)
    bot.reply_to(message, strip_str(help_msg))

@bot.message_handler(commands=["start"])
def handle_start(message):
    global EndSentenceStr

    introduction = """
    嗨！我是你的智能小助手AI醬❤️，很高興能為您服務
    我可以幫助您管理行程、提醒您重要事項、查詢天氣等等
    我的指令如下
    
    /help : 顯示所有指令、使用說明
    /createSchedule : 排程行程
    /displayToday : 顯示今日所有行程
    /displayTomorrow : 顯示明日所有行程
    /displayWeek : 顯示一週行程
    /displayMonth : 顯示一個月內所有 ongoing 行程
    /settings : 句尾設定
    /mode：選擇秘書類型
    
    如果忘記怎麼使用，也可以隨時打 `/help` 詢問喔～

    另外，主人在我為您生成客製化的內容時，也可以決定我的句尾要使用什麼喔～
    目前的預設是"{custom_ending}"，但主人也可以透過 `/settings` 指令來更改喔～
    而且，主人也可以選擇我是哪種類型的秘書，有細心可愛型、高冷型、傲嬌型可以選擇喔～
    預設是細心可愛型，但主人也可以透過 `/mode` 指令來更改喔～

    那麼，期待能夠為主人服務(,,・ω・,,)
    """.format(custom_ending=EndSentenceStr)
    bot.reply_to(message, strip_str(introduction))    

# 以下五個函數都是屬於 Create Schedule 的相關函式，會從一～五依序執行，一步一步要到相關資訊
@bot.message_handler(commands=["createSchedule"])
def add_calendar_schedule(event):
    global NewEventCache
    NewEventCache = {
        "name": None,
        "start_date": None,
        "location": None,
        "description": None
    }
    new_msg = bot.reply_to(event, "收到d(`･∀･)b AI醬即將為主人加入新行程")
    ask_schedule_msg = bot.reply_to(new_msg, "主人的行程是～?  :")
    bot.register_next_step_handler(ask_schedule_msg, add_event_reg_name)

def add_event_reg_name(message):
    global NewEventCache
    NewEventCache["name"] = message.text
    ask_date_msg = bot.send_message(message.chat.id, "主人，請問行程開始時間是？請用 MM/DD 的格式輸入喔～")
    bot.register_next_step_handler(ask_date_msg, add_event_reg_start_date)    

def add_event_reg_start_date(message):
    pattern = r'^\d{2}/\d{2}$' # regex
    if re.match(pattern, message.text):
        try:
            ask_loc_msg = bot.reply_to(message, "主人，行程地點是~？(目前僅開放臺北、臺中、高雄、臺東)：")
            parsed_date = datetime.strptime(message.text, '%m/%d')
            NewEventCache["start_date"] = parsed_date
            bot.register_next_step_handler(ask_loc_msg, add_event_reg_loc)
        except ValueError as e:
            date_parse_err_msg = bot.reply_to(message, "主人，我看不太懂您打的日期 >...< 您可以再次確認輸入的日期格式沒錯嗎？")
            bot.register_next_step_handler(date_parse_err_msg, add_event_reg_start_date)    
    else:
        wrong_format_err = bot.reply_to(message, "主人，您的日期格式好像不太對 >...< 請用 MM/DD 的格式輸入喔～")
        bot.register_next_step_handler(wrong_format_err, add_event_reg_start_date)    

def add_event_reg_loc(message):
    global NewEventCache
    NewEventCache["location"] = message.text
    ask_desc_msg = bot.reply_to(message, "主人，請問最後有什麼想在行程上備註的事情嗎？~？")
    bot.register_next_step_handler(ask_desc_msg, add_event_reg_desc)

def add_event_reg_desc(message):
    global NewEventCache
    NewEventCache["description"] = message.text
    try:
        url = add_calendar_event(NewEventCache)
        bot.reply_to(message, f"主人，戳戳這個 URL {url}\n，就可以把您的行程加入囉！")
    except Exception as e:
        bot.reply_to(message, "主人，我好像遇到一點問題 >...< 請再打一次 /createSchedule")


# 因為顯示今天、一週、一月的邏輯都相同，所以可以獨立成一個Function來讓程式碼更簡潔
def get_ai_summarized_events(message, days):
    pre_msg = bot.reply_to(message, "主人，我正在為您整理行事曆內容，會花一點時間，請稍等AI醬一下喔～")
    calendar_events = get_calendar_events(days)
    ai_response = ai_reply(f"把這段從今天開始數{days}的行事曆內容與各地天氣狀況整理成一個通順的敘述", calendar_events, get_weather(), EndSentenceStr, player_choose) #TODO: Revise Prompt
    text_string = ''.join(str(x) for x in ai_response)
    text = text_string.replace("TextBlock(text='", "").replace("', type='text')", "").replace("\\n", "\n")
    bot.reply_to(pre_msg, text)

@bot.message_handler(commands=["displayToday"])
def send_today_schedule(message):
    get_ai_summarized_events(message, 1)
    
@bot.message_handler(commands=["displayWeek"])
def send_weekly_schedule(message):
    get_ai_summarized_events(message, 7)

@bot.message_handler(commands=["displayMonth"])
def send_monthly_schedule(message):
    get_ai_summarized_events(message, 30)

# 因為這邊get_calendar_events需要特別只取明天的行程，所以要特別處理
@bot.message_handler(commands=["displayTomorrow"])
def handle_display_tmr(message):
    pre_msg = bot.reply_to(message, "主人，我正在為您整理行事曆內容，可能會花一點時間，請稍等AI醬一下喔～")
    calendar_events = get_calendar_events_tomorrow()
    ai_response = ai_reply(f"請把這段明天的行事曆內容整理成一個通順的敘述", calendar_events, get_weather(), EndSentenceStr, player_choose) #TODO: Revise Prompt ai_reply(input_prompt, data_dict, location_weather, end_sentence_str, player_choose):
    text_string = ''.join(str(x) for x in ai_response)
    text = text_string.replace("TextBlock(text='", "").replace("', type='text')", "").replace("\\n", "\n")
    bot.reply_to(pre_msg, text)
    
# 以下兩個函數都是屬於 settings 的相關函式，會從一～二依序執行，一步一步要到相關資訊
@bot.message_handler(commands=["settings"])
def handle_settings(message):
    ask_end_msg = bot.reply_to(message, "主人，請輸入您希望我在句尾加入什麼內容～（一定要設定呦～）")
    bot.register_next_step_handler(ask_end_msg, settings_custom_ending)

def settings_custom_ending(message):
    global EndSentenceStr
    EndSentenceStr = message.text
    bot.reply_to(message, f"沒問題！我以後回覆主人時，會在句尾加上「{EndSentenceStr}」喔～")



#buttom
@bot.message_handler(commands=['mode'])
def message_hander(message):
    bot.send_message(message.chat.id, "主人請選擇類型", reply_markup=gen_markup())

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton('細心可愛型', callback_data="cute"),
                InlineKeyboardButton('高冷型', callback_data="cold"),
                InlineKeyboardButton('傲嬌型', callback_data="tsundere"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global player_choose
    player_choose = call.data
    player_choose_str = ""
    if call.data == "cute":
        player_choose_str = "細心可愛型"
    elif call.data == "cold":
        player_choose_str = "高冷型"
    elif call.data == "tsundere":
        player_choose_str = "傲嬌型"
        
    bot.send_message(call.message.chat.id, f"主人您選擇的是: {player_choose_str}")



if __name__ == '__main__':
    bot.infinity_polling()
   
    
 
#Archived code

# @bot.message_handler(commands=["weather"])
# def get_weather(message):
#     station_id = "466920"
#     data_json = get_weather(station_id)
#     weather_info = get_weather(data_json)
#     bot.send_message(message.chat.id, f"還是主人細心呢~❤️，我最親愛的主人，這是現在的天氣呦{weather_info}")
