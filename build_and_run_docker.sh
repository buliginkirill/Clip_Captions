docker build -t my-python-service .
docker run --net= host -p 5001:5001 -p 5000:5000 my-python-service
