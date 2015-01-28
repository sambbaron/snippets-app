
import logging, sys, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

# Connect to PostgreSQL database
logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet, hidden = False):
  """Store a snippet with an associated name.
  Returns the name and the snippet"""
    
  logging.info("Storing snippet {!r}: {!r}, hidden flag = {!r}".format(name, snippet, hidden))
  cursor = connection.cursor()
  with connection, connection.cursor() as cursor:
    try:
      cursor.execute("insert into snippets values (%s, %s, %s)", (name, snippet, hidden))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      cursor.execute("update snippets set message=%s, hidden=%s where keyword=%s", (snippet, hidden, name))
  logging.debug("Snippet stored successfully.")
  return name, snippet, hidden
  
def get(name):
  """Retrieve the snippet with a given name.
  If there is no such snippet, return error message that snippet with name does not exist
  Returns the snippet."""
  logging.info("Retrieving snippet {!r}".format(name))
  with connection, connection.cursor() as cursor:
    cursor.execute("select message from snippets where keyword=%s", (name,))
    row = cursor.fetchone()
  
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
  Returns the snippet.    """
    
  logging.error("FIXME: Unimplemented - delete({!r})".format(name))
  return ""
  
def catalog():
  """Return listing of snippet names"""
  
  logging.info("Retrieving name catalog")
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets where not hidden order by keyword")
    names = cursor.fetchall()
  logging.debug("Names catalog retrieved successfully.")
  return names

def search(searchstr):
  """Search for string in names
  Return names"""

  logging.info("Searching names for {!r}".format(searchstr))
  with connection, connection.cursor() as cursor:
    cursor.execute("select keyword from snippets where keyword like %s and not hidden order by keyword", ('%{}%'.format(searchstr),))
    names = cursor.fetchall()
  logging.debug("Names catalog searched successfully.")
  return searchstr, names

def print_names(names, search_filter = ""):
  """Print catalog of names"""
  if search_filter:
    search_filter = " (Searched for {}) ".format(search_filter)
  print "Name Catalog{}:".format(search_filter)
  print "------------"
  for name in names:
    print name[0]
  
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("--hide", dest="hidden", help="Hide snippet in catalog", action="store_true")
    put_parser.add_argument("--show, --unhide, --no-hide, -hide=0", dest="hidden", help="Show snippet in catalog", action="store_false")
        
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet") 
    
    # Subparser for catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Retrieve catalog of snippet names")
    
    # Subparser for the search command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Search a name")
    search_parser.add_argument("searchstr", help="The text string to search") 

    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
      name, snippet, hidden = put(**arguments)
      print("Stored {!r} as {!r}, hidden flag = {!r}".format(snippet, name, hidden))
    elif command == "get":
      snippet = get(**arguments)
      print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
      names = catalog()
      print_names(names)
    elif command == "search":
      searchstr, names = search(**arguments)
      print_names(names, searchstr)
      
        
if __name__ == "__main__":
    main()