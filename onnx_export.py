# export.py
from optimum.exporters.onnx import main_export

main_export(
    model_name_or_path="nomic-ai/nomic-embed-text-v1",
    output="nomic_onnx/",
    task="feature-extraction",
    trust_remote_code=True,
)
