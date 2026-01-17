#!/usr/bin/env python3
"""
Генератор изображений для CLAVICULA NOVA
Использует ComfyUI на порту 8190 с Qwen 2.5 VL + Lightning LoRA
"""

import json
import time
import random
import subprocess
from pathlib import Path
from urllib.parse import urlencode

COMFYUI_URL = "http://127.0.0.1:8190"
OUTPUT_DIR = Path("C:/Users/PC/Downloads/clavicula-nova-site/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
        "89": {"class_type": "LoraLoaderModelOnly", "inputs": {
            "model": ["37", 0],
            "lora_name": "Qwen-Image-2512-Lightning-4steps-V1.0-bf16.safetensors",
            "strength_model": 1.0
        }},
        "66": {"class_type": "ModelSamplingAuraFlow", "inputs": {
            "model": ["89", 0],
            "shift": 3.0
        }},
        "75": {"class_type": "CFGNorm", "inputs": {
            "model": ["66", 0],
            "strength": 1.0
        }},
        "58": {"class_type": "EmptySD3LatentImage", "inputs": {
            "width": width,
            "height": height,
            "batch_size": 1
        }},
        "7": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["38", 0],
            "text": prompt
        }},
        "40": {"class_type": "CLIPTextEncode", "inputs": {
            "clip": ["38", 0],
            "text": ""
        }},
        "3": {"class_type": "KSampler", "inputs": {
            "model": ["75", 0],
            "positive": ["7", 0],
            "negative": ["40", 0],
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

# ============================================================================
# СПИСОК ИЗОБРАЖЕНИЙ ДЛЯ ГРИМУАРА (200+)
# ============================================================================

IMAGES = [
    # -------------------------------------------------------------------------
    # ОБЛОЖКА И ТИТУЛЬНЫЕ
    # -------------------------------------------------------------------------
    {
        "name": "cover-main",
        "prompt": "Ancient grimoire book cover, golden Key of Solomon emblem on black leather, mystical symbols glowing with ethereal blue light, Hebrew letters around border, ornate medieval manuscript style, dark occult aesthetic, highly detailed, 8k"
    },
    {
        "name": "title-book1",
        "prompt": "Ornate chapter title page 'Foundations', Kabbalistic Tree of Life glowing in center, ten spheres connected by paths, golden light on dark parchment background, medieval illuminated manuscript style"
    },
    {
        "name": "title-book2",
        "prompt": "Ornate chapter title page 'Keys', ancient Solomon's key symbol, 72-pointed star pattern, angelic script around border, silver and gold on aged parchment"
    },
    {
        "name": "title-book3",
        "prompt": "Ornate chapter title page 'Practice', ritual circle with candles and magical tools, ceremonial dagger and chalice, mystical smoke, dark atmospheric lighting"
    },
    {
        "name": "title-book4",
        "prompt": "Ornate chapter title page 'Operations', planetary symbols arranged in circle, seven classical planets, astrological chart design, celestial blue and gold colors"
    },
    {
        "name": "title-book5",
        "prompt": "Ornate chapter title page 'Mastery', human figure in meditation pose with glowing chakras, divine light descending from above, cosmic background with stars"
    },

    # -------------------------------------------------------------------------
    # ДРЕВО ЖИЗНИ И КАББАЛА
    # -------------------------------------------------------------------------
    {
        "name": "tree-of-life-full",
        "prompt": "Kabbalistic Tree of Life diagram, ten glowing spheres (sephiroth) connected by 22 paths, Hebrew letters on each path, golden light emanating from Kether, cosmic background, detailed mystical illustration"
    },
    {
        "name": "tree-of-life-pillars",
        "prompt": "Three pillars of Kabbalistic Tree of Life, Severity on left in red, Mercy on right in blue, Middle Pillar in gold, balanced mystical diagram, dark background"
    },
    {
        "name": "sephirah-kether",
        "prompt": "Kabbalistic sephirah Kether, brilliant white crown of light, pure divine radiance, cosmic void background, Hebrew letter Aleph glowing, mystical ethereal style"
    },
    {
        "name": "sephirah-chokmah",
        "prompt": "Kabbalistic sephirah Chokmah, grey sphere of wisdom, starfield background representing zodiac, Hebrew letter Yod, ancient sage figure in meditation"
    },
    {
        "name": "sephirah-binah",
        "prompt": "Kabbalistic sephirah Binah, black sphere of understanding, Saturn symbol, dark mother archetype, cosmic womb imagery, deep space background"
    },
    {
        "name": "sephirah-chesed",
        "prompt": "Kabbalistic sephirah Chesed, blue sphere of mercy, Jupiter symbol, benevolent king on throne, abundance imagery, golden light"
    },
    {
        "name": "sephirah-geburah",
        "prompt": "Kabbalistic sephirah Geburah, red sphere of severity, Mars symbol, warrior with flaming sword, strength and justice imagery"
    },
    {
        "name": "sephirah-tiphareth",
        "prompt": "Kabbalistic sephirah Tiphareth, golden sun sphere, beauty and harmony, Christ-like figure with radiating light, center of Tree of Life"
    },
    {
        "name": "sephirah-netzach",
        "prompt": "Kabbalistic sephirah Netzach, green sphere of victory, Venus symbol, goddess of love and beauty, roses and nature imagery"
    },
    {
        "name": "sephirah-hod",
        "prompt": "Kabbalistic sephirah Hod, orange sphere of splendor, Mercury symbol, Hermes with caduceus, intellect and communication imagery"
    },
    {
        "name": "sephirah-yesod",
        "prompt": "Kabbalistic sephirah Yesod, purple sphere foundation, Moon symbol, dreams and astral imagery, silver crescent moon"
    },
    {
        "name": "sephirah-malkuth",
        "prompt": "Kabbalistic sephirah Malkuth, earth sphere kingdom, four elements united, physical world, stable brown and green colors, material manifestation"
    },
    {
        "name": "four-worlds",
        "prompt": "Four Kabbalistic Worlds diagram: Atziluth (fire, red), Briah (water, blue), Yetzirah (air, yellow), Assiah (earth, green), layered cosmic spheres, divine emanation"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ САТУРНА (7)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-saturn-1",
        "prompt": "First Pentacle of Saturn, magical square 3x3 with numbers, Hebrew letters AGIEL and ZAZEL around border, black and silver design on aged parchment, occult grimoire style"
    },
    {
        "name": "pentacle-saturn-2",
        "prompt": "Second Pentacle of Saturn, Saturn symbol (sickle) in center, Latin psalm inscription around circle, protection against enemies, black lead-colored design"
    },
    {
        "name": "pentacle-saturn-3",
        "prompt": "Third Pentacle of Saturn, cross pattern with IHVH letters, angel names Omeliel Anachiel around border, protection from night spirits, dark mystical design"
    },
    {
        "name": "pentacle-saturn-4",
        "prompt": "Fourth Pentacle of Saturn, pentagram star in center, Hebrew divine names, respect and obedience magic, black and silver geometric design"
    },
    {
        "name": "pentacle-saturn-5",
        "prompt": "Fifth Pentacle of Saturn, magical square surrounded by protective symbols, house protection, dark earth tones, medieval grimoire illustration"
    },
    {
        "name": "pentacle-saturn-6",
        "prompt": "Sixth Pentacle of Saturn, four concentric circles with angel names of death, necromantic symbols, very dark and mysterious design"
    },
    {
        "name": "pentacle-saturn-7",
        "prompt": "Seventh Pentacle of Saturn, square within circle, earth spirits names, destructive power symbolism, cracked earth imagery"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ ЮПИТЕРА (7)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-jupiter-1",
        "prompt": "First Pentacle of Jupiter, hexagram (Star of David) with Hebrew letters in triangles, divine names around circle, blue and gold colors, wealth and treasure"
    },
    {
        "name": "pentacle-jupiter-2",
        "prompt": "Second Pentacle of Jupiter, equal-armed cross dividing circle into quarters, glory and honor symbols, royal purple and gold design"
    },
    {
        "name": "pentacle-jupiter-3",
        "prompt": "Third Pentacle of Jupiter, four angel names Netoniel Devachiah, protection and wealth, blue light emanating, medieval manuscript style"
    },
    {
        "name": "pentacle-jupiter-4",
        "prompt": "Fourth Pentacle of Jupiter, magical square 4x4 with numbers summing to 34, most famous wealth pentacle, golden coins imagery, prosperity symbols"
    },
    {
        "name": "pentacle-jupiter-5",
        "prompt": "Fifth Pentacle of Jupiter, vision symbols for seeing Jupiter spirits, mystical eye in center, prophetic imagery, deep blue cosmic background"
    },
    {
        "name": "pentacle-jupiter-6",
        "prompt": "Sixth Pentacle of Jupiter, protection from earthly dangers, shield symbolism, Jupiter glyph prominent, royal blue and silver"
    },
    {
        "name": "pentacle-jupiter-7",
        "prompt": "Seventh Pentacle of Jupiter, power over air spirits, wind and cloud imagery, ethereal blue design, angelic wings motif"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ МАРСА (7)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-mars-1",
        "prompt": "First Pentacle of Mars, magical square 5x5, Mars symbol (spear and shield), red iron color, warrior energy, aggressive design"
    },
    {
        "name": "pentacle-mars-2",
        "prompt": "Second Pentacle of Mars, scorpion symbol in center, victory over enemies, healing martial diseases, blood red and black design"
    },
    {
        "name": "pentacle-mars-3",
        "prompt": "Third Pentacle of Mars, causing discord and war, crossed swords imagery, flames and conflict symbols, aggressive red design"
    },
    {
        "name": "pentacle-mars-4",
        "prompt": "Fourth Pentacle of Mars, victory in battle, triumphant warrior imagery, Mars glyph with laurel wreath, crimson and gold"
    },
    {
        "name": "pentacle-mars-5",
        "prompt": "Fifth Pentacle of Mars, terrifying demons, scorpion with IHVH name, protection through fear, dark red and black intense design"
    },
    {
        "name": "pentacle-mars-6",
        "prompt": "Sixth Pentacle of Mars, protection from weapons, shield with deflecting arrows, defensive warrior symbols, iron grey and red"
    },
    {
        "name": "pentacle-mars-7",
        "prompt": "Seventh Pentacle of Mars, causing hail and storms, lightning and tempest imagery, destructive natural forces, dramatic dark sky"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ СОЛНЦА (7)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-sun-1",
        "prompt": "First Pentacle of the Sun, magical square 6x6, golden solar disk, rays of light emanating, calling solar spirits, brilliant yellow gold"
    },
    {
        "name": "pentacle-sun-2",
        "prompt": "Second Pentacle of the Sun, suppressing pride of others, humbling solar crown, balanced golden design, royal authority symbols"
    },
    {
        "name": "pentacle-sun-3",
        "prompt": "Third Pentacle of the Sun, gaining kingdom and empire, royal scepter and crown, commanding presence, golden imperial design"
    },
    {
        "name": "pentacle-sun-4",
        "prompt": "Fourth Pentacle of the Sun, seeing invisible spirits, mystical eye of providence, clairvoyant vision symbols, golden light revealing hidden things"
    },
    {
        "name": "pentacle-sun-5",
        "prompt": "Fifth Pentacle of the Sun, rapid transport and movement, winged solar disk, swift travel symbols, dynamic golden design"
    },
    {
        "name": "pentacle-sun-6",
        "prompt": "Sixth Pentacle of the Sun, invisibility power, fading figure into light, concealment magic, translucent golden aura"
    },
    {
        "name": "pentacle-sun-7",
        "prompt": "Seventh Pentacle of the Sun, liberation from prison, broken chains, freedom symbolism, rays breaking through darkness"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ ВЕНЕРЫ (5)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-venus-1",
        "prompt": "First Pentacle of Venus, magical square 7x7, Venus symbol, calling spirits of love, rose pink and green, romantic mystical design"
    },
    {
        "name": "pentacle-venus-2",
        "prompt": "Second Pentacle of Venus, obtaining grace and favor, heart and rose symbols, love angel names, soft pink and copper colors"
    },
    {
        "name": "pentacle-venus-3",
        "prompt": "Third Pentacle of Venus, attracting love, intertwined hearts, magnetic attraction symbols, romantic pink glow"
    },
    {
        "name": "pentacle-venus-4",
        "prompt": "Fourth Pentacle of Venus, compelling spirits to show beauty, mirror and venus symbols, aesthetic perfection, elegant copper design"
    },
    {
        "name": "pentacle-venus-5",
        "prompt": "Fifth Pentacle of Venus, exciting passion, flame and heart combined, intense romantic energy, deep rose and gold"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ МЕРКУРИЯ (5)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-mercury-1",
        "prompt": "First Pentacle of Mercury, magical square 8x8, Mercury caduceus symbol, calling mercurial spirits, orange and silver quicksilver design"
    },
    {
        "name": "pentacle-mercury-2",
        "prompt": "Second Pentacle of Mercury, achieving impossible things, breaking barriers symbol, dynamic mercury wings, energetic orange design"
    },
    {
        "name": "pentacle-mercury-3",
        "prompt": "Third Pentacle of Mercury, summoning knowledge spirits, book and quill symbols, intellectual mercury light, scholarly design"
    },
    {
        "name": "pentacle-mercury-4",
        "prompt": "Fourth Pentacle of Mercury, knowing hidden things, revealing eye symbol, secrets unveiled, mysterious orange glow"
    },
    {
        "name": "pentacle-mercury-5",
        "prompt": "Fifth Pentacle of Mercury, opening locked doors, key and gate symbols, pathway revealing, transitional orange and silver"
    },

    # -------------------------------------------------------------------------
    # ПЕНТАКЛИ ЛУНЫ (6)
    # -------------------------------------------------------------------------
    {
        "name": "pentacle-moon-1",
        "prompt": "First Pentacle of the Moon, magical square 9x9, opening all doors, silver crescent moon, mystical doorway, lunar silver design"
    },
    {
        "name": "pentacle-moon-2",
        "prompt": "Second Pentacle of the Moon, protection from water dangers, waves and ship symbols, safe voyage, silver blue water"
    },
    {
        "name": "pentacle-moon-3",
        "prompt": "Third Pentacle of the Moon, calling rain and water, clouds and raindrops, lunar water magic, fluid silver design"
    },
    {
        "name": "pentacle-moon-4",
        "prompt": "Fourth Pentacle of the Moon, protection from water evils, defensive wave barrier, lunar shield, silvery protective aura"
    },
    {
        "name": "pentacle-moon-5",
        "prompt": "Fifth Pentacle of the Moon, answers in dreams, sleeping figure with moon above, prophetic dream symbols, violet and silver"
    },
    {
        "name": "pentacle-moon-6",
        "prompt": "Sixth Pentacle of the Moon, destruction through water, tsunami wave, lunar destructive power, dark silver and deep blue"
    },

    # -------------------------------------------------------------------------
    # АРХАНГЕЛЫ
    # -------------------------------------------------------------------------
    {
        "name": "archangel-michael",
        "prompt": "Archangel Michael, warrior angel with flaming sword, red robes, standing on dragon, solar radiance, powerful protective presence, classical religious art style"
    },
    {
        "name": "archangel-gabriel",
        "prompt": "Archangel Gabriel, angel with lily and chalice, blue robes, crescent moon, water element, gentle messenger of God, ethereal beauty"
    },
    {
        "name": "archangel-raphael",
        "prompt": "Archangel Raphael, healer angel with staff and fish, yellow golden robes, eastern wind, healing light, compassionate expression"
    },
    {
        "name": "archangel-uriel",
        "prompt": "Archangel Uriel, angel with book of wisdom and flame, green earth robes, northern guardian, grounded wisdom, autumn imagery"
    },
    {
        "name": "archangel-metatron",
        "prompt": "Archangel Metatron, angel of the presence, cube of Metatron geometry, transcendent white light, highest angelic form, sacred geometry"
    },
    {
        "name": "archangel-sandalphon",
        "prompt": "Archangel Sandalphon, twin of Metatron, feet on earth head in heaven, prayers ascending, grounding divine presence, earthy tones"
    },
    {
        "name": "archangel-tzadkiel",
        "prompt": "Archangel Tzadkiel, angel of mercy and benevolence, purple Jupiter robes, abundant blessing gesture, royal compassion"
    },
    {
        "name": "archangel-camael",
        "prompt": "Archangel Camael, angel of strength and courage, red Mars armor, divine warrior of justice, fierce but righteous"
    },
    {
        "name": "archangel-haniel",
        "prompt": "Archangel Haniel, angel of love and beauty, green Venus robes with roses, graceful feminine energy, moonlit garden"
    },
    {
        "name": "archangel-tzaphkiel",
        "prompt": "Archangel Tzaphkiel, angel of understanding, black Saturn robes, contemplative wisdom, cosmic mother energy, deep space"
    },

    # -------------------------------------------------------------------------
    # ЭЛЕМЕНТЫ
    # -------------------------------------------------------------------------
    {
        "name": "element-fire",
        "prompt": "Elemental Fire symbol, upward pointing triangle, flames and salamanders, passionate red and orange, transformative energy, alchemical fire"
    },
    {
        "name": "element-water",
        "prompt": "Elemental Water symbol, downward pointing triangle, waves and undines, flowing blue and silver, emotional depth, alchemical water"
    },
    {
        "name": "element-air",
        "prompt": "Elemental Air symbol, upward triangle with line, clouds and sylphs, light yellow and white, intellectual clarity, alchemical air"
    },
    {
        "name": "element-earth",
        "prompt": "Elemental Earth symbol, downward triangle with line, mountains and gnomes, stable brown and green, material solidity, alchemical earth"
    },
    {
        "name": "elemental-king-djinn",
        "prompt": "Djinn king of fire elementals, majestic fire spirit on throne of flames, crown of fire, commanding presence, desert palace of flame"
    },
    {
        "name": "elemental-king-nixsa",
        "prompt": "Nixsa king of water elementals, regal water spirit on coral throne, crown of pearls, underwater palace, blue and silver"
    },
    {
        "name": "elemental-king-paralda",
        "prompt": "Paralda king of air elementals, wind spirit on cloud throne, crown of feathers, sky palace, ethereal and translucent"
    },
    {
        "name": "elemental-king-ghob",
        "prompt": "Ghob king of earth elementals, sturdy earth spirit on stone throne, crown of gems, underground cavern palace, brown and green"
    },

    # -------------------------------------------------------------------------
    # РИТУАЛЬНЫЕ ИНСТРУМЕНТЫ
    # -------------------------------------------------------------------------
    {
        "name": "tool-wand",
        "prompt": "Magical wand, ceremonial rod of power, almond wood with copper bands, fire symbols engraved, glowing tip, ritual tool on altar"
    },
    {
        "name": "tool-cup",
        "prompt": "Magical chalice, silver ceremonial cup, water element symbols, blue gemstones, ritual wine vessel, sacred altar tool"
    },
    {
        "name": "tool-sword",
        "prompt": "Magical sword, ceremonial dagger, air element symbols engraved on blade, yellow handle, intellectual power, ritual weapon"
    },
    {
        "name": "tool-pentacle",
        "prompt": "Magical pentacle disk, earth element altar tool, pentagram inscribed on wooden or metal disk, material manifestation symbol"
    },
    {
        "name": "tool-lamp",
        "prompt": "Magical lamp, eternal flame vessel, spirit element symbol, golden oil lamp, divine light, illumination of temple"
    },
    {
        "name": "tool-censer",
        "prompt": "Magical censer, incense burner with chains, smoke rising, purification tool, aromatic offering, brass ceremonial design"
    },
    {
        "name": "tool-robe",
        "prompt": "Ceremonial magician robe, white linen with golden symbols, hood, sacred vestment for ritual work, pure and consecrated"
    },
    {
        "name": "tool-altar",
        "prompt": "Magical altar setup, double cube altar, four elemental tools arranged, candles lit, incense smoke, sacred workspace"
    },

    # -------------------------------------------------------------------------
    # РИТУАЛЬНЫЕ СЦЕНЫ
    # -------------------------------------------------------------------------
    {
        "name": "ritual-lbrp",
        "prompt": "Magician performing LBRP, standing in circle, drawing pentagram in blue light, archangels at four quarters, protective ritual"
    },
    {
        "name": "ritual-evocation",
        "prompt": "Evocation ritual scene, magician in circle, triangle of art outside, spirit manifesting in smoke, candles and incense, dramatic lighting"
    },
    {
        "name": "ritual-invocation",
        "prompt": "Invocation ritual, magician with arms raised, divine light descending, golden aura, spiritual possession, ecstatic state"
    },
    {
        "name": "ritual-scrying",
        "prompt": "Scrying session, magician gazing into crystal ball, visions appearing in sphere, candlelit room, mystical concentration"
    },
    {
        "name": "ritual-meditation",
        "prompt": "Middle Pillar meditation, magician in lotus position, five spheres of light along spine, energy circulation, astral body visible"
    },
    {
        "name": "ritual-consecration",
        "prompt": "Tool consecration ritual, magician blessing wand over altar, divine names spoken, light infusing the tool, sacred ceremony"
    },
    {
        "name": "ritual-circle",
        "prompt": "Magic circle from above, elaborate design with divine names, four quarters marked, protective boundary, chalk on floor"
    },
    {
        "name": "ritual-triangle",
        "prompt": "Triangle of Art with spirit manifestation, equilateral triangle with names, smoke forming entity shape, evocation scene"
    },

    # -------------------------------------------------------------------------
    # ПЛАНЕТЫ
    # -------------------------------------------------------------------------
    {
        "name": "planet-saturn",
        "prompt": "Saturn as magical planet, ringed planet with dark aura, Father Time imagery, limitation and structure, deep purple and black"
    },
    {
        "name": "planet-jupiter",
        "prompt": "Jupiter as magical planet, great benefic, expansion and luck, king of gods imagery, blue and purple with golden lightning"
    },
    {
        "name": "planet-mars",
        "prompt": "Mars as magical planet, red warrior planet, aggression and courage, sword and shield imagery, crimson and iron"
    },
    {
        "name": "planet-sun",
        "prompt": "Sun as magical planet, central luminary, vitality and success, golden solar disk with rays, brilliant yellow gold"
    },
    {
        "name": "planet-venus",
        "prompt": "Venus as magical planet, morning and evening star, love and beauty, goddess imagery, green and pink with copper"
    },
    {
        "name": "planet-mercury",
        "prompt": "Mercury as magical planet, swift messenger, intellect and communication, caduceus imagery, orange and quicksilver"
    },
    {
        "name": "planet-moon",
        "prompt": "Moon as magical planet, silver crescent and full, dreams and intuition, lunar goddess imagery, silver and violet"
    },

    # -------------------------------------------------------------------------
    # ДУХИ ГОЭТИИ (избранные 20)
    # -------------------------------------------------------------------------
    {
        "name": "goetia-bael",
        "prompt": "Goetic spirit Bael, king demon with three heads (cat, toad, man), wearing crown, power of invisibility, dark regal presence"
    },
    {
        "name": "goetia-paimon",
        "prompt": "Goetic spirit Paimon, king riding camel, crown and feminine face, preceded by musicians, arts and sciences, oriental majesty"
    },
    {
        "name": "goetia-asmodeus",
        "prompt": "Goetic spirit Asmodeus, king with three heads (bull, man, ram), serpent tail, riding dragon, treasure and mathematics"
    },
    {
        "name": "goetia-astaroth",
        "prompt": "Goetic spirit Astaroth, duke riding dragon, serpent in hand, foul breath, past and future knowledge, dark academic"
    },
    {
        "name": "goetia-bune",
        "prompt": "Goetic spirit Bune, duke with three dragon heads, eloquence and wisdom, changing dead places, wealth bringer"
    },
    {
        "name": "goetia-beleth",
        "prompt": "Goetic spirit Beleth, mighty king on pale horse, fire before him, causing love, fearsome but controllable"
    },
    {
        "name": "goetia-marbas",
        "prompt": "Goetic spirit Marbas, president appearing as lion, mechanical arts and healing, revealing secrets, noble bearing"
    },
    {
        "name": "goetia-foras",
        "prompt": "Goetic spirit Foras, president as strong man, teaching logic and herbs, finding treasure, scholarly demon"
    },
    {
        "name": "goetia-sitri",
        "prompt": "Goetic spirit Sitri, prince with leopard head and griffin wings, inflaming love and lust, revealing secrets of women"
    },
    {
        "name": "goetia-dantalion",
        "prompt": "Goetic spirit Dantalion, duke with many faces, book in hand, knowing thoughts of all, changing minds, psychological power"
    },
    {
        "name": "goetia-vassago",
        "prompt": "Goetic spirit Vassago, prince of good nature, finding lost things, telling future, helpful spirit appearance"
    },
    {
        "name": "goetia-barbatos",
        "prompt": "Goetic spirit Barbatos, duke with four kings and troops, understanding animal speech, finding treasure, woodland spirit"
    },
    {
        "name": "goetia-gusion",
        "prompt": "Goetic spirit Gusion, duke appearing as baboon, telling past present future, reconciling friends, honored diplomat"
    },
    {
        "name": "goetia-orobas",
        "prompt": "Goetic spirit Orobas, prince as horse then man, truthful answers, faithful spirit, no deception, noble equine form"
    },
    {
        "name": "goetia-amy",
        "prompt": "Goetic spirit Amy, president as flaming fire then man, astrology teaching, giving familiars, scholarly fire spirit"
    },
    {
        "name": "goetia-belial",
        "prompt": "Goetic spirit Belial, mighty king in chariot of fire, beautiful appearance, dignities and favors, powerful fallen angel"
    },
    {
        "name": "goetia-leraje",
        "prompt": "Goetic spirit Leraje, marquis as archer in green, causing battles, wounds from arrows, martial hunter"
    },
    {
        "name": "goetia-naberius",
        "prompt": "Goetic spirit Naberius, marquis as crow, restoring dignities, teaching arts, eloquent blackbird spirit"
    },
    {
        "name": "goetia-glasya-labolas",
        "prompt": "Goetic spirit Glasya-Labolas, president as winged dog, bloodshed knowledge, invisibility, fierce canine demon"
    },
    {
        "name": "goetia-zepar",
        "prompt": "Goetic spirit Zepar, duke in red armor, causing love between persons, making women barren, martial love spirit"
    },

    # -------------------------------------------------------------------------
    # СИМВОЛЫ И ЗНАКИ
    # -------------------------------------------------------------------------
    {
        "name": "symbol-pentagram",
        "prompt": "Upright pentagram star, five elements labeled, man in center, microcosm symbol, golden lines on dark background"
    },
    {
        "name": "symbol-hexagram",
        "prompt": "Hexagram Star of David, two interlaced triangles, macrocosm symbol, as above so below, silver and gold"
    },
    {
        "name": "symbol-tetragrammaton",
        "prompt": "YHVH Tetragrammaton in Hebrew letters, Yod He Vav He, burning golden letters, divine name, sacred power"
    },
    {
        "name": "symbol-caduceus",
        "prompt": "Caduceus of Hermes, two serpents around winged staff, Mercury symbol, healing and transformation, silver and gold"
    },
    {
        "name": "symbol-ankh",
        "prompt": "Egyptian Ankh symbol, key of life, loop cross, eternal life symbol, golden ancient artifact"
    },
    {
        "name": "symbol-eye-providence",
        "prompt": "Eye of Providence in triangle, all-seeing eye, divine watchfulness, rays of light, mystical surveillance"
    },
    {
        "name": "symbol-ouroboros",
        "prompt": "Ouroboros serpent eating tail, infinity and cycles, eternal return, alchemical symbol, green and gold dragon"
    },
    {
        "name": "symbol-rose-cross",
        "prompt": "Rosicrucian Rose Cross, rose blooming on cross, 22 petals for Hebrew letters, mystical Christianity symbol"
    },
    {
        "name": "symbol-sigil-template",
        "prompt": "Blank sigil template with magical rose design, Hebrew letters around petals, space for personal sigil, instructional diagram"
    },
    {
        "name": "symbol-kamea-template",
        "prompt": "Magic square kamea grid template, numbers and connecting lines, sigil creation method demonstration, instructional"
    },

    # -------------------------------------------------------------------------
    # ВЫСШЕЕ Я И ВНУТРЕННИЙ ОГОНЬ
    # -------------------------------------------------------------------------
    {
        "name": "higher-self-connection",
        "prompt": "Human figure connected to Higher Self, golden cord from crown to divine presence above, guardian angel merging with person, spiritual union"
    },
    {
        "name": "inner-fire-awakening",
        "prompt": "Person with internal fire awakening, flame in heart spreading through body, spiritual illumination, golden inner light"
    },
    {
        "name": "yechidah-spark",
        "prompt": "Divine spark Yechidah in human form, point of light in center of being, connection to Ain Soph, cosmic background"
    },
    {
        "name": "five-souls",
        "prompt": "Five levels of soul diagram, Nefesh Ruach Neshamah Chayah Yechidah, layered spiritual anatomy, ascending light"
    },
    {
        "name": "pleroma-personal",
        "prompt": "Personal Pleroma sphere, individual divine realm, creator within creation, cosmic egg of personal universe"
    },
    {
        "name": "sigil-inner-creator",
        "prompt": "Sigil of the Inner Creator, outer circle of Ain Soph Aur, seven demiurge points connected to center, personal symbol in middle"
    },
    {
        "name": "demiurge-cooperation",
        "prompt": "Multiple demiurges in cooperation, seven planetary creators working together, human demiurge among equals, creative council"
    },
    {
        "name": "ain-soph-aur",
        "prompt": "Ain Soph Aur infinite light, before creation, pure potential, limitless radiance, cosmic void of light"
    },

    # -------------------------------------------------------------------------
    # ПСАЛМЫ И МОЛИТВА
    # -------------------------------------------------------------------------
    {
        "name": "psalm-protection",
        "prompt": "Person reciting protective psalm, shield of light forming, Psalm 91 text floating, divine protection visualization"
    },
    {
        "name": "psalm-healing",
        "prompt": "Healing psalm recitation, green healing light, Raphael presence, restoration energy, peaceful recovery scene"
    },
    {
        "name": "prayer-direct",
        "prompt": "Direct prayer to Source, person with upraised hands, vertical beam of light, no intermediaries, pure connection"
    },
    {
        "name": "vibration-names",
        "prompt": "Vibrating divine names, sound waves emanating from mouth, Hebrew letters forming in air, sonic magic"
    },

    # -------------------------------------------------------------------------
    # СОВРЕМЕННЫЕ ПРАКТИКИ
    # -------------------------------------------------------------------------
    {
        "name": "modern-urban-magic",
        "prompt": "Urban magician in city apartment, small altar in corner, candles and incense, modern magical practice, night city view"
    },
    {
        "name": "modern-digital-sigil",
        "prompt": "Digital sigil on computer screen, glowing magical symbol, modern sigil magic, technology and occultism fusion"
    },
    {
        "name": "modern-quick-ritual",
        "prompt": "Quick protection ritual in public space, subtle hand gesture, invisible shield forming, discrete modern magic"
    },
    {
        "name": "modern-meditation-commute",
        "prompt": "Meditation during commute, person in subway with closed eyes, subtle aura visible, daily spiritual practice"
    },

    # -------------------------------------------------------------------------
    # ЗАЩИТА И ИЗГНАНИЕ
    # -------------------------------------------------------------------------
    {
        "name": "protection-sphere",
        "prompt": "Protective sphere around person, white light bubble, impenetrable barrier, safe within chaos, shielded figure"
    },
    {
        "name": "banishing-ritual",
        "prompt": "Banishing unwanted entity, commanding gesture, spirit dissolving, blue pentagram flames, cleansing energy"
    },
    {
        "name": "home-warding",
        "prompt": "Home protection ward, house surrounded by light, salt at doorway, protective symbols above entrance, safe dwelling"
    },
    {
        "name": "energy-cleansing",
        "prompt": "Energy cleansing with sage smoke, negative energy dispersing, purification ritual, cleansed space"
    },

    # -------------------------------------------------------------------------
    # ЛУНА И ВРЕМЯ
    # -------------------------------------------------------------------------
    {
        "name": "moon-phases",
        "prompt": "All moon phases in sequence, new to full to new, lunar cycle diagram, silver moons on dark background"
    },
    {
        "name": "planetary-hours",
        "prompt": "Planetary hours wheel diagram, seven planets arranged by day, Chaldean order, timing magic, astrological clock"
    },
    {
        "name": "solar-year",
        "prompt": "Solar year wheel, eight sabbats, solstices and equinoxes, seasonal magic diagram, wheel of the year"
    },

    # -------------------------------------------------------------------------
    # ДОПОЛНИТЕЛЬНЫЕ ИЛЛЮСТРАЦИИ
    # -------------------------------------------------------------------------
    {
        "name": "magician-study",
        "prompt": "Magician in study surrounded by books, grimoires and scrolls, candlelit workspace, scholarly occultist"
    },
    {
        "name": "temple-setup",
        "prompt": "Complete temple room setup, altar in east, pillars, elemental quarters, proper magical workspace"
    },
    {
        "name": "vision-astral",
        "prompt": "Astral vision experience, spirit leaving body, silver cord visible, astral plane visible, out of body"
    },
    {
        "name": "initiation-ceremony",
        "prompt": "Magical initiation ceremony, candidate blindfolded, officers in robes, dramatic moment of revelation"
    },
    {
        "name": "book-open-grimoire",
        "prompt": "Open grimoire page, illustrated magical manuscript, symbols and text, aged parchment, candlelight"
    },
    {
        "name": "seance-spirit",
        "prompt": "Spirit communication session, ghostly presence manifesting, medium in trance, ectoplasm forming"
    },
    {
        "name": "alchemy-transformation",
        "prompt": "Alchemical transformation, lead to gold, philosopher stone, great work completion, transmutation"
    },
    {
        "name": "kundalini-rising",
        "prompt": "Kundalini energy rising, serpent of fire ascending spine, chakras igniting, spiritual awakening"
    },
    {
        "name": "merkaba-vehicle",
        "prompt": "Merkaba light vehicle, two interlocked tetrahedrons, ascension vehicle, sacred geometry body of light"
    },
    {
        "name": "angel-human-contact",
        "prompt": "Angel touching human, moment of divine contact, light transferring, spiritual transmission, sacred meeting"
    },
]

# ============================================================================
# ФУНКЦИИ ГЕНЕРАЦИИ
# ============================================================================

def http_post_json(url, data, timeout=60):
    result = subprocess.run([
        'curl', '-s', '--noproxy', '*', '-m', str(timeout),
        '-X', 'POST', '-H', 'Content-Type: application/json',
        '-d', json.dumps(data), url
    ], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return {}
    return {}

def http_get(url, timeout=30):
    result = subprocess.run([
        'curl', '-s', '--noproxy', '*', '-m', str(timeout), url
    ], capture_output=True, text=True)
    if result.returncode == 0 and result.stdout:
        try:
            return json.loads(result.stdout)
        except:
            return {}
    return {}

def http_get_binary(url, timeout=60):
    result = subprocess.run([
        'curl', '-s', '--noproxy', '*', '-m', str(timeout), url
    ], capture_output=True)
    return result.stdout

def generate_image(img_info, retry=3):
    name = img_info["name"]
    prompt = img_info["prompt"]

    out_path = OUTPUT_DIR / f"{name}.png"
    if out_path.exists():
        print(f"SKIP (exists): {name}")
        return True

    print(f"Generating: {name}")

    for attempt in range(retry):
        workflow = create_workflow(prompt)
        response = http_post_json(f"{COMFYUI_URL}/prompt", {"prompt": workflow})
        prompt_id = response.get("prompt_id")

        if not prompt_id:
            print(f"  Attempt {attempt+1}: Failed to queue")
            time.sleep(2)
            continue

        # Ожидание результата
        start = time.time()
        while time.time() - start < 300:
            history = http_get(f"{COMFYUI_URL}/history/{prompt_id}")
            if prompt_id in history:
                outputs = history[prompt_id].get("outputs", {})
                for node_id, output in outputs.items():
                    if "images" in output:
                        for img in output["images"]:
                            params = urlencode({
                                "filename": img["filename"],
                                "subfolder": img.get("subfolder", ""),
                                "type": img.get("type", "output")
                            })
                            img_data = http_get_binary(f"{COMFYUI_URL}/view?{params}")
                            if img_data:
                                out_path.write_bytes(img_data)
                                print(f"  SUCCESS: {out_path}")
                                return True
            time.sleep(2)

        print(f"  Attempt {attempt+1}: Timeout")

    print(f"  FAILED: {name}")
    return False

def convert_to_jpeg():
    """Конвертация PNG в JPEG с сжатием"""
    try:
        from PIL import Image
    except ImportError:
        print("PIL not installed, skipping conversion")
        return

    print("\nConverting PNG to JPEG...")
    for png_path in OUTPUT_DIR.glob("*.png"):
        jpg_path = png_path.with_suffix(".jpg")
        try:
            img = Image.open(png_path)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            img.save(jpg_path, 'JPEG', quality=85, optimize=True)
            png_path.unlink()
            print(f"  Converted: {jpg_path.name}")
        except Exception as e:
            print(f"  Error converting {png_path.name}: {e}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys

    print(f"Total images to generate: {len(IMAGES)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Проверка ComfyUI
    try:
        response = http_get(f"{COMFYUI_URL}/system_stats")
        if not response:
            print("ERROR: ComfyUI not responding. Start it first:")
            print("  wsl -d Ubuntu-24.04 -- bash -c 'cd ~/ComfyUI && python main.py --port 8190'")
            sys.exit(1)
    except:
        print("ERROR: Cannot connect to ComfyUI")
        sys.exit(1)

    print("ComfyUI connected!\n")

    # Генерация
    success = 0
    failed = 0

    for i, img in enumerate(IMAGES):
        print(f"[{i+1}/{len(IMAGES)}] ", end="")
        if generate_image(img):
            success += 1
        else:
            failed += 1
        time.sleep(1)  # Пауза между генерациями

    print(f"\n\nDone! Success: {success}, Failed: {failed}")

    # Конвертация
    convert_to_jpeg()

    print("\nImages ready in:", OUTPUT_DIR)
