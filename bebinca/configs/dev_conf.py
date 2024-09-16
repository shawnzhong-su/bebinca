from bebinca.configs.base_conf import BaseSettings


class DevSettings(BaseSettings):
    env = 'dev'

    # mysql
    db_name = 'bebinca'
    db_port = 3306
    db_host = 'localhost'

    db_pool_size = 1
    db_max_overflow = 10

    httpx_pool_size = 10
    httpx_max_overflow = 100

    stream_pool_size = 10
    stream_max_overflow = 100
