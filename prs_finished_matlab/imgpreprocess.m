function label=imgpreprocess(img, net)

img=imresize(img,[227,227]);
img=preprocess_input(img);

[label, con] = classify(net, img);