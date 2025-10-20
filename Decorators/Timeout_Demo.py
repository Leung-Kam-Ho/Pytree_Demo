import py_trees
import time
from pathlib import Path

# Timeout is a decorator in py_trees that executes a child/subtree with a timeout. If the timeout is reached, the encapsulated behaviour’s stop() method is called with status FAILURE otherwise it will simply directly tick and return with the same status as that of it’s encapsulated behaviour.

class AlwaysRunning(py_trees.behaviour.Behaviour):
    def __init__(self, name="Background"):
        super().__init__(name)

    def update(self):
        return py_trees.common.Status.RUNNING


class DelayedSuccess(py_trees.behaviour.Behaviour):
    def __init__(self, name="Task", ticks=3):
        super().__init__(name)
        self.ticks = ticks
        self.count = 0

    def initialise(self):
        self.count = 0

    def update(self):
        self.count += 1
        if self.count < self.ticks:
            return py_trees.common.Status.RUNNING
        return py_trees.common.Status.SUCCESS


class DelayedFailure(py_trees.behaviour.Behaviour):
    def __init__(self, name="Task", ticks=3):
        super().__init__(name)
        self.ticks = ticks
        self.count = 0

    def initialise(self):
        self.count = 0

    def update(self):
        self.count += 1
        if self.count < self.ticks:
            return py_trees.common.Status.RUNNING
        return py_trees.common.Status.FAILURE


def build_tree():
    root = py_trees.composites.Sequence(name="TimeoutDemo", memory=True)

    # Task that runs for 5 ticks
    long_task = DelayedSuccess("Long Task (5 ticks)", ticks=5)

    # Timeout decorator: fail if child takes more than 3 seconds
    timeout_decorator = py_trees.decorators.Timeout(
        name="Timeout After 3s",
        child=long_task,
        duration=3.0
    )

    # Final task to show what happens after timeout
    final_task = DelayedSuccess("After Timeout", ticks=1)

    root.add_children([timeout_decorator, final_task])
    return root


if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    path = Path() / "Decorators" / "render"
    path.mkdir(parents=True, exist_ok=True)
    py_trees.display.render_dot_tree(tree.root, name="timeout_demo_tree", target_directory=path)
    tree.setup(timeout=1.0)
    count = 0
    while True:
        count += 1
        RATE_HZ = 1.0
        period = 1.0 / RATE_HZ

        now = time.perf_counter()
        if not hasattr(tree, "_next_tick_time"):
            tree._next_tick_time = now

        if now < tree._next_tick_time:
            time.sleep(tree._next_tick_time - now)
        print(f"--- Tick {count} ---")
        tree.tick()
        tree._next_tick_time += period
        child_states = ", ".join(f"{c.name}:{c.status.name}" for c in tree.root.children)
        print(py_trees.display.ascii_tree(tree.root, show_status=True))
        print("\n")
        if tree.root.status != py_trees.common.Status.RUNNING:
            break
