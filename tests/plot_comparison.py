import get_all_movies
import get_all_movies_id_only
import get_movie_with_id
import add_movie
import update_movie
import delete_movie
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime

tests = {
    'get_all_movies': get_all_movies,
    'get_all_movies_id_only': get_all_movies_id_only,
    'get_movie_with_id': get_movie_with_id,
    'add_movie': add_movie,
    'update_movie': update_movie,
    # 'delete_movie': delete_movie,
}

data = []
for t, f in tests.items():
    print(t)
    data.append(f.run_tests())

dataT = np.transpose(data)

# set width of bar
barWidth = 0.25
fig, ax = plt.subplots(figsize=(12, 8))
length = len(tests)

# Set position of bar on X axis
br1 = np.arange(length)
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, dataT[0], color='b', width=barWidth, label='REST')
plt.bar(br2, dataT[1], color='g', width=barWidth, label='gRPC')
plt.bar(br3, dataT[2], color='r', width=barWidth, label='GraphQL')

# Adding Xticks
plt.title('Time spent for each microservice', fontweight='bold', fontsize=15)
plt.xlabel('Function called', fontweight='bold', fontsize=13)
plt.ylabel('Time spent (seconds)', fontweight='bold', fontsize=13)
plt.xticks([r + barWidth for r in range(length)], list(tests.keys()))

ax.set_ylim(0, 0.4)
plt.legend()
plt.grid(True)
plt.show()

dtstr = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
fig.savefig(f'results/plot_result_{dtstr}.png')
