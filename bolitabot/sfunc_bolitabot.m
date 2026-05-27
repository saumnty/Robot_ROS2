function sfunc_bolitabot(block)
    setup(block);
end

function setup(block)
    block.NumInputPorts = 2;
    block.NumOutputPorts = 0;
    block.SetPreCompInpPortInfoToDynamic;
    block.InputPort(1).Dimensions = 1;
    block.InputPort(1).DataTypeId = 0;
    block.InputPort(2).Dimensions = 1;
    block.InputPort(2).DataTypeId = 0;
    block.SampleTimes = [0.1 0];
    block.RegBlockMethod('Outputs', @Outputs);
end

function Outputs(block)
    linear_x = block.InputPort(1).Data;
    angular_z = block.InputPort(2).Data;
    try
        t = tcpclient('127.0.0.1', 9090);
        cmd = struct('linear_x', double(linear_x), 'angular_z', double(angular_z));
        write(t, uint8(jsonencode(cmd)));
        pause(0.05);
        clear t;
    catch e
        disp(['Error: ' e.message]);
    end
end
