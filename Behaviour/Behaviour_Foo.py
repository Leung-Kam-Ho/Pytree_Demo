"""Example showing how to create a skeleton behaviour."""

import random
import typing
import time
import py_trees
from pathlib import Path

# Foo is a skeleton behaviour in py_trees that demonstrates the basic structure of a custom behaviour. It randomly returns RUNNING, SUCCESS, or FAILURE to illustrate the lifecycle methods.

class Foo(py_trees.behaviour.Behaviour):
    """A skeleton behaviour that inherits from the PyTrees Behaviour class."""

    def __init__(self, name: str) -> None:
        """
        Minimal one-time initialisation.

        A good rule of thumb is to only include the initialisation relevant
        for being able to insert this behaviour in a tree for offline rendering to dot graphs.

        Other one-time initialisation requirements should be met via
        the setup() method.
        """
        super(Foo, self).__init__(name)

    def setup(self, **kwargs: typing.Any) -> None:
        """
        Minimal setup implementation.

        When is this called?
          This function should be either manually called by your program
          to setup this behaviour alone, or more commonly, via
          :meth:`~py_trees.behaviour.Behaviour.setup_with_descendants`
          or :meth:`~py_trees.trees.BehaviourTree.setup`, both of which
          will iterate over this behaviour, it's children (it's children's
          children ...) calling :meth:`~py_trees.behaviour.Behaviour.setup`
          on each in turn.

          If you have vital initialisation necessary to the success
          execution of your behaviour, put a guard in your
          :meth:`~py_trees.behaviour.Behaviour.initialise` method
          to protect against entry without having been setup.

        What to do here?
          Delayed one-time initialisation that would otherwise interfere
          with offline rendering of this behaviour in a tree to dot graph
          or validation of the behaviour's configuration.

          Good examples include:

          - Hardware or driver initialisation
          - Middleware initialisation (e.g. ROS pubs/subs/services)
          - A parallel checking for a valid policy configuration after
            children have been added or removed
        """
        self.logger.debug("  %s [Foo::setup()]" % self.name)

    def initialise(self) -> None:
        """
        Minimal initialisation implementation.

        When is this called?
          The first time your behaviour is ticked and anytime the
          status is not RUNNING thereafter.

        What to do here?
          Any initialisation you need before putting your behaviour
          to work.
        """
        self.logger.debug("  %s [Foo::initialise()]" % self.name)

    def update(self) -> py_trees.common.Status:
        """
        Minimal update implementation.

        When is this called?
          Every time your behaviour is ticked.

        What to do here?
          - Triggering, checking, monitoring. Anything...but do not block!
          - Set a feedback message
          - return a py_trees.common.Status.[RUNNING, SUCCESS, FAILURE]
        """
        self.logger.debug("  %s [Foo::update()]" % self.name)
        ready_to_make_a_decision = random.choice([True, False])
        decision = random.choice([True, False])
        if not ready_to_make_a_decision:
            return py_trees.common.Status.RUNNING
        elif decision:
            self.feedback_message = "We are not bar!"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "Uh oh"
            return py_trees.common.Status.FAILURE

    def terminate(self, new_status: py_trees.common.Status) -> None:
        """
        Minimal termination implementation.

        When is this called?
          Whenever your behaviour switches to a non-running state.
            - SUCCESS || FAILURE : your behaviour's work cycle has finished
            - INVALID : a higher priority branch has interrupted, or shutting down
        """
        self.logger.debug(
            "  %s [Foo::terminate().terminate()][%s->%s]"
            % (self.name, self.status, new_status)
        )


def build_tree() -> py_trees.behaviour.Behaviour:
    """Helper function to build a sample tree with Foo behaviour."""
    root = py_trees.composites.Sequence(name="FooDemo", memory=True)

    foo_task = Foo(name="Foo Task")

    final_task = py_trees.behaviours.Success(name="Done")

    root.add_children([foo_task, final_task])
    return root

if __name__ == "__main__":
    tree = py_trees.trees.BehaviourTree(root=build_tree())
    path = Path() / "Behaviour" / "render"
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