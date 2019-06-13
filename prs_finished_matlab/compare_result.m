clear;
rosshutdown;
setenv('ROS_IP', '10.109.16.183');%use ipconfig to find your laptop ip
setenv('ROS_MASTER_URI', 'http://10.109.99.41:11311');%find your beagle ip
rosinit();
classnames={'none', 'paper', 'rock', 'scissors'};
net = importKerasNetwork('rps.json', 'WeightFile', 'data_95.h5', 'OutputLayerType', 'classification', 'ClassNames',classnames)
camera = webcam(1);

while true   % whil loop, let the function contionuous
    t1=clock;
    disp('start ')
    %Generate a random number and send to ros  
    pub = rospublisher('/rand_no','std_msgs/Int32');
    msg = rosmessage(pub);
    robo  = randi([1,3]);
    msg.Data = robo;
    %disp(msg.Data);
    send(pub,msg);
    disp('randon number =')
    disp(robo)
    
    t0 = clock;
    while etime(clock, t0)<6
        picture = camera.snapshot;              % Take a picture [Image recognition]
        picture = flip(picture,2);               % Mirroring 
        label = imgpreprocess(picture,net);      % Classify the picture [Image recognition]
        image(picture); % Show the picture [Image recognition]
        title(char(label)); % Show the label [Image recognition]5
        drawnow; % updates figures  
    end
    disp(char(label));
    
    if robo==1
        disp('Rock');
    elseif robo==2
        disp('Paper');
    else
        disp('Scissors');
    end
    
    lab = char(label);
    if lab(end)=='k'
        human=1;
    elseif lab(end)=='r'
        human=2;
    elseif lab(end)=='s'
        human=3;
    else
        human=0;
    end
    %compare
    if human==1
        if robo==1
            result = 3;
            disp('Tie!');
        elseif robo==2
            result = 2; 
           disp( 'You lose!');
        else
            result =  1 ;
            disp('You win!');
        end
    elseif human==2
        if robo==1
            result = 1 ;
            disp('You win!');
        elseif robo==2
            result = 3;
            disp('Tie!');
        else
            result = 2;
            disp('You lose!');
        end
    elseif human==3
        if robo==1
            result = 2;
            disp('You lose!');
        elseif robo==2
            result = 1;
            disp('You win!');
        else
            result = 3;
            disp('Tie!');
        end
    else
        result = 4;
    end
    disp('\n The result is \n ');
    disp(result);
    pub = rospublisher('/final_result','std_msgs/Int32');
    msg = rosmessage(pub);
    msg.Data = result;
    %disp(msg.Data);
    send(pub,msg);
    if result==1
        resultfig = imread('win.jpg');
    elseif result==2
        resultfig = imread('lose.jpg');
    elseif result==3
        resultfig = imread('tie.jpg');
    else
        resultfig = imread('playwithme.jpg');
    end
    pause(2)
    figure(2);
    imshow(resultfig)
    h=figure(2);
    pause(4);
    close(h)
    disp('end')
    pause(2)
    t2=clock;
    etime(t2,t1)
    
end