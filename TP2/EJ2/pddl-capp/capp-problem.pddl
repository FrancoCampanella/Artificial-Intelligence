(define (problem capp-pieza)
    (:domain capp)
    (:objects 
        orientacionX
        orientacionY
        orientacionZ
        orientacion-X
        orientacion-Y
        orientacion-Z
     
     	s2
        s4
        s6
     	s8
        s9
        s10
     	h1
     	h3
     	h5
     	h7
     	h9
     	h11
     	h12
     
        slot
        through-hole
        blind-hole
     
        fresado
        taladrado
        torneado
    )
    (:init 
        (orientacion orientacionX)
        (orientacion orientacionY)
        (orientacion orientacionZ)
        (orientacion orientacion-X)
        (orientacion orientacion-Y)
        (orientacion orientacion-Z)
     
        (feature s2)
        (feature s4)
        (feature s6)
        (feature s8)
        (feature s9)
        (feature s10)
     	(feature h1)
     	(feature h3)
     	(feature h5)
     	(feature h7)
     	(feature h9)
     	(feature h11)
     	(feature h12)
     
        (tipo slot)
        (tipo through-hole)
        (tipo blind-hole)
     
        (operacion fresado)
        (operacion taladrado)
        (operacion torneado)
     
        (feature-tipo s2 slot)
        (feature-tipo s4 slot)
        (feature-tipo s6 slot)
        (feature-tipo s8 slot)
        (feature-tipo s9 slot)
        (feature-tipo s10 slot)
        (feature-tipo h1 through-hole)
        (feature-tipo h3 through-hole)
        (feature-tipo h5 through-hole)
        (feature-tipo h7 through-hole)
        (feature-tipo h9 through-hole)
        (feature-tipo h11 through-hole)
        (feature-tipo h12 through-hole)
     
        (orientacion-pieza orientacion-X)
     
        (orientacion-feature s2 orientacionX)
        (orientacion-feature s4 orientacion-X)
        (orientacion-feature s6 orientacionX)
        (orientacion-feature s8 orientacion-X)
        (orientacion-feature s9 orientacionZ)
        (orientacion-feature s10 orientacionZ)
     	(orientacion-feature h1 orientacionZ)
     	(orientacion-feature h3 orientacionZ)
     	(orientacion-feature h5 orientacionZ)
        (orientacion-feature h7 orientacionX)
        (orientacion-feature h9 orientacionX)
        (orientacion-feature h11 orientacionX)
        (orientacion-feature h12 orientacionX)
     
        (fabricable slot fresado)
        (fabricable through-hole taladrado)
    )
    (:goal 
        (and
            (fabricada s2)
            (fabricada s4)
            (fabricada s6)
            (fabricada s8)
            (fabricada s9)
            (fabricada s10)
            (fabricada h1)
            (fabricada h3)
            (fabricada h5)
            (fabricada h7)
            (fabricada h9)
            (fabricada h11)
            (fabricada h12)
        )
    )
)