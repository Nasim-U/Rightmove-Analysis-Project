# importing our libraries

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random
import datetime

BOROUGHS = {
    "Reading": "5E1114"
}


def main():

    # initialise index, this tracks the page number we are on. every additional page adds 24 to the index

    # create lists to store our data
    all_apartment_links = []
    all_description = []
    all_address = []
    all_price = []

    # apparently the maximum page limit for rightmove is 42
    for borough in list(BOROUGHS.values()):

        # initialise index, this tracks the page number we are on. every additional page adds 24 to the index
        index = 0

        key = [key for key, value in BOROUGHS.items() if value == borough]
        print(f"We are scraping the borough named: {key}")
        for pages in range(41):

            # define our user headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
            }

            if index == 0:
                rightmove = f"https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=REGION%{borough}&insId=1&radius=0.0&minPrice=&maxPrice=&minBedrooms=&maxBedrooms=&displayPropertyType=&maxDaysSinceAdded=&sortByPriceDescending=&_includeLetAgreed=on&primaryDisplayPropertyType=&secondaryDisplayPropertyType=&oldDisplayPropertyType=&oldPrimaryDisplayPropertyType=&letType=&letFurnishType=&houseFlatShare="
            elif index != 0:
                rightmove = f"https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%{borough}&index={index}&propertyTypes=&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords="

            # request our webpage
            res = requests.get(rightmove, headers=headers)

            # check status
            res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            # This gets the list of apartments
            apartments = soup.find_all("div", class_="l-searchResult is-list")

            # This gets the number of listings
            number_of_listings = soup.find(
                "span", {"class": "searchHeader-resultCount"}
            )
            number_of_listings = number_of_listings.get_text()
            number_of_listings = int(number_of_listings.replace(",", ""))

            for i in range(len(apartments)):

                # tracks which apartment we are on in the page
                first_var = apartments[i]

                # append link
                apartment_info = first_var.find("a", class_="propertyCard-link")
                link = "https://www.rightmove.co.uk" + apartment_info.attrs["href"]
                all_apartment_links.append(link)

                # append address
                address = (
                    apartment_info.find("address", class_="propertyCard-address")
                    .get_text()
                    .strip()
                )
                all_address.append(address)

                # append description
                description = (
                    apartment_info.find("h2", class_="propertyCard-title")
                    .get_text()
                    .strip()
                )
                all_description.append(description)

                # append price
                price = (
                    first_var.find("div", class_="propertyCard-rentalPrice-primary")
                    .get_text()
                    .strip()
                )
                all_price.append(price)


            print(f"You have scrapped {pages + 1} pages of apartment listings.")
            print(f"You have {number_of_listings - index} listings left to go")
            print("\n")

            # code to make them think we are human
            time.sleep(random.randint(1, 3))
            index = index + 24

            if index >= number_of_listings:
                break

    # convert data to dataframe
    data = {
        "Links": all_apartment_links,
        "Address": all_address,
        "Description": all_description,
        "Price": all_price,
    }
    df = pd.DataFrame.from_dict(data)
    df.to_csv(r"sales_data_reading.csv", encoding="utf-8", header="true", index=False)


if __name__ == "__main__":
    main()