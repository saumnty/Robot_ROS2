function [x_r, y_r, theta_r] = leer_odom()
    persistent ultimo_x ultimo_y ultimo_theta;
    if isempty(ultimo_x)
        ultimo_x=0.0; ultimo_y=0.0; ultimo_theta=0.0;
    end
    try
        raw = fileread('/home/saumnty/mis_robots/bolitabot/odom_data.json');
        odom = jsondecode(raw);
        ultimo_x     = double(odom.x);
        ultimo_y     = double(odom.y);
        ultimo_theta = double(odom.theta);
    catch
    end
    x_r=ultimo_x; y_r=ultimo_y; theta_r=ultimo_theta;
end
