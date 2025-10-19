import py_trees
import time
from pathlib import Path

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


def build_tree():
    root = py_trees.composites.Parallel(
        name="ParallelDemo",
        # policy=py_trees.common.ParallelPolicy.SuccessOnOne()
        policy=py_trees.common.ParallelPolicy.SuccessOnAll()
    )
    root.add_children([
        DelayedSuccess("TaskA (3 ticks)", ticks=3),
        DelayedSuccess("TaskB (10 ticks)", ticks=10),
        AlwaysRunning("Background (Never Stop)"),  # Uncomment to see RUNNING status
    ])
    return root


if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    tree.setup(timeout=1.0)
    count = 0
    # render the tree to png
    py_trees.display.render_dot_tree(tree.root, name="parallel_demo_tree", target_directory=Path() / "Demo" / "render")
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
        # print(f"tick {i+1} -> root:{tree.root.status.name} | {child_states}")
        # render the tree to the console
        print(py_trees.display.ascii_tree(tree.root,show_status=True))
        print("\n")
        if tree.root.status != py_trees.common.Status.RUNNING:
            break
