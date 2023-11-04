echo "Создание бэкапа"
local DB_NAME=$(grep DB_NAME .env | cut -d '=' -f2)
mkdir -p backups
local FILE_PATH="./backups/dump_`date +%d-%m-%Y"_"%H_%M_%S`.backup"
docker-compose exec db mkdir -p backups
docker-compose exec db pg_dump -Ft $DB_NAME -f $FILE_PATH
local DB_CONTAINER_NAME=$(docker-compose ps -q db)
docker cp $DB_CONTAINER_NAME:/home/postgres/$FILE_PATH $FILE_PATH
docker-compose exec db rm $FILE_PATH
echo "Бэкап создан: $FILE_PATH"
