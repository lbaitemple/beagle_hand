function label=picpreprocess(pic, net)
pic=imread(pic);
pic=imresize(pic,[227,227]);
pic=preprocess_input(pic);

[label, con] = classify(net, pic)