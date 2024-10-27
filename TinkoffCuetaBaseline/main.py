import logging

import uvicorn
from fastapi import FastAPI

from src.routes import api_routers

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(api_routers)


@app.on_event("startup")
async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s',
    )

    logger.info('Starting api')


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
