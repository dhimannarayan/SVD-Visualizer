import numpy as np
from PIL import Image
import fastapi

#loads image from file path.
def load_image(file):
    image = Image.open(file)
    return np.array(image)


#Computes the svd of the image
def compute_svd(image):
    U, S, Vt = np.linalg.svd(image, full_matrices=False)
    return U, S, Vt

#Makes the rank-k approximation matrix
def reconstruct(U, S, Vt, k):
   U_k = U[:, :k]
   Vt_k = Vt[:k, :]
   S_k = np.diag(S[:k])
   result = U_k.dot(S_k).dot(Vt_k)
   return result

#saves the rank k approximation matrix as an image file to path.
def save_image(svd, path):
    svd = np.clip(svd, 0, 255).astype(np.uint8)
    image = Image.fromarray(svd)
    image.save(path)

#Error in reconstruction.
def reconstruction_error(original, matrix):

#
def info_retained(original, matrix):
