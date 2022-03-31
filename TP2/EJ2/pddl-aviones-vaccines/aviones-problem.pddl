; Online-Solver: http://lcas.lincoln.ac.uk/fast-downward/
; ^__ No anduvo!!

; Por consola:
; cd TP2/EJ2
; A_estrella: ./downward/fast-downward.py pddl-aviones-vaccines/aviones-domain.pddl pddl-aviones-vaccines/aviones-problem.pddl --search "astar(lmcut())"
; Default: ./downward/fast-downward.py pddl-aviones-vaccines/aviones-domain.pddl pddl-aviones-vaccines/aviones-problem.pddl --search "lazy_greedy([ff()], preferred=[ff()])"
; Ver plan: cat sas_plan

(define (problem carga-aerea)
    (:domain aviones)
    (:objects 
        ; Aviones Disponibles
        LA01
        LA02
        LA03
        AA01
        AA02
        AA03
        FB01
        FB02
        FB03

        ; Origen de las Vacunas y Destino (Argentina, España)
        INDIA
        CHINA
        UK
        RUSIA
        EEUU
        ARG
        ESP

        ; Vacunas COVID
        COVISHIELD
        SINOPHARM
        ASTRAZENECA
        SPUTNIK-V
        PFIZER
        MODERNA
    )
    (:init 
        (avion LA01)
        (avion LA02)
        (avion LA03)
        (avion AA01)
        (avion AA02)
        (avion AA03)
        (avion FB01)
        (avion FB02)
        (avion FB03)

        (aeropuerto INDIA)
        (aeropuerto CHINA)
        (aeropuerto UK)
        (aeropuerto RUSIA)
        (aeropuerto EEUU)
        (aeropuerto ARG)
        (aeropuerto ESP)

        (carga COVISHIELD)
        (carga SINOPHARM)
        (carga ASTRAZENECA)
        (carga SPUTNIK-V)
        (carga PFIZER)
        (carga MODERNA)

        (en LA01 ARG)
        (en LA02 ARG)
        (en LA03 ESP)
        (en AA01 ARG)
        (en AA02 ARG)
        (en AA03 ESP)
        (en FB01 ARG)
        (en FB02 ESP)
        (en FB03 ESP)

        (en COVISHIELD INDIA)
        (en SINOPHARM CHINA)
        (en ASTRAZENECA UK)
        (en SPUTNIK-V RUSIA)
        (en PFIZER EEUU)
        (en MODERNA EEUU)
    )
    (:goal 
        (and
            (en ASTRAZENECA ARG)
            (en SINOPHARM ARG)
            (en SPUTNIK-V ARG)
            (en COVISHIELD ARG)

            (en PFIZER ESP)
            (en MODERNA ESP)
        )
    )
)