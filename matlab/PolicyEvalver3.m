%% ASEN 6519-001
% Final Project
% Attempt 3 at policy evaluation and iteration
% Ramya kanlapuli

function [Util_vec,new_action] = PolicyEvalver3(start_auto,stop_auto,start_decep,stop_decep,obst_loc,hor,old_action,decep_loc)

grid_x = 10; %number of horizontal and vertical cells
grid_y = 10;
n_state = grid_x * grid_y;

load('Trans_fxn.mat')

% Iterative policy evaluation
% its a 10 by 10 grid, 100 states
% Utility vector can be 100 times horizon : 100*n 
% n is the arbitrary horizon
n = hor;

% action(:,1) is ze set of actions for all states at time step 1
% n = 107; % Whatever you want it to be
Util_vec = zeros(n,n_state); % 100 columns 
gamma = 0.9;
% Initialize first row to zero % Util_vec(1,:) = zeros;

new_action = ones(n_state,1);

for t = 1:n
    reward = ones(n_state,3);
    % i = 1 left
    % i = 2 forward
    % i = 3 right
    
    for s = 1:n_state
    s_x = fix(s/10)+1;
    s_y = mod(s,10);
        if s_y==0
             s_x = s_x-1;
             s_y = grid_y;
        end
        s_old = [s_x-0.5;s_y-0.5];
      
    for j = 1:3
        if j==1
            s_new = [s_old(1);s_old(2)+1]; 
        elseif j==2
            s_new = [s_old(1)+1;s_old(2)];
        elseif j==3
            s_new = [s_old(1);s_old(2)-1];
        end
        
        obst_flag = 0;
        for k=1:numel(obst_loc)/2
            if obst_loc(k,1)==s_new(1)&&obst_loc(k,2)==s_new(2)
                obst_flag = 1;
            end
        end
        
        if obst_flag ==1
            reward(s,j)= -100;
        end
        
        if s_new(1)==stop_auto(1) && s_new(2)==stop_auto(2)
            reward(s,j) = 100;
        elseif s_new(1)==decep_loc(1) &&s_new(2)==decep_loc(2)
            reward(s,j) = -1000;
        end
        
        if s_new(1)>grid_x
            reward(s,j) = -10;
        elseif s_new(2)>grid_y
            reward(s,j) = -10;
        end
      
    end
        
        if t==1   
       
        Util_vec(t,s) = reward(s,old_action(s));
        [~,max_idx] = max(reward(s,:));
        new_action(s) = max_idx;
        
        else
            sum_tran_prob = 0;
            for i=1:3 %3 new states to be summed over %define em %4 states?
                if i==1 %left
                    s_new(1) = s_old(1);
                    s_new(2) = s_old(2)+1;
                elseif i==2 %forward
                    s_new(1) = s_old(1)+1;
                    s_new(2) = s_old(2);
                elseif i==3 %right
                    s_new(1) = s_old(1);
                    s_new(2) = s_old(2)-1;                     
                end
                
                if s_new(2)<0
                    s_new(2) = s_old(2);
                end 
                    
                if s_new(1)>grid_x
                    s_new(1) = s_old(1);
                
                elseif s_new(2)>grid_y
                    s_new(2) = s_old(2);
                     
                end
               count_snew = 10*floor(s_new(1)) + floor(s_new(2));
               
               if count_snew ==0
                   continue
               end
               
               dir = s_new-s_old;
               if dir(1)==0 && dir(2)==1
                   % right
                   d=1;
               elseif dir(1)==0 && dir(2)==-1
                   %left
                   d=3;
               elseif dir(1)==1 &&dir(2)==0
                   d=2;
               else
                   d=4; % Same position, trans prob = 1
               end
               
               if d==4
                   p = 1;
               else
                   p = Trans_fxn2(d,old_action(s));
               end
               
               sum_tran_prob = sum_tran_prob + ...
                    p*Util_vec(t-1,count_snew); % pick max util vector and get action out of that
               
            end
            
            Util_vec(t,s) = Util_vec(t,s) + ...
                reward(s,old_action(s)) + gamma*sum_tran_prob;
                  [~,max_idx] = max(reward(s,:));
                  new_action(s) = max_idx;
                 
        end
    end
end
%% plotting 
% It plots for every time step of the utility function (till the horizon)
% Comment it out when iterating for policy
% Takes time to plot :(

figure;
for i = 1:n
   
    u = Util_vec(i,:);
    u_pos_idx = find(u>0);
    u(u_pos_idx) = u(u_pos_idx)/max(u(u_pos_idx));
    u_neg_idx = find(u<0);
    u(u_neg_idx) = -u(u_neg_idx)/min(u(u_neg_idx));
    
  for s = 1:n_state
    s_x = fix(s/10)+1;
    s_y = mod(s,10);
    if s_y==0
         s_x = s_x-1;
         s_y = grid_y;
    end
    s_x = s_x - 1;
    s_y = s_y - 1;
  
   pos = [s_x,s_y,1,1];
   if u(s)<0
       rectangle('Position',pos,'FaceColor',[abs(u(s)) 0 0])
   else
       rectangle('Position',pos,'FaceColor',[0 u(s) 0])
   end
   
  end
  
xlabel('x position(units)')
ylabel('y position(units)')
title(['Utility for t=', num2str(i)])
pause(5)  
  
end

end