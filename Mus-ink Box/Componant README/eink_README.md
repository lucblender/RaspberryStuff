# E-ink

Model tested from waveshare:
- 2.7inch_e-paper_b 
- 5.83inch_e-paper_b

official git:
https://github.com/waveshare/e-Paper

## Requirement

For driving the e-Paper Screen
```
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

For the image processing part
```
sudo pip3 install numpy
sudo pip3 install scipy
sudo pip3 install scikit-image
sudo pip3 install cython
sudo pip3 install scikit-learn
```

## Structure of the code

The code imageDivider.py is used to divide an image in 3 channels to get compatible image for the 3 colours e-Paper (Red Black White). It will resize the image as desired and save them as black and red bitmap for the red and black channels.

MusicDisplay.py wich display data about a track played by its name, artist, album, lenght and album picture (generated with imageDivider) as parameters. The musicDisplay need the 'noir' font, not provided in this repo. The function musicDisplay is for the 5.83 inch e-Paper and the musicDisplaySmall is for the 2.7 inch e-Paper