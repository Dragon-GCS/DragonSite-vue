import argparse

import uvicorn

from server import CONF

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bind", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000, type=int)
    args = parser.parse_args()
    uvicorn.run(app="server:app", host=args.bind, port=args.port, reload=CONF.DEBUG)
