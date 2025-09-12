# -*- coding: utf-8 -*-
"""
Created on Thu Sep 11 17:37:29 2025

@author: amine
"""

import logging
from pathlib import Path
import sys
from typing import List

#%% Logging

LOGFILE = True

if LOGFILE:
    LOGFILE = Path(__file__).resolve().parent.parents[1] / Path(*["output"])
    LOGFILE.mkdir(parents=True, exist_ok=True)
    LOGFILE /= Path(*["output.log"])
    
    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOGFILE, mode="w", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),  # console
        ]
    )
    
def disp(text, logged: bool=LOGFILE):
    if logged:
        logging.info(text)
    else:
        print(text)
        
def close_loggers():
    for handler in logging.root.handlers[:]:
        handler.close()
        logging.root.removeHandler(handler)

#%% Tensorboard

def project_dataframe_in_tensorboard(
    df: object,
    embedding_col: str,
    logdir: Path | list,
    metadata_cols: List[str] =None
):
    """
    Export a Pandas DataFrame to TensorBoard's Embedding Projector.

    Parameters
    ----------
    df : pandas.DataFrame
        Your table. One column must contain embedding vectors (list/np.array).
    embedding_col : str
        Name of the column with embeddings (each cell: list/array of floats).
    logdir : Path or str
        Directory to write TensorBoard files into (will be created if missing).
    metadata_cols : list[str] | None
        Which columns to include as metadata. Defaults to ALL columns except `embedding_col`.

    Output
    ------
    Writes:
      - a TensorFlow checkpoint containing the embedding tensor
      - a metadata.tsv with the other columns (header included)
      - a projector_config.pbtxt so TensorBoard can load the projection

    Usage
    -----
    >>> project_dataframe_in_tensorboard(df, "embedding", "./tb_logs")
    # then launch:
    # tensorboard --logdir ./tb_logs

    Requirements
    ------------
    pip install pandas numpy tensorflow>=2.0
    """
    import numpy as np
    import tensorflow as tf
    from tensorboard.plugins import projector

    # --- validate inputs ---
    if embedding_col not in df.columns:
        raise ValueError(f"`{embedding_col}` not in DataFrame columns.")

    # pick metadata columns
    if metadata_cols is None:
        metadata_cols = [c for c in df.columns if c != embedding_col]
    else:
        for c in metadata_cols:
            if c not in df.columns:
                raise ValueError(f"metadata column `{c}` not found in DataFrame.")

    # --- build embeddings matrix (N, D) ---
    emb_series = df[embedding_col].to_numpy()
    # Ensure every row is an array-like numeric sequence
    try:
        embs = np.vstack([np.asarray(x, dtype=np.float32).ravel() for x in emb_series])
    except Exception as e:
        raise ValueError(
            "Failed to stack embeddings. Ensure each cell in "
            f"`{embedding_col}` is a same-length list/array of numbers."
        ) from e

    if embs.ndim != 2:
        raise ValueError("Embeddings must form a 2D array of shape (N, D).")

    # --- write metadata.tsv ---
    def _clean_cell(x):
        s = str(x)
        s = s.replace("\t", " ").replace("\n", " ").replace("\r", " ")
        # keep it small but informative
        return s

    meta_matrix = [[_clean_cell(val) for val in df[metadata_cols].iloc[i]] for i in range(len(df))]
    header = "\t".join(metadata_cols)
    meta_lines = [header] + ["\t".join(row) for row in meta_matrix]


    if isinstance(logdir, list):
        logdir = Path(*logdir)
    logdir /= Path(*["TensorBoard"])
    logdir.mkdir(parents=True, exist_ok=True)
    metadata_path = logdir / Path(*["metadata.tsv"])
    with open(metadata_path, "w", encoding="utf-8") as f:
        f.write("\n".join(meta_lines))

    # --- create TensorFlow checkpoint + projector config ---
    # Uses TF2 with v1 compatibility utilities (this is the simplest stable path)

    tf.compat.v1.reset_default_graph()
    tf.compat.v1.disable_eager_execution()  # projector expects a graph + checkpoint

    with tf.compat.v1.Graph().as_default():
        embedding_var = tf.compat.v1.get_variable(
            name="embeddings",
            shape=embs.shape,
            dtype=tf.float32,
            initializer=tf.compat.v1.constant_initializer(embs),
            trainable=False,
        )

        # Saver to write a checkpoint containing only the embedding variable
        saver = tf.compat.v1.train.Saver([embedding_var])

        with tf.compat.v1.Session() as sess:
            sess.run(tf.compat.v1.global_variables_initializer())

            # Save checkpoint
            ckpt_prefix = str(logdir / Path(*["model.ckpt"]))
            saver.save(sess, ckpt_prefix)

            # Projector config
            config = projector.ProjectorConfig()
            emb_conf = config.embeddings.add()
            emb_conf.tensor_name = embedding_var.name
            # Use relative path inside the run dir
            emb_conf.metadata_path = Path(metadata_path).name

            projector.visualize_embeddings(
                tf.compat.v1.summary.FileWriter(logdir), config
            )

    disp(f'tensorboard --logdir "{logdir}"')

        
#%% Pydantic

def print_schema_tree(obj):
    """
    Print a full schema tree (including container layers) for a Pydantic model
    class or instance. Works with Pydantic v1 and v2. Handles forward refs,
    deep nesting (List/Dict/Tuple/Union/Optional), and recursive models.
    """
    
    # ---- local imports so this remains a single top-level function ----
    from typing import Any, get_args, get_origin, Union, Optional, get_type_hints
    import sys, types
    try:
        from pydantic import BaseModel
    except Exception as e:
        raise RuntimeError("pydantic is required") from e

    # ---------------- helpers (nested) ----------------
    def _is_model(t: Any) -> bool:
        return isinstance(t, type) and issubclass(t, BaseModel)

    def _pretty_type(t: Any) -> str:
        if _is_model(t):
            return t.__name__
        origin = get_origin(t)
        if origin is None:
            return getattr(t, "__name__", repr(t))
        origin_name = getattr(origin, "__name__", str(origin).replace("typing.", ""))
        # Optional[T] prettifier
        if origin is Union:
            args = get_args(t)
            non_none = [a for a in args if a is not type(None)]
            if len(args) == 2 and len(non_none) == 1:
                return f"Optional[{_pretty_type(non_none[0])}]"
        return f"{origin_name}[{', '.join(_pretty_type(a) for a in get_args(t))}]"

    def _node_label(typ: Any, as_field_name: Optional[str]) -> str:
        prefix = f"{as_field_name}: " if as_field_name is not None else ""
        if _is_model(typ):
            return f"{prefix}{typ.__name__}"
        origin = get_origin(typ)
        if origin is None:
            return f"{prefix}{getattr(typ, '__name__', repr(typ))}"
        origin_name = getattr(origin, "__name__", str(origin).replace("typing.", ""))
        # Optional[T]
        if origin is Union:
            args = get_args(typ)
            non_none = [a for a in args if a is not type(None)]
            if len(args) == 2 and len(non_none) == 1:
                return f"{prefix}Optional[{_pretty_type(non_none[0])}]"
        return f"{prefix}{origin_name}[{', '.join(_pretty_type(a) for a in get_args(typ))}]"

    def _resolve_type(t: Any, owner: Optional[type]) -> Any:
        """
        Resolve ForwardRefs / string annotations using module globals of the owner model
        (or the type's module if owner is None). Falls back gracefully.
        """
        try:
            module = sys.modules[owner.__module__] if owner else sys.modules.get(getattr(t, "__module__", ""), None)
            globalns = module.__dict__ if isinstance(module, types.ModuleType) else {}
            hints = get_type_hints(dict(__ann__={"_x": t}), globalns=globalns, include_extras=True)
            return hints["_x"]
        except Exception:
            return t

    def _iter_fields(model_cls: type[BaseModel]):
        """
        Yield (name, type, required) across Pydantic v1 & v2.
        """
        fields = getattr(model_cls, "model_fields", None)  # v2
        if fields is not None:
            for name, field in fields.items():
                yield name, getattr(field, "annotation", Any), getattr(field, "is_required", False)
            return
        v1_fields = getattr(model_cls, "__fields__", None)  # v1
        if v1_fields is not None:
            for name, field in v1_fields.items():
                yield name, getattr(field, "outer_type_", Any), getattr(field, "required", False)
            return
        # Fallback (rare)
        hints = get_type_hints(model_cls, include_extras=True)
        for name, typ in hints.items():
            yield name, typ, True

    def _print_type(typ: Any, prefix: str, is_last: bool, seen_models: set[int], as_field_name: Optional[str]) -> None:
        branch = "└─ " if is_last else "├─ "
        print(f"{prefix}{branch}{_node_label(typ, as_field_name)}")
        child_prefix = f"{prefix}{'   ' if is_last else '│  '}"
        # Recurse into model fields
        if _is_model(typ):
            if id(typ) in seen_models:
                print(f"{child_prefix}↪ (cycle)")
                return
            seen_models.add(id(typ))
            fields = list(_iter_fields(typ))
            for i, (fname, ftype, required) in enumerate(fields):
                last = i == len(fields) - 1
                req = "required" if required else "optional"
                field_branch = "└─ " if last else "├─ "
                print(f"{child_prefix}{field_branch}{fname} ({req})")
                _print_type(
                    _resolve_type(ftype, typ),
                    prefix=child_prefix + ("   " if last else "│  "),
                    is_last=True,
                    seen_models=seen_models,
                    as_field_name=None,
                )
            return
        # Containers / unions
        origin = get_origin(typ)
        args = list(get_args(typ))
        # Dict[K, V]
        if origin is dict and args:
            k, v = (args + [Any, Any])[:2]
            _print_type(_resolve_type(k, None), child_prefix, is_last=False, seen_models=seen_models, as_field_name="key")
            _print_type(_resolve_type(v, None), child_prefix, is_last=True,  seen_models=seen_models, as_field_name="value")
            return
        # Tuple[X, Y, ...] or Tuple[T, ...]
        if origin is tuple and args:
            if len(args) == 2 and args[1] is Ellipsis:
                _print_type(_resolve_type(args[0], None), child_prefix, is_last=True, seen_models=seen_models, as_field_name="*")
            else:
                for i, a in enumerate(args):
                    _print_type(_resolve_type(a, None), child_prefix, is_last=(i == len(args)-1), seen_models=seen_models, as_field_name=str(i))
            return
        # Generic case: iterate args
        for i, a in enumerate(args):
            _print_type(_resolve_type(a, None), child_prefix, is_last=(i == len(args)-1), seen_models=seen_models, as_field_name=None)

    # ---------------- entrypoint ----------------
    model_cls = obj if isinstance(obj, type) and _is_model(obj) else type(obj)
    seen: set[int] = set()
    _print_type(model_cls, prefix="", is_last=True, seen_models=seen, as_field_name=None)
        