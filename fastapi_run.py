import uvicorn
from fastapi_deid import app
import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 10213
    uvicorn.run(app, host="0.0.0.0", port=port)