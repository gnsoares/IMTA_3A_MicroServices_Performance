# tp-perfs

## Running comparisons between REST/gRPC/GraphQL

```
docker-compose up [--build] plot_comparison
```

The resulting plot will be in a `results` folder

## Running comparisons of NGINX available containers

```
docker-compose up -d [--build] movie_rest movie2 movie3 movie4
```

Edit the `nginx.conf` file to vary the number of containers available.

```
docker-compose up [--build] nginx nginx_test
```

Get the results from the logs.
