function sfunc_bolitabot(block)
    setup(block);
end

function setup(block)
    block.NumInputPorts = 2;
    block.NumOutputPorts = 3; % [x_real, y_real, theta_real]
    
    block.SetPreCompInpPortInfoToDynamic;
    
    % Entradas: v, w
    block.InputPort(1).Dimensions = 1;
    block.InputPort(1).DataTypeId = 0; 
    block.InputPort(2).Dimensions = 1;
    block.InputPort(2).DataTypeId = 0; 
    
    % Salidas: x, y, theta de Gazebo
    block.OutputPort(1).Dimensions = 1;
    block.OutputPort(1).DataTypeId = 0;
    block.OutputPort(2).Dimensions = 1;
    block.OutputPort(2).DataTypeId = 0;
    block.OutputPort(3).Dimensions = 1;
    block.OutputPort(3).DataTypeId = 0;
    
    block.SampleTimes = [0.1 0];
    block.RegBlockMethod('Outputs', @Outputs);
end

function Outputs(block)
    v = block.InputPort(1).Data;
    w = block.InputPort(2).Data;
    try
        % Conectamos con un Timeout corto para no trabar Simulink
        t = tcpclient('127.0.0.1', 9090, 'Timeout', 1);
        cmd = struct('linear_x', double(v), 'angular_z', double(w));
        write(t, uint8(jsonencode(cmd)));
        
        % Esperamos una fracción de segundo la respuesta
        pause(0.05);
        
        if t.NumBytesAvailable > 0
            data = read(t);
            estado = jsondecode(char(data));
            
            % Si la respuesta es correcta, sacamos los datos
            if isfield(estado, 'x')
                block.OutputPort(1).Data = estado.x;
                block.OutputPort(2).Data = estado.y;
                block.OutputPort(3).Data = estado.theta;
            end
        end
        clear t;
    catch e
        % Si algo falla, sacamos 0 para que la simulación no muera
        block.OutputPort(1).Data = 0.0;
        block.OutputPort(2).Data = 0.0;
        block.OutputPort(3).Data = 0.0;
    end
end