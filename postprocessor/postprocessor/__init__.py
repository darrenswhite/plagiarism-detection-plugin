import argparse

from postprocessor.postprocessor import PostProcessor


def main():
    """
    Parse CLI arguments and then start the post processor
    """
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', help='The submission file to process')
    parser.add_argument('-p', '--plot', action='store_true', dest='plot',
                        help='Show plot of changes')
    args = parser.parse_args()

    try:
        PostProcessor(args.plot).run(args.file)
    except KeyboardInterrupt:
        pass
