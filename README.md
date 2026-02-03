# RPG Engine

A text-based RPG inspired by Final Fantasy VI with an Active Time Battle (ATB) system.

## Features

- **Active Time Battle (ATB) System**: Turn order determined by Speed stat
- **Character Stats**: HP, MP, Strength, Magic, and Speed
- **Elemental Magic System**: Fire, Ice, Thunder, and Cure spells
- **Enemy Weakness System**: Exploit elemental weaknesses for double damage
- **AI-Generated Enemies**: Uses Gemini API to create dynamic enemies based on biome
- **Rich Terminal UI**: Colorful and retro terminal output using the `rich` library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/matthewfreeze/rpg-engine.git
cd rpg-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up Gemini API for dynamic enemy generation:
```bash
export GEMINI_API_KEY=your_api_key_here
```

Note: If you don't set up a Gemini API key, the game will use predefined fallback enemies.

## Usage

Run the game:
```bash
python main.py
```

### Game Controls

1. **Select a Biome**: Choose from various locations like Magitek Factory, Floating Continent, etc.
2. **Battle Actions**:
   - **Attack**: Physical attack based on Strength stat
   - **Magic**: Cast elemental spells (costs MP)
   - **Wait**: Skip turn and reset ATB gauge

### Combat Tips

- Watch the ATB gauge - when it reaches 100, you can take your turn
- Characters with higher Speed stats fill their ATB gauge faster
- Exploit enemy weaknesses with matching elemental spells for 2x damage
- Manage your MP carefully - spells are powerful but limited by your MP pool

## Project Structure

```
rpg-engine/
├── main.py          # Entry point with game loop
├── characters.py    # Character and Spell classes
├── battle.py        # Battle system with ATB logic
├── ai.py            # Gemini API integration for enemy generation
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Code Overview

### Characters (`characters.py`)

- **Character Class**: Base class with HP, MP, Strength, Magic, Speed stats
- **Spell Class**: Magic spells with MP cost, power, and elemental types
- **ATB System**: Characters have ATB gauges that fill based on Speed

### Battle System (`battle.py`)

- **ATB Turn Logic**: Gauges fill each turn, character acts when gauge reaches 100
- **Combat Actions**: Attack, Magic casting, and Wait
- **Battle Log**: Tracks recent actions
- **Rich UI**: Colorful tables showing HP, MP, and ATB status

### AI Integration (`ai.py`)

- **Gemini API**: Generates unique enemies based on biome input
- **Fallback System**: Predefined enemies if API is unavailable
- **Dynamic Stats**: Enemy stats, descriptions, and weaknesses vary by location

## Example Battle

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Character               ┃ HP         ┃ MP         ┃ ATB      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Terra                   │ 100/100    │ 50/50      │ 100/100  │
│ Magitek Armor (Weak:    │ 80/80      │ 20/20      │ 72/100   │
│ thunder)                │            │            │          │
└─────────────────────────┴────────────┴────────────┴──────────┘

Your turn!
1. Attack
2. Magic
3. Wait (skip turn)
```

## Technologies Used

- **Python 3**: Core programming language
- **Rich**: Terminal UI library for colorful output
- **Google Generative AI**: Gemini API for dynamic content generation

## License

MIT License - Feel free to use and modify!