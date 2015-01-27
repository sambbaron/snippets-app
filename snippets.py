
import logging

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """Store a snippet with an associated name.

    Returns the name and the snippet
    """
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return name, snippet
  
def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, return error message that snippet with name does not exist

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return ""

def delete(name):
    """Delete the snippet with a given name.

    If there is no such snippet, return error message that snippet with name does not exist

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - delete({!r})".format(name))
    return ""

  
if __name__ == "__main__":
  put("Test Name", "Test Snippet")