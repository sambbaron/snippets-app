
import logging, sys, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# Connect to PostgreSQL database
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
  """Store a snippet with an associated name.
  Returns the name and the snippet"""
    
  logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
  cursor = connection.cursor()
  try:
    command = "insert into snippets values (%s, %s)"
    cursor.execute(command, (name, snippet))
  except psycopg2.IntegrityError as e:
    connection.rollback()
    command = "update snippets set message=%s where keyword=%s"
    cursor.execute(command, (snippet, name))
  connection.commit()
  logging.debug("Snippet stored successfully.")
  return name, snippet
  
def get(name):
  """Retrieve the snippet with a given name.
  If there is no such snippet, return error message that snippet with name does not exist
  Returns the snippet."""
  logging.info("Retrieving snippet {!r}".format(name))
  cursor = connection.cursor()
  command = "select message from snippets where keyword = %s"
  cursor.execute(command, (name,))
  row = cursor.fetchone()
  connection.commit()
  
  if not row:
    # No snippet was found with that name.
    logging.debug("Snippet does not exist.")
    return "ERROR: Snippet with {} name does not exist.".format(name)
  else:
    logging.debug("Snippet retrieved successfully.")
    return row[0]

def delete(name):
    """Delete the snippet with a given name.

    If there is no such snippet, return error message that snippet with name does not exist

    Returns the snippet.
    """
    logging.error("FIXME: Unimplemented - delete({!r})".format(name))
    return ""

  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="Thpyte name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="Thpyte name of the snippet")    

    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))

if __name__ == "__main__":
    main()