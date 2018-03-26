import sys

from postprocessor.postprocessor import PostProcessor

postprocessor = PostProcessor()


def main():
    """
    Start the post processor
    """
    try:
        filename = None
        if len(sys.argv) == 2:
            filename = sys.argv[1]
        postprocessor.run(filename)
    except KeyboardInterrupt:
        pass
