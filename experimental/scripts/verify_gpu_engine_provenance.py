#!/usr/bin/env python3
"""Check optional GPU engine kernel provenance without importing the engines."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ENGINE_FILES = (
    ROOT / "experimental" / "scripts" / "gpu" / "sigmac_gpu.py",
    ROOT / "experimental" / "scripts" / "gpu" / "staircase_gpu.py",
)
CERTIFICATE_ROOT = ROOT / "experimental" / "data" / "certificates"


def status_payload(status: str, **fields: Any) -> str:
    payload = {"status": status, **fields}
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def rawkernel_source_from_ast(path: Path) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "RAWKERNEL_SOURCE":
                value = ast.literal_eval(node.value)
                require(isinstance(value, str), f"{path}: RAWKERNEL_SOURCE is not a string")
                return value
    raise AssertionError(f"{path}: RAWKERNEL_SOURCE assignment not found")


def engine_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for path in ENGINE_FILES:
        require(path.exists(), f"missing engine file: {path}")
        source = rawkernel_source_from_ast(path)
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
        hashes[digest] = path.relative_to(ROOT).as_posix()
    return hashes


def collect_gpu_run_blocks(value: Any, path: Path, pointer: str) -> list[tuple[Path, str, dict[str, Any]]]:
    blocks: list[tuple[Path, str, dict[str, Any]]] = []
    if value is None:
        return blocks
    if isinstance(value, dict):
        if "kernel_source_sha256" in value:
            blocks.append((path, pointer, value))
            return blocks
        for key, child in value.items():
            blocks.extend(collect_gpu_run_blocks(child, path, f"{pointer}.{key}"))
        return blocks
    if isinstance(value, list):
        for index, item in enumerate(value):
            blocks.extend(collect_gpu_run_blocks(item, path, f"{pointer}[{index}]"))
        return blocks
    raise AssertionError(f"{path}:{pointer} is not a GPU provenance object or container")


def iter_gpu_blocks(value: Any, path: Path, pointer: str = "$") -> list[tuple[Path, str, dict[str, Any]]]:
    blocks: list[tuple[Path, str, dict[str, Any]]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_pointer = f"{pointer}.{key}"
            if key in {"gpu_run", "gpu_runs"}:
                blocks.extend(collect_gpu_run_blocks(child, path, child_pointer))
            blocks.extend(iter_gpu_blocks(child, path, child_pointer))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            blocks.extend(iter_gpu_blocks(item, path, f"{pointer}[{index}]"))
    return blocks


def scan_certificate_blocks() -> list[tuple[Path, str, dict[str, Any]]]:
    blocks: list[tuple[Path, str, dict[str, Any]]] = []
    for path in sorted(CERTIFICATE_ROOT.rglob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"{path}: invalid JSON: {exc}") from exc
        blocks.extend(iter_gpu_blocks(payload, path))
    return blocks


def check_provenance() -> dict[str, Any]:
    hashes = engine_hashes()
    blocks = scan_certificate_blocks()
    references: list[dict[str, Any]] = []
    failures: list[str] = []
    for path, pointer, block in blocks:
        digest = block.get("kernel_source_sha256")
        rel_path = path.relative_to(ROOT).as_posix()
        if not isinstance(digest, str):
            failures.append(f"{rel_path}:{pointer} lacks kernel_source_sha256")
            continue
        if digest not in hashes:
            failures.append(f"{rel_path}:{pointer} references unknown kernel hash {digest}")
            continue
        references.append(
            {
                "certificate": rel_path,
                "json_pointer": pointer,
                "kernel_source_sha256": digest,
                "engine_file": hashes[digest],
            }
        )
    return {
        "engine_hashes": {path: digest for digest, path in sorted(hashes.items(), key=lambda item: item[1])},
        "gpu_blocks_checked": len(blocks),
        "references": references,
        "failures": failures,
    }


def run_self_test() -> tuple[str, dict[str, Any]]:
    if os.environ.get("RSMCA_GPU_SELF_TEST_FORCE_SKIP") == "1":
        return "SKIP", {"reason": "forced by RSMCA_GPU_SELF_TEST_FORCE_SKIP"}
    try:
        cp = importlib.import_module("cupy")
    except Exception as exc:  # pragma: no cover - host dependent
        return "SKIP", {"reason": f"cupy import failed: {exc.__class__.__name__}: {exc}"}

    try:
        source = r'''
extern "C" __global__ void add_one(const int* src, int* dst) {
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx < 4) dst[idx] = src[idx] + 1;
}
'''
        src = cp.asarray([1, 2, 3, 4], dtype=cp.int32)
        dst = cp.zeros(4, dtype=cp.int32)
        kernel = cp.RawKernel(source, "add_one")
        kernel((1,), (4,), (src, dst))
        cp.cuda.Stream.null.synchronize()
        values = cp.asnumpy(dst).tolist()
        require(values == [2, 3, 4, 5], f"unexpected self-test output: {values}")
        props = cp.cuda.runtime.getDeviceProperties(0)
        name = props["name"].decode() if isinstance(props.get("name"), bytes) else str(props.get("name"))
        return "PASS", {"cupy_version": cp.__version__, "device": name, "result": values}
    except Exception as exc:  # pragma: no cover - host dependent
        return "SKIP", {"reason": f"CUDA self-test unavailable: {exc.__class__.__name__}: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify optional GPU engine provenance.")
    parser.add_argument("--check", action="store_true", help="check certificate kernel hashes")
    parser.add_argument("--self-test", action="store_true", help="launch a tiny optional CUDA kernel")
    args = parser.parse_args()

    if args.self_test:
        status, details = run_self_test()
        print(status_payload(f"SELF-TEST: {status}", **details), end="")
        return 0

    if args.check or not args.self_test:
        try:
            result = check_provenance()
        except AssertionError as exc:
            print(status_payload("FAIL", error=str(exc)), end="")
            return 1
        status = "PASS" if not result["failures"] else "FAIL"
        print(status_payload(status, **result), end="")
        return 0 if status == "PASS" else 1

    parser.error("select --check or --self-test")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
