/*Verificacion de evacuacion discontinua de gas*/
/*Rama izquierda del arbol de busqueda */
verificar(pilot_ok) :-
    (
        (estado(pilot_ok, desconocido), estado(sit_and_orifice_ok, yes), writeln('Verificar Pilot'));
        (estado(pilot_ok, yes), writeln('Sistem ok, set the safety valve acording to the instructions'));
        (estado(pilot_ok, no), writeln('Make a full service and reinstall it'));
        verificar(sit_and_orifice_ok)
    ).

verificar(sit_and_orifice_ok) :-
    (
        (estado(sit_and_orifice_ok, desconocido), estado(efficiency_of_safety_valve_spring, E), E>=70, writeln('Verificar leakage prevention between sit and orifice'));
        (estado(sit_and_orifice_ok, no), writeln('Replace sit and orifice and put the safety valve into circuit'));
        verificar(efficiency_of_safety_valve_spring)
    ).

verificar(efficiency_of_safety_valve_spring) :-
(
    (estado(efficiency_of_safety_valve_spring, E), E==(-1), estado(control_valve_sensors, Tension), Tension>=5, Tension=<12, writeln('Verificar safety valve spring efficiency'));
    (estado(efficiency_of_safety_valve_spring, E), E<70, E>=0, writeln('Low efficiency: put spring and safety valve in service'));
    verificar(control_valve_sensors)
).

verificar(control_valve_sensors) :-
(
    (estado(control_valve_sensors, Tension), Tension==(-1), estado(valve_status, opened), writeln('Verificar control valve sensors'));
    (estado(control_valve_sensors, Tension), Tension<5, Tension>0, writeln('Low voltage: troubleshoot the sensing pipes'));
    verificar(valve_status)
).
    
verificar(valve_status) :- 
(
    (estado(valve_status, desconocido), estado(pressure_of_the_relief_valve, P), regulating_pressure(RP), P<(RP+(RP*(10/100))), P>0, writeln('Verificar valve status'));
    (estado(valve_status, closed), writeln('Place the safety valve in "Open"'));
    verificar(pressure_of_the_relief_valve)
).
    
verificar(pressure_of_the_relief_valve) :- 
(
    (estado(pressure_of_the_relief_valve, P), P==(-1), estado(safety_valve_has_continuous_evacuation, no), writeln('Verificar si relief valve works correctly with +10% over regular pressure')); 
    (estado(pressure_of_the_relief_valve, P), regulating_pressure(RP), P>=(RP+(RP*(10/100))), P<(RP+(RP*(30/100))), writeln('Safety function appropriate'));
    verificar(safety_valve_has_continuous_evacuation)  
).
/*-----------------------------------------------------------------------------------------------------------------------------*/

/*Verificacion de evacuacion continua de gas */
/*Rama derecha del arbol de busqueda*/
verificar(preventable_leakage_between_sit_and_orifice) :-
    (
        (estado(preventable_leakage_between_sit_and_orifice, desconocido), estado(safety_spring_ok, yes), writeln('Verificar if there is a preventable leakage'));  
        (estado(preventable_leakage_between_sit_and_orifice, no), writeln('Replace sit and orifice and put the safety valve into circuit'));
        (estado(preventable_leakage_between_sit_and_orifice, yes), writeln('Sistem ok, set the safety valve acording to the instructions'));
        verificar(safety_spring_ok)
    ).

verificar(safety_spring_ok) :-
    (
        (estado(safety_spring_ok, desconocido), estado(pressure_sensor_pipes_blocked, no), writeln('Verificar if safety spring is effective'));
        (estado(safety_spring_ok, no), writeln('Replace the safety spring'));
        verificar(pressure_sensor_pipes_blocked)
    ).

verificar(pressure_sensor_pipes_blocked) :-
    (
        (estado(pressure_sensor_pipes_blocked, desconocido), estado(line_gas_pressure, P), regulating_pressure(RP), P==RP, writeln('Verificar if pressure sensor pipes are blocked'));
        (estado(pressure_sensor_pipes_blocked, yes), writeln('Clean up and fix the faults of sensing pipes'));
        verificar(line_gas_pressure)
    ).
verificar(line_gas_pressure) :-
    (
        (estado(line_gas_pressure, P), P==(-1), estado(safety_valve_has_continuous_evacuation, yes), writeln('Verificar line gas pressure'));
        (estado(line_gas_pressure, P), regulating_pressure(RP), P<RP, P>0, writeln('Please adjust the regulator acording to the instructions'));
    	verificar(safety_valve_has_continuous_evacuation)
    ).
/*---------------------------------------------------------------------------------------------*/

verificar(safety_valve_has_continuous_evacuation) :- 
    (
        (estado(safety_valve_has_continuous_evacuation, desconocido), writeln('Verificar the evacuation of safety valve'))
    ).

/*Verificacion del espesor de tubrias*/
verificar(safety_system_having_dazzling_rusting_efects) :- 
                (
                    (estado(safety_system_having_dazzling_rusting_efects, desconocido), writeln('Verificar safety system dazzling and rusting efects'));
                    (estado(safety_system_having_dazzling_rusting_efects, yes), writeln('Coordination is required in order to render and color the equipment'))
                    /*verificar(piloto_ok)*/
                ). 

verificar(thickness) :-
                (
                    (estado(thickness, Esp), Esp==(-1), estado(safety_system_having_dazzling_rusting_efects, no),writeln('Verificar system thickness'));
                    (estado(thickness, Esp), Esp<3, Esp>0, writeln('Please report to technical inspection unit, little tickness'));
                    (estado(thickness, Esp), Esp>=3, writeln('No dazzling and rusting efects , equipment in good conticions'));
                    verificar(safety_system_having_dazzling_rusting_efects)
                ).
/*---------------------------------------------------------------------------------------------*/


/*Verificacion de fugas de gas*/
verificar(gas_leakage_at_joint) :-
                (
                    (estado(gas_leakage_at_joint, desconocido), writeln('Verificar leakage at joint'));
                    (estado(gas_leakage_at_joint, no), writeln('The safety gas joint is free of gas'))
                ).

verificar(leakage_fixed_with_wrench) :-
                (
                	(estado(leakage_fixed_with_wrench, desconocido), (estado(gas_leakage_at_joint, yes), writeln('Verificar si leakage was fixed with wrench')));
                    (estado(leakage_fixed_with_wrench, yes), writeln('Report to technical inspection unit - leakage fixed with wrench'));
                    (estado(leakage_fixed_with_wrench, no), writeln('Report to the repair departament, there is a trouble with the joint'));
                    verificar(gas_leakage_at_joint)
                ).
/*---------------------------------------------------------------------------------------------*/

/*Clausula de verificacion del sistema completo*/
verificar(sistema) :-
    estado(sistema, desconocido), writeln('Analizando sistema...'), 
	(   
    	verificar(thickness), verificar(leakage_fixed_with_wrench), 
    	verificar(pilot_ok);
    	verificar(pressure_of_the_relief_valve)
    ).
/*--------------------------------------------------------------------------------------------------*/

/* GROUND FACTS*/
/*Verificacion de la evacuacion de gas*/
estado(pilot_ok, desconocido).
estado(sit_and_orifice_ok, desconocido).
estado(efficiency_of_safety_valve_spring, X) :- X is (-1).
estado(control_valve_sensors, Tension) :- Tension is (-1).
estado(valve_status, opened) :- valve_opening_status(O), O>=60.
estado(valve_status, closed) :- valve_opening_status(O), O<60, O>0.
estado(valve_status, desconocido) :- valve_opening_status(O), O==(-1).
estado(pressure_of_the_relief_valve, X) :- X is (-1).

estado(line_gas_pressure, X) :- X is (-1).
estado(pressure_sensor_pipes_blocked, desconocido).
estado(safety_spring_ok, desconocido).
estado(preventable_leakage_between_sit_and_orifice, desconocido).
estado(safety_valve_has_continuous_evacuation, desconocido).
/*---------------------------------------------------------------------------------------------*/


/*Verificacion del espesor de tubrias*/
estado(thickness, X) :- X is (-1).
estado(safety_system_having_dazzling_rusting_efects, desconocido).
/*---------------------------------------------------------------------------------------------*/

/*Verificacion de fugas de gas*/
estado(gas_leakage_at_joint, desconocido).
estado(leakage_fixed_with_wrench, desconocido).
/*---------------------------------------------------------------------------------------------*/

estado(sistema, desconocido).

regulating_pressure(RP) :- RP is 300.
valve_opening_status(O) :- O is (-1).
