"""Battle system with Active Time Battle (ATB) mechanics."""
import random
from typing import Optional, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from characters import Character, Spell, SPELLS


class Battle:
    """Battle class handling ATB turn logic and combat."""
    
    def __init__(self, player: Character, enemy: Character, console: Console):
        """Initialize battle.
        
        Args:
            player: Player character
            enemy: Enemy character
            console: Rich console for output
        """
        self.player = player
        self.enemy = enemy
        self.console = console
        self.turn_count = 0
        self.battle_log = []
        
    def display_status(self):
        """Display battle status using rich formatting."""
        # Create status table
        table = Table(show_header=True, header_style="bold magenta", expand=True)
        table.add_column("Character", style="cyan", width=20)
        table.add_column("HP", style="green", width=20)
        table.add_column("MP", style="blue", width=20)
        table.add_column("ATB", style="yellow", width=15)
        
        # Player row
        player_hp = f"{self.player.hp}/{self.player.max_hp}"
        player_mp = f"{self.player.mp}/{self.player.max_mp}"
        player_atb = f"{self.player.atb_gauge}/100"
        
        player_hp_color = "green" if self.player.hp > self.player.max_hp * 0.5 else "yellow" if self.player.hp > self.player.max_hp * 0.25 else "red"
        table.add_row(
            f"[bold cyan]{self.player.name}[/bold cyan]",
            f"[{player_hp_color}]{player_hp}[/{player_hp_color}]",
            f"[blue]{player_mp}[/blue]",
            f"[yellow]{player_atb}[/yellow]"
        )
        
        # Enemy row
        enemy_hp = f"{self.enemy.hp}/{self.enemy.max_hp}"
        enemy_mp = f"{self.enemy.mp}/{self.enemy.max_mp}"
        enemy_atb = f"{self.enemy.atb_gauge}/100"
        enemy_weakness_str = f" (Weak: {self.enemy.weakness})" if self.enemy.weakness else ""
        
        enemy_hp_color = "green" if self.enemy.hp > self.enemy.max_hp * 0.5 else "yellow" if self.enemy.hp > self.enemy.max_hp * 0.25 else "red"
        table.add_row(
            f"[bold red]{self.enemy.name}[/bold red]{enemy_weakness_str}",
            f"[{enemy_hp_color}]{enemy_hp}[/{enemy_hp_color}]",
            f"[blue]{enemy_mp}[/blue]",
            f"[yellow]{enemy_atb}[/yellow]"
        )
        
        self.console.print(table)
        
    def display_battle_log(self):
        """Display recent battle actions."""
        if self.battle_log:
            log_text = "\n".join(self.battle_log[-5:])  # Show last 5 actions
            self.console.print(Panel(log_text, title="[bold]Battle Log[/bold]", border_style="blue"))
    
    def log_action(self, message: str):
        """Add message to battle log.
        
        Args:
            message: Message to log
        """
        self.battle_log.append(message)
        
    def player_attack(self) -> Tuple[bool, str]:
        """Execute player physical attack.
        
        Returns:
            Tuple of (success, message)
        """
        # Calculate damage with some randomness
        base_damage = self.player.strength + random.randint(0, 5)
        damage = self.enemy.take_damage(base_damage)
        
        message = f"[cyan]{self.player.name}[/cyan] attacks for [red]{damage}[/red] damage!"
        self.log_action(message)
        return True, message
    
    def player_magic(self, spell_name: str) -> Tuple[bool, str]:
        """Execute player magic attack.
        
        Args:
            spell_name: Name of spell to cast
            
        Returns:
            Tuple of (success, message)
        """
        if spell_name not in SPELLS:
            return False, f"Unknown spell: {spell_name}"
        
        spell = SPELLS[spell_name]
        
        # Check MP
        if not self.player.use_mp(spell.mp_cost):
            message = f"[yellow]Not enough MP to cast {spell.name}![/yellow]"
            return False, message
        
        # Calculate damage or healing
        if spell.element == "healing":
            heal_amount = self.player.heal(spell.power)
            message = f"[cyan]{self.player.name}[/cyan] casts [green]{spell.name}[/green] and recovers [green]{heal_amount}[/green] HP!"
        else:
            damage = spell.calculate_damage(self.player.magic, self.enemy.weakness)
            actual_damage = self.enemy.take_damage(damage)
            
            weakness_bonus = ""
            if spell.element and self.enemy.weakness and spell.element.lower() == self.enemy.weakness.lower():
                weakness_bonus = " [bold yellow]WEAKNESS![/bold yellow]"
            
            message = f"[cyan]{self.player.name}[/cyan] casts [magenta]{spell.name}[/magenta] for [red]{actual_damage}[/red] damage!{weakness_bonus}"
        
        self.log_action(message)
        return True, message
    
    def enemy_turn(self) -> str:
        """Execute enemy turn with simple AI.
        
        Returns:
            Action message
        """
        # Simple AI: 70% attack, 30% magic if enough MP
        action = random.random()
        
        if action < 0.7 or self.enemy.mp < 10:
            # Physical attack
            base_damage = self.enemy.strength + random.randint(0, 5)
            damage = self.player.take_damage(base_damage)
            message = f"[red]{self.enemy.name}[/red] attacks for [red]{damage}[/red] damage!"
        else:
            # Cast a random spell
            spell = random.choice(list(SPELLS.values()))
            if self.enemy.use_mp(spell.mp_cost):
                if spell.element == "healing":
                    heal_amount = self.enemy.heal(spell.power)
                    message = f"[red]{self.enemy.name}[/red] casts [green]{spell.name}[/green] and recovers [green]{heal_amount}[/green] HP!"
                else:
                    damage = spell.calculate_damage(self.enemy.magic, self.player.weakness)
                    actual_damage = self.player.take_damage(damage)
                    message = f"[red]{self.enemy.name}[/red] casts [magenta]{spell.name}[/magenta] for [red]{actual_damage}[/red] damage!"
            else:
                # Fallback to attack if not enough MP
                base_damage = self.enemy.strength + random.randint(0, 5)
                damage = self.player.take_damage(base_damage)
                message = f"[red]{self.enemy.name}[/red] attacks for [red]{damage}[/red] damage!"
        
        self.log_action(message)
        return message
    
    def update_atb_gauges(self):
        """Update ATB gauges for both characters based on speed."""
        self.player.update_atb()
        self.enemy.update_atb()
    
    def get_action_choice(self) -> Optional[str]:
        """Get player's action choice.
        
        Returns:
            Action string or None if invalid
        """
        self.console.print("\n[bold yellow]Your turn![/bold yellow]")
        self.console.print("1. Attack")
        self.console.print("2. Magic")
        self.console.print("3. Wait (skip turn)")
        
        choice = Prompt.ask("\nChoose action", choices=["1", "2", "3"], default="1")
        
        if choice == "1":
            return "attack"
        elif choice == "2":
            return "magic"
        elif choice == "3":
            return "wait"
        else:
            return None
    
    def get_spell_choice(self) -> Optional[str]:
        """Get player's spell choice.
        
        Returns:
            Spell name or None if cancelled
        """
        self.console.print("\n[bold magenta]Available Spells:[/bold magenta]")
        spell_list = list(SPELLS.keys())
        for i, spell_name in enumerate(spell_list, 1):
            spell = SPELLS[spell_name]
            self.console.print(f"{i}. {spell}")
        self.console.print(f"{len(spell_list) + 1}. Cancel")
        
        choices = [str(i) for i in range(1, len(spell_list) + 2)]
        choice = Prompt.ask(
            f"\nChoose spell",
            choices=choices,
            default=str(len(spell_list) + 1)
        )
        
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(spell_list):
                return spell_list[choice_num - 1]
            elif choice_num == len(spell_list) + 1:
                return None
        except ValueError:
            pass
        
        return None
    
    def run(self) -> bool:
        """Run the battle loop.
        
        Returns:
            True if player wins, False if player loses
        """
        self.console.print(Panel.fit(
            f"[bold red]Battle Start![/bold red]\n\n"
            f"[cyan]{self.player.name}[/cyan] vs [red]{self.enemy.name}[/red]",
            border_style="red"
        ))
        
        while self.player.is_alive() and self.enemy.is_alive():
            self.turn_count += 1
            self.console.print(f"\n[bold]--- Turn {self.turn_count} ---[/bold]")
            
            # Update ATB gauges
            self.update_atb_gauges()
            
            # Display status
            self.display_status()
            self.display_battle_log()
            
            # Check whose turn it is
            player_ready = self.player.atb_gauge >= 100
            enemy_ready = self.enemy.atb_gauge >= 100
            
            if player_ready and enemy_ready:
                # Both ready, speed determines order
                if self.player.speed >= self.enemy.speed:
                    # Player goes first
                    if not self.execute_player_turn():
                        continue
                    if not self.enemy.is_alive():
                        break
                    self.execute_enemy_turn()
                else:
                    # Enemy goes first
                    self.execute_enemy_turn()
                    if not self.player.is_alive():
                        break
                    if not self.execute_player_turn():
                        continue
            elif player_ready:
                if not self.execute_player_turn():
                    continue
            elif enemy_ready:
                self.execute_enemy_turn()
            else:
                # Neither ready, continue updating gauges
                self.console.print("[dim]Gauges charging...[/dim]")
                continue
        
        # Battle ended
        self.console.print("\n")
        if self.player.is_alive():
            self.console.print(Panel.fit(
                "[bold green]Victory![/bold green]\n\n"
                f"You defeated the [red]{self.enemy.name}[/red]!",
                border_style="green"
            ))
            return True
        else:
            self.console.print(Panel.fit(
                "[bold red]Defeat![/bold red]\n\n"
                f"You were defeated by the [red]{self.enemy.name}[/red]...",
                border_style="red"
            ))
            return False
    
    def execute_player_turn(self) -> bool:
        """Execute player's turn.
        
        Returns:
            True if turn was executed, False if cancelled/wait
        """
        action = self.get_action_choice()
        
        if action == "attack":
            success, message = self.player_attack()
            self.console.print(message)
            self.player.reset_atb()
            return True
        elif action == "magic":
            spell_choice = self.get_spell_choice()
            if spell_choice:
                success, message = self.player_magic(spell_choice)
                self.console.print(message)
                if success:
                    self.player.reset_atb()
                    return True
                return False
            return False
        elif action == "wait":
            self.console.print("[yellow]You wait...[/yellow]")
            self.player.reset_atb()
            return True
        else:
            self.console.print("[red]Invalid choice![/red]")
            return False
    
    def execute_enemy_turn(self):
        """Execute enemy's turn."""
        message = self.enemy_turn()
        self.console.print(message)
        self.enemy.reset_atb()
