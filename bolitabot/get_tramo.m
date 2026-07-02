function [P0, P1, V0, V1] = get_tramo(tramo)
    % --- 1. DEFINICIÓN DE GEOMETRÍA ---
    L = 3.0;
    
    % mag: Es la "fuerza" de la curva. 
    % L*1.5 hace que los pétalos del trébol sean redondos y suaves.
    mag = L * 1.5; 
    
    % Puntos de Posición (Nodos)
    C = [0,0];   E = [L,0];   W = [-L,0];  N = [0,L];   S = [0,-L];
    NE = [L,L];  NW = [-L,L]; SE = [L,-L]; SW = [-L,-L];
    
    % Vectores de Velocidad (Hacia dónde apunta el robot en cada nodo)
    vN = [0, mag];   % Apunta al Norte
    vS = [0, -mag];  % Apunta al Sur
    vE = [mag, 0];   % Apunta al Este
    vW = [-mag, 0];  % Apunta al Oeste

    % --- 2. ASIGNACIÓN POR TRAMO ---
    switch tramo
        % --- Lóbulo 1: Inferior Izquierdo ---
        case 0;  P0=C;  P1=S;   V0=vS; V1=vW;
        case 1;  P0=S;  P1=SW;  V0=vW; V1=vN;
        case 2;  P0=SW; P1=W;   V0=vN; V1=vE;
        case 3;  P0=W;  P1=C;   V0=vE; V1=vE;  % Llega a C mirando al Este
        
        % --- Lóbulo 2: Inferior Derecho ---
        case 4;  P0=C;  P1=E;   V0=vE; V1=vS;  % Sale de C mirando al Este (Suave)
        case 5;  P0=E;  P1=SE;  V0=vS; V1=vW;
        case 6;  P0=SE; P1=S;   V0=vW; V1=vN;
        case 7;  P0=S;  P1=C;   V0=vN; V1=vN;  % Llega a C mirando al Norte
        
        % --- Lóbulo 3: Superior Derecho ---
        case 8;  P0=C;  P1=N;   V0=vN; V1=vE;  % Sale de C mirando al Norte (Suave)
        case 9;  P0=N;  P1=NE;  V0=vE; V1=vS;
        case 10; P0=NE; P1=E;   V0=vS; V1=vW;
        case 11; P0=E;  P1=C;   V0=vW; V1=vW;  % Llega a C mirando al Oeste
        
        % --- Lóbulo 4: Superior Izquierdo ---
        case 12; P0=C;  P1=W;   V0=vW; V1=vN;  % Sale de C mirando al Oeste (Suave)
        case 13; P0=W;  P1=NW;  V0=vN; V1=vE;
        case 14; P0=NW; P1=N;   V0=vE; V1=vS;
        case 15; P0=N;  P1=C;   V0=vS; V1=vS;  % Llega a C mirando al Sur (Conecta con Tramo 0)
        
        otherwise; P0=C; P1=C; V0=[0,0]; V1=[0,0];
    end
end