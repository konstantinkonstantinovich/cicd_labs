from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/healthcheck")
async def healthcheck():
    return {'status':'ok'}
