function preprocessed_image = preprocess_input(image)
%preprocess_input Preprocess an image for tensorfire keras

[height, width] = size(image);
dataProcessedTensor = ones(size(image)) .* (width*height*3); %create processed tensor

blue = image(:,:,3) - 103.939; % alter each color 
%we change the data from 102.939 to 103.939
green = image(:,:,2) - 116.779;
red = image(:,:,1) - 123.68;

dataProcessedTensor(:, :, 3) = red; % flip the color axis
dataProcessedTensor(:, :, 1) = blue;
dataProcessedTensor(:, :, 2) = green;
%we change the order 
preprocessed_image = dataProcessedTensor; % return the processed img

end

