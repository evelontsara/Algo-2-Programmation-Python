from bs4 import BeautifulSoup
import requests
import csv
import re


def find_url(page = 1):
    url = 'https://www.lacentrale.fr/listing?makesModelsCommercialNames=AUDI&options=&page={page}'.format(page=page) 
    return url

def main():
    stock = []

    for page in range(1, 11):
        url = find_url(page)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        search_elements = soup.find_all('div', 'Vehiculecard_Vehiculecard_cardBody')

        for string in search_elements:
            title = string.find("h3").text
            brand, model = title.split(maxsplit=1)
            element = string.find_all('div', 'Text_Text_text Vehiculecard_Vehiculecard_characteristicsItems Text_Text_body2') 
            year_text = element [0].text.strip()
            year = int(''.join(filter(str.isdigit, year_text)))
            fuel_text = element[1].text.strip() 
            fuel = int(''.join(filter(str.isdigit, fuel_text)))
            mileage = element [2].text                  
            price_text = string.find('span', 'Text_Text_text Vehiculecard_Vehiculecard_price Text_Text_subtitle2').text
            price = int(re.sub("[^0-9]", "", price_text))
            motor = string.find('div', 'Text_Text_text Vehiculecard_Vehiculecard_subTitle Text_Text_body2').text           

            if string:
                print("brand :", brand, '\n', "model  :", model, '\n', "year :", year, '\n', "price :", price, '\n', "motor :", motor, '\n' "fuel :", fuel, '\n', "mileage :", mileage, '\n')

                stock.append([brand, model, motor, year, mileage, fuel, price])

    with open("final.csv", "w", newline="") as fd:
        writer = csv.writer(fd)
        writer.writerow(
            ["brand", "model", "motor", "year","mileage", "fuel", "price"])
        for row in stock:
            writer.writerow(row)

if __name__ == "__main__":
    main()
