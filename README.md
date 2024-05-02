# docker-seatable

## Additional Env

- REDIS_HOST: `string`
- MEMCACHED_HOST: `string`
- DB_ROOT_PASSWD_FILE: `filepath`


## For Upgrade new image version 

### Checking new script
1. Run container with new seatable/seatable-enterprise:latest version, using default [docker-compose.yml](https://manual.seatable.io/docker/Enterprise-Edition/Deploy%20SeaTable-EE%20with%20Docker/#downloading-and-modifying-docker-composeyml)
2. copy file at `/templates/`
```
docker cp CONTAINER:/templates test/templates
```
