from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(content))

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))

    elif file.filename.endswith(".json"):
        df = pd.read_json(io.BytesIO(content))

    else:
        return {"error": "Unsupported file"}

    profile = []

    for col in df.columns:
        profile.append({
            "name": col,
            "dtype": str(df[col].dtype),
            "missing": int(df[col].isnull().sum()),
            "unique": int(df[col].nunique())
        })

    result = {
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "preview": df.to_dict(orient="records"),
        "profile": profile
    }

    return result