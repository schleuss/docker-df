# Docker - disk usage

Script utility to verify docker volume usage

## Run 

### Directly with docker

```bash
docker run -it --rm \
    -v "/var/run/docker.sock:/var/run/docker.sock" \
    -v "/var/lib/docker:/var/lib/docker" schleuss/docker-df:latest
```

### With utility shell script 

```bash
./docker-df.sh
```
