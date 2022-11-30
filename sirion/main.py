import pickle
import numpy as np
import matplotlib.pyplot as plt

from assembler import solve_cavity




#nx = 80#120
#ny = 80#120


# Load ghia results for validation
ghia100 = np.genfromtxt('experimental_data/Re100.csv', delimiter=',')
ghia400 = np.genfromtxt('experimental_data/Re400.csv', delimiter=',')
ghia1000 = np.genfromtxt('experimental_data/Re1000.csv', delimiter=',')



# # # RUN FOR MULTIPLE MESHES
# reynolds = 400
# tolerance = 1e-5

# meshes = [100]##10, 20, 40, 80, 120]
# for n in meshes:

#     print(f' __________ MESH : {n} __________')

#     try:
#         output = solve_cavity(n, n, reynolds, tolerance, ghia100, save=True)

#     except:
#         print(f'No convergence for mesh {n}x{n}')


# RUN FOR MULTIPLE TOLERANCES
n = 100
reynolds = 400
tols = [1e-5]
for tol in tols:

    print(f' __________ MESH : {n} __________')

    try:
        output = solve_cavity(n, n, reynolds, tol, ghia100, save=True)

    except:
        print(f'No convergence for mesh {n}x{n}')


n = 120
reynolds = 400
tols = [1e-6]
for tol in tols:

    print(f' __________ MESH : {n} __________')

    try:
        output = solve_cavity(n, n, reynolds, tol, ghia100, save=True)

    except:
        print(f'No convergence for mesh {n}x{n}')


n = 80
reynolds = 100
tols = [1e-6]
for tol in tols:

    print(f' __________ MESH : {n} __________')

    try:
        output = solve_cavity(n, n, reynolds, tol, ghia100, save=True)

    except:
        print(f'No convergence for mesh {n}x{n}')



##########################################################################
## COMPARE TOLERANCE
ghiau = ghia100[:,:2]
ghiav = ghia100[:,2:]

uu = dict()
uNormal = dict()
yyU = dict()
yNormal = dict()

mesh = 80

for tol in [0.01, 0.001, 0.0001, 0.00001]:

    name = f'Reynolds_{100}__Mesh_{80}_Tol_{tol}.pickle'
    path = 'results/Re100_tolerance_test/'

    with open(path + name, 'rb') as handle:
        output = pickle.load(handle)

    nx = ny = 80
    um = output['um']
    pmesh = output['pmesh']

    y = pmesh.elements['y']
    y = y.reshape((nx, ny))

    prime_it = output['prime_it']
    comp_time = output['comp_time']


    print(f'Tolerance: {tol}x{tol}')
    print(f'    Iterações: {prime_it}')
    print(f'    Tempo [s]: {comp_time}')

    um = um.reshape((nx, ny))

    mid = nx // 2

    
    uu[str(tol)] = um[:, mid]
    yyU[str(tol)] = y[:, mid]
   

fig, ax = plt.subplots()


ax.set_xlabel('u/U', fontsize=14)  
ax.set_ylabel('y', fontsize=14)
ax.grid()

## FOR Re100
## By Color
ax.plot(uu['0.01'], yyU['0.01'], label = '1e-2')
ax.plot(uu['0.001'], yyU['0.001'], label = '1e-3')
ax.plot(uu['0.0001'], yyU['0.0001'], label = '1e-4')
ax.plot(uu['1e-05'], yyU['1e-05'], label = '1e-5')

ax.plot(ghiau[:,1], ghiau[:,0], 'x', color='k', mew=2, markersize=7, label='(Ghia, 1982)')
ax.legend()
plt.show()

# Error
i = 1
meshes = [0.01, 0.001, 0.0001, 0.00001]
for nx in meshes[:-1]:#]:
    error = np.sum(np.abs(uu[str(nx)] - uu[str(meshes[i])])) / 80
    print(f'{nx}x{nx} : {error*100}')
    i += 1




## COMPARE MESH

ax.set_xlabel('u/U', fontsize=14)  
ax.set_ylabel('y', fontsize=14)
ax.grid()

## FOR Re100
## By Color
ax.plot(uu['0.001'], yyU['0.0001'], label = '1e-3')
ax.plot(uu['0.0001'], yyU['0.0001'], label = '1e-4')
ax.plot(uu['1e-05'], yyU['1e-05'], label = '1e-5')

ax.plot(ghiau[:,1], ghiau[:,0], 'x', color='k', mew=2, markersize=7, label='(Ghia et al.)')
ax.legend()
plt.show()

ghiau = ghia100[:,:2]
ghiav = ghia100[:,2:]

uu = dict()
uNormal = dict()
yyU = dict()
yNormal = dict()

for mesh in [10, 20, 40, 80, 100]:

    name = f'Reynolds_{100}__Mesh_{mesh}_Tol_{1e-5}.pickle'
    path = 'results/Re100 _mesh_test/'

    with open(path + name, 'rb') as handle:
        output = pickle.load(handle)

    nx = ny = mesh
    um = output['um']
    pmesh = output['pmesh']

    y = pmesh.elements['y']
    y = y.reshape((nx, ny))

    prime_it = output['prime_it']
    comp_time = output['comp_time']


    print(f'Mesh: {mesh}x{mesh}')
    print(f'    Iterações: {prime_it}')
    print(f'    Tempo [s]: {comp_time}')

    um = um.reshape((nx, ny))

    mid = nx // 2

    
    uu[str(mesh)] = um[:, mid]
    yyU[str(mesh)] = y[:, mid]

    uNormal[str(mesh)] = um[0:nx:int(mesh/10), mid]
    yNormal[str(mesh)] = y[0:nx:int(mesh/10), mid]

    

fig, ax = plt.subplots()


ax.set_xlabel('u/U', fontsize=14)  
ax.set_ylabel('y', fontsize=14)
ax.grid()

## FOR Re100
## By Color
ax.plot(uu['10'], yyU['10'], label = '10x10')
ax.plot(uu['20'], yyU['20'], label = '20x20')
ax.plot(uu['40'], yyU['40'], label = '40x40')
ax.plot(uu['80'], yyU['80'], label = '80x80')
ax.plot(uu['100'], yyU['100'], label = '100x100')

ax.plot(ghiau[:,1], ghiau[:,0], 'x', color='k', mew=2, markersize=7, label='(Ghia, 1982)')
ax.legend()
plt.show()

## By Linestyle
# ax.plot(uu['10'], yyU['10'])#, color='k', marker='.', label = '10x10')
# ax.plot(uu['20'], yyU['20'], color='k', marker='*', label = '20x20')
# ax.plot(uu['40'], yyU['40'], color='k', label = '40x40')
# ax.plot(uu['80'], yyU['80'], color='k', linestyle='-.', label = '80x80')
# ax.plot(uu['160'], yyU['160'])#, color='k', linestyle='')
# ax.legend()
# plt.show()

## Mean variation## By Color
fig, ax = plt.subplots()
ax.plot(uNormal['10'], yNormal['10'], label = '10x10')
ax.plot(uNormal['20'], yNormal['20'], label = '20x20')
ax.plot(uNormal['40'], yNormal['40'], label = '40x40')
ax.plot(uNormal['80'], yNormal['80'], label = '80x80')
ax.plot(uNormal['160'], yNormal['160'], label = '160x160')
ax.legend()
plt.show()

i = 1
meshes = [100, 80, 40, 20, 10]
for nx in meshes[:-1]:#]:
    error = np.sum(np.abs(uNormal[str(nx)] - uNormal[str(meshes[i])])) / 10
    print(f'{nx}x{nx} : {error*100}')
    i += 1



# ## FOR Re400
# # ax.plot(uu['80'], yyU['80'], color='k', linestyle='--', label = '80x80')
# # ax.plot(uu['120'], yyU['120'], color='k', label = '120x120')
# # ax.legend()
# # plt.show()

#error = np.sum(np.abs(uNormal['120'] - uNormal['80'])) / 20

# ax.plot(uNormal['80'], yNormal['80'], color='k', marker = '*', label = '80x80')
# ax.plot(uNormal['120'], yNormal['120'], color='k', marker = '*', label = '120x120')
# ax.legend()
# plt.show()


## OFICIAL MESH FOR Re 100
# 80 x 80

############################################################################
############################################################################
## Re 400

ghiau = ghia400[:,:2]
ghiav = ghia400[:,2:]

uu = dict()
uNormal = dict()
yyU = dict()
yNormal = dict()

for mesh in [80, 120]:

    name = f'Reynolds_{400}__Mesh_{mesh}_Tol_{1e-5}.pickle'
    path = 'results/Re400_mesh/'

    with open(path + name, 'rb') as handle:
        output = pickle.load(handle)

    nx = ny = mesh
    um = output['um']
    pmesh = output['pmesh']

    y = pmesh.elements['y']
    y = y.reshape((nx, ny))

    prime_it = output['prime_it']
    comp_time = output['comp_time']


    print(f'Mesh: {mesh}x{mesh}')
    print(f'    Iterações: {prime_it}')
    print(f'    Tempo [s]: {comp_time}')

    um = um.reshape((nx, ny))

    mid = nx // 2

    
    uu[str(mesh)] = um[:, mid]
    yyU[str(mesh)] = y[:, mid]

    uNormal[str(mesh)] = um[0:nx:int(mesh/10), mid]
    yNormal[str(mesh)] = y[0:nx:int(mesh/10), mid]

    

fig, ax = plt.subplots()

ax.plot(ghiau[:,1], ghiau[:,0], 'x', mew=2, markersize=7)
ax.set_xlabel('u/U', fontsize=14)  
ax.set_ylabel('y', fontsize=14)
ax.grid()

ax.plot(uu['80'], yyU['80'], label = '80x80')
ax.plot(uu['120'], yyU['120'], label = '120x120')
# ax.plot(uu['40'], yyU['40'], label = '40x40')
# ax.plot(uu['80'], yyU['80'], label = '80x80')
# ax.plot(uu['160'], yyU['160'], label = '160x160')
ax.legend()
plt.show()


i = 1
meshes = [120, 80]
for nx in meshes[:-1]:#]:
    error = np.sum(np.abs(uNormal[str(nx)] - uNormal[str(meshes[i])])) / 10
    print(f'{nx}x{nx} : {error*100}')
    i += 1




## TOLERANCE

ghiau = ghia400[:,:2]
ghiav = ghia400[:,2:]

uu = dict()
uNormal = dict()
yyU = dict()
yNormal = dict()

mesh = 80

for tol in [0.001, 0.0001, 0.00001]:

    name = f'Reynolds_{400}__Mesh_{80}_Tol_{tol}.pickle'
    path = 'results/Re400_tolerance test/'

    with open(path + name, 'rb') as handle:
        output = pickle.load(handle)

    nx = ny = 80
    um = output['um']
    pmesh = output['pmesh']

    y = pmesh.elements['y']
    y = y.reshape((nx, ny))

    prime_it = output['prime_it']
    comp_time = output['comp_time']


    print(f'Tolerance: {tol}x{tol}')
    print(f'    Iterações: {prime_it}')
    print(f'    Tempo [s]: {comp_time}')

    um = um.reshape((nx, ny))

    mid = nx // 2

    
    uu[str(tol)] = um[:, mid]
    yyU[str(tol)] = y[:, mid]
    

fig, ax = plt.subplots()


ax.set_xlabel('u/U', fontsize=14)  
ax.set_ylabel('y', fontsize=14)
ax.grid()

## FOR Re100
## By Color
ax.plot(uu['0.001'], yyU['0.0001'], label = '1e-3')
ax.plot(uu['0.0001'], yyU['0.0001'], label = '1e-4')
ax.plot(uu['1e-05'], yyU['1e-05'], label = '1e-5')

ax.plot(ghiau[:,1], ghiau[:,0], 'x', color='k', mew=2, markersize=7, label='(Ghia, 1982)')
ax.legend()
plt.show()