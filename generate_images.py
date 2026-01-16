#!/usr/bin/env python3
"""
Генератор изображений для CLAVICULA NOVA через ComfyUI API
Используем workflow: квен_создание_быстрый
"""

import socket
import json
import uuid
import time
import os
from pathlib import Path

COMFY_HOST = "127.0.0.1"
COMFY_PORT = 8190
OUTPUT_DIR = Path("/mnt/c/Users/PC/Downloads/clavicula-nova-site/images")

# Промпты для иллюстраций гримуара
GRIMOIRE_PROMPTS = {
    # Обложка
    "cover": {
        "prompt": "mystical golden key made of fire and light, ancient grimoire cover, sacred geometry pentagram, dark magical atmosphere, esoteric symbols floating, golden particles, volumetric lighting, 8k detailed illustration",
        "negative": "text, watermark, signature, blurry, low quality",
        "size": (1024, 1536)  # Вертикальная для обложки
    },

    # Три Царства
    "upper_realm": {
        "prompt": "celestial upper realm, golden angels with wings of light, crystalline palace in clouds, divine radiance, sacred geometry patterns, heavenly choir, ethereal atmosphere, rays of pure white light, cosmic stars",
        "negative": "dark, horror, demons, blood",
        "size": (1024, 768)
    },
    "middle_realm": {
        "prompt": "middle realm of humans, ancient forest with mystical fog, world tree Yggdrasil, spirits of nature, shamanic journey, stone circles, twilight atmosphere, magical realism",
        "negative": "modern, technology, cars",
        "size": (1024, 768)
    },
    "lower_realm": {
        "prompt": "underworld realm, dark caverns with glowing crystals, ancestral spirits, roots of world tree, river Styx, ancient bones, mysterious shadows, deep earth colors, chthonic deities",
        "negative": "bright, cheerful, modern",
        "size": (1024, 768)
    },

    # Семь Планетарных Сил
    "sun_force": {
        "prompt": "solar deity, golden sun disc with rays, lion and eagle symbols, radiant masculine energy, solar eclipse corona, amber and gold colors, royal crown of light",
        "negative": "moon, darkness, cold",
        "size": (768, 768)
    },
    "moon_force": {
        "prompt": "lunar goddess, silver crescent moon, reflective waters, owls and cats, feminine mystical energy, moonlit forest, pearls and silver, dreamy ethereal atmosphere",
        "negative": "sun, fire, harsh light",
        "size": (768, 768)
    },
    "mars_force": {
        "prompt": "warrior deity Mars, iron sword and shield, red planet glow, wolves and hawks, battle energy, flames and sparks, strong masculine power, crimson and iron colors",
        "negative": "peaceful, flowers, soft",
        "size": (768, 768)
    },
    "mercury_force": {
        "prompt": "Hermes Mercury deity, caduceus staff with snakes, winged sandals, quicksilver liquid metal, communication symbols, fast movement blur, orange and silver colors",
        "negative": "slow, heavy, static",
        "size": (768, 768)
    },
    "jupiter_force": {
        "prompt": "Jupiter Zeus deity, thunder and lightning, royal purple robes, eagle with thunderbolt, expansion and abundance, storm clouds, majestic throne, blue and purple colors",
        "negative": "small, weak, poor",
        "size": (768, 768)
    },
    "venus_force": {
        "prompt": "Venus Aphrodite deity, rose flowers and doves, copper mirror, beauty and love energy, emerald green and pink colors, sensual feminine grace, sea foam and pearls",
        "negative": "ugly, war, violence",
        "size": (768, 768)
    },
    "saturn_force": {
        "prompt": "Saturn Chronos deity, hourglass and scythe, lead gray colors, ancient wisdom, time and limitation, black cube, bones and earth, stern elderly figure",
        "negative": "young, colorful, fast",
        "size": (768, 768)
    },

    # Ангелы
    "archangel_michael": {
        "prompt": "Archangel Michael, flaming sword of divine justice, golden armor with sun symbols, defeating dragon, protective warrior of light, wings of pure fire, holy radiance",
        "negative": "demon, evil, dark",
        "size": (768, 1024)
    },
    "archangel_gabriel": {
        "prompt": "Archangel Gabriel, silver trumpet of annunciation, lily flower, messenger of divine will, wings of moonlight, blue and white robes, water element",
        "negative": "war, violence, fire",
        "size": (768, 1024)
    },

    # Демоны Гоэтии
    "goetia_spirit": {
        "prompt": "Goetia spirit in magic circle, sigil glowing with fire, brass vessel, solomon seal, ceremonial magic evocation, dark ritual chamber, candles and incense smoke",
        "negative": "cute, cartoon, anime",
        "size": (768, 768)
    },

    # Элементали
    "salamander": {
        "prompt": "fire elemental salamander spirit, living flames dancing, volcanic energy, red and orange aura, heat distortion, ancient fire being",
        "negative": "water, ice, cold",
        "size": (768, 768)
    },
    "undine": {
        "prompt": "water elemental undine spirit, flowing liquid form, ocean depths, blue and turquoise colors, bubbles and currents, feminine water being",
        "negative": "fire, dry, desert",
        "size": (768, 768)
    },
    "gnome": {
        "prompt": "earth elemental gnome spirit, crystals and gems, underground cavern, brown and green colors, mushrooms and roots, ancient stone being",
        "negative": "sky, flying, light",
        "size": (768, 768)
    },
    "sylph": {
        "prompt": "air elemental sylph spirit, wind and clouds, transparent ethereal form, white and pale blue, feathers floating, breath of life",
        "negative": "heavy, solid, earth",
        "size": (768, 768)
    },

    # Инструменты
    "pentacle": {
        "prompt": "Solomon pentacle magical seal, intricate sacred geometry, Hebrew letters, planetary symbols, parchment texture, golden ink on dark background, protective talisman",
        "negative": "simple, modern, plain",
        "size": (768, 768)
    },
    "ritual_altar": {
        "prompt": "magical altar with candles, chalice, athame dagger, pentagram cloth, incense smoke, crystals and herbs, grimoire open, ceremonial magic setup",
        "negative": "messy, modern, technology",
        "size": (1024, 768)
    },

    # Таро
    "tarot_spread": {
        "prompt": "tarot cards spread on velvet cloth, major arcana visible, mystical divination scene, candlelight, crystal ball, fortune telling atmosphere",
        "negative": "modern, digital, bright",
        "size": (1024, 768)
    },

    # Руны
    "rune_stones": {
        "prompt": "elder futhark rune stones, carved ancient symbols, nordic mysticism, wooden background with fur, Viking divination, mystical glow on runes",
        "negative": "modern, plastic, bright",
        "size": (1024, 768)
    },

    # Травник
    "herbarium": {
        "prompt": "magical herbarium page, dried herbs and flowers pressed, alchemical annotations, botanical illustration, moonlit gathering, witch garden plants",
        "negative": "modern, digital, plain",
        "size": (768, 1024)
    },

    # Камни
    "crystals": {
        "prompt": "magical crystals and gemstones, amethyst quartz obsidian, healing stones arrangement, mystical glow, dark velvet background, mineral collection",
        "negative": "plastic, fake, bright",
        "size": (1024, 768)
    }
}


def http_request(host, port, method, path, body=None):
    """Простой HTTP запрос через сокет (обход прокси)"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(300)  # 5 минут таймаут для генерации
    sock.connect((host, port))

    headers = f"{method} {path} HTTP/1.1\r\nHost: {host}:{port}\r\n"
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

    # Парсим ответ
    parts = response.split(b"\r\n\r\n", 1)
    header = parts[0].decode()
    body = parts[1] if len(parts) > 1 else b""

    status_line = header.split("\r\n")[0]
    status_code = int(status_line.split()[1])

    return status_code, body


def queue_prompt(workflow):
    """Отправляем workflow на генерацию"""
    prompt_id = str(uuid.uuid4())
    payload = json.dumps({"prompt": workflow, "client_id": prompt_id})

    status, body = http_request(COMFY_HOST, COMFY_PORT, "POST", "/prompt", payload)

    if status == 200:
        result = json.loads(body)
        return result.get("prompt_id")
    else:
        print(f"Error queuing prompt: {status}")
        return None


def get_history(prompt_id):
    """Получаем результат генерации"""
    status, body = http_request(COMFY_HOST, COMFY_PORT, "GET", f"/history/{prompt_id}")
    if status == 200:
        return json.loads(body)
    return None


def wait_for_completion(prompt_id, timeout=300):
    """Ждём завершения генерации"""
    start = time.time()
    while time.time() - start < timeout:
        history = get_history(prompt_id)
        if history and prompt_id in history:
            return history[prompt_id]
        time.sleep(2)
    return None


def create_workflow(prompt_text, negative_prompt, width=1024, height=1024):
    """Создаём простой workflow для SDXL/Flux"""
    return {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": int(time.time()) % 2147483647,
                "steps": 20,
                "cfg": 7.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            }
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "sd_xl_base_1.0.safetensors"
            }
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt_text,
                "clip": ["4", 1]
            }
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["4", 1]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "clavicula",
                "images": ["8", 0]
            }
        }
    }


def generate_image(name, config):
    """Генерируем одно изображение"""
    print(f"\n{'='*50}")
    print(f"Generating: {name}")
    print(f"Prompt: {config['prompt'][:80]}...")

    width, height = config.get("size", (1024, 1024))
    workflow = create_workflow(config["prompt"], config["negative"], width, height)

    prompt_id = queue_prompt(workflow)
    if not prompt_id:
        print(f"Failed to queue: {name}")
        return None

    print(f"Queued with ID: {prompt_id}")
    print("Waiting for generation...")

    result = wait_for_completion(prompt_id)
    if result:
        outputs = result.get("outputs", {})
        for node_id, output in outputs.items():
            if "images" in output:
                for img in output["images"]:
                    filename = img["filename"]
                    print(f"Generated: {filename}")
                    return filename

    print(f"Failed to generate: {name}")
    return None


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("="*60)
    print("CLAVICULA NOVA Image Generator")
    print(f"ComfyUI: {COMFY_HOST}:{COMFY_PORT}")
    print(f"Output: {OUTPUT_DIR}")
    print("="*60)

    # Проверяем связь
    status, body = http_request(COMFY_HOST, COMFY_PORT, "GET", "/system_stats")
    if status != 200:
        print(f"ComfyUI not available: {status}")
        return

    stats = json.loads(body)
    print(f"ComfyUI v{stats['system']['comfyui_version']}")
    print(f"GPU: {stats['devices'][0]['name']}")
    print(f"VRAM Free: {stats['devices'][0]['vram_free'] // 1024**3} GB")

    # Генерируем изображения
    generated = []
    for name, config in GRIMOIRE_PROMPTS.items():
        result = generate_image(name, config)
        if result:
            generated.append((name, result))
        time.sleep(2)  # Пауза между генерациями

    print("\n" + "="*60)
    print(f"Generated {len(generated)} of {len(GRIMOIRE_PROMPTS)} images")
    for name, filename in generated:
        print(f"  {name}: {filename}")


if __name__ == "__main__":
    main()
