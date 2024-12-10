DEV_USER_ID = 40322523
GREETINGS_TABLE = 'greeting_messages'
PERMISSIONS_TABLE = 'user_permissions'
MESSAGE_HIST_TABLE = 'messages_to_delete'
REPORTS_TABLE = 'report_spam_users'
BAN_TRESHOLD = 3
DTTM_FORMAT = 'YYYY-MM-DD HH:mm:SS'
DB_MAPPING = {
    "greetings": {
        "ENDPOINT": "YDB_ENDPOINT",
        "DATABASE": "YDB_DATABASE",
    },
    "reports": {
        "ENDPOINT": "REPORTS_ENDPOINT",
        "DATABASE": "REPORTS_DATABASE",
    },
}