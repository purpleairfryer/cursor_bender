# AI Hand-Controlled Cursor for Windows

A Python desktop application that allows you to control your Windows mouse cursor using right hand gestures detected through a webcam feed.

## Features

- **Cursor Movement**: Extend your right index finger to activate cursor control. Moving your finger moves the mouse cursor.
- **Left Click**: Pinch your thumb and index finger together to perform a left-click.
- **Scrolling**: Extend both your index and middle fingers, then move your hand up or down to scroll the screen.

## Requirements

- Python 3.7 or higher
- Windows operating system
- Webcam

## Installation

1. Clone or download this repository.

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python hand_cursor_control.py
```

2. A window will open showing your webcam feed with hand landmark visualization.

3. Use the following gestures:
   - **Index finger up**: Move the cursor
   - **Index + Thumb pinch**: Left-click
   - **Index + Middle fingers up**: Scroll up/down

4. Press 'q' to quit the application.

## Configuration

You can adjust the following parameters at the top of `hand_cursor_control.py`:
- `PINCH_THRESHOLD`: Distance threshold for pinch detection (default: 0.04)
- `SCROLL_SENSITIVITY`: Sensitivity for scroll detection (default: 50)
- `CLICK_DEBOUNCE_TIME`: Minimum time between clicks in seconds (default: 0.5)
- `SCROLL_DEBOUNCE_TIME`: Minimum time between scroll actions in seconds (default: 0.1)

## Troubleshooting

- Ensure your webcam is working and not being used by another application.
- Make sure you have good lighting for better hand detection.
- Adjust the thresholds if gestures are not being detected correctly.

