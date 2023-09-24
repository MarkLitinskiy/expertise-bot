import sqlalchemy as sa
import bot.models as models
from sqlalchemy.orm import sessionmaker

from bot import config

main_engine = sa.create_engine(
    config.sqlite_database_url
)

DBSession = sessionmaker(
    binds={
        models.Base: main_engine,
    },
    expire_on_commit=False,
)

# Создаем объект сессии
session = DBSession()