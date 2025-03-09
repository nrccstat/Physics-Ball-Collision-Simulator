

---

```markdown
# Ball Collision Simulation

This project is a 2D physics-based simulation built with Pygame, where balls move, collide with each other, and bounce off a circular boundary. Users can interactively customize ball properties such as radius, initial velocity, bounciness, and color through a graphical user interface (GUI) featuring sliders and buttons. The simulation demonstrates elastic collisions and boundary reflections in a vacuum-like environment (no gravity or friction).

## Installation

To set up and run the Ball Collision Simulation, follow these steps:

1. **Install Python**: Ensure you have Python 3.6 or higher installed. Download it from [python.org](https://www.python.org/downloads/) if needed.
2. **Install Pygame**: Pygame is the primary library required for this project. Install it via pip:
   ```bash
   pip install pygame
   ```
3. **Download the Code**: Save the provided code into a file named `ball_simulation.py` (or any name you prefer).
4. **Run the Simulation**: Open a terminal or command prompt, navigate to the directory containing the file, and execute:
   ```bash
   python ball_simulation.py
   ```

No additional setup is required beyond installing Python and Pygame.

## Dependencies

The project relies on the following Python libraries, some of which are part of the standard library:

- **Pygame**: Used for rendering graphics, handling user input, and managing the game loop. Install with:
  ```bash
  pip install pygame
  ```
- **Math**: Provides mathematical functions like `hypot` for distance calculations and `cos`/`sin` for trigonometry. (Standard library, no installation needed.)
- **Random**: Generates random positions for new balls. (Standard library, no installation needed.)
- **Sys**: Handles system exit functionality. (Standard library, no installation needed.)

## Project Structure

The code is contained within a single Python script (`ball_simulation.py`) and is organized into the following components:

- **Imports and Initialization**: Imports required libraries and sets up the Pygame window, constants, and font.
- **Slider Class**: Defines interactive sliders for adjusting ball properties.
- **Ball Class**: Represents each ball with attributes like position, velocity, radius, color, and bounciness.
- **Helper Functions**: Utility functions for physics calculations and random position generation.
- **Main Loop**: Manages the simulation, including event handling, physics updates, and rendering.

## Features

This simulation offers a rich set of features:

- **Customizable Ball Properties**:
  - **Radius**: Adjustable from 1 to 25 pixels.
  - **Initial Velocity**: X and Y components (Vx and Vy) range from -30 to 30 units.
  - **Bounciness**: Coefficient of restitution ranges from 0.8 (less bouncy) to 1 (perfectly elastic).
  - **Color**: Choose between Red, Green, or Blue.
- **Interactive GUI**:
  - Sliders for real-time adjustment of radius, velocity, and bounciness.
  - Color selection buttons.
  - "Add Ball" button to introduce new balls with current settings.
- **Physics Engine**:
  - Elastic collisions between balls based on their masses (proportional to radius squared) and bounciness.
  - Boundary reflections within a circular area (radius 290 pixels).
- **Dynamic Interaction**:
  - Add balls with a single click.
  - Remove balls by clicking on them.
- **Visual Feedback**:
  - Real-time display of slider values.
  - Highlighted color selection.

## How to Use

Follow these steps to interact with the simulation:

1. **Launch the Program**:
   Run the script as described in the Installation section. A window (800x600 pixels) will open with a circular boundary and a control panel on the left.

2. **Adjust Ball Properties**:
   - **Radius Slider**: Drag the top slider (at y=10) to set the ball radius (1 to 25).
   - **Vx Slider**: Drag the second slider (at y=50) to set the horizontal velocity (-30 to 30).
   - **Vy Slider**: Drag the third slider (at y=90) to set the vertical velocity (-30 to 30).
   - **Bounciness Slider**: Drag the fourth slider (at y=130) to set the bounciness (0.8 to 1).
   - **Color Buttons**: Click one of the three buttons (Red at y=170, Green at x=50, Blue at x=90) to select the ball color.

3. **Add a Ball**:
   - Click the "Add Ball" button (at y=210) to create a new ball with the selected properties. The ball appears at a random position within the circular boundary.

4. **Interact with Balls**:
   - Watch the balls move and collide with each other and the boundary.
   - Click on any ball to remove it from the simulation.

5. **Exit the Simulation**:
   - Close the window by clicking the "X" button to quit the program.

## Code Explanation

### Key Components

#### Slider Class
- **Purpose**: Creates draggable sliders for adjusting numeric properties.
- **Attributes**:
  - `rect`: The slider bar's bounding box.
  - `handle_rect`: The draggable handle's position.
  - `min_val`, `max_val`: Range of possible values.
  - `value`: Current value, updated by dragging.
- **Methods**:
  - `draw`: Renders the slider and handle.
  - `get_value`: Calculates the current value based on handle position.
  - `set_value`: Sets the handle position based on a value.
  - `handle_event`: Processes mouse events for dragging.

#### Ball Class
- **Purpose**: Represents a ball with physical properties.
- **Attributes**:
  - `x`, `y`: Position (floating-point).
  - `vx`, `vy`: Velocity components (floating-point).
  - `r`: Radius.
  - `color`: RGB tuple.
  - `e`: Bounciness (coefficient of restitution).
  - `m`: Mass, calculated as `r ** 2`.
- **Initialization**: Sets initial values with floating-point precision.

#### Helper Functions
- **`distance(p1, p2)`**: Computes the Euclidean distance between two points using `math.hypot`.
- **`normalize(v)`**: Returns a unit vector from a given vector, handling zero magnitude cases.
- **`get_random_position(ball_radius)`**: Generates a random position within the circular boundary using polar coordinates.

#### Main Loop
- **Event Handling**:
  - Closes the window on quit.
  - Updates sliders on mouse drag.
  - Changes color on button click.
  - Adds a ball on "Add Ball" click.
  - Removes a ball on ball click.
- **Physics Updates**:
  - Moves each ball based on its velocity.
  - Handles boundary collisions by reflecting velocity using the bounciness coefficient.
  - Resolves ball-to-ball collisions using conservation of momentum and energy, averaging bounciness between colliding balls.
- **Rendering**:
  - Draws the black background and white circular boundary.
  - Renders sliders, color buttons (with selection highlight), and the "Add Ball" button.
  - Displays labels and current slider values.
  - Draws each ball at its updated position.

### Physics Details
- **Boundary Collisions**: When a ball hits the circular boundary, its velocity is reflected based on the normal vector and bounciness (`e`).
- **Ball Collisions**: Uses impulse-based collision resolution, calculating the impulse (`J`) from relative velocity, masses, and average bounciness, then updating velocities accordingly.

## Example Workflow
1. Set Radius to 15, Vx to 10, Vy to -5, Bounciness to 0.9, and select Green.
2. Click "Add Ball" to add a green ball moving right and slightly upward.
3. Add another ball with different settings (e.g., Blue, Radius 20, Vx -15, Vy 0).
4. Observe collisions and boundary bounces.
5. Click a ball to remove it.

## Contributing

This project is open-source and welcomes contributions! To contribute:
1. Fork the repository (if hosted online) or copy the code.
2. Make improvements or add features (e.g., gravity, friction, or new UI elements).
3. Submit a pull request or share your updated code.

Suggestions for enhancements:
- Add a reset button to clear all balls.
- Implement a slider for controlling simulation speed.
- Add sound effects for collisions.



---

Enjoy experimenting with ball collisions and physics in this interactive simulation!
```

---

This README provides a thorough guide to your Ball Collision Simulation, covering everything from setup to code details. It’s designed to be user-friendly and informative, ensuring that anyone can understand and use your project effectively. Let me know if you’d like to tweak anything!
