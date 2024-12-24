# Cargo Tracking System

A cargo tracking system implemented in Python with both CLI and GUI interfaces. The system uses various data structures including linked lists, priority queues, trees, and stacks to manage cargo shipments and routing.

## Features

- Customer Management

  - Add and manage customer profiles
  - View customer history and preferences
  - Track customer-specific shipments

- Cargo Handling

  - Create new cargo shipments
  - Set cargo priorities and categories
  - Monitor cargo status and location

- Route Management

  - Define and optimize delivery routes
  - Track shipments along routes
  - View route performance metrics

- Shipment Tracking
  - Real-time shipment status updates
  - Search and filter shipments
  - Generate shipment reports

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Jelsin29/cargo-tracking.git
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Launch the GUI interface:

```bash
python src/gui_main.py
```

### Launch the terminal interface:

```bash
python src/main.py
```

### Run Tests:

To run all tests:

```bash
python src/main.py
```

To run specific test files:

```bash
pytest tests/test_cargo_priority.py    # Test cargo priority queue
pytest tests/test_customer.py          # Test customer linked list
pytest tests/test_route_tree.py        # Test route tree
pytest tests/test_shipment.py          # Test shipment stack
pytest tests/test_integration.py       # Test integration
```

To run tests with coverage report:

```bash
python src/main.py
```

## Project Structure

```
src/
├── database/         # Database management
├── gui/             # GUI components
│   ├── dialogs/     # Dialog windows
│   └── widgets/     # Custom widgets
├── models/          # Data models
└── utils/           # Utility functions
```

## Technology Stack

- Python 3.x
- PyQt5 (GUI Framework)
- SQLite (Database)
- pytest (Testing)

## Author

Jelsin Stiben Sanchez Almanza / Jelsin29

## Version

1.0.0
