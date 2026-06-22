from pathlib import Path
import gc
import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer
)

from config import (
    MODELS_DIR
)


class ModelLoader:

    _tokenizer = None
    _model = None
    _current_model_name = None

    if torch.cuda.is_available():
        _device = "cuda"
        _runtime = "GPU (CUDA)"
    else:
        _device = "cpu"
        _runtime = "CPU"

    @classmethod
    def load_model(
        cls,
        model_name: str
    ):

        # Reuse already loaded model
        if (
            cls._tokenizer is not None
            and cls._model is not None
            and cls._current_model_name == model_name
        ):
            return (
                cls._tokenizer,
                cls._model
            )

        # Different model requested
        # Unload previous model first
        if (
            cls._current_model_name is not None
            and cls._current_model_name != model_name
        ):
            print(
                f"[ModelLoader] Switching model: "
                f"{cls._current_model_name} -> {model_name}"
            )

            cls.unload_model()

        model_path = (
            MODELS_DIR /
            model_name.split("/")[-1]
        )

        print(
            f"[ModelLoader] Loading: "
            f"{model_path}"
        )

        cls._tokenizer = (
            AutoTokenizer.from_pretrained(
                model_path,
                local_files_only=True,
                trust_remote_code=True
            )
        )

        dtype = (
            torch.float16
            if cls._device == "cuda"
            else torch.float32
        )

        cls._model = (
            AutoModelForCausalLM.from_pretrained(
                model_path,
                local_files_only=True,
                trust_remote_code=True,
                torch_dtype=dtype
            )
        )

        cls._model.to(
            cls._device
        )

        cls._model.eval()

        cls._current_model_name = model_name

        return (
            cls._tokenizer,
            cls._model
        )

    @classmethod
    def is_loaded(cls):
        return (
            cls._tokenizer is not None
            and cls._model is not None
        )

    @classmethod
    def get_device(cls):
        return cls._device

    @classmethod
    def get_runtime(cls):
        return cls._runtime

    @classmethod
    def get_model_name(cls):

        if cls._current_model_name is None:
            return "Not Loaded"

        return (
            cls._current_model_name
            .split("/")[-1]
            .replace("-Instruct", "")
        )

    @classmethod
    def unload_model(cls):

        print(
            f"[ModelLoader] Unloading: "
            f"{cls._current_model_name}"
        )

        if cls._model is not None:
            del cls._model

        if cls._tokenizer is not None:
            del cls._tokenizer

        cls._model = None
        cls._tokenizer = None
        cls._current_model_name = None

        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

            try:
                torch.cuda.ipc_collect()
            except Exception:
                pass