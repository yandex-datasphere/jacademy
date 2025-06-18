import cv2
import dlib
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
import os

print("Библиотека проектории")

def sample_file(fn):
    return list(glob(fn))[0]

def sample_files(fn,n=5):
    return list(glob(fn))[:n]


def load_image(fn):
  img = cv2.imread(fn)
  return cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

def display_images(l, titles=None, fontsize=12):
    """
    Display a list of images in a single row.

    Parameters:
    l (list): A list of images to be displayed.
    titles (list, optional): A list of titles corresponding to each image. Defaults to None.
    fontsize (int, optional): The font size for the titles. Defaults to 12.

    Returns:
    None
    """
    if not isinstance(l, list):
        l = [l]
    if titles is not None and not isinstance(titles, list):
       titles = [titles]
    n = len(l)
    if n>1:
        fig, ax = plt.subplots(1, n)
        for i, im in enumerate(l):
            ax[i].imshow(im)
            ax[i].axis('off')
            if titles is not None:
                ax[i].set_title(titles[i], fontsize=fontsize)
        fig.set_size_inches(fig.get_size_inches() * n)
        plt.tight_layout()
    else:
        plt.imshow(l[0])
        plt.axis('off')
    plt.show()

if not os.path.exists("shape_predictor_68_face_landmarks.dat"):
    print("Загружаю распознаватель опорных точек...",end='') 
    os.system("wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2")
    os.system("7za x shape_predictor_68_face_landmarks.dat.bz2")
    print("Готово!")

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def detect_faces(img):
    return detector(img)

def detect_keypoints(img,face):
    return predictor(img,face)

def plot_face(img,rects,dots=None):
  i = img.copy()
  for r in rects:
    cv2.rectangle(i,(r.left(),r.top()),(r.right(),r.bottom()), (255,255,0), 3)
  if dots:
    for t in range(68):
        cv2.circle(i,(dots.part(t).x,dots.part(t).y),3,(255,255,0),2)
  plt.imshow(i)
  plt.axis('off')
  plt.show()

def transform_image(img,lmarks,size,target_triangle):
    target_triangle = np.float32(target_triangle)
    lefteye = ((lmarks.part(37).x+lmarks.part(40).x)/2,(lmarks.part(37).y+lmarks.part(40).y)/2)
    riteeye = ((lmarks.part(43).x+lmarks.part(46).x)/2,(lmarks.part(43).y+lmarks.part(46).y)/2)
    mouth = (lmarks.part(67).x,lmarks.part(67).y)
    tr = cv2.getAffineTransform(np.float32([lefteye,riteeye,mouth]), target_triangle)                               
    return cv2.warpAffine(img,tr,(size,size))

def merge(images):
    return np.array(images).mean(axis=0).astype(np.uint8)

def save_image(img,fname):
    cv2.imwrite(fname,img)