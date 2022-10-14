from concurrent.futures import wait
from requests_futures.sessions import FuturesSession
import time
import grpc

import movie_pb2
import movie_pb2_grpc


def run_rest_tests(n: int):
    print(f'Running {n} REST tests')
    with FuturesSession() as session:
        start = time.time()
        # start all requests
        futures = (
            session.get(f'http://movie_rest:5001/movies') for _ in range(n))
        # wait for all results
        map(lambda f: [m['id'] for m in f.result()],
            list(map(lambda f: f.result(), futures)))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')
    return end - start


def run_grpc_tests(n: int):
    print(f'Running {n} gRPC tests')
    with grpc.insecure_channel('movie_grpc:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        start = time.time()
        # start all requests
        futures = (stub.GetListMovies(movie_pb2.Empty()) for _ in range(n))
        # wait for all results
        list(map(lambda f: [m.id for m in f], futures))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')
    return end - start


def run_graphql_tests(n: int):
    print(f'Running {n} GraphQL tests')
    query = """query { all_movies { id } }"""
    with FuturesSession() as session:
        start = time.time()
        # start all requests
        futures = (session.post('http://movie_graphql:3301/graphql',
                                json={'query': query}) for _ in range(n))
        # wait for all results
        list(map(lambda f: f.result(), futures))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')
    return end - start


def run_tests():
    n_tests = 100
    return [
        run_rest_tests(n_tests),
        run_grpc_tests(n_tests),
        run_graphql_tests(n_tests),
    ]


if __name__ == '__main__':
    run_tests()
