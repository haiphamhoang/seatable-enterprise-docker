# docker-seatable

## Env

- REDIS_HOST: `string`
- MEMCACHED_HOST: `string`
- SEATABLE_SERVER_URL_FORCE_HTTPS: `bool` 
    - it's useful when use with reverse proxy like traefik.
- DB_ROOT_PASSWD_FILE: `filepath`




# Dev

## Upgrade 
### Checking new script
1. Run container with new seatable/seatable-enterprise:latest version, using default [docker-compose.yml](https://manual.seatable.io/docker/Enterprise-Edition/Deploy%20SeaTable-EE%20with%20Docker/#downloading-and-modifying-docker-composeyml)
2. copy file at `/templates/`
```
docker cp CONTAINER:/templates test/templates
```
