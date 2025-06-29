#!/usr/bin/env python3
"""
Image Memory Match Game

A 4x4 grid memory matching game with image cards.
Features animations, move counter, timer, and win detection.
"""

import pygame
import random
import time
import sys
import os
from typing import List, Tuple, Optional, Dict
from enum import Enum


class CardState(Enum):
    """Enum representing the different states a card can be in."""
    HIDDEN = "hidden"
    REVEALED = "revealed"
    MATCHED = "matched"
    FLIPPING = "flipping"


class Card:
    """Represents a single card in the memory game."""
    
    def __init__(self, image_id: str, image_surface: pygame.Surface, row: int, col: int):
        self.image_id = image_id
        self.image_surface = image_surface
        self.row = row
        self.col = col
        self.state = CardState.HIDDEN
        self.flip_animation_progress = 0.0
        self.match_animation_progress = 0.0
    
    def start_flip_animation(self):
        """Start the flip animation for this card."""
        self.state = CardState.FLIPPING
        self.flip_animation_progress = 0.0
    
    def update_flip_animation(self, dt: float) -> bool:
        """Update flip animation. Returns True when animation is complete."""
        if self.state == CardState.FLIPPING:
            self.flip_animation_progress += dt * 8.0  # Animation speed
            if self.flip_animation_progress >= 1.0:
                self.flip_animation_progress = 1.0
                self.state = CardState.REVEALED
                return True
        return False
    
    def start_match_animation(self):
        """Start the match animation for this card."""
        self.match_animation_progress = 0.0
    
    def update_match_animation(self, dt: float) -> bool:
        """Update match animation. Returns True when animation is complete."""
        if self.state == CardState.MATCHED:
            self.match_animation_progress += dt * 4.0  # Animation speed
            if self.match_animation_progress >= 1.0:
                self.match_animation_progress = 1.0
                return True
        return False


class MemoryGame:
    """Main game class handling game logic and state."""
    
    # Game constants
    GRID_SIZE = 4
    CARD_SIZE = 100
    CARD_MARGIN = 10
    WINDOW_WIDTH = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN + 200
    WINDOW_HEIGHT = GRID_SIZE * (CARD_SIZE + CARD_MARGIN) - CARD_MARGIN + 150
    
    # Colors
    COLOR_BACKGROUND = (40, 40, 40)
    COLOR_CARD_HIDDEN = (70, 130, 180)
    COLOR_CARD_REVEALED = (255, 255, 255)
    COLOR_CARD_MATCHED = (60, 179, 113)
    COLOR_TEXT = (255, 255, 255)
    COLOR_WIN_TEXT = (255, 215, 0)
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Image Memory Match")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        # Load images
        self.images = self.load_images()
        
        # Game state
        self.cards: List[List[Card]] = []
        self.revealed_cards: List[Card] = []
        self.moves = 0
        self.start_time = None
        self.game_won = False
        self.mismatch_timer = 0.0
        self.showing_mismatch = False
        
        self.setup_game()
    
    def load_images(self) -> Dict[str, pygame.Surface]:
        """Load and scale images from the images directory."""
        images = {}
        image_dir = "/home/ell/q/images"
        
        # Define the image files we want to use (now we have 8 unique images)
        image_files = ["1.jpg", "2.png", "3.png", "6.jpg", "9.jpg", "11.png", "12.jpg", "13.jpg"]
        
        for filename in image_files:
            filepath = os.path.join(image_dir, filename)
            if os.path.exists(filepath):
                try:
                    # Load image
                    image = pygame.image.load(filepath)
                    # Scale to fit card size with some padding
                    scaled_image = pygame.transform.scale(image, (self.CARD_SIZE - 10, self.CARD_SIZE - 10))
                    images[filename] = scaled_image
                    print(f"Loaded image: {filename}")
                except pygame.error as e:
                    print(f"Could not load image {filename}: {e}")
        
        if len(images) < 8:
            print(f"Warning: Only {len(images)} images loaded, need 8 for optimal gameplay.")
            # Create fallback colored rectangles if needed
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), 
                     (255, 0, 255), (0, 255, 255), (128, 128, 128), (255, 128, 0)]
            for i in range(len(images), 8):
                surface = pygame.Surface((self.CARD_SIZE - 10, self.CARD_SIZE - 10))
                surface.fill(colors[i])
                images[f"fallback_{i}"] = surface
        
        return images
    
    def setup_game(self):
        """Set up a new game by creating and shuffling cards."""
        # Get all available image keys
        image_keys = list(self.images.keys())
        
        # We now have exactly 8 unique images, so no repetition needed!
        # Each image will appear exactly twice (8 images × 2 = 16 cards for 4×4 grid)
        if len(image_keys) >= 8:
            # Use exactly 8 unique images
            selected_images = image_keys[:8]
        else:
            # Fallback: repeat images if we don't have enough
            selected_images = []
            for i in range(8):
                selected_images.append(image_keys[i % len(image_keys)])
        
        # Create pairs - each image appears exactly twice
        image_pairs = selected_images * 2  # Each image appears twice
        random.shuffle(image_pairs)
        
        # Create card grid
        self.cards = []
        image_index = 0
        
        for row in range(self.GRID_SIZE):
            card_row = []
            for col in range(self.GRID_SIZE):
                image_key = image_pairs[image_index]
                image_surface = self.images[image_key]
                
                # Use the image key directly as the ID (no need for unique suffixes)
                card = Card(image_key, image_surface, row, col)
                card_row.append(card)
                image_index += 1
            self.cards.append(card_row)
        
        # Reset game state
        self.revealed_cards = []
        self.moves = 0
        self.start_time = None
        self.game_won = False
        self.mismatch_timer = 0.0
        self.showing_mismatch = False
    
    def get_card_rect(self, row: int, col: int) -> pygame.Rect:
        """Get the rectangle for a card at the given position."""
        x = col * (self.CARD_SIZE + self.CARD_MARGIN)
        y = row * (self.CARD_SIZE + self.CARD_MARGIN) + 100  # Offset for UI
        return pygame.Rect(x, y, self.CARD_SIZE, self.CARD_SIZE)
    
    def handle_card_click(self, pos: Tuple[int, int]):
        """Handle clicking on a card."""
        if self.game_won or self.showing_mismatch:
            return
        
        # Find which card was clicked
        for row in range(self.GRID_SIZE):
            for col in range(self.GRID_SIZE):
                card_rect = self.get_card_rect(row, col)
                if card_rect.collidepoint(pos):
                    card = self.cards[row][col]
                    
                    # Only allow clicking on hidden cards (not matched or already revealed)
                    if card.state == CardState.HIDDEN:
                        self.reveal_card(card)
                    # Matched cards are blocked and cannot be clicked
                    return
    
    def reveal_card(self, card: Card):
        """Reveal a card and handle game logic."""
        # Start timer on first card flip
        if self.start_time is None:
            self.start_time = time.time()
        
        # Start flip animation
        card.start_flip_animation()
        self.revealed_cards.append(card)
        
        # Check if we have two revealed cards
        if len(self.revealed_cards) == 2:
            self.moves += 1
            
            # Check for match after a short delay to show both cards
            card1, card2 = self.revealed_cards
            if card1.image_id == card2.image_id:
                # Match found
                card1.state = CardState.MATCHED
                card2.state = CardState.MATCHED
                card1.start_match_animation()
                card2.start_match_animation()
                self.revealed_cards = []
                
                # Check for win condition
                self.check_win()
            else:
                # No match - will hide cards after delay
                self.showing_mismatch = True
                self.mismatch_timer = 1.0  # 1 second delay
    
    def check_win(self):
        """Check if all cards have been matched."""
        for row in self.cards:
            for card in row:
                if card.state != CardState.MATCHED:
                    return
        
        self.game_won = True
    
    def update(self, dt: float):
        """Update game state."""
        # Update card animations
        for row in self.cards:
            for card in row:
                card.update_flip_animation(dt)
                card.update_match_animation(dt)
        
        # Handle mismatch timer
        if self.showing_mismatch:
            self.mismatch_timer -= dt
            if self.mismatch_timer <= 0:
                # Hide the mismatched cards
                for card in self.revealed_cards:
                    card.state = CardState.HIDDEN
                self.revealed_cards = []
                self.showing_mismatch = False
    
    def draw_card(self, card: Card):
        """Draw a single card with appropriate state and animations."""
        rect = self.get_card_rect(card.row, card.col)
        
        # Determine card color based on state
        if card.state == CardState.HIDDEN:
            color = self.COLOR_CARD_HIDDEN
        elif card.state == CardState.MATCHED:
            color = self.COLOR_CARD_MATCHED
        else:
            color = self.COLOR_CARD_REVEALED
        
        # Apply match animation (fade effect)
        if card.state == CardState.MATCHED and card.match_animation_progress < 1.0:
            alpha = int(255 * (1.0 - card.match_animation_progress * 0.3))
            temp_surface = pygame.Surface((self.CARD_SIZE, self.CARD_SIZE))
            temp_surface.fill(color)
            temp_surface.set_alpha(alpha)
            self.screen.blit(temp_surface, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)
        
        # Draw border - thicker border for matched cards to show they're blocked
        border_width = 4 if card.state == CardState.MATCHED else 2
        border_color = (0, 100, 0) if card.state == CardState.MATCHED else (0, 0, 0)
        pygame.draw.rect(self.screen, border_color, rect, border_width)
        
        # Draw image if card is revealed or matched
        if card.state in [CardState.REVEALED, CardState.MATCHED] or \
           (card.state == CardState.FLIPPING and card.flip_animation_progress > 0.5):
            
            # Apply flip animation scaling
            scale = 1.0
            if card.state == CardState.FLIPPING:
                # Scale effect during flip
                progress = card.flip_animation_progress
                if progress < 0.5:
                    scale = 1.0 - progress
                else:
                    scale = progress
            
            # Get image surface
            image_surface = card.image_surface
            
            # Apply scaling
            if scale != 1.0:
                current_size = image_surface.get_size()
                new_size = (int(current_size[0] * scale), int(current_size[1] * scale))
                if new_size[0] > 0 and new_size[1] > 0:
                    image_surface = pygame.transform.scale(image_surface, new_size)
            
            # Center image on card
            image_rect = image_surface.get_rect()
            image_rect.center = rect.center
            self.screen.blit(image_surface, image_rect)
            
            # Add a subtle overlay for matched cards to show they're blocked
            if card.state == CardState.MATCHED:
                overlay = pygame.Surface((self.CARD_SIZE, self.CARD_SIZE))
                overlay.fill((255, 255, 255))
                overlay.set_alpha(30)  # Very subtle white overlay
                self.screen.blit(overlay, rect)
    
    def draw_ui(self):
        """Draw the user interface elements."""
        # Draw moves counter
        moves_text = self.font.render(f"Moves: {self.moves}", True, self.COLOR_TEXT)
        self.screen.blit(moves_text, (10, 10))
        
        # Draw timer
        if self.start_time:
            elapsed = time.time() - self.start_time
            if self.game_won and hasattr(self, 'win_time'):
                elapsed = self.win_time - self.start_time
            timer_text = self.font.render(f"Time: {elapsed:.1f}s", True, self.COLOR_TEXT)
            self.screen.blit(timer_text, (10, 50))
        
        # Draw win message
        if self.game_won:
            if not hasattr(self, 'win_time'):
                self.win_time = time.time()
            
            win_text = self.big_font.render("Congratulations!", True, self.COLOR_WIN_TEXT)
            win_rect = win_text.get_rect(center=(self.WINDOW_WIDTH // 2, 30))
            self.screen.blit(win_text, win_rect)
            
            final_time = self.win_time - self.start_time
            stats_text = self.font.render(f"Completed in {self.moves} moves and {final_time:.1f} seconds!", 
                                        True, self.COLOR_WIN_TEXT)
            stats_rect = stats_text.get_rect(center=(self.WINDOW_WIDTH // 2, 70))
            self.screen.blit(stats_text, stats_rect)
            
            restart_text = self.font.render("Press SPACE to play again or ESC to quit", 
                                          True, self.COLOR_TEXT)
            restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, 
                                                       self.WINDOW_HEIGHT - 30))
            self.screen.blit(restart_text, restart_rect)
    
    def draw(self):
        """Draw the entire game."""
        self.screen.fill(self.COLOR_BACKGROUND)
        
        # Draw all cards
        for row in self.cards:
            for card in row:
                self.draw_card(card)
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.game_won:
                    self.setup_game()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_card_click(event.pos)
        
        return True
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
            
            running = self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        sys.exit()


def main():
    """Main function to start the game."""
    game = MemoryGame()
    game.run()


if __name__ == "__main__":
    main()
