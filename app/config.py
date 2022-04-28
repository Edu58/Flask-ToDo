class Config:
    SECRET_KEY = "JVCY56U6TTT6FVUvJHVYT67T67hgvh7878JHBU7T78T"


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    pass
