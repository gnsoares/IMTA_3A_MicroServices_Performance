from concurrent.futures import wait
from requests_futures.sessions import FuturesSession
import time
import grpc

import movie_pb2
import movie_pb2_grpc

MOVIE_ID = '39ab85e5-5e8e-4dc6-afea-65dc368bd7ab'


def run_rest_tests(n: int):
    print(f'Running {n} REST tests')
    jsonRequest = {
        "title": "Knives Out",
        "rating": 7.9,
        "director": "Ryan Johnson"
    }
    with FuturesSession() as session:
        start = time.time()
        # start all requests
        futures = (session.post(f'http://movie_rest:5001/movies/{MOVIE_ID}',
                                json=jsonRequest) for _ in range(n))
        # wait for all results
        list(map(lambda f: f.result(), futures))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')
    return end - start


def run_grpc_tests(n: int):
    print(f'Running {n} gRPC tests')
    with grpc.insecure_channel('movie_grpc:3001') as channel:
        stub = movie_pb2_grpc.MovieStub(channel)
        movie = movie_pb2.MovieData(id=MOVIE_ID,
                                    title="Knives Out",
                                    rating=7.9,
                                    director="Rian Johnson")
        start = time.time()
        # start all requests
        futures = (stub.CreateMovie.future(movie) for _ in range(n))
        # wait for all results
        list(map(lambda f: f.result(), futures))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')
    return end - start


def run_graphql_tests(n: int):
    print(f'Running {n} GraphQL tests')
    query = """mutation {{
    create_movie(_id:"{movieid}",
                 _title: "Knives Out",
                 _director: "Rian Johnson",
                 _rate: 7.9) {{ ... on Movie {{
                                title
                                rating
                                director
                                id }} }} }}""".format(movieid=MOVIE_ID)
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
    rest = run_rest_tests(n_tests)
    grpc = run_grpc_tests(n_tests)
    graphql = run_graphql_tests(n_tests)
    data = [rest, grpc, graphql]
    return data


if __name__ == '__main__':
    run_tests()
