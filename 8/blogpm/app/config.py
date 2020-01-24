import os


base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config:
    # 秘钥，禁止使用中文
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件配置
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.1000phone.com'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'lijie@1000phone.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '123456'
    # 使用本地库中的bootstrap依赖包
    BOOTSTRAP_SERVE_LOCAL = True
    # 文件上传
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')

    # 初始化的方法
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认配置
    'default': DevelopmentConfig
}
