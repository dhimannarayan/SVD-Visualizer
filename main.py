from uuid import uuid4

import io
from fastapi import Response
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from PIL import UnidentifiedImageError
from fastapi.middleware.cors import CORSMiddleware

from svd_class import SVD_compressor


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Absolute-Error", "Relative-Error", "Info-Retained", 
                        "K-Value"],
)

compressors = {}

@app.get("/")
def root():
    return {"message": "SVD Visualizer is running"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        compressor = SVD_compressor(file.file)
        image_id = str(uuid4())
        compressors[image_id] = compressor

        print("Uploaded image ID:", image_id)
        print("Stored IDs:", list(compressors.keys()))

        return {
            "image_id": image_id,
            "filename": file.filename,
            "message": "Image uploaded successfully",
            "min_k": compressor.min_k,
            "max_k": compressor.max_k
        }
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid image."
        )
    finally:
        await file.close()

@app.get("/reconstructed/{image_id}")
def reconstruct(image_id: str, k:int = Query(..., ge=1)):
    if image_id not in compressors:
        raise HTTPException(status_code=404, detail="Image not found.")
    compressor = compressors[image_id]

    try:
        matrix = compressor.reconstruct(k)
    except ValueError as error:
        raise HTTPException(status_code=400, detail = str(error))

    abs_error = compressor.abs_reconstruction_error(matrix)
    rel_error = compressor.rel_reconstruction_error(matrix)
    info_ret =compressor.info_retained()

    #filename for output path
    #out_path = f"../reconstruction_{image_id}_{k}.png"



    #save to path
    #compressor.save_image(matrix, out_path)

    # Return the PNG file, with data in the response headers
    buffer = io.BytesIO()
    compressor.save_image(matrix, buffer)

    return Response(content=buffer.getvalue(), media_type="image/png",
                    headers={
                        "Absolute-Error": str(abs_error),
                        "Relative-Error": str(rel_error),
                        "Info-Retained": str(info_ret),
                        "K-Value": str(k)
                    })


