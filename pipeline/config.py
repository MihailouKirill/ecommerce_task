from pydantic_settings import BaseSettings , SettingsConfigDict
from pathlib import Path

__all__ = ['Settings','app_settings']

#Описание схемы настроек
class Settings(BaseSettings):
    #Настройки бд
    db_host:str
    db_port:int
    db_user:str
    db_password:str
    db_name:str

    #Настройка размера батчей
    batch_size:int

    #Откуда читает
    model_config= SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent/".env",
        env_file_encoding='utf-8'
    )
# Загрузка настроек при импорте
app_settings = Settings()