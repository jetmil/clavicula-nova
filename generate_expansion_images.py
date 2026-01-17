#!/usr/bin/env python3
"""Generate 73 images for expansion chapters (38-47)"""

import json
import urllib.request
import urllib.error
import time
import random
import os
from PIL import Image

COMFYUI_URL = "http://127.0.0.1:8190"
OUTPUT_DIR = "images"

def create_workflow(prompt: str, seed: int = None, width: int = 1024, height: int = 1024) -> dict:
    if seed is None:
        seed = random.randint(1, 2**32 - 1)

    return {
        "37": {"class_type": "UNETLoader", "inputs": {
            "unet_name": "qwen_image_2512_fp8_e4m3fn.safetensors",
            "weight_dtype": "default"
        }},
        "38": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": "qwen_2.5_vl_7b_fp8_scaled.safetensors",
            "type": "qwen_image",
            "device": "default"
        }},
        "39": {"class_type": "VAELoader", "inputs": {
            "vae_name": "qwen_image_vae.safetensors"
        }},
        "73": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["37", 0],
            "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
            "strength_model": 1.0
        }},
        "66": {"class_type": "ModelSamplingAuraFlow", "inputs": {
            "model": ["73", 0],
            "shift": 3.1
        }},
        "58": {"class_type": "EmptySD3LatentImage", "inputs": {
            "width": width,
            "height": height,
            "batch_size": 1
        }},
        "6": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["38", 0],
            "text": prompt
        }},
        "7": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["38", 0],
            "text": ""
        }},
        "3": {"class_type": "KSampler", "inputs": {
            "model": ["66", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["58", 0],
            "seed": seed,
            "steps": 4,
            "cfg": 1.0,
            "sampler_name": "euler",
            "scheduler": "simple",
            "denoise": 1.0
        }},
        "8": {"class_type": "VAEDecode", "inputs": {
            "samples": ["3", 0],
            "vae": ["39", 0]
        }},
        "60": {"class_type": "SaveImage", "inputs": {
            "images": ["8", 0],
            "filename_prefix": "grimoire"
        }}
    }

# 73 new images for expansion chapters
IMAGES = [
    # Chapter 38: Hebrew Alphabet (9)
    {"name": "hebrew-aleph-card", "prompt": "Ancient Hebrew letter Aleph א carved in gold on dark stone tablet, mystical glow, kabbalistic correspondences shown around it, Tarot Fool card reference, path on Tree of Life, occult manuscript style, highly detailed"},
    {"name": "hebrew-full-alphabet", "prompt": "Complete Hebrew alphabet all 22 letters beautifully arranged in mystical circle, each letter glowing with inner light, ancient parchment background, kabbalistic diagram, sacred geometry, occult manuscript illumination"},
    {"name": "hebrew-mother-letters", "prompt": "Three Mother Letters of Hebrew: Aleph Mem Shin, representing Air Water Fire elements, mystical triangular arrangement, elemental energies flowing between them, cosmic backdrop, kabbalistic art"},
    {"name": "hebrew-double-letters", "prompt": "Seven Double Letters of Hebrew arranged in heptagram pattern, planetary symbols around each letter, golden light connections, mystical space background, ceremonial magic style"},
    {"name": "hebrew-simple-letters", "prompt": "Twelve Simple Letters of Hebrew arranged in zodiac wheel, each letter paired with its zodiac sign, cosmic starfield background, astrological magic diagram, mystical illumination"},
    {"name": "gematria-calculation", "prompt": "Ancient scroll showing gematria calculation example, Hebrew letters with numerical values, mathematical mysticism, glowing numbers, kabbalistic mathematics, occult scholar desk"},
    {"name": "hebrew-tarot-connection", "prompt": "Hebrew letters connected to Tarot Major Arcana cards, mystical correspondence chart, golden threads linking symbols, esoteric art, occult reference diagram"},
    {"name": "hebrew-tree-paths", "prompt": "Tree of Life diagram with 22 Hebrew letters on the paths between sephiroth, glowing connections, kabbalistic map, mystical geometry, sacred diagram"},
    {"name": "notarikon-example", "prompt": "AGLA notarikon: Atah Gibor Le-olam Adonai spelled out with mystical Hebrew letters, magical abbreviation explained, glowing text, protective talisman style"},

    # Chapter 39: Magical Diary (6)
    {"name": "diary-page-template", "prompt": "Magical diary page template, beautifully formatted with sections for date, moon phase, planetary hour, ritual description, results, handwritten calligraphy style, aged parchment"},
    {"name": "diary-evocation-template", "prompt": "Evocation record page in magical diary, spirit name, sigil drawn, offerings listed, manifestation notes, detailed ritual journal, mystical handwriting"},
    {"name": "theban-alphabet", "prompt": "Complete Theban alphabet (Witches alphabet) beautifully rendered, each letter with Latin equivalent, mystical script chart, occult calligraphy, aged parchment background"},
    {"name": "malachim-script", "prompt": "Malachim angelic script alphabet chart, celestial writing system, angelic letters glowing softly, mystical manuscript, Hebrew letter correspondences"},
    {"name": "celestial-script", "prompt": "Celestial alphabet (Angelic Script) complete chart, ethereal glowing letters, heavenly writing system, occult calligraphy reference, mystical parchment"},
    {"name": "diary-analysis-chart", "prompt": "Magical operation analysis chart in diary, tracking success rates, moon phases correlation, statistical mysticism, organized occult journal page"},

    # Chapter 40: Astral Travel (8)
    {"name": "astral-body-exit", "prompt": "Astral body separating from physical body during projection, ethereal translucent form rising, bedroom scene, silver cord visible, mystical blue glow, spiritual art"},
    {"name": "silver-cord", "prompt": "Silver cord connecting astral body to physical body, luminous thread stretching into astral plane, protective connection, spiritual anatomy diagram"},
    {"name": "lucid-dream-state", "prompt": "Person becoming aware in dream, reality shifting and transforming, hands examined for reality check, surreal dreamscape, consciousness awakening"},
    {"name": "rope-technique", "prompt": "Visualization of rope technique for astral projection, person pulling ethereal rope upward, astral body rising, vibrational state depicted, meditation scene"},
    {"name": "scrying-black-mirror", "prompt": "Black obsidian scrying mirror on altar, candlelight reflected, misty visions forming in surface, divination setup, mysterious atmosphere, occult practice"},
    {"name": "scrying-crystal-ball", "prompt": "Crystal ball scrying session, seer gazing into sphere, mystical visions swirling inside, candles around, purple velvet cloth, fortune telling scene"},
    {"name": "astral-plane-layers", "prompt": "Diagram of astral plane layers: lower middle upper astral, different vibrational realms depicted, spiritual cosmology map, ethereal landscape zones"},
    {"name": "astral-guardian", "prompt": "Astral temple guardian figure, protective entity at doorway, ethereal warrior form, spiritual security, mystical defender, glowing protective aura"},

    # Chapter 41: Ancestor Work (6)
    {"name": "ancestor-altar-setup", "prompt": "Ancestor altar with photographs, candles, offerings, flowers, glass of water, personal items of deceased, respectful memorial shrine, spiritual practice"},
    {"name": "family-tree-spiritual", "prompt": "Spiritual family tree diagram, ancestors depicted as glowing figures above, roots reaching deep, generations connected by light, genealogical mysticism"},
    {"name": "ancestor-offerings", "prompt": "Traditional offerings for ancestors: food, drink, incense, flowers, tobacco, arranged beautifully on altar cloth, honoring the dead, spiritual practice"},
    {"name": "ancestor-meditation", "prompt": "Person meditating before ancestor altar, golden light connecting them to ancestral spirits above, lineage healing, spiritual communion, peaceful scene"},
    {"name": "samhain-ancestor-ritual", "prompt": "Samhain ritual honoring ancestors, candles for the dead, veil between worlds thin, spirits gathering, autumn leaves, harvest altar, Celtic spirituality"},
    {"name": "lineage-healing-ritual", "prompt": "Ancestral healing ceremony, breaking chains of trauma, golden light transforming darkness, generational healing, spiritual therapy visualization"},

    # Chapter 42: Alchemy (8)
    {"name": "seven-alchemical-stages", "prompt": "Seven stages of Great Work illustrated: Calcination Dissolution Separation Conjunction Fermentation Distillation Coagulation, alchemical process diagram, mystical transformation"},
    {"name": "sulfur-mercury-salt", "prompt": "Three Principles of alchemy: Sulfur Mercury Salt represented symbolically, tria prima diagram, alchemical trinity, mystical chemistry symbols"},
    {"name": "alchemical-symbols-chart", "prompt": "Complete chart of alchemical symbols: elements metals processes planetary signs, reference diagram, occult chemistry notation, medieval manuscript style"},
    {"name": "spagyric-tincture", "prompt": "Spagyric tincture creation process, plant material in flask, distillation apparatus, alchemical laboratory, herbal alchemy, practical operation"},
    {"name": "athanor-furnace", "prompt": "Athanor alchemical furnace, philosophical egg inside, gentle heat maintaining, alchemist laboratory equipment, medieval chemistry, mystical apparatus"},
    {"name": "philosophers-stone-symbol", "prompt": "Philosopher's Stone symbol: red stone with golden aura, alchemical achievement, transmutation complete, mystical treasure, ultimate goal represented"},
    {"name": "inner-alchemy-stages", "prompt": "Inner alchemy transformation stages in human figure, spiritual purification visualized, psychological Great Work, meditation on self-transformation"},
    {"name": "plant-alchemy-process", "prompt": "Plant alchemy steps illustrated: maceration fermentation distillation calcination reunion, spagyric process diagram, herbal magic laboratory"},

    # Chapter 43: Group Rituals (7)
    {"name": "group-circle-formation", "prompt": "Group of robed practitioners standing in magical circle, holding hands, energy flowing between them, ceremonial magic lodge, candlelit temple room"},
    {"name": "lodge-officer-positions", "prompt": "Diagram of lodge officer positions: Hierophant Hiereus Hegemon Stolistes Dadouchos, ceremonial magic temple layout, Golden Dawn style"},
    {"name": "group-lbrp-formation", "prompt": "Group performing Lesser Banishing Ritual of Pentagram together, synchronized movements, blue pentagrams at quarters, ceremonial magic practice"},
    {"name": "egregore-visualization", "prompt": "Group egregore forming above practitioners, collective thought-form taking shape, group mind entity, mystical energy coalescence, lodge spirit"},
    {"name": "initiation-ceremony-group", "prompt": "Initiation ceremony in magical lodge, candidate blindfolded, officers in positions, ceremonial drama, ritual transformation, mystery school"},
    {"name": "coven-altar", "prompt": "Wiccan coven altar setup for group ritual, goddess and god representations, elemental quarters, seasonal decorations, neo-pagan practice"},
    {"name": "online-ritual-setup", "prompt": "Modern online ritual setup, computer screen showing video participants in robes, candles on desk, digital age ceremonial magic, synchronous practice"},

    # Chapter 44: Bibliography (8)
    {"name": "key-of-solomon-manuscript", "prompt": "Ancient Key of Solomon manuscript page, Latin text with magical circles, pentacles drawn in margins, medieval grimoire, illuminated manuscript"},
    {"name": "lemegeton-goetia-page", "prompt": "Lemegeton Goetia page showing spirit seal, demon description, conjuration text, medieval demonology manuscript, occult book interior"},
    {"name": "agrippa-three-books", "prompt": "Three Books of Occult Philosophy by Agrippa, Renaissance magical text, woodcut illustrations, early printed grimoire, scholarly occultism"},
    {"name": "eliphas-levi-portrait", "prompt": "Portrait of Eliphas Levi, 19th century French occultist, Baphomet image creator, ceremonial magician, scholarly appearance, Victorian era"},
    {"name": "crowley-magick-cover", "prompt": "Magick in Theory and Practice book cover style, Aleister Crowley work, Thelemic symbolism, 20th century occultism, ceremonial magic text"},
    {"name": "golden-dawn-cipher", "prompt": "Golden Dawn cipher manuscript page, encoded magical knowledge, secret society documents, Victorian occultism, mysterious writing"},
    {"name": "modern-grimoire-shelf", "prompt": "Bookshelf of modern grimoires and occult books, contemporary magical library, well-organized collection, practitioner's study"},
    {"name": "sefer-yetzirah", "prompt": "Sefer Yetzirah ancient Kabbalistic text, Hebrew letters and creation, mystical cosmology, Jewish mysticism foundation text"},

    # Chapter 45: Magic Traditions (7)
    {"name": "golden-dawn-temple-room", "prompt": "Golden Dawn temple room interior, black and white pillars, altar of double cube, officer thrones, ceremonial equipment, Victorian lodge"},
    {"name": "thelema-unicursal-hexagram", "prompt": "Unicursal hexagram Thelema symbol, continuous line hexagram, Crowley's design, magical emblem, mystical geometry, golden on purple"},
    {"name": "chaos-magic-sphere", "prompt": "Chaos magic symbol: eight-pointed star of chaos, chaosphere, postmodern occultism emblem, belief as tool, paradigm shifting imagery"},
    {"name": "wicca-altar-setup", "prompt": "Traditional Wiccan altar, goddess and god candles, athame and chalice, pentacle, nature-based spirituality, neo-pagan practice"},
    {"name": "enochian-tablet-earth", "prompt": "Enochian Tablet of Earth, complex grid with letters, Dee and Kelly system, angelic magic tool, Victorian occultism, magical board"},
    {"name": "eastern-western-synthesis", "prompt": "Synthesis of Eastern and Western magic: yin-yang meeting pentagram, chakras and sephiroth combined, cross-cultural spirituality"},
    {"name": "hoodoo-mojo-bag", "prompt": "Hoodoo mojo bag with ingredients, roots herbs curios, folk magic practice, African American spiritual tradition, conjure work"},

    # Chapter 46: History of Tradition (8)
    {"name": "solomon-temple-reconstruction", "prompt": "King Solomon's Temple artistic reconstruction, ancient Jerusalem, biblical architecture, bronze pillars Jachin Boaz, holy of holies"},
    {"name": "egyptian-temple-magic", "prompt": "Egyptian priest performing temple magic, hieroglyphic walls, ritual offerings, ancient Kemet spirituality, pharaonic religion"},
    {"name": "medieval-grimoire-page", "prompt": "Medieval grimoire page being written by candlelight, monk copying magical text, monastery scriptorium, middle ages occultism"},
    {"name": "renaissance-magus-study", "prompt": "Renaissance magus in his study, surrounded by books and instruments, scholarly magic, Faust-like scene, 16th century occultism"},
    {"name": "john-dee-enochian", "prompt": "John Dee and Edward Kelly receiving Enochian revelations, crystal ball scrying, angelic communication, Elizabethan magic, historical scene"},
    {"name": "victorian-seance", "prompt": "Victorian spiritualist seance, medium in trance, ectoplasm manifestation, parlor setting, 19th century occultism, historical spiritualism"},
    {"name": "modern-ceremonial-magician", "prompt": "Modern ceremonial magician in full regalia, contemporary temple, traditional practice in modern setting, 21st century occultism"},
    {"name": "magic-history-timeline", "prompt": "Timeline of magical history illustrated: Egypt Greece Rome Medieval Renaissance Victorian Modern eras, evolution of occultism diagram"},

    # Chapter 47: Practitioner Stories (6)
    {"name": "successful-evocation-scene", "prompt": "Successful spirit evocation moment, entity manifesting in triangle, magician in circle, candles flickering, incense smoke, dramatic magical operation"},
    {"name": "magical-diary-entries", "prompt": "Open magical diary showing detailed entries, drawings of sigils, notes on results, personal magical record, practitioner's journal"},
    {"name": "synchronicity-signs", "prompt": "Meaningful coincidences illustrated: repeated numbers, symbolic animals, perfect timing events, universe responding, magical confirmation signs"},
    {"name": "beginner-altar-mistakes", "prompt": "Cluttered messy altar showing common beginner mistakes, too many items, disorganized, learning process illustration, what not to do"},
    {"name": "master-magician-advice", "prompt": "Experienced magician teaching student, wisdom being passed down, mentorship in magical tradition, elder and apprentice scene"},
    {"name": "balance-magic-life", "prompt": "Balance between magical practice and daily life illustrated, scales with ritual tools and everyday objects, integration theme, healthy practitioner"},
]

def generate_image(img_info, retry=3):
    """Generate a single image"""
    name = img_info["name"]
    prompt = img_info["prompt"]

    print(f"Generating: {name}")

    workflow = create_workflow(prompt)

    for attempt in range(retry):
        try:
            data = json.dumps({"prompt": workflow}).encode('utf-8')
            req = urllib.request.Request(
                f"{COMFYUI_URL}/prompt",
                data=data,
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                prompt_id = result.get('prompt_id')

            # Wait for completion
            for _ in range(120):  # 2 minutes max
                time.sleep(1)
                try:
                    status_req = urllib.request.Request(f"{COMFYUI_URL}/history/{prompt_id}")
                    with urllib.request.urlopen(status_req, timeout=10) as status_response:
                        history = json.loads(status_response.read().decode('utf-8'))
                        if prompt_id in history:
                            outputs = history[prompt_id].get('outputs', {})
                            if '60' in outputs and 'images' in outputs['60']:
                                img_data = outputs['60']['images'][0]
                                filename = img_data['filename']
                                subfolder = img_data.get('subfolder', '')

                                # Download image
                                img_url = f"{COMFYUI_URL}/view?filename={filename}&subfolder={subfolder}&type=output"
                                img_path = os.path.join(OUTPUT_DIR, f"{name}.png")
                                urllib.request.urlretrieve(img_url, img_path)
                                print(f"  Saved: {name}.png")
                                return True
                except:
                    pass

            print(f"  Timeout for {name}, retrying...")

        except Exception as e:
            print(f"  Error: {e}, attempt {attempt+1}/{retry}")
            time.sleep(5)

    print(f"  FAILED: {name}")
    return False

def convert_to_jpeg():
    """Convert all PNGs to compressed JPEGs"""
    print("\nConverting to JPEG...")
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.png'):
            png_path = os.path.join(OUTPUT_DIR, filename)
            jpg_path = os.path.join(OUTPUT_DIR, filename.replace('.png', '.jpg'))

            try:
                with Image.open(png_path) as img:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')

                    # Resize if larger than 1024
                    if max(img.size) > 1024:
                        img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

                    img.save(jpg_path, 'JPEG', quality=85, optimize=True)

                os.remove(png_path)
                print(f"  Converted: {filename} -> {filename.replace('.png', '.jpg')}")
            except Exception as e:
                print(f"  Error converting {filename}: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Generating {len(IMAGES)} images for expansion chapters...")
    print("=" * 50)

    success = 0
    failed = 0

    for i, img_info in enumerate(IMAGES):
        print(f"\n[{i+1}/{len(IMAGES)}]", end=" ")
        if generate_image(img_info):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 50)
    print(f"Generation complete: {success} success, {failed} failed")

    convert_to_jpeg()

    print("\nDone!")

if __name__ == '__main__':
    main()
