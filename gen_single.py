#!/usr/bin/env python3
"""
Генератор одного изображения через ComfyUI API
Workflow: квен_создание_быстрый (Qwen Image + Lightning LoRA)
"""

import socket
import json
import time
import sys
import random

COMFY_HOST = "127.0.0.1"
COMFY_PORT = 8190

def http_request(method, path, body=None):
    """HTTP через сокет (обход прокси)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(600)
    sock.connect((COMFY_HOST, COMFY_PORT))

    headers = f"{method} {path} HTTP/1.1\r\nHost: {COMFY_HOST}:{COMFY_PORT}\r\n"
    if body:
        headers += f"Content-Type: application/json\r\nContent-Length: {len(body)}\r\n"
    headers += "Connection: close\r\n\r\n"

    sock.sendall(headers.encode())
    if body:
        sock.sendall(body.encode())

    response = b""
    while True:
        chunk = sock.recv(8192)
        if not chunk:
            break
        response += chunk
    sock.close()

    parts = response.split(b"\r\n\r\n", 1)
    body_resp = parts[1] if len(parts) > 1 else b""
    return body_resp


def generate(prompt, width=1024, height=1024, prefix="clavicula"):
    """Генерация изображения"""

    # Workflow from квен_создание_быстрый.json
    workflow = {
        "60": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": prefix,
                "images": ["75", 0]
            }
        },
        "75": {
            "class_type": "2c61139d-9c34-4c7e-a083-7a67cc4770ad",  # Qwen Subgraph
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                "width": width,
                "height": height,
                "batch_size": 1,
                "seed": random.randint(0, 2**32-1),
                "steps": 4,
                "text": prompt
            }
        }
    }

    payload = json.dumps({"prompt": workflow})

    print(f"Sending prompt to ComfyUI...")
    print(f"  Prompt: {prompt[:80]}...")
    print(f"  Size: {width}x{height}")

    body = http_request("POST", "/prompt", payload)
    result = json.loads(body)

    if "prompt_id" in result:
        prompt_id = result["prompt_id"]
        print(f"  Queued: {prompt_id}")

        # Ждём завершения
        for i in range(120):  # Макс 10 минут
            time.sleep(5)
            history = json.loads(http_request("GET", f"/history/{prompt_id}"))

            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, out in outputs.items():
                    if "images" in out:
                        filename = out["images"][0]["filename"]
                        print(f"  Generated: {filename}")
                        return filename
                break

            print(f"  Waiting... ({(i+1)*5}s)")

    else:
        print(f"  Error: {result}")

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gen_single.py 'prompt' [width] [height] [prefix]")
        sys.exit(1)

    prompt = sys.argv[1]
    width = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    height = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
    prefix = sys.argv[4] if len(sys.argv) > 4 else "clavicula"

    generate(prompt, width, height, prefix)
