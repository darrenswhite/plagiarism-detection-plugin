from postprocessor.postprocessor import PostProcessor

postprocessor = PostProcessor()


def main():
    """
    Start the post processor
    """
    try:
        postprocessor.run()
    except KeyboardInterrupt:
        pass
