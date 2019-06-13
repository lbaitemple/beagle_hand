%@Author:Cheng cheng
% @Date:   2018-07-27
% @Last Modified time: 2018-07-07
%This function is used to sent image recogniton's result to ROS.
%You should have a net that can recognize image.
%find information about ros action please search the following website
%https://www.mathworks.com/help/robotics/ref/robotics.simpleactionclient.html
function c_test()
load('nnet') % load a trained  network [Image recognition]   
clear;
rosshutdown;
setenv('ROS_IP', '10.109.107.205');%use ipconfig to find your laptop ip
setenv('ROS_MASTER_URI', 'http://10.109.99.41:11311');%find your beagle ip
rosinit();

%rosinit('10.109.99.41')%  [ROS action]
[actClient,goalMsg] = rosactionclient('/fibonacci'); % [ROS action]
waitForServer(actClient); % [ROS action]
%camera = webcam(1);%test 
t = clock;
a = 4 ;% Assign 'a' to a  inital value, preventing data overflow.
    while true   % whil loop, let the function contionuous
        picture = camera.snapshot;              % Take a picture [Image recognition]    
        picture = imresize(picture,[227,227]);  % Resize the picture [Image recognition] 
        label = classify(nnet, picture);        % Classify the picture [Image recognition] 
        image(picture);     % Show the picture [Image recognition] 
        title(char(label)); % Show the label [Image recognition] 
        drawnow; % updates figures  
        if etime(clock,t)>= 5 % [matlab delay function]
            t = clock;% [matlab delay function]
            %get the recognizing result and converted to number that can be
            %sent to ros
           if label == 'button'
                a = 0;
           elseif label == 'bottle'
                a = 1;
           elseif label == 'phone'
               a = 2;
           end
           a % display a in matlab command window
           goalMsg.Order = a; % [ROS action]
           sendGoal(actClient,goalMsg)% [ROS action]
        end 
    end
end