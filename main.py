from dotenv import load_dotenv

from libs.api import APIHandler
from libs.db import DBHandler


def main():
    # load environment variables
    load_dotenv()

    # get repositories
    api_handler = APIHandler()
    repos = api_handler.get_repos()

    # populate table with repositories (remove duplicates, add new)
    db_handler = DBHandler()
    db_handler.populate(repos)


if __name__ == "__main__":
    main()
