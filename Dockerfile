FROM proycon/python-frog

WORKDIR /app/

RUN pip install tqdm

ENTRYPOINT [ "python3", "/app/Frog.py" ]