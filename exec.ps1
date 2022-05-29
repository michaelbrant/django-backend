pipenv lock -r > requirements.txt
docker build -t disco-backend-docker .
docker run --env-file .env -p 8000:8000 -it disco-backend-docker
