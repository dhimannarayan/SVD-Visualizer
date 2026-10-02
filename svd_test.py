from svd_class import SVD_compressor
import time

start = time.time()
compressor = SVD_compressor("test.jpg")

print("SVD TIME: ", time.time() - start, "\n")

# Checking member variables
print("Image shape:", compressor.image.shape, "\n")
print("Minimum k:", compressor.min_k, "\n")
print("Maximum k:", compressor.max_k, "\n")
print("-------------------------------------------------------------\n")

start = time.time()
#testing reconstruct function
reconstruction = compressor.reconstruct(50)
print("RECONSTRUCTION TIME: ", time.time() - start, "\n")

print("Current k:", compressor.k, "\n")
print("-------------------------------------------------------------\n")

start = time.time()
print("Information retained:", compressor.info_retained(), "\n")
print("Absolute error:", 
      compressor.abs_reconstruction_error(reconstruction), "\n")
print("Relative error:", 
      compressor.rel_reconstruction_error(reconstruction), "\n")

print("INFO TIME: ", time.time() - start, "\n")
print("-------------------------------------------------------------\n")

start = time.time()
# Testing save function
compressor.save_image(reconstruction, "reconstructed.jpg")
print("SAVE TIME: ", time.time() - start, "\n")

print("-------------------------------------------------------------\n")

