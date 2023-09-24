# Expertise Bot

## Описание

Бот предназначен для регистрации клиентов на строительные экспертизы с выбором даты и времени. Предусмотрены уведомления клиентов и сотрудников.  
В мои задачи входили: создание базы даныых на Postgresql, работа с Docker (разделение бекэнда и базы данных в разных контейнерах и организация связи между ними через compose).  

## Структура проекта

├── db_data  
├── db_init  
│ ├── creating_base.sql  
├── server  
│ ├── telegram_bot  
│ │ ├── bot  
│ │ └── run.py  
│ ├── Dockerfile  
├── docker-compose.yml  
├── README.md  
└── run.sh  

`db_data` - папка, в которой хранится база данных, она монтируется в контейнер докера, чтобы при удалении последнего данные не терялись (создаётся автоматически);  
`db_init` - в этой папке находится скрипт инициализации базы данных при первом развёртывании бота (`creating_base.sql`);  
`server` - бэкэнд бота, точкой компиляции является файл `run.py`. `Dockerfile` содержит инструкции для развёртывания контейнера с ботом.   
`docker-compose.yml` - файл с инструкциями для развёртывания двух контейнеров - с базой данных и ботом.  
`run.sh` - скрипт для автоматического развёртывания.  
