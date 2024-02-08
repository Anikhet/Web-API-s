from flask import Flask, render_template, request, jsonify
import requests
from zeep import Client

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'animal_name' in request.form:
        animal_name = request.form['animal_name'].lower()
        animal_info_url = f'https://api.api-ninjas.com/v1/animals?name={animal_name}'
        animal_response = requests.get(api_url, headers={'X-Api-Key': 'g6xtlmtdodBhSqZ0MP4hrA==1s79fFkgQcdxm3nt'})

        if animal_response.status_code == 200:
            animal_data = animal_response.json()[0]  # Assuming the animal data is in the first index
            location = animal_data.get('location')

            # Now use the location to get the country name
            country_name = get_country_from_location(location)
            return render_template('animal.html', animal_name=animal_name, location=location, country_name=country_name)
        else:
            return render_template('index.html', error='Failed to fetch animal data.')

    return render_template('index.html')


#  if 'country_code' in request.form:
#             country_code = request.form['country_code']
#             wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
#             client = Client(wsdl=wsdl)
#             result = client.service.FullCountryInfo(country_code)['sCountryFlag']
#             return render_template('index.html', capital_city=result)



if __name__ == '__main__':
    app.run(debug=True)
