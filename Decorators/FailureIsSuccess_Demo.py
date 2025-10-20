import py_trees
import time
from pathlib import Path

# FailureIsSuccess is a decorator in py_trees that converts a FAILURE status from its child to SUCCESS.


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
    root = py_trees.composites.Sequence(name="FailureIsSuccessDemo", memory=True)

    # Task that fails after delay
    failing_task = DelayedFailure("Fail After 1 Tick", ticks=1)

    # FailureIsSuccess decorator turns FAILURE to SUCCESS
    failure_is_success_decorator = py_trees.decorators.FailureIsSuccess(
        name="Failure to Success",
        child=failing_task
    )

    # Final task to show sequence continues
    final_task = DelayedSuccess("Done", ticks=1)

    root.add_children([failure_is_success_decorator, final_task])
    return root


if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    path = Path() / "Decorators" / "render"
    path.mkdir(parents=True, exist_ok=True)
    py_trees.display.render_dot_tree(tree.root, name="failure_is_success_demo_tree", target_directory=path)
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