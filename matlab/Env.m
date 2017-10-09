%% ASEN 6519-001
% Ramya Kanlapuli
% Final Project

% Create environment for autobot obstacle avoidance

grid_x = 10; %number of horizontal and vertical cells
grid_y = 10;
[X,Y] = meshgrid(0:1:grid_x,0:1:grid_y);


% specify x,y static obstacle locations
% The 0.5s are so the obstacles are inside the cells 
obst_loc = [1.5,3.5;
        6.5,8.5;
        7.5,1.5;
        4.5,6.5];
% Specify obstacle locations for plotting
% I plot obstacles using the rectangle function, so that needs me to
% specify the lower left corner of the rectangle

obst_plot = [1,3;
        6,8;
        7,1;
        4,6];

    
    
 start_auto = [0.5;1.5]; % so it starts in cell 1,1 %Similar reasoning for the 0.5s
 start_decep = [0.5;9.5];
 stop_auto = [9.5;9.5];
 stop_decep = [0.5;0.5];

 
figure;
% To plot the grid
plot(X,Y,'color',[0.5 0.5 0.5]);hold on; 
plot(Y,X,'color',[0.5 0.5 0.5]);
plot(stop_auto(1),stop_auto(2),'rx','LineWidth',2.5,'MarkerSize',25)
plot(start_auto(1),start_auto(2),'rx','LineWidth',2.5,'MarkerSize',25)
plot(stop_decep(1),stop_decep(2),'kx','LineWidth',2.5,'MarkerSize',25)
plot(start_decep(1),start_decep(2),'kx','LineWidth',2.5,'MarkerSize',25)
hold on 
 for i=1:numel(obst_plot)/2
     pos = [obst_plot(i,1),obst_plot(i,2),1,1];
     rectangle('Position',pos,'FaceColor',[.5 .5 .5])
 end
%plot(obst(:,1),obst(:,2),'bs','LineWidth',2.5,'MarkerSize',30)

%% 
% This section is to plot the decepticon path.
% The decepticon moves in a lawnmower pattern, avoiding obstacles that it
% might face.

time = 107; % The decepticon wraps around so you can do how many ever time steps
[path] = DecepticonPath(start_decep,stop_decep,obst_loc,grid_x,grid_y,time);
% Tolerance for each path point = +/-0.5,+/-0.5

%figure;


hold on
plot(path(:,1),path(:,2),'b')
path = path';
%quiver(x,y,u,v)
%figure;
for i=1:(numel(path)/2-1)
    
    temp = path(:,i+1)-path(:,i);
    hold on;
    quiver(path(1,i),path(2,i),temp(1),temp(2))
end


%% Policy iteration again
% Using policyevalver3 now
time = 107;
n_state = grid_x*grid_y;
pi_action = zeros(n_state,time);

%initialize random pi action
for a = 1:n_state
    pi_action(a,1) = randi(3);
end
old_action = pi_action(:,1);

count = 1;

time= 107;

[decep_path] = DecepticonPath(start_decep,stop_decep,obst_loc,grid_x,grid_y,time);
decep_path = decep_path';


while 1
    decep_loc = decep_path(:,count);


[Util_vec,new_action] = PolicyEvalver3(start_auto,stop_auto,start_decep,stop_decep,obst_loc,time,old_action,decep_loc);

if count>77 %Change count based onwhat pos wrt the time step you want the decepticon in
    break;
else
    old_action = new_action;
end

count = count+1;
end

figure;
for s = 1:n_state
     s_x = fix(s/10)+1;
     s_y = mod(s,10);
        if s_y==0
             s_x = s_x-1;
             s_y = grid_y;
        end
        s_old = [s_x-0.5;s_y-0.5];

if new_action(s)==1
    u=0;v=1;
elseif new_action(s)==2
    u=1;v=0;
elseif new_action(s) ==3
    u=0;v=-1;
end

hold on
obst_flag = 0;
        for k=1:numel(obst_loc)/2
            if obst_loc(k,1)==s_old(1)&&obst_loc(k,2)==s_old(2)
                obst_flag = 1;
            end
        end

     if s_old(1)==decep_loc(1) && s_old(2)==decep_loc(2)
        u=0;v=0; 
     elseif obst_flag==1
        u=0;v=0;
     end
     
  
     quiver(s_old(1),s_old(2),u,v,'linewidth',2,'MaxHeadSize',0.9,'Color','b')
     
end

hold on

plot(X,Y,'color',[0.5 0.5 0.5]);hold on; 
plot(Y,X,'color',[0.5 0.5 0.5]);
plot(stop_auto(1),stop_auto(2),'kx','LineWidth',2.5,'MarkerSize',25)
plot(start_auto(1),start_auto(2),'kx','LineWidth',2.5,'MarkerSize',25)
plot(decep_loc(1),decep_loc(2),'rx','LineWidth',2.5,'MarkerSize',25)

hold on 

for i=1:numel(obst_plot)/2
     pos = [obst_plot(i,1),obst_plot(i,2),1,1];
     rectangle('Position',pos,'FaceColor',[.5 .5 .5])
end


xlabel('x position(units)')
ylabel('y position(units)')
title(['Policy for t=', num2str(count)])
