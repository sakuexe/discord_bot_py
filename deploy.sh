docker build -t raino-python .
docker run -d --rm --name raino-bot raino-python
docker update --restart always raino-bot
