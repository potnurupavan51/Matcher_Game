# Image Memory Match Game

A fun and interactive 4×4 grid memory matching game built with Python and Pygame, featuring custom image cards from your local directory. This project was developed with assistance from **Amazon Q**, AWS's AI-powered coding assistant.

## About Amazon Q

[Amazon Q](https://aws.amazon.com/q/) is AWS's generative AI-powered assistant designed to help developers and IT professionals be more productive. Amazon Q can help with:

- **Code Generation**: Writing, debugging, and optimizing code across multiple programming languages
- **AWS Services**: Providing guidance on AWS best practices and service recommendations  
- **Problem Solving**: Assisting with technical challenges and architectural decisions
- **Documentation**: Creating comprehensive project documentation and explanations

This memory matching game was created with Amazon Q's assistance, demonstrating how AI can help accelerate development while maintaining clean, well-documented code.

---

## 🎮 Game Overview

The Image Memory Match Game is a classic concentration-style puzzle game where players flip cards to find matching pairs. The game uses your own custom images, making it personalized and engaging.

### 🎯 Objective
Match all 8 pairs of identical images in the fewest moves and shortest time possible!

---

## ✨ Features

### Core Gameplay
- **4×4 Grid Layout**: 16 cards total with 8 unique image pairs
- **Custom Images**: Uses your own images from the local `/images` directory
- **Smart Pairing**: Automatically creates pairs from available images without repetition
- **Progressive Difficulty**: Matched pairs become blocked, focusing attention on remaining cards

### Visual & Audio
- **Smooth Animations**: 
  - Card flip animations with scaling effects
  - Match animations with fade effects
  - Visual feedback for different card states
- **Color-Coded States**:
  - 🔵 **Blue Cards**: Hidden/face-down cards (clickable)
  - ⚪ **White Cards**: Currently revealed cards
  - 🟢 **Green Cards**: Successfully matched pairs (blocked)
- **Enhanced Visual Indicators**:
  - Thick borders on matched cards
  - Subtle overlay effects for blocked cards

### Game Mechanics
- **Move Counter**: Tracks pairs of card flips (not individual clicks)
- **Timer**: Starts with first card flip, stops when game is won
- **Mismatch Delay**: Non-matching cards flip back after 1 second
- **Win Detection**: Automatic game completion when all pairs are matched
- **Restart Functionality**: Play again without restarting the application

### Technical Features
- **Image Auto-Loading**: Automatically detects and loads images from directory
- **Smart Scaling**: Images are automatically resized to fit card dimensions
- **Error Handling**: Graceful fallback if images can't be loaded
- **Memory Efficient**: Optimized image loading and rendering

---

## 🎮 Controls

| Input | Action |
|-------|--------|
| **Mouse Click** | Flip/reveal cards |
| **Space Bar** | Restart game (on win screen) |
| **Escape Key** | Quit game |

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.6 or higher
- Pygame 2.0 or higher

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd image-memory-match
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your images**:
   - Create an `images` directory in the project root
   - Add 8 unique image files (JPG, PNG formats supported)
   - Supported filenames: `1.jpg`, `2.png`, `3.png`, `6.jpg`, `9.jpg`, `11.png`, `12.jpg`, `13.jpg`

4. **Run the game**:
   ```bash
   python emoji_memory_match.py
   ```

---

## 🖼️ Image Requirements

### Supported Formats
- **JPG/JPEG**: High-quality photographs
- **PNG**: Images with transparency support
- **Other formats**: Any format supported by Pygame

### Image Specifications
- **Quantity**: 8 unique images required for optimal gameplay
- **Auto-Scaling**: Images are automatically resized to 90×90 pixels
- **Directory**: Place images in `/images` folder in project root
- **Naming**: Use descriptive filenames (e.g., `1.jpg`, `nature.png`, etc.)

### Fallback System
If fewer than 8 images are available, the game includes a fallback system with colored rectangles to ensure playability.

---

## 🏗️ Technical Architecture

### Project Structure
```
image-memory-match/
├── emoji_memory_match.py    # Main game file
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── images/                 # Image assets directory
    ├── 1.jpg
    ├── 2.png
    ├── 3.png
    ├── 6.jpg
    ├── 9.jpg
    ├── 11.png
    ├── 12.jpg
    └── 13.jpg
```

### Code Architecture

#### Classes & Components

**`CardState` (Enum)**
- Manages card state transitions
- States: `HIDDEN`, `REVEALED`, `MATCHED`, `FLIPPING`

**`Card` Class**
- Represents individual game cards
- Handles animations and state management
- Properties: `image_id`, `image_surface`, `row`, `col`, `state`

**`MemoryGame` Class**
- Main game controller
- Manages game logic, rendering, and user input
- Key methods:
  - `load_images()`: Dynamic image loading and scaling
  - `setup_game()`: Game initialization and card shuffling
  - `handle_card_click()`: User interaction processing
  - `draw()`: Rendering pipeline

#### Key Technical Features

**Image Management**
```python
def load_images(self) -> Dict[str, pygame.Surface]:
    # Automatically loads and scales images from directory
    # Handles multiple formats and error cases
    # Returns dictionary of loaded image surfaces
```

**Animation System**
- Smooth card flip animations using delta time
- Scaling effects during card reveals
- Fade animations for matched pairs

**Game State Management**
- Robust state machine for card interactions
- Move counting and timing systems
- Win condition detection

---

## 🎯 Game Mechanics Deep Dive

### Card Interaction Flow
1. **Click Detection**: Mouse position mapped to card grid coordinates
2. **State Validation**: Only hidden cards can be clicked
3. **Reveal Animation**: Smooth flip animation with scaling
4. **Match Checking**: Compare revealed card pairs
5. **State Transition**: Cards become matched or flip back to hidden

### Matching Logic
```python
# Simplified matching logic
if card1.image_id == card2.image_id:
    # Match found - cards become permanently visible and blocked
    card1.state = CardState.MATCHED
    card2.state = CardState.MATCHED
else:
    # No match - cards flip back after delay
    self.showing_mismatch = True
    self.mismatch_timer = 1.0
```

### Performance Optimizations
- **Efficient Rendering**: Only redraws changed elements
- **Memory Management**: Images loaded once and reused
- **Event Handling**: Optimized mouse click detection
- **Animation Smoothing**: Delta time-based animations for consistent performance

---

## 🎨 Customization Options

### Visual Customization
```python
# Color scheme (easily modifiable)
COLOR_BACKGROUND = (40, 40, 40)      # Dark gray background
COLOR_CARD_HIDDEN = (70, 130, 180)   # Steel blue for hidden cards
COLOR_CARD_REVEALED = (255, 255, 255) # White for revealed cards
COLOR_CARD_MATCHED = (60, 179, 113)   # Medium sea green for matches
```

### Game Parameters
```python
# Grid and sizing (configurable)
GRID_SIZE = 4           # 4×4 grid
CARD_SIZE = 100         # Card dimensions in pixels
CARD_MARGIN = 10        # Spacing between cards
```

---

## 🐛 Troubleshooting

### Common Issues

**Images Not Loading**
- Verify images are in the correct `/images` directory
- Check file permissions and formats
- Ensure filenames match expected patterns

**Performance Issues**
- Reduce image file sizes if experiencing lag
- Close other applications to free up system resources
- Update Pygame to the latest version

**Display Problems**
- Verify your system supports the required screen resolution
- Check graphics drivers are up to date
- Try running in windowed mode

---

## 🤝 Contributing

Contributions are welcome! Here are some areas for potential improvements:

- **Sound Effects**: Add audio feedback for card flips and matches
- **Difficulty Levels**: Implement different grid sizes (3×3, 5×5, 6×6)
- **Themes**: Create different visual themes and color schemes
- **Statistics**: Add high score tracking and game statistics
- **Multiplayer**: Add turn-based multiplayer functionality

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes with proper documentation
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

- **Amazon Q**: AI assistance for code development and optimization
- **Pygame Community**: Excellent documentation and community support
- **Contributors**: Thanks to all who help improve this project

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the code comments for implementation details
3. Open an issue on GitHub with detailed information
4. Consider contributing improvements back to the project

---

**Enjoy the game and challenge yourself to improve your memory skills!** 🧠✨
