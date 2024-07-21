import datetime
import requests
import jicson

url = "your ics url"

def __get_calendar_json() -> dict:
    r = requests.get(url)
    result = jicson.fromText(r.text)
    return result

def get_calendar_events(days) -> list:
    # Get the events from Calendar 
    # input: int days - 想要查看的天數 
    # output: 顯示在 Calendar 上 days 天的事件、時間、地點
    
    result = __get_calendar_json()

    # 計算從今天開始到 days 天後的事件
    # 創建一個 list 來存放事件，其中有數個 dict 包含各個事件的資訊
    schedule = []
    events = result["VCALENDAR"][0]["VEVENT"]

    end_date = datetime.datetime.now().date() + datetime.timedelta(days-1)

    for event in events:
        event_start_datetime = None

        if "DTSTART" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART"], "%Y%m%dT%H%M%SZ")
            except ValueError:
                pass
        elif "DTSTART;VALUE=DATE" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART;VALUE=DATE"], "%Y%m%d")
            except ValueError:
                pass

        if event_start_datetime is None:
            continue

        if datetime.datetime.now().date() <= event_start_datetime.date() <= end_date:
            event_details = {
                "summary": event.get("SUMMARY", "No summary"),
                "date": event_start_datetime.date(),
                "time": event_start_datetime.time() if "DTSTART" in event else "All day",
                "description": event.get("DESCRIPTION", "No description"),
                "location": event.get("LOCATION", "No location")
            }
            schedule.append(event_details)

  
    return schedule

def add_calendar_event(event) -> str:
    """
    Add an event to Calendar
    input: dict event - 想要新增的事件
    input 格式: {
        "name": str,
        "start_date": datetime,
        "location": str,
        "description": str
    }
    """
    #event_date_str = event["start_date"].strftime('%Y%m%dT%H%M%S')
    event_date_str = event["start_date"].strftime('2024%m%d')

    base_url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
    event_data = {
        "text": event["name"],
        "details": event["description"],
        "dates": event_date_str + "/" + event_date_str + "&allDay=true",
        "ctz": "Asia/Taipei",
        "location": event["location"]
    }

    print(event_data)

    final_url = "&".join([base_url] + [f"{key}={value}" for key, value in event_data.items()])  
    print(final_url)          
    return final_url

def get_calendar_events_tomorrow() -> list:
    # Get the events from Calendar for tomorrow
    # input: None
    # output: 顯示在 Calendar 上明天的事件、時間、地點
    
    result = __get_calendar_json()

    schedule = []
    events = result["VCALENDAR"][0]["VEVENT"]

    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    for event in events:
        event_start_datetime = None

        if "DTSTART" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART"], "%Y%m%dT%H%M%SZ")
            except ValueError:
                pass
        elif "DTSTART;VALUE=DATE" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART;VALUE=DATE"], "%Y%m%d")
            except ValueError:
                pass

        if event_start_datetime is None:
            continue

        if event_start_datetime.date() == tomorrow:
            event_details = {
                "summary": event.get("SUMMARY", "No summary"),
                "date": event_start_datetime.date(),
                "time": event_start_datetime.time() if "DTSTART" in event else "All day",
                "description": event.get("DESCRIPTION", "No description"),
                "location": event.get("LOCATION", "No location")
            }
            schedule.append(event_details)

    return schedule

"""
Archived code

def add_calendar_event(event) -> str:
     
    if event["end_date"] == "":
        event["end_date"] = event["start_date"]

    if event["start_time"] == "":
        event["start_time"] = datetime.datetime.now().strftime("%H%M") + "00"
        event["end_time"] = datetime.datetime.now().strftime("%H%M") + "00"

    # example data:
    # event = {"event_name": "test",  (must have)
    #     "start_date": "0701",  (must have)
    #     "end_date": "0701",
    #     "start_time": "1000",  
    #     "end_time": "1200",
    #     "location": "Taipei", (must have)
    #     "description": "test"} 
    # output: 顯示新增的事件、時間、地點

def get_calendar_events_tomorrow() -> list:
    # Get the events from Calendar for tomorrow
    # input: None
    # output: 顯示在 Calendar 上明天的事件、時間、地點
    
    result = __get_calendar_json()

    schedule = []
    events = result["VCALENDAR"][0]["VEVENT"]

    tomorrow = datetime.datetime.now().date() + datetime.timedelta(days=1)
    for event in events:
        event_start_datetime = None

        if "DTSTART" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART"], "%Y%m%dT%H%M%SZ")
            except ValueError:
                pass
        elif "DTSTART;VALUE=DATE" in event:
            try:
                event_start_datetime = datetime.datetime.strptime(event["DTSTART;VALUE=DATE"], "%Y%m%d")
            except ValueError:
                pass

        if event_start_datetime is None:
            continue

        if event_start_datetime.date() == tomorrow:
            event_details = {
                "summary": event.get("SUMMARY", "No summary"),
                "date": event_start_datetime.date(),
                "time": event_start_datetime.time() if "DTSTART" in event else "All day",
                "description": event.get("DESCRIPTION", "No description"),
                "location": event.get("LOCATION", "No location")
            }
            schedule.append(event_details)

    return schedule

def get_calendar_events_by_date(date) -> str:
    # Get the events from Calendar
    # input:string  date - 想要查看的日期
    # input 格式: "YYYY-MM-DD"
    # output: 顯示在 Calendar 上 date 的事件、時間、地點
    # 視 API 會需要再拆分
    return "Events from Google Calendar"

def delete_calendar_event(event) -> str:
    # Delete an event from Calendar
    # input: dict event - 想要刪除的事件
    # input 格式: {"event": "event_name", "time": "event_time", "location": "event_location"}
    # output: 顯示刪除的事Weather - Get Daily Historical Normals - REST API (Azure Maps)
    # 使用 來取得氣候學數據，例如過去每日正常溫度、降水量和冷卻/加熱度日資訊，以取得指定位置的氣候學數據。件、時間、地點    
    try :
        return "Event deleted from Google Calendar"
    except:
        return "Event not found in Google Calendar"
"""

