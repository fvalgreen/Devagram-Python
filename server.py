import uvicorn


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=5000, reload=True) # Definindo um servidor unicorn para rodar nosso
    # main.py