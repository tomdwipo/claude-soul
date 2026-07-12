FROM python:3.12-slim
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch
RUN pip install --no-cache-dir "sentence-transformers>=5.0" "optimum[onnxruntime]>=1.20" onnx "fastapi>=0.115" "uvicorn[standard]>=0.30"
COPY server.py /server.py
RUN useradd -m app && mkdir -p /home/app/.cache/huggingface && chown -R app /home/app
ENV HF_HOME=/home/app/.cache/huggingface
USER app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
