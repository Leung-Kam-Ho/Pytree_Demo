from Behaviour_Foo import Foo
import py_trees
import time


def main():
    action = Foo("Root Foo")
    # py_trees.logging.level = py_trees.logging.Level.DEBUG
    action.setup(timeout=15)
    try:
        for _unused_i in range(0, 12):
            action.tick_once()
            print(action.feedback_message)
            time.sleep(0.5)
        print("\n")
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
