#the purpose of this script is to get the length of the wikipeida pages of US presidents
#and then to find the president with the longest wikipedia page

#I am going to do this by first using the requests library to go through the table here
#https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States
#from there, I am going to go to each of the presidentrs and get the length of the page


import requests
from bs4 import BeautifulSoup

def get_president_links(url):
    # this function will get the links to the presidents
    # and return a list of links
    presidents_list = []
    request = requests.get(url)
    if request.status_code != 200:
        print("Error: {}".format(request.status_code))
        return None
    else:
        soup = BeautifulSoup(request.text, "html.parser")
        table = soup.find("table", {"class": "wikitable"}) #This gets the table of Presidents
        count = 0
        for row in table.find_all("tr"):
            #if the first cell in the row has a number which is a link, then the third item is the name of the president
            if row.find("th") is not None:
                count += 1
                for cell in row.find_all("td"):
                    if cell.find("b") is not None:
                        presidents_list.append(cell.find("b").find("a").get("href"))
    return presidents_list

#this is the main method of the script
def main():
    pres_name_and_length = {}
    presidents = get_president_links('https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States')
    for president in presidents:
        president = "https://en.wikipedia.org/" + president
        request = requests.get(president)
        if request.status_code != 200:
            print("Error: {}".format(request.status_code))
            continue
        else:
            soup = BeautifulSoup(request.text, "html.parser")
            title = soup.find("h1", {"id": "firstHeading"})
            pres_name_and_length[title.text] = len(soup.get_text())
    longest_pres = max(pres_name_and_length, key=pres_name_and_length.get)
    print(longest_pres)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
