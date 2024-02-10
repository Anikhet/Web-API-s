from flask import Flask, render_template, request
import requests
from zeep import Client

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'movie_name' in request.form:
        movie_name = request.form['movie_name'].lower()
        url = "https://movie-database-alternative.p.rapidapi.com/"
        querystring = {"s":movie_name,"r":"json","page":"1"}
        headers = {
        "X-RapidAPI-Key": "7476ee983dmshf63250f46fec516p11287fjsn873e15c8eda0",
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
        }
        try:
            movie_response = requests.get(url, headers=headers, params=querystring)
            if movie_response.status_code == 200:

                imdb_ID = movie_response.json()['Search'][0]['imdbID']
                querystring = {"r": "json", "i": imdb_ID}

                celeb_response = requests.get(url, headers=headers, params=querystring)
                actor = celeb_response.json()['Actors']
                all_actors =celeb_response.json()['Actors']
                temp = actor.find(',')
                actor = actor[:temp]
                actor = actor.replace(".", "")


                celebrity_info_url = f'https://api.api-ninjas.com/v1/celebrity?name={actor}'
                celebrity_response = requests.get(celebrity_info_url, headers={'X-Api-Key': 'g6xtlmtdodBhSqZ0MP4hrA==1s79fFkgQcdxm3nt'})
                print(celebrity_response.text)
                location = celebrity_response.json()[0]['nationality']
                birthday = celebrity_response.json()[0]['birthday']
            
            
                # Now use the location to get the country name
                wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
                client = Client(wsdl=wsdl)
                result = client.service.FullCountryInfo(location.upper())
                country_flag = result['sCountryFlag']
                country_name = result['sName']
                city = result['sCapitalCity']

                api_url = 'https://api.api-ninjas.com/v1/weather?city={}'.format(city)
                response = requests.get(api_url, headers={'X-Api-Key': 'g6xtlmtdodBhSqZ0MP4hrA==1s79fFkgQcdxm3nt'})
                temp = response.json()['temp']

                return render_template('index.html', movie_name=movie_name, actor = all_actors,nationality = location,birth_date = birthday, country_flag = country_flag, country_name = country_name, temp = temp,city= city)
       
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e}")
            return render_template('index.html', error='Failed to fetch data due to an HTTPError.')
        except requests.exceptions.RequestException as e:
            print(f"RequestException: {e}")
            return render_template('index.html', error='Failed to make a request.')
        except Exception as e:
            print(f"Error: {e}")
            return render_template('index.html', error='An unexpected error occurred.')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000,debug=True)
