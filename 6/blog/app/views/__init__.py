from .main import main
from .user import user


# 蓝本配置元组
DEFAULT_BLUEPRINT = (
    # 蓝本 前缀
    (main, ''),
    (user, '/user')
)

