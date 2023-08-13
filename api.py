ENDPOINT = 'https://www.kookapp.cn/api'
GATEWAY = '/api/v3/gateway/index'


class Guild:
    LIST = "/api/v3/guild/list"  # GET
    VIEW = "/api/v3/guild/view"  # GET
    USERLIST = "/api/v3/guild/user-list"  # GET
    NICKNAME = "/api/v3/guild/nickname"  # POST
    MUTELIST = "/api/v3/guild-mute/list"  # GET
    BOOSTHISTORY = "/api/v3/guild-boost/history"  # GET


class Channel:
    LIST = "/api/v3/channel/list"
    VIEW = "/api/v3/channel/view"
    CREATE = "/api/v3/channel/create"
    UPDATE = "/api/v3/channel/update"
    DELETE = "/api/v3/channel/delete"
    USERLIST = "/api/v3/channel/user-list"


class Message:
    CREATE = "/api/v3/message/create"  # POST


class User:
    ME = "/api/v3/user/me"  # GET
