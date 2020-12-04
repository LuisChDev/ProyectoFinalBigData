import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from dataframe import PARTIDOS
from pickle import load

fig = plt.figure()
ax = Axes3D(fig)

for p, c, s in PARTIDOS:
    with open('dataframes/' + p + '.pkl', 'rb') as archivo:
        frame = load(archivo)
    ax.scatter(xs=frame['positive'], ys=frame['neutral'], zs=frame['negative'])


plt.show()
