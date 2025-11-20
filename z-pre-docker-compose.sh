
sudo chmod -R 777 ./app
sudo mkdir -p ./logs
sudo chmod -R 777 ./logs

# volumes for databases
sudo mkdir -p ./infra/pgdata
sudo mkdir -p ./infra/mongo/mongodata

sudo chmod -R 777 ./infra/pgdata
sudo chmod -R 777 ./infra/mongo/mongodata