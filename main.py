#!/usr/bin/env python3
"""Main entry point for the RPG Engine."""
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from characters import Character
from battle import Battle
from ai import generate_enemy


def create_player() -> Character:
    """Create the player character with predefined stats.
    
    Returns:
        Player character instance
    """
    # Create a balanced player character
    return Character(
        name="Terra",
        hp=100,
        mp=50,
        strength=16,
        magic=18,
        speed=12
    )


def display_intro(console: Console):
    """Display game introduction.
    
    Args:
        console: Rich console for output
    """
    intro_text = Text()
    intro_text.append("╔═══════════════════════════════════════╗\n", style="bold cyan")
    intro_text.append("║   ", style="bold cyan")
    intro_text.append("FINAL FANTASY VI", style="bold yellow")
    intro_text.append(" - RPG ENGINE   ║\n", style="bold cyan")
    intro_text.append("╚═══════════════════════════════════════╝", style="bold cyan")
    
    console.print(intro_text)
    console.print()
    console.print(Panel.fit(
        "[bold white]Welcome to a world of magic and machinery![/bold white]\n\n"
        "In this Active Time Battle system, your turns are\n"
        "determined by your Speed stat. Choose your actions\n"
        "wisely and exploit enemy weaknesses!",
        border_style="magenta",
        title="[bold]Introduction[/bold]"
    ))
    console.print()


def select_biome(console: Console) -> str:
    """Let player select a biome for the battle.
    
    Args:
        console: Rich console for output
        
    Returns:
        Selected biome name
    """
    biomes = [
        "Magitek Factory",
        "Floating Continent",
        "World of Ruin",
        "Vector Imperial Base",
        "Phantom Forest"
    ]
    
    console.print("[bold yellow]Select a biome for your battle:[/bold yellow]\n")
    for i, biome in enumerate(biomes, 1):
        console.print(f"  {i}. [cyan]{biome}[/cyan]")
    
    while True:
        choice = Prompt.ask(
            "\nEnter biome number",
            choices=[str(i) for i in range(1, len(biomes) + 1)],
            default="1"
        )
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(biomes):
                return biomes[index]
        except ValueError:
            pass
        
        console.print("[red]Invalid choice. Please try again.[/red]")


def main():
    """Main game loop."""
    console = Console()
    
    # Display intro
    display_intro(console)
    
    # Create player
    player = create_player()
    console.print(f"[bold green]You are playing as:[/bold green] [cyan]{player.name}[/cyan]")
    console.print(f"  HP: {player.max_hp} | MP: {player.max_mp} | STR: {player.strength} | "
                  f"MAG: {player.magic} | SPD: {player.speed}\n")
    
    # Select biome
    biome = select_biome(console)
    console.print(f"\n[bold]You venture into the [magenta]{biome}[/magenta]...[/bold]\n")
    
    # Generate enemy using AI
    console.print("[dim]Generating enemy...[/dim]")
    enemy_data = generate_enemy(biome)
    
    # Create enemy character
    enemy = Character(
        name=enemy_data["name"],
        hp=enemy_data["hp"],
        mp=enemy_data["mp"],
        strength=enemy_data["strength"],
        magic=enemy_data["magic"],
        speed=enemy_data["speed"]
    )
    enemy.weakness = enemy_data.get("weakness")
    
    # Display enemy
    console.print(Panel.fit(
        f"[bold red]{enemy.name}[/bold red]\n\n"
        f"{enemy_data['description']}\n\n"
        f"[yellow]Weakness:[/yellow] [magenta]{enemy.weakness}[/magenta]",
        border_style="red",
        title="[bold]Enemy Encountered![/bold]"
    ))
    console.print()
    
    # Start battle
    battle = Battle(player, enemy, console)
    victory = battle.run()
    
    # Game over
    console.print()
    if victory:
        console.print("[bold green]Thank you for playing![/bold green]")
    else:
        console.print("[bold yellow]Better luck next time...[/bold yellow]")


if __name__ == "__main__":
    main()
