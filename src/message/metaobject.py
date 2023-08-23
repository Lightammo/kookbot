from dataclasses import dataclass


@dataclass
class User:
    id: str  # 用户的 id
    username:	str  # 用户的名称
    nickname:	str  # 用户在当前服务器的昵称
    identify_num:	str  # 用户名的认证数字，用户名正常为：user_name#identify_num
    online: bool  # 当前是否在线
    bot: bool  # 是否为机器人
    status: int  # 用户的状态, 0 和 1 代表正常，10 代表被封禁
    avatar: str  # 用户的头像的 url 地址
    vip_avatar:	str  # vip 用户的头像的 url 地址，可能为 gif 动图
    mobile_verified:	bool  # 是否手机号已验证
    roles: list  # 用户在当前服务器中的角色 id 组成的列表


@dataclass
class Guild:
    id: str  # 服务器 id
    name: str  # 服务器名称
    topic: str  # 服务器主题
    user_id: str  # 服务器主的 id
    icon: str  # 服务器 icon 的地址
    notify_type:	int  # 通知类型, 0代表默认使用服务器通知设置，1代表接收所有通知, 2代表仅@被提及，3代表不接收通知
    region: str  # 服务器默认使用语音区域
    enable_open: bool  # 是否为公开服务器
    open_id: str  # 公开服务器 id
    default_channel_id:	str  # 默认频道 id
    welcome_channel_id: str  # 欢迎频道 id
    roles:	list  # 角色列表
    channels:	list  # 频道列表


@dataclass
class Role:
    role_id:	int  # 角色 id
    name: str  # 角色名称
    color: int  # 颜色色值
    position:	int  # 顺序位置
    hoist: int  # 是否为角色设定(与普通成员分开显示)
    mentionable: int  # 是否允许任何人@提及此角色
    permissions: int  # 权限码


@dataclass
class Channel:
    id: str  # 频道 id
    name: str  # 频道名称
    user_id: str  # 创建者 id
    guild_id: str  # 服务器 id
    topic: str  # 频道简介
    is_category: bool  # 是否为分组，事件中为 int 格式
    parent_id: str  # 上级分组的 id (若没有则为 0 或空字符串)
    level: int  # 排序 level
    slow_mode: int  # 慢速模式下限制发言的最短时间间隔, 单位为秒(s)
    type: int  # 频道类型: 1 文字频道, 2 语音频道
    permission_overwrites: list  # 针对角色在该频道的权限覆写规则组成的列表
    permission_users: list  # 针对用户在该频道的权限覆写规则组成的列表
    permission_sync: int  # 权限设置是否与分组同步, 1 or 0
    has_password: bool  # 是否有密码


@dataclass
class Quote:
    id: str  # 引用消息 id
    type: int  # 引用消息类型
    content: str  # 引用消息内容
    create_at: int  # 引用消息创建时间（毫秒）
    author:	dict  # 作者的用户信息


@dataclass
class Attachments:
    type: str  # 多媒体类型
    url: str  # 多媒体地址
    name: str  # 多媒体名
    size: int  # 大小 单位 Byte
