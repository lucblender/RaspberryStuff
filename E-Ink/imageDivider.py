import numpy as np
from skimage import io
from sklearn.cluster import KMeans
from skimage.transform import rescale

# file paths
inputFile = "album.jpg"
outputRedFile = "albumOutRed.bmp"
outputBlackFile = "albumOutBlack.bmp"
inputFileResized = "inputFileResized.bmp"

#get input image
original = io.imread(inputFile) 

#get width and legngth
width= len(original)
length = len(original[0])
desiredSize = 350

#find the correct ratio to resize the picture to 300 pixels
if width > length:
    ratio = desiredSize / width
else:
    ratio = desiredSize / length
#save the resized picture
io.imsave(inputFileResized,rescale(original, ratio, multichannel=True, anti_aliasing=False))

#re-open the saved picture 
original = io.imread(inputFileResized) 

#define the number of colors for our k means clustering
n_colors = 3

# do the actual clusturing
arr = original.reshape((-1, 3))
kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(arr)
labels = kmeans.labels_
centers = kmeans.cluster_centers_
less_colors = centers[labels].reshape(original.shape).astype('uint8')

# get rgb value of 3 colors --> sadly its sorded so get also index to sort it after
unique, index = np.unique(less_colors, return_index=True)

unique = less_colors.flat[np.sort(index)]

# get every color individually
unique0 = unique[0:3]
unique1 = unique[3:6]
unique2 = unique[6:9]

#get the mean of every color
mean0 = unique0.mean()
mean1 = unique1.mean()
mean2 = unique2.mean()

white = None
red = None
black = None

# determine which color is red, black or white by its mean
if mean0 > mean1 and mean0 > mean2:
    white = unique0
    if mean1 > mean2:
        red = unique1
        black = unique2
    else:
        red = unique2
        black = mean1
elif mean1 > mean0 and mean1 > mean2:
    white = unique1
    if mean0 > mean2:
        red = unique0
        black = unique2
    else:
        red = unique2
        black = unique0
else:
    white = unique2
    if mean0 > mean1:
        red = unique0
        black = unique1
    else:
        red = unique1
        black = unique0
        
# get an array with boolean and True value for red or black
red_colors_picture = (less_colors == red)       
black_colors_picture = (less_colors == black)

# invert those boolean array
red_colors_picture = (red_colors_picture == False)
black_colors_picture = (black_colors_picture == False)

# Turn the array into uint8 array and multiply them by 255
#true, true ,true become 255 255 255 --> white
#false, false, false become 0 0 0 --> black
red_colors_picture = np.uint8(red_colors_picture.astype(int)*255)
black_colors_picture = np.uint8(black_colors_picture.astype(int)*255)
    
#save the picture 
io.imsave(outputRedFile,red_colors_picture)
io.imsave(outputBlackFile,black_colors_picture)