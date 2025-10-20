import py_trees
import time
from pathlib import Path

# Condition is a decorator in py_trees that waits for its child to return a specific status before allowing the tree to proceed.


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
    root = py_trees.composites.Sequence(name="ConditionDemo", memory=True)

    # Task that succeeds after delay
    succeeding_task = DelayedSuccess("Succeed After 2 Ticks", ticks=2)

    # Condition decorator waits for SUCCESS
    condition_decorator = py_trees.decorators.Condition(
        name="Wait for Success",
        child=succeeding_task,
        status=py_trees.common.Status.SUCCESS
    )

    # Final task to show sequence continues
    final_task = DelayedSuccess("Done", ticks=1)

    root.add_children([condition_decorator, final_task])
    return root


if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    path = Path() / "Decorators" / "render"
    path.mkdir(parents=True, exist_ok=True)
    py_trees.display.render_dot_tree(tree.root, name="condition_demo_tree", target_directory=path)
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