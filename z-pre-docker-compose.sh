
sudo chmod -R 777 ./app
sudo mkdir -p ./logs
sudo chmod -R 777 ./logs

# volumes for databases
sudo rm -r ./infra/pgdata
sudo rm -r ./infra/mongo/mongodata
sudo rm -r ./infra/qdrant_data
sudo rm -r ./logs/*
sudo rm -r ./infra/redis_data
