"""
1) Identify the website you want to scrape and the information you want to extract.

2) Choose a programming language for your scraper. Popular options include Python, Ruby, and JavaScript.

3) Use a web scraping library or tool that is compatible with your chosen programming language. 
    - BeautifulSoup

4) Analyze the structure of the website's HTML code and determine how to target the information you want to extract. 
    This may involve inspecting the page's source code and identifying specific tags or attributes that contain 
    the data you need.

5) Write a scraper that extracts the desired data from the website's HTML code. This may involve using the 
library or tool you selected to parse the HTML and extract the relevant information.

6) Save the scraped data in a structured format, such as a CSV file, a spreadsheet, or a database.
"""

import requests
from bs4 import BeautifulSoup
from csv import writer
import json
from random import randint


def randomFill(osu_ids: set[int], num: int):
    """
    Fills ids set with random numbers indicating player ids. Caches IDs in a CSV file to remove duplicates

    :param ids: Set of ids to be filled
    :param num: Number of ids that will be added
    :return: void
    """

    cache_file = open('cache.csv', 'a+')
    cache_file.seek(0)

    cache = set()
    target = num + len(osu_ids)

    for line in cache_file:
        cache.add(int(line))

    while len(osu_ids) != target:
        r = randint(4539930, 29571657)
        if r in cache:
            continue
        cache_file.write(str(r) + '\n') # KoiFishu - Mochul
        osu_ids.add(r)
    

def getPlayerData(allPlayers: set, osu_ids: set[int]):
    """
    Fills associated set (allPlayers) with data containing the player of that id.

    :param allPlayers: Set to be filled.
    :param osu_ids: Set of IDs (denoted by the number at the end of the URLs)
    :return: void
    """

    # Create a session object to reuse the same TCP connection
    session = requests.Session()

    for id in osu_ids:
        URL = f"https://osu.ppy.sh/users/{id}"
        
        # Use the session object to make the request
        r = session.get(URL)

        # Create new soup object using the 'lxml' parser
        soup = BeautifulSoup(r.content, 'lxml')

        # Find the section that contains the global rank using a more specific CSS selector
        playerData = soup.select_one('div.js-react--profile-page.osu-layout.osu-layout--full')

        if playerData is None:
            continue
        
        # Access the value of the data-initial-data attribute
        initialData = playerData.get('data-initial-data')

        # Convert the data-initial-data string to a dictionary
        data_dict = json.loads(initialData)['user']
        stats = data_dict['statistics']

        # Add associated player data to the set
        if stats['global_rank'] != None:
            allPlayers.add((
                data_dict['username'],
                stats['global_rank'],
                stats['level']['current'] + stats['level']['progress'] / 100,
                stats['pp'],
                stats['ranked_score'],
                stats['play_time'],
                stats['play_count']
            ))
        
 
def toCSV(allPlayers: set[list[int,str]]):
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open('data.csv', 'a') as f_object:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object,lineterminator='\n')

        for l in allPlayers:
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(l)
    
        # Close the file object
        f_object.close()

if __name__ == "__main__":
    # Initialize empty set
    allPlayers = set()

    # All ids
    osu_ids = set()
    
    # Fill id list with randomFill
    randomFill(osu_ids, 2000)

    # Call getPlayerData to retrieve data from websites
    getPlayerData(allPlayers, osu_ids)

    # Write to CSV
    toCSV(allPlayers)
