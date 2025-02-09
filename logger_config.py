# logger_config.py

import logging

def setup_logging(
    logger_name: str = __name__,
    log_level: int = logging.INFO,
    log_format: str = '%(asctime)s - %(levelname)s - %(message)s',
    date_format: str = '%Y-%m-%d %H:%M:%S'
) -> logging.Logger:
    """
    ログ設定を行う関数。

    Args:
        logger_name (str): ロガーの名前。デフォルトは現在のモジュール名。
        log_level (int): ログレベル。デフォルトは logging.INFO。
        log_format (str): ログフォーマット。デフォルトは 'timestamp - level - message'。
        date_format (str): 日付フォーマット。デフォルトは 'YYYY-MM-DD HH:MM:SS'。

    Returns:
        logging.Logger: 設定されたロガーオブジェクト。
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # 既にハンドラーが設定されている場合は追加しない
    if not logger.handlers:
        # コンソール用ハンドラーの作成
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # ログフォーマットの設定
        formatter = logging.Formatter(
            fmt=log_format,
            datefmt=date_format
        )
        console_handler.setFormatter(formatter)

        # ハンドラーをロガーに追加
        logger.addHandler(console_handler)

    return logger
