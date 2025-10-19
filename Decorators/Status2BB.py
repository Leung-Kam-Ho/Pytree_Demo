# Demo for py_trees.decorators.StatusToBlackboard
import time
import py_trees


class CyclingStatus(py_trees.behaviour.Behaviour):
    """
    Cycles through RUNNING -> SUCCESS -> FAILURE -> RUNNING -> ...
    on successive ticks to show status mirroring to the blackboard.
    """
    def __init__(self, name="CyclingStatus"):
        super().__init__(name=name)
        self.count = 0

    def update(self) -> py_trees.common.Status:
        self.count += 1
        phase = self.count % 3
        if phase == 1:
            self.feedback_message = "RUNNING"
            return py_trees.common.Status.RUNNING
        elif phase == 2:
            self.feedback_message = "SUCCESS"
            return py_trees.common.Status.SUCCESS
        else:
            self.feedback_message = "FAILURE"
            return py_trees.common.Status.FAILURE


def main():
    print(f"py_trees version: {getattr(py_trees, '__version__', 'unknown')}")
    key = "cyclist_status"

    # Child whose status we want to mirror to the blackboard
    child = CyclingStatus()

    # Decorator that writes the child's status to the blackboard
    decorated = py_trees.decorators.StatusToBlackboard(name="Status->BB", child=child, variable_name=key)

    # Build and tick the tree
    tree = py_trees.trees.BehaviourTree(root=decorated)

    # Blackboard reader to observe the mirrored status
    reader = py_trees.blackboard.Client(name="Observer")
    reader.register_key(key=key, access=py_trees.common.Access.READ)

    # Tick several times and show: child status, decorator status, blackboard value
    for i in range(1, 10):
        tree.tick()

        bb_value = getattr(reader, key, None)
        if isinstance(bb_value, py_trees.common.Status):
            bb_display = bb_value.name
        else:
            bb_display = repr(bb_value)

        print(
            f"Tick {i:02d} | child={child.status.name} | decorator={decorated.status.name} | blackboard[{key}]={bb_display}"
        )
        time.sleep(0.2)


if __name__ == "__main__":
    main()