import uvicorn
import os

os.environ["APPKEY"] = "1234567890"

if __name__ == '__main__':
    uvicorn.run(app="server:app", port=8080, reload=True)
