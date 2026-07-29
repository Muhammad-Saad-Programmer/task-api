from fastapi import FastAPI
 
app = FastAPI()

@app.get("/")
async def root():
    return { 
        "name":  "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
        }
@app.get("/health")
async def health():
    return {
        "status": "ok"
    }