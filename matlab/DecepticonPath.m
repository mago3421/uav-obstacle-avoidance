%% ASEN 6519-001
% Decepticon path planning
% It follows a lawnmower pattern
%
%
% Inputs to this function are: 
%
% Outputs from this function are: 
%           - x and y coordinates


function [path] = DecepticonPath(ini_pos,goal_pos,obst,grid_x,grid_y,time)
% We assume we start from the top left corner and move to the bottom left
% corner
path = [];

%grid_x = 10;
%grid_y = 10;
%t = 0;
%ini_pos =  [0.5;9.5];
%goal_pos = [0.5;0.5];

curr_pos = ini_pos;
dir = 1; %1 for right facing and -1 for left facing
c = 1;
flag = 0;


while 1
    obstflag=0;
    for i =1:numel(obst)/2
    if curr_pos(1)==obst(i,1)&&curr_pos(2)==obst(i,2)
        obstflag = 1;
        if flag==1
            %curr_pos = [curr_pos(1)-1;curr_pos(2)]; 
            next_pos(:,1) = [curr_pos(1)-1;curr_pos(2)+1];
            next_pos(:,2) = [next_pos(1,1)+1;next_pos(2,1)];
            next_pos(:,3) = [next_pos(1,2)+1;next_pos(2,2)];
            next_pos(:,4) = [next_pos(1,3);next_pos(2,3)-1];
            curr_pos = next_pos(:,4);
        elseif flag==2
              %curr_pos = [curr_pos(1)+1;curr_pos(2)];
            next_pos(:,1) = [curr_pos(1)+1;curr_pos(2)+1];
            next_pos(:,2) = [next_pos(1,1)-1;next_pos(2,1)];
            next_pos(:,3) = [next_pos(1,2)-1;next_pos(2,2)];
            next_pos(:,4) = [next_pos(1,3);next_pos(2,3)-1];
            curr_pos = next_pos(:,4);
        elseif flag==3
              %curr_pos = [curr_pos(1); curr_pos(2)+1];
              %next_pos(:,1) = [curr_pos(1);curr_pos(2)+1];
              next_pos2(:,1) = [path(:,c-2)];
              next_pos2(:,2) = [next_pos2(1,1);next_pos2(2,1)-1];
              curr_pos = next_pos2(:,2);
        end
        
    end
    end
    
    if obstflag==0
        path = [path,curr_pos];c=c+1;
    else
        
        if flag==3
            path = [path,next_pos2];c=c+2;
        elseif flag==1||flag==2
            path = [path,next_pos]; c=c+4;
        end
            
    end
    
%     path = [path,curr_pos];
    if curr_pos(1) ==goal_pos(1) &&curr_pos(2)==goal_pos(2)
        break
    end
    
    if curr_pos(1)+1 <= grid_x && dir==1
        curr_pos = [curr_pos(1)+1;curr_pos(2)];
        flag=1;
        continue
    
    elseif curr_pos(1)-1 >=0 && dir== -1
        curr_pos = [curr_pos(1)-1;curr_pos(2)];
        flag=2;
        continue
    
    elseif curr_pos(2)-1 >=0
        curr_pos = [curr_pos(1);curr_pos(2)-1];
        dir = dir*-1;
        flag=3;
        continue
    end       
end

% For wrap around, if the path needs to be more than 1 orbit(?)
path_onerun = path; 
path_flip = fliplr(path_onerun);
time_onerun = size(path_onerun,2);

num = fix(time/time_onerun);

for i=2:num+1
    if rem(i,2)==0
        path = [path,path_flip];
        
    else
        path = [path,path];
    end
end

path = path(:,1:time);
path = path';
end