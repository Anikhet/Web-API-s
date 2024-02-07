from flask import Flask, render_template
from zeep import Client

app = Flask(__name__)

@app.route('/')
def home():
    wsdl = 'http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL'
    client = Client(wsdl=wsdl)
    result = client.service.FullCountryInfo('US')['sCapitalCity']
    return render_template('index.html', capital_city=result)

if __name__ == '__main__':
    app.run(debug=True)
