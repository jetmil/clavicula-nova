#!/usr/bin/env python3
"""
Генератор изображений через ComfyUI API - Qwen Image (развёрнутый workflow)
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
    """Генерация изображения - полный развёрнутый workflow"""

    seed = random.randint(0, 2**32-1)

    # Развёрнутый workflow из subgraph
    workflow = {
        # Загрузка моделей
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
                "weight_dtype": "default"
            }
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
                "type": "qwen_image",
                "device": "default"
            }
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "qwen_image_vae.safetensors"
            }
        },
        # LoRA
        "4": {
            "class_type": "LoraLoaderModelOnly",
            "inputs": {
                "model": ["1", 0],
                "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
                "strength_model": 1.0
            }
        },
        # ModelSamplingAuraFlow
        "5": {
            "class_type": "ModelSamplingAuraFlow",
            "inputs": {
                "model": ["4", 0],
                "shift": 3.1
            }
        },
        # Latent
        "6": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        # Positive prompt
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["2", 0],
                "text": prompt
            }
        },
        # Negative prompt (empty for Qwen)
        "8": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["2", 0],
                "text": ""
            }
        },
        # KSampler
        "9": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["5", 0],
                "positive": ["7", 0],
                "negative": ["8", 0],
                "latent_image": ["6", 0],
                "seed": seed,
                "steps": 4,
                "cfg": 1.0,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1.0
            }
        },
        # VAE Decode
        "10": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["9", 0],
                "vae": ["3", 0]
            }
        },
        # Save
        "11": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": prefix,
                "images": ["10", 0]
            }
        }
    }

    payload = json.dumps({"prompt": workflow})

    print(f"Generating image via Qwen...")
    print(f"  Prompt: {prompt[:80]}...")
    print(f"  Size: {width}x{height}")
    print(f"  Seed: {seed}")

    body = http_request("POST", "/prompt", payload)
    result = json.loads(body)

    if "prompt_id" in result:
        prompt_id = result["prompt_id"]
        print(f"  Queued: {prompt_id}")

        # Ждём завершения
        for i in range(120):
            time.sleep(5)
            history = json.loads(http_request("GET", f"/history/{prompt_id}"))

            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, out in outputs.items():
                    if "images" in out:
                        filename = out["images"][0]["filename"]
                        print(f"  SUCCESS: {filename}")
                        return filename
                break

            print(f"  Waiting... ({(i+1)*5}s)")

    else:
        print(f"  Error: {result}")

    return None


# Промпты для гримуара
GRIMOIRE_PROMPTS = {
    "cover": "mystical golden key made of fire and light, ancient grimoire book cover, sacred geometry pentagram, dark magical atmosphere, esoteric Kabbalistic symbols floating, golden particles, volumetric lighting, ornate border design, dark indigo background",

    "upper_realm": "celestial upper realm, ethereal golden angels with radiant wings of pure light, crystalline palace floating in luminous clouds, divine radiance rays, sacred geometry patterns, heavenly atmosphere, cosmic stars and nebulae background",

    "middle_realm": "mystical middle realm, ancient forest with magical fog and fireflies, world tree Yggdrasil with glowing runes, nature spirits emerging from trees, stone circle with Celtic symbols, twilight magical atmosphere",

    "lower_realm": "dark underworld realm, vast caverns with glowing purple crystals, river of souls, roots of world tree descending into darkness, ancestral spirits as wisps of light, chthonic deities silhouettes",

    "sun_force": "solar deity archetype, magnificent golden sun disc with corona rays, regal lion and majestic eagle as sacred animals, amber and gold radiant energy, royal crown made of sunlight",

    "moon_force": "lunar goddess archetype, elegant silver crescent moon reflection on still water, mystical owls and white cats, pearls and moonstone glow, dreamy ethereal silver and blue atmosphere",

    "pentacle": "Solomon pentacle magical seal on parchment, intricate sacred geometry, Hebrew mystical letters, planetary symbols, aged paper texture, golden illuminated manuscript style",

    "archangel_michael": "Archangel Michael warrior of light, wielding flaming sword of divine justice, radiant golden armor with sun emblems, defeating dark dragon, wings of pure fire, holy light halo",

    "tarot_spread": "mystical tarot card reading scene, major arcana cards spread on deep purple velvet, golden candlelight, crystal ball reflection, ancient wisdom atmosphere",

    "crystals": "magical crystals and gemstones collection, amethyst clusters, clear quartz points, obsidian sphere, rose quartz heart, arranged on dark velvet with mystical glow"
}


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Генерация по имени
        name = sys.argv[1]
        if name in GRIMOIRE_PROMPTS:
            generate(GRIMOIRE_PROMPTS[name], 1024, 1024, name)
        else:
            # Или просто промпт
            width = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
            height = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
            prefix = sys.argv[4] if len(sys.argv) > 4 else "clavicula"
            generate(sys.argv[1], width, height, prefix)
    else:
        print("Доступные изображения:", ", ".join(GRIMOIRE_PROMPTS.keys()))
        print("\nUsage: gen_qwen.py <name|prompt> [width] [height] [prefix]")
