import anthropic

def ai_reply(input_prompt, data_dict, location_weather, end_sentence_str, player_choose):
    client = anthropic.Anthropic(
        api_key = "YOUR_API_KEY"
    )

    sentece_prompt = ""
    if player_choose == "cute":
        sentece_prompt = f"你是一位很講話可愛的秘書，使用繁體中文，常常會可以呀、好ㄉ、等語助詞來回覆，如果天氣熱就可以說多喝水等關心的語氣，冷就說多穿外套，注意保暖的關心語句，並在出門前，提醒我出門記得注意安全喔！針對行事曆的標題與敘述，額外給出符合人物設定的提醒與對話，並在對話的結尾詢問「那還有要我幫忙嘛」，在每一句話的最後，經常加上{end_sentence_str}作為句末的額外語助詞"
    elif player_choose == "cold":
        sentece_prompt = f"你是一位很高冷類型的秘書，使用繁體中文，常常用無關緊要的口氣，講出最狠的話，如果天氣熱就會說「滾去喝水」、「不准中暑」之類的語句，冷就會說「不會穿外套嗎」、「感冒的話饒不了你」，出門前會說「不准太晚回來」，語句盡可能簡短、冰冷！針對行事曆的標題與敘述，額外給出符合人物設定的提醒與對話，在每一句的最後，經常加上{end_sentence_str}作為句末的額外語助詞"
    elif player_choose == "tsundere":
        sentece_prompt = f"你是一位傲嬌型類型的秘書，使用繁體中文，常常口是心非，會使用一些凶狠的話，但是實際上卻十分關心我，舉例來說，如果今天天氣熱，會說「哼最好不要喝水，渴死你」或是「你就繼續曬太陽沒關係，我...我才不會關心你呢」等話語，如果天氣冷，會說「這件外套只是借給你，我才不會心疼你」等話語，並在出門前，「趕快出去！你...幾點回來，才不是關心你！」等語句，並在對話的結尾詢問「有問題不要找我，我才不會在乎你呢」，針對行事曆的標題與敘述，額外給出符合人物設定的提醒與對話，在每一句的最後，會加上{end_sentence_str}作為句末的額外語助詞"
    else :
        print("default")
        sentece_prompt = f"你是一位很講話可愛的秘書，使用繁體中文，常常會可以呀、好ㄉ、等語助詞來回覆，如果天氣熱就可以說多喝水等關心的語氣，冷就說多穿外套，注意保暖的關心語句，並在出門前，提醒我出門記得注意安全喔！針對行事曆的標題與敘述，額外給出符合人物設定的提醒與對話，並在對話的結尾詢問「那還有要我幫忙嘛」，在每一句話的最後，經常加上{end_sentence_str}作為句末的額外語助詞"

    event_prompt = ""
    location_weather_prompt = ""
    print(data_dict)
    for i in range(len(data_dict)):
        event_prompt = event_prompt + f"事件名稱：{data_dict[i]['summary']}，開始時間：{data_dict[i]['date']} {data_dict[i]['time']}，地點：{data_dict[i]['location']}，描述：{data_dict[i]['description']}。"
    for i in range(len(location_weather)):
        location_weather_prompt = location_weather_prompt + f"地點：{location_weather[i]['Station']}，天氣：{location_weather[i]['Weather']}，溫度：{location_weather[i]['Temperature']}。"                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                  
        
    input_prompt = f"{input_prompt}以下是今天行程：{event_prompt}以下是今天各地天氣：{location_weather_prompt}。僅輸出對應行程地點的天氣資訊，並將天氣資訊輸出在各個行程資訊之後。"

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        temperature=0,
        system=sentece_prompt,
        messages=[ 
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": input_prompt
                    }
                ]
            }
        ]
    )

    return message.content

'''
end_sentence_str = "喵"
input_prompt = "你好，請告訴我今天天氣如何？"
data_dict = [
    {
        "summary": "test",
        "date": "0701",
        "end_date": "0701",
        "time": "1000",
        "end_time": "1200",
        "location": "Taipei",
        "description": "test"
    },
    {
        "summary": "test2",
        "date": "0701",
        "end_date": "0701",
        "time": "1300",
        "end_time": "1500",
        "location": "Taipei",
        "description": "test2"
    },
    {
        "summary": "test3",
        "date": "0701",
        "end_date": "0701",
        "time": "1600",
        "end_time": "1800",
        "location": "Taipei",
        "description": "test3"
    }
]

location_weather = [
    {
        "Station": "Taipei",
        "Weather": "sunny",
        "Temperature": "30",
    },
    {
        "Station": "Taichung",
        "Weather": "sunny",
        "Temperature": "25"
    },
    {
        "Station": "Taipei",
        "Weather": "sunny",
        "Temperature": "27"
    }
]


text = ai_reply(input_prompt, data_dict, location_weather, end_sentence_str)
print(text)
'''





















