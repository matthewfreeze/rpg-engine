"""AI integration for dynamic enemy generation using Gemini API."""
import os
import json
from typing import Dict, Optional
import google.generativeai as genai


def initialize_gemini() -> Optional[genai.GenerativeModel]:
    """Initialize Gemini API with API key from environment.
    
    Returns:
        GenerativeModel instance or None if API key not found
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')


def generate_enemy(biome: str) -> Dict[str, any]:
    """Generate a random enemy based on biome using Gemini API.
    
    Args:
        biome: The biome/location for the enemy (e.g., 'Magitek Factory', 'Floating Continent')
        
    Returns:
        Dictionary with enemy data including name, description, stats, and weakness
    """
    model = initialize_gemini()
    
    # Fallback enemy if API not available
    fallback_enemies = {
        "Magitek Factory": {
            "name": "Magitek Armor",
            "description": "A mechanical soldier powered by magical energy, its metal frame glows with an eerie blue light.",
            "hp": 80,
            "mp": 20,
            "strength": 15,
            "magic": 12,
            "speed": 8,
            "weakness": "thunder"
        },
        "Floating Continent": {
            "name": "Sky Serpent",
            "description": "A winged serpent that rides the wind currents high above the clouds.",
            "hp": 70,
            "mp": 30,
            "strength": 12,
            "magic": 16,
            "speed": 10,
            "weakness": "ice"
        }
    }
    
    if not model:
        # Use fallback enemy if API key not available
        return fallback_enemies.get(biome, {
            "name": "Wild Beast",
            "description": "A mysterious creature that lurks in the shadows.",
            "hp": 60,
            "mp": 15,
            "strength": 14,
            "magic": 10,
            "speed": 9,
            "weakness": "fire"
        })
    
    try:
        prompt = f"""Generate a random enemy for a Final Fantasy VI-inspired RPG. The enemy should fit the biome: {biome}.

Please provide the following in JSON format:
- name: A creative enemy name fitting the biome
- description: A brief atmospheric description (1-2 sentences)
- hp: Health points (between 50-100)
- mp: Magic points (between 10-40)
- strength: Physical attack power (between 8-20)
- magic: Magical power (between 8-20)
- speed: Speed stat for turn order (between 5-15)
- weakness: Elemental weakness (choose from: fire, ice, thunder)

Return only valid JSON without any markdown formatting or code blocks."""

        response = model.generate_content(prompt)
        
        # Parse JSON response
        result_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if result_text.startswith("```"):
            result_text = result_text.split("```")[1]
            if result_text.startswith("json"):
                result_text = result_text[4:]
            result_text = result_text.strip()
        
        enemy_data = json.loads(result_text)
        
        # Validate required fields
        required_fields = ["name", "description", "hp", "mp", "strength", "magic", "speed", "weakness"]
        if all(field in enemy_data for field in required_fields):
            return enemy_data
        else:
            # Missing fields, use fallback
            return fallback_enemies.get(biome, fallback_enemies["Magitek Factory"])
            
    except Exception as e:
        # On any error, use fallback enemy
        print(f"Error generating enemy with AI: {e}")
        return fallback_enemies.get(biome, fallback_enemies["Magitek Factory"])


def generate_enemy_simple(biome: str) -> Dict[str, any]:
    """Generate enemy without AI (for testing or when API unavailable).
    
    Args:
        biome: The biome/location for the enemy
        
    Returns:
        Dictionary with enemy data
    """
    enemies = {
        "Magitek Factory": {
            "name": "Magitek Armor",
            "description": "A mechanical soldier powered by magical energy, its metal frame glows with an eerie blue light.",
            "hp": 80,
            "mp": 20,
            "strength": 15,
            "magic": 12,
            "speed": 8,
            "weakness": "thunder"
        },
        "Floating Continent": {
            "name": "Sky Serpent",
            "description": "A winged serpent that rides the wind currents high above the clouds.",
            "hp": 70,
            "mp": 30,
            "strength": 12,
            "magic": 16,
            "speed": 10,
            "weakness": "ice"
        },
        "World of Ruin": {
            "name": "Doom Gaze",
            "description": "A spectral entity that feeds on despair, its form constantly shifting and flickering.",
            "hp": 90,
            "mp": 35,
            "strength": 18,
            "magic": 14,
            "speed": 7,
            "weakness": "fire"
        }
    }
    
    return enemies.get(biome, {
        "name": "Wild Beast",
        "description": "A mysterious creature that lurks in the shadows.",
        "hp": 60,
        "mp": 15,
        "strength": 14,
        "magic": 10,
        "speed": 9,
        "weakness": "fire"
    })
