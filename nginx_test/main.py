from requests_futures.sessions import FuturesSession
import time

MOVIE_ID = '267eedb8-0f5d-42d5-8f43-72426b9fb3e6'


def run_tests():
    n = 100_000
    print(f'Running {n} REST tests')
    with FuturesSession() as session:
        start = time.time()
        # start all requests
        futures = [
            session.get(f'http://nginx:8000/movies/{MOVIE_ID}')
            for _ in range(n)
        ]
        # wait for all results
        list(map(lambda f: f.result(), futures))
        end = time.time()
    print(f'Total elapsed time for {n} tests: {end - start}s')


if __name__ == '__main__':
    run_tests()
