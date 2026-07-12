import os

import onnxruntime as ort
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import CrossEncoder

_MODEL = os.getenv("RERANKER_MODEL", "onnx-community/bge-reranker-v2-m3-ONNX")
_QFILE = os.getenv("RERANKER_ONNX_FILE", "onnx/model_quantized.onnx")
_THREADS = int(os.getenv("ORT_THREADS", str(os.cpu_count() or 4)))
_backend = "unknown"


def _log(msg: str) -> None:
    print(f"[reranker] {msg}", flush=True)


def _load():
    global _backend
    so = ort.SessionOptions()
    so.intra_op_num_threads = _THREADS
    so.inter_op_num_threads = 1
    _log(f"loading prebuilt quantized ONNX: {_MODEL} :: {_QFILE} (intra_op_threads={_THREADS})")
    model = CrossEncoder(
        _MODEL, backend="onnx", model_kwargs={"file_name": _QFILE, "session_options": so}
    )
    _backend = f"onnx-int8-prebuilt-{_THREADS}t"
    _log("reranker ready")
    return model


_model = _load()
app = FastAPI()


class RerankRequest(BaseModel):
    query: str
    texts: list[str]
    raw_scores: bool = False


@app.get("/health")
def health():
    return {"status": "ok", "backend": _backend}


@app.post("/rerank")
def rerank(req: RerankRequest):
    if not req.texts:
        return []
    scores = _model.predict([(req.query, t) for t in req.texts])
    ranked = [{"index": i, "score": float(s)} for i, s in enumerate(scores)]
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
