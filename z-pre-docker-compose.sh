
sudo chmod -R 777 ./app
sudo mkdir -p ./logs
sudo chmod -R 777 ./logs

# volumes for databases
sudo rm -r ./infra/pgdata
sudo rm -r ./infra/mongo/mongodata
sudo rm -r ./infra/qdrant_data
sudo rm -r ./logs/*

sudo mkdir -p ./infra/pgdata
sudo mkdir -p ./infra/mongo/mongodata
sudo mkdir -p ./infra/qdrant_data

sudo chmod -R 777 ./infra/pgdata
sudo chmod -R 777 ./infra/mongo/mongodata
sudo chmod -R 777 ./infra/qdrant_data