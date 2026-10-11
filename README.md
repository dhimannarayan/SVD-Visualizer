An interactive web app that demonstrates image compression using Singular Value Decomposition (SVD). 
Upload an image, drag the rank slider, and watch the reconstruction sharpen as more singular values are kept.

Features:
  1. Upload any image (converted to grayscale)
  2. Adjust the rank k with a slider and see the rank-k reconstruction update live
  3. View reconstruction metrics for each rank:
  4. Absolute error: Frobenius norm of the difference between the original and the reconstruction
  5. Relative error: absolute error divided by the norm of the original image
  6. Information retained: percentage of the total energy (sum of squared singular values) kept by the top k values

A grayscale image is a matrix of pixel values. SVD factors it into three matrices:
--- A = U · S · Vt ---
S holds the singular values, sorted from largest to smallest. Keeping only the top k of them gives the best possible rank-k approximation of the image. Small k gives a blurry image, large k gives a sharp one, and at the maximum k you get the original back.

Storing a rank-k approximation takes about k × (height + width) numbers instead of height × width, which is where the compression comes from.

Getting started:
  1. Clone the repo and install the dependencies:
       pip install -r requirements.txt
  2. Start the backend (runs on port 8000):
       uvicorn main:app --reload
  3. Serve the frontend on port 5500. The easiest way is the Live Server extension in VS Code: right-click index.html and choose "Open with Live Server".
  4. Pick an image, click Upload, and move the slider.
