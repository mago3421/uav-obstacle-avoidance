%% ASEN 6519-008
% Ramya Kanlapuli
% Final Project
% Change reward function to incorporate action

function [r] = ComputeReward(state,obst_loc,start_auto,stop_auto,decep_loc)
obst_flag=0;

x = state(1);
y = state(2);
if x==start_auto(1)&&y==start_auto(2)
    r=0;
elseif x==stop_auto(1) && y==stop_auto(1)
    r = 1;
elseif x==10 || y==10
    r = -0.1;
elseif x==decep_loc(1) && y==decep_loc(2)
    r = -0.9;
    
else 
    for i=1:numel(obst_loc)/2
     if obst_loc(i,1)==x&&obst_loc(i,2)==y
         obst_flag = 1;
     end
    end
    if obst_flag ==1
        r= -0.7;
    else
        r = 0.1;
    end
end


end