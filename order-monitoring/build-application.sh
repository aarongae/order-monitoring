#!/bin/bash

# clean
rm -f apache_flink_statefun-*-py3-none-any.whl
rm -rf __pycache__

# remove old docker images
docker rmi order-monitoring_order-generator
docker rmi order-monitoring_python-worker
docker rmi order-monitoring_master
docker rmi order-monitoring_worker
docker rmi order-monitoring_results-consumer

# copy the whl distribution
cp ../statefun-python-sdk/dist/apache_flink_statefun-*-py3-none-any.whl monitoring/apache_flink_statefun-snapshot-py3-none-any.whl 2>/dev/null
rc=$?
if [[ ${rc} -ne 0 ]]; then
    echo "Failed copying the whl distribution, please build the Python distribution first."
    echo "To build the distribution:"
    echo "  goto to statefun-python-sdk/"
    echo "  call ./build-distribution.sh"
    exit 1;
fi

# build
docker-compose build

rm -f monitoring/apache_flink_statefun-*-py3-none-any.whl

echo "Done. To start the example run: docker-compose up"

