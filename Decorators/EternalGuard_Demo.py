import py_trees
import time
from pathlib import Path

# EternalGuard is a decorator in py_trees that checks a condition every tick and only allows its child to execute if the condition evaluates to true.


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


def condition_true():
    # Condition that always allows execution
    return True


def condition_false():
    # Condition that never allows execution
    return False


def condition_inverted_false():
    # Condition that inverts the false condition (always true)
    return not condition_false()


def build_tree():
    root = py_trees.composites.Parallel(name="EternalGuardDemo", policy=py_trees.common.ParallelPolicy.SuccessOnAll())

    # Task that succeeds after delay for true condition
    succeeding_task_true = DelayedSuccess("Succeed After 3 Ticks (True)", ticks=3)

    # EternalGuard decorator with true condition
    eternal_guard_true = py_trees.decorators.EternalGuard(
        name="Eternal Guard (True)",
        child=succeeding_task_true,
        condition=condition_true
    )

    # Task that succeeds after delay for false condition
    succeeding_task_false = DelayedSuccess("Succeed After 3 Ticks (False)", ticks=3)

    # EternalGuard decorator with false condition
    eternal_guard_false = py_trees.decorators.EternalGuard(
        name="Eternal Guard (Condition False, Child Never Runs)",
        child=succeeding_task_false,
        condition=condition_false
    )

    root.add_children([eternal_guard_true, py_trees.decorators.Inverter(name="Inverter (Keep Parallel Running)", child=eternal_guard_false)])
    return root


if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    path = Path() / "Decorators" / "render"
    path.mkdir(parents=True, exist_ok=True)
    py_trees.display.render_dot_tree(tree.root, name="eternal_guard_demo_tree", target_directory=path)
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