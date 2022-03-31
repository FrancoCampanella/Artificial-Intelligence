
# Guia de comandos para ejecutar el solver de planificación

Primero tener instalado el Fast-Downward y pegarlo en la carpeta del problema. Luego seguir los sig. pasos:
#
# 1. Dirigirse a la carpeta donde esta el Fast-Downward:
> cd '/Volumes/HDD 500/PROYECTOS/repos git/vibraboys2/TP2/EJ2'

#
# 2. Como se resuelve el problema:
Ejemplo:
> ./fast-downward.py domain.pddl problem.pddl --search "lazy_greedy([ff()], preferred=[ff()])"

Ubicarse en la carpeta EJ2 del TP2 por consola y ejecutar la siguiente linea:

> ./downward/fast-downward.py pddl-aviones/aviones-domain.pddl pddl-aviones/aviones-problem.pddl --search "lazy_greedy([ff()], preferred=[ff()])"

Esto va a buscar una solucion utilizando un solver por defecto.

#
# 3. Tambien podemos usar otros algoritmos de busqueda:

## A estrella:

* ### landmark-cut heuristic
> ./fast-downward.py domain.pddl task.pddl --search "astar(lmcut())"

* ### iPDB heuristic with default settings
> ./fast-downward.py domain.pddl task.pddl --search "astar(ipdb())"

* ### blind heuristic
> ./fast-downward.py domain.pddl task.pddl --search "astar(blind())"

## Lazy Greedy:

* ### using FF heuristic and context-enhanced additive heuristic (previously: "fFyY")
> ./fast-downward.py domain.pddl task.pddl \
    --evaluator "hff=ff()" --evaluator "hcea=cea()" \
    --search "lazy_greedy([hff, hcea], preferred=[hff, hcea])" \

* ### using FF heuristic (previously: "fF")
> ./fast-downward.py domain.pddl task.pddl \
    --evaluator "hff=ff()" \
    --search "lazy_greedy([hff], preferred=[hff])" \

* ### using context-enhanced additive heuristic (previously: "yY")
> ./fast-downward.py domain.pddl task.pddl \
    --evaluator "hcea=cea()" \
    --search "lazy_greedy([hcea], preferred=[hcea])" \

#
# 4. Buscando con A*:
Ejemplo de como resolver con A estrella:
> ./downward/fast-downward.py pddl-aviones/aviones-domain.pddl pddl-aviones/aviones-problem.pddl --search "astar(lmcut())"
#
# 5. Para ver el plan encontrado ejecutar:
Ejecutar por consola el siguiente comando que muestra el plan encontrado:
> cat sas_plan

#
# 6. Config
Pddl Search Debugger: Planner Command Line
> --search-tree-dump=http://localhost:$(port)