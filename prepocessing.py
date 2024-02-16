import cv2
import numpy as np
from PIL import Image


def bfs(visited, queue, array, node):
    # I make BFS itterative instead of recursive
    def getNeighboor(array, node):
        neighboors = []
        if node[0]+1<array.shape[0]:
            if array[node[0]+1,node[1]] == 0:
                neighboors.append((node[0]+1,node[1]))
        if node[0]-1>0:
            if array[node[0]-1,node[1]] == 0:
                neighboors.append((node[0]-1,node[1]))
        if node[1]+1<array.shape[1]:
            if array[node[0],node[1]+1] == 0:
                neighboors.append((node[0],node[1]+1))
        if node[1]-1>0:
            if array[node[0],node[1]-1] == 0:
                neighboors.append((node[0],node[1]-1))
        return neighboors

    queue.append(node)
    visited.add(node)

    while queue:
        current_node = queue.pop(0)
        for neighboor in getNeighboor(array, current_node):
            if neighboor not in visited:
    #            print(neighboor)
                visited.add(neighboor)
                queue.append(neighboor)

def removeIsland(img_arr, threshold):
    # !important: the black pixel is 0 and white pixel is 1
    while 0 in img_arr:
        x,y = np.where(img_arr == 0)
        point = (x[0],y[0])
        visited = set()
        queue = []
        bfs(visited, queue, img_arr, point)
        
        if len(visited) <= threshold:
            for i in visited:
                img_arr[i[0],i[1]] = 1
        else:
            # if the cluster is larger than threshold (i.e is the text), 
            # we convert it to a temporary value of 2 to mark that we 
            # have visited it. 
            for i in visited:
                img_arr[i[0],i[1]] = 2
                
    img_arr = np.where(img_arr==2, 0, img_arr)
    return img_arr

def preprocess_image(image_name):

    img  = cv2.imread(image_name)
    # Convert to grayscale
    c_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Median filter
    kernel = np.ones((3,3),np.uint8)
    out = cv2.medianBlur(c_gray,1)
    # Image thresholding 
    a = np.where(out>30, 1, out)
    out = np.where(a!=1, 0, a)
    # Islands removing with threshold = 30
    out = removeIsland(out, 50)
    # Median filter
    out = cv2.medianBlur(out,3)
    # Convert to Image type and pass it to tesseract
    im = Image.fromarray(out*255)

    new_name = "preprocessed_"+image_name
    #save im
    im.save(new_name)
    return new_name

