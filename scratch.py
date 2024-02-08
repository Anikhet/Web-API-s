from flask import Flask, render_template, request, jsonify
import requests
from zeep import Client

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'celebrity_name' in request.form:
        celebrity_name = request.form['celebrity_name'].lower()
        celebrity_info_url = f'https://api.api-ninjas.com/v1/celebrity?name={celebrity_name}'
        celebrity_response = requests.get(celebrity_info_url, headers={'X-Api-Key': 'g6xtlmtdodBhSqZ0MP4hrA==1s79fFkgQcdxm3nt'})

        if celebrity_response.status_code == 200:
            celebrity_data = celebrity_response.json()[0]['name'].title()
            location = celebrity_response.json()[0]['nationality'] 
            # Now use the location to get the country name
            wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
            client = Client(wsdl=wsdl)
            result = client.service.FullCountryInfo(location.upper())

            url = "https://search-celebrity-biography.p.rapidapi.com/search/miley%20cyrus"

            headers = {"X-RapidAPI-Key": "7476ee983dmshf63250f46fec516p11287fjsn873e15c8eda0",
                       "X-RapidAPI-Host": "search-celebrity-biography.p.rapidapi.com"}

            new_response = requests.get(url, headers=headers)
            birth_date = age = new_response.json()['moreFacts'][1]['value']
            age = new_response.json()['moreFacts'][2]['value']
            birth_loc = new_response.json()['moreFacts'][21]['value']
            nationality = new_response.json()['moreFacts'][22]['value']

            
            country_flag = result['sCountryFlag']
            return render_template('index.html', celebrity_name=celebrity_data, country_flag=country_flag,
                                     birth_date = birth_date, age=age)
        else:
            return render_template('index.html', error='Failed to fetch celebrity data.')

    return render_template('index.html')


#  if 'country_code' in request.form:
#             country_code = request.form['country_code']
#             wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
#             client = Client(wsdl=wsdl)
#             result = client.service.FullCountryInfo(country_code)['sCountryFlag']
#             return render_template('index.html', capital_city=result)



if __name__ == '__main__':
    app.run(port=5000,debug=True)
