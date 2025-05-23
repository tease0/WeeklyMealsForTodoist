from todoist_api_python.api import TodoistAPI
import datetime
import os
import logging
from typing import Dict, Any

# logger_config.py から setup_logging 関数をインポート
from logger_config import setup_logging

# ロギングの設定を行う
logger = setup_logging()

# 定数
SECTION_ID = "173865593"
PROJECT_ID = "6Rmr4M4m3McmR9JV"
SATURDAY = 5
DAYS_OF_WEEK_JP = ["日", "月", "火", "水", "木", "金", "土"]

def initialize_api():
    """APIの初期化を行う関数
    
    Returns:
        TodoistAPI: 初期化されたTodoistAPIインスタンス
        
    Raises:
        ValueError: TODOIST_API_KEYが環境変数に設定されていない場合
    """
    api_key = os.getenv("TODOIST_API_KEY")
    if not api_key:
        logger.error("TODOIST_API_KEY is not set in environment variables.")
        raise ValueError("TODOIST_API_KEY is not set in environment variables.")
    return TodoistAPI(api_key)

def create_day() -> list[str]:
    """来週の土曜日から始まる1週間の日付と曜日を日本語でリストとして返す関数
    
    Returns:
        list[str]: 日付と曜日の文字列のリスト（例: ["1(土):", "2(日):", ...]）
    """
    today = datetime.date.today()
    logger.debug(f"Today's date: {today}")

    # 次の土曜日を見つける
    days_until_saturday = (SATURDAY - today.weekday() + 7) % 7
    next_saturday = today + datetime.timedelta(days=days_until_saturday)

    # 来週の土曜日にする
    next_saturday += datetime.timedelta(days=7)
    logger.debug(f"Next week's Saturday: {next_saturday}")
    today = next_saturday

    WEEKDAY_FORMAT = "%w"
    days = []
    for i in range(7):
        current_date = today + datetime.timedelta(days=i)
        day_of_week = current_date.strftime(WEEKDAY_FORMAT)
        day_of_week_jp = DAYS_OF_WEEK_JP[int(day_of_week)]
        day_str = f"{current_date.day}({day_of_week_jp}):"
        logger.debug(f"Adding day: {day_str}")
        days.append(day_str)

    return days

def add_task(api: TodoistAPI, content: str) -> None:
    """Todoistに新しいタスクを追加する関数

    Args:
        api (TodoistAPI): TodoistAPIインスタンス
        content (str): 追加するタスクの内容

    Returns:
        None

    Raises:
        Exception: タスク追加時にエラーが発生した場合
    """
    try:
        task: Dict[str, Any] = api.add_task(content=content, project_id=PROJECT_ID, section_id=SECTION_ID)
        logger.info(f"Task added successfully: {task}")
    except Exception as error:
        logger.error(f"Error adding task: {error}")
        raise

def main() -> None:
    """ローカル実行用のメイン関数
    
    Returns:
        None
    """
    logger.info("Script started.")
    api = initialize_api()
    days = create_day()
    for day in days:
        logger.info(day)
        add_task(api, day)
    logger.info("Script finished.")
    
#
if __name__ == "__main__":
    main()
