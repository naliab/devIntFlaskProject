#!/bin/bash

if [ "$DB_HOST" = "db" ]
then
 echo "Ожидание инициализации MySQL..."
 while !</dev/tcp/$DB_HOST/$DB_PORT; do sleep 1; done 2>/dev/null
 echo "MySQL готов к работе"
fi

flask db init
flask db migrate
flask db upgrade
flask create_initial_admin
flask load_data
flask run --host=0.0.0.0