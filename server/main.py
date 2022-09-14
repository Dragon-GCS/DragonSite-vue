import uvicorn

if __name__ == '__main__':
    uvicorn.run(app="server:app", port=8080, reload=True)
