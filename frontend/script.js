console.log("SCRIPT STARTED");

window.addEventListener("beforeunload", function () {
    console.log("PAGE IS UNLOADING");
});
const imageInput = document.getElementById("image-input")
const uploadButton = document.getElementById("upload-button")
const uploadStatus = document.getElementById("upload-status")
const originalImage = document.getElementById("original-image");
const imageDimensions = document.getElementById("image-dimensions")

let currentImageId = null;

const rankSlider = document.getElementById("rank-slider");
const rankValue = document.getElementById("rank-value");
const reconstructedImage = document.getElementById("reconstructed-image");
const absoluteError = document.getElementById("absolute-error");
const relativeError = document.getElementById("relative-error");
const informationRetained = document.getElementById("information-retained");



/*  Upload Button Event Listener  */
uploadButton.addEventListener("click", async function(){
    console.log("UPLOAD BUTTON CLICKED");
    const file = imageInput.files[0]

    if(!file){
        uploadStatus.textContent = "Please select an image first."
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    uploadStatus.textContent = "Uploading Image...";

    try{
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        console.log("UPLOAD RESPONSE RECEIVED", data);

        if (!response.ok) {
                throw new Error(data.detail || "Upload failed.");
            }

        imageDimensions.textContent = `${data.height} × ${data.width} pixels`;
        originalImage.src = URL.createObjectURL(file);

        uploadStatus.textContent =
            `Uploaded successfully! Maximum rank: ${data.max_k}`;
        
        currentImageId = data.image_id
        console.log("Image ID:", data.image_id);
        console.log("Maximum rank:", data.max_k);

        // Data for the slider
        rankSlider.min = data.min_k;
        rankSlider.max = data.max_k;
        rankSlider.value = 1;
        rankSlider.disabled = false;
        rankValue.textContent = "1";

        // Display the first reconstruction
        updateReconstruction(1);

    } catch(error){
        uploadStatus.textContent = error.message;
    }
});

async function updateReconstruction(k){
    if(!currentImageId){
        return;
    }

    try{
        const response = await fetch(
            `http://127.0.0.1:8000/reconstructed/${currentImageId}?k=${k}`
        );

        if(!response.ok){
            const data = await response.json();
            throw new Error(data.detail || "Reconstruction failed");
        }

        const imageBlob = await response.blob();
        // for debugging:
        console.log("Reconstruction received");
        console.log("Image size:", imageBlob.size, "bytes");
        console.log("Image type:", imageBlob.type);


        reconstructedImage.src = URL.createObjectURL(imageBlob)

        reconstructedImage.onload = function () {
            console.log("Reconstructed image displayed successfully");
        };

        reconstructedImage.onerror = function () {
            console.log("Browser could not display reconstructed image");
        };

        absoluteError.textContent = response.headers.get("Absolute-Error");

        relativeError.textContent = response.headers.get("Relative-Error")

        informationRetained.textContent = 
                `${Number(response.headers.get("Info-Retained")).toFixed(2)}%`;
        
    } catch(error){
        uploadStatus.textContent = error.message;
    }
}

rankSlider.addEventListener("input", function(){
    const k = Number(rankSlider.value);

    rankValue.textContent = k;
    updateReconstruction(k);
});

