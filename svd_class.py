import numpy as np
from PIL import Image

class SVD_compressor:

    #loads image from file path.
    def load_image(self, file):
        image = Image.open(file).convert("L")
        return np.array(image)


    #Computes the svd of the image
    def compute_svd(self, image):
        U, S, Vt = np.linalg.svd(image, full_matrices=False)
        return U, S, Vt

    #Initializer of svd compressor.
    def __init__(self, file):
            self.image = self.load_image(file)
            self.U, self.S, self.Vt = self.compute_svd(self.image)
            self.k = 1
            self.min_k = 1
            self.max_k = min(self.image.shape)

    #Makes the rank-k approximation matrix
    def reconstruct(self,  k):
        if( (k < self.min_k) or (k > self.max_k)):
             raise ValueError("k must be between 1 and the min of dimensions.")

        U_k = self.U[:, :k]
        Vt_k = self.Vt[:k, :]
        S_k = np.diag(self.S[:k])
        self.k = k
        result = U_k.dot(S_k).dot(Vt_k)
        return result

    #saves the rank k approximation matrix as an image file to path.
    def save_image(self, svd, path):
        print("Saving image...")
        svd = np.clip(svd, 0, 255).astype(np.uint8)
        image = Image.fromarray(svd)
        image.save(path)
        print("saved image to: ", path)

    #Absolute Error in rank-k reconstruction.
    def abs_reconstruction_error(self, matrix):
        difference = self.image - matrix
        error = np.linalg.norm(difference, "fro")
        return error

    #Relative Error in rank-k reconstruction.
    def rel_reconstruction_error(self, matrix):
        difference = self.image - matrix
        error = np.linalg.norm(difference, "fro")
        norm_original = np.linalg.norm(self.image)
        return error/norm_original
    
    # Percentage of total information/ energy retained in the aproximation.
    def info_retained(self):
        total = np.sum(self.S**2)
        retained = np.sum(self.S[:self.k]**2)
        return 100 * retained/total
    