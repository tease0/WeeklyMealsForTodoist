# main.py

from todoist_api_python.api import TodoistAPI
import datetime
import os
import logging

# logger_config.py から setup_logging 関数をインポート
from logger_config import setup_logging

# ロギングの設定を行う
logger = setup_logging()

# 環境変数からAPIキーを取得
api_key = os.getenv("TODOIST_API_KEY")
if not api_key:
    logger.error("TODOIST_API_KEY is not set in environment variables.")
    raise ValueError("TODOIST_API_KEY is not set in environment variables.")
api = TodoistAPI(api_key)

# 定数
SECTION_ID = "173865593"
PROJECT_ID = "6Rmr4M4m3McmR9JV" 
SATURDAY = 5
DAYS_OF_WEEK_JP = ["日", "月", "火", "水", "木", "金", "土"]

def create_day() -> list[str]:
    """
    次の土曜日から始まる1週間の日付と曜日を日本語でリストとして返す関数。
    
    Returns:
        list[str]: 日付と曜日を日本語で表した文字列のリスト。
    """
    today = datetime.date.today()
    logger.debug(f"Today's date: {today}")

    # 次の土曜日を見つける
    while today.weekday() != SATURDAY:  # 5は土曜日を表します
        today += datetime.timedelta(days=1)
        logger.debug(f"Checking next day: {today}")

    WEEKDAY_FORMAT = "%w"
    days = []
    for i in range(7):
        current_date = today + datetime.timedelta(days=i)
        day_of_week = current_date.strftime(WEEKDAY_FORMAT)  # 0: 日曜日, 1: 月曜日, ..., 6: 土曜日
        day_of_week_jp = DAYS_OF_WEEK_JP[int(day_of_week)]
        day_str = f"{current_date.day}({day_of_week_jp}):"
        logger.debug(f"Adding day: {day_str}")
        days.append(day_str)

    return days

def add_task(content: str) -> None:
    """
    Todoistに新しいタスクを追加する関数。

    Args:
        content (str): タスクの内容。

    Returns:
        None
    """
    try:
        task = api.add_task(content=content, project_id=PROJECT_ID, section_id=SECTION_ID)
        logger.info(f"Task added successfully: {task}")
    except Exception as error:
        logger.error(f"Error adding task: {error}")

def main() -> None:
    logger.info("Script started.")
    days = create_day()
    for day in days:
        logger.info(day)
        add_task(day)
    logger.info("Script finished.")

if __name__ == "__main__":
    main()
