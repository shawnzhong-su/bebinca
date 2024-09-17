from bebinca.configs.base_conf import BaseSettings


class ProdSettings(BaseSettings):
    env = 'prod'

    # mysql
    db_name = 'WantSun$bebinca'
    db_port = 3306
    db_host = 'WantSun.mysql.pythonanywhere-services.com'

    db_pool_size = 1
    db_max_overflow = 10

    httpx_pool_size = 10
    httpx_max_overflow = 100

    stream_pool_size = 10
    stream_max_overflow = 100
