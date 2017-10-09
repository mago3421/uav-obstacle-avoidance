%% Define policy pi_action

function action = pi_action(s)

x_coord = s(1);
y_coord = s(2);
% give a string 
% 'forward' 'left' 'right' 

a = randi(3);
if a ==1
    action = 'forward'
elseif a == 2
    action = 'left'
elseif a == 3
    action = 'right'
end   
%% The real thing, not a random policy



end