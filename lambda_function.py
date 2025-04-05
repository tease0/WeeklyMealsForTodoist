import logging
from typing import Dict, Any

# logger_config.py から setup_logging 関数をインポート
# main.py から main 関数をインポートする必要がある
from logger_config import setup_logging
from main import main as main_process # main という名前が被るので別名でインポート

# ロギングの設定を行う
logger = setup_logging()

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """AWS Lambda用のハンドラー関数
    
    Args:
        event (Dict[str, Any]): Lambda関数のイベントデータ
        context (Any): Lambda関数のコンテキスト
        
    Returns:
        Dict[str, Any]: レスポンス情報を含む辞書
            - statusCode (int): HTTPステータスコード
            - body (str): レスポンスメッセージ
    """
    logger.info("Lambda handler started.")
    try:
        # main.py の main 関数を実行する
        main_process()
        
        logger.info("Lambda handler finished successfully.")
        return {
            'statusCode': 200,
            'body': 'Tasks created successfully via main process'
        }
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error executing main process: {str(e)}'
        }

# ローカルテスト用 (もし必要なら)
# if __name__ == "__main__":
#     print(lambda_handler({}, {}))
