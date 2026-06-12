from pathlib import Path
from huggingface_hub import snapshot_download

from config import (
    MODELS_DIR,
    CODE_MODEL_NAME,
    REVIEW_MODEL_NAME
)


class ModelDownloader:
    @staticmethod
    def download():
        MODELS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

    for model_name in [
        CODE_MODEL_NAME,
        REVIEW_MODEL_NAME
    ]:

        local_path = (
            MODELS_DIR /
            model_name.split("/")[-1]
        )

        if local_path.exists():
            print(
                f"{model_name} already exists."
            )
            continue

        print(
            f"Downloading {model_name}..."
        )

        snapshot_download(
            repo_id=model_name,
            local_dir=local_path,
            local_dir_use_symlinks=False
        )
        print(
            f"{model_name} download complete."
        )

if __name__ == "__main__":
    ModelDownloader.download()