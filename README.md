# docker-seatable

## Addition Enviroments

- REDIS_HOST: `string`
    - it's useful when use with reverse proxy like traefik.
- DB_ROOT_PASSWD_FILE: `filepath`




# Develop

## Upgrade 
### Checking new script
1. Run container with new seatable/seatable-enterprise:latest version, using default [docker-compose.yml](https://manual.seatable.io/docker/Enterprise-Edition/Deploy%20SeaTable-EE%20with%20Docker/#downloading-and-modifying-docker-composeyml)

2. Run `docker-compose up -d` to start the container

3. copy file at `/templates/`
```
docker cp seatable-server:/templates test/templates
```

## Test Dockerfile

```
docker compose up --build
```