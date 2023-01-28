import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','theis_project.settings')
import django
django.setup()

from districts.models import District, Branch
from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    url = f'https://www.mojegolebie.pl/PZHGP/katalog'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')

    number_district = 1
    districts = []
    branches = []

    for row in rows[1:]:
        tds = row.find_all('td')
        district = tds[0]
        branch = tds[1]
        if len(district.find_all('span'))>0:
            if len(district.find_all('a', href=True))>0:
                url_district = district.find_all('a', href=True)[0]['href']
            else:
                url_district = ""
            name_district = district.find_all('span')[0].text
            districts.append([number_district,
                name_district,
                url_district])
            number_district += 1

        if len(branch.find_all('a', href=True))>0:
            url_branch = branch.find_all('a', href=True)[0]['href']
        else:
            url_branch = ""

        name_branch = branch.find_all('span')[0].text
        number_branch = branch.find_all('span')[1].text
        name_branch = name_branch + " " + number_branch
        branches.append([name_district,
            name_branch,
            number_branch,
            url_branch])

    #Branch.objects.all().delete()
    #District.objects.all().delete()

    for district in districts:
        District.objects.get_or_create(id=district[0],
            name=district[1],
            website=district[2])[0]

    for branch in branches:
        district = District.objects.get(name=branch[0])
        Branch.objects.get_or_create(name=branch[1],
            district=district,
            website=branch[3],
            id=branch[2])[0]
