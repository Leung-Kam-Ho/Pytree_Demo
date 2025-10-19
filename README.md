

# PyTree Behavior Tree Demo

This repository contains demonstration scripts for learning and experimenting with **behavior trees** using the `py_trees` Python library. It includes examples of core behavior tree concepts such as:

- **Behaviors** – leaf nodes that perform actions or checks
- **Composites** – nodes that control behavior flow (`Sequence`, `Selector`, `Parallel`)
- **Decorators** – modify or wrap behavior logic (`Retry`, `Timeout`, `Inverter`, etc.)
- **Blackboard** – shared memory for behavior communication
- **Tree Visualisation** – rendering trees to `.dot` and `.png`

---

## 📚 Purpose

This repo is designed as a **learning playground** for understanding how behavior trees work, especially for robotics applications (ROS, AI agents, automation decision systems).

Each script in the repo demonstrates a different tree structure or behavior pattern. Example topics include:

- Basic action nodes
- Using `Sequence` for ordered control flow
- Using `Selector` for fallback logic
- Running continuous background tasks
- Adding retry or safety decorators
- Blackboard variable usage
- Visualising trees step by step

---

## ✅ Requirements

This project uses **uv** (a very fast Python package manager and virtual environment tool).  
If you don't already have `uv` installed, you can install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then, create and activate the virtual environment automatically when syncing dependencies:

```bash
uv sync
```

You can also run Python scripts inside the uv environment without activating it manually:

```bash
uv run python Composites/Selector_Demo.py
```

To add a new library to the project, use:

```bash
uv add <package-name>
```

To remove a package:

```bash
uv remove <package-name>
```

To update all dependencies:

```bash
uv sync --upgrade
```

---

## ▶️ Run a Demo

Each Python file is a standalone behavior tree demo.

For example:

```bash
uv run python Composites/Selector_Demo.py
```

Most scripts will tick the tree and print results in the console. Some will also generate `.png` tree visualisations.

---


## 🧠 What are Behavior Trees?

Behavior trees are a modular and readable way to define decision-making logic. They are widely used in:

- **Robotics**
- **Game AI**
- **Autonomous agents**
- **Simulation**

They offer better structure than simple `if/else` logic or finite-state machines.

---


### 🔧 Future Plans

- ROS2 integration examples
- More advanced decorator demos
- Blackboard memory for multi-agent coordination
- Real robot task planning demo

---

### 👨‍💻 Author

Demo repo by **Leung Kam Ho** – for learning and sharing py_trees behavior tree examples.

---
If you want to add more examples or have any questions, feel free to ask!