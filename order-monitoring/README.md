# Prerequisites

1. Installation of
   - Python
   - Docker

# Building the application

1. Build the flink-statefun and flink docker images (once)

   - Clone StateFun repository
   - Go into repository
   - Run `mvn clean package`
   - Go to 'order-monitoring' directory
   - `cd docker/`
   - Run `build-stateful-functions.sh`

2. Build the Python distribution (once)
   - `cd statefun-python-sdk/`
   - Run `./build-distribution.sh`

3. Run `./build-application.sh` (After every change of the codebase)

# Running the example

docker-compose up

[Alternatively:
docker-compose up -d.
To see what comes out of the topics `status` and `reports`:
docker-compose logs -f order-generator]

# Für Protokolländerungen

1. Installiere Protobuf Compiler 
   1. Binary Windows Version 
   2. Python Umgebung
   https://github.com/protocolbuffers/protobuf/releases (Siehe ReadMe)

Generiere pb2.py aus .proto Datei:
protoc messages.proto --python_out=./

# Kafka-Fehler beheben

Alle Container entfernen:
docker rm $(docker ps -aq)
