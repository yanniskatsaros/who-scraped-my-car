# Who Scraped My Car?
Let's build a web-scraper to download and parse car listings from AutoTrader to build a pricing model!
_____

## Requirements
The project depends on `requests`, `beautifulsoup4`, and `pydantic`. You can install the appropriate versions using the following command:

`python -m pip install -r requirements.txt`

## Usage
The project comes with a simple CLI to easily download links to URLs for car listings of a specific brand (make) in a given ZIP code. You can specify your search radius relative to your target ZIP code and limit the total number of entries to download.

To specify a car make, use one of the following "car codes" common to AutoTrader's system.

`python cars/main.py`
```
usage: main.py [-h] [--search-radius SEARCH_RADIUS] [--limit LIMIT]
               {AMC,ACURA,ALFA,ASTON,AUDI,BMW,BENTL,BUGATTI,BUICK,CAD,CHEV,CHRY,DAEW,DATSUN,DELOREAN,DODGE,EAGLE,FIAT,FER,FISK,FORD,FREIGHT,GMC,GENESIS,GEO,AMGEN,HONDA,HYUND,INFIN,ISU,JAG,JEEP,KARMA,KIA,LAM,ROV,LEXUS,LINC,LOTUS,MAZDA,MINI,MAS,MAYBACH,MCLAREN,MB,MERC,MIT,NISSAN,OLDS,PLYM,PONT,POR,RAM,RR,SRT,SAAB,SATURN,SCION,SUB,SUZUKI,TESLA,TOYOTA,VOLKS,VOLVO,YUGO,SMART}
               zip_code

Download car listings for a given car make, within a certain radius of a given
ZIP code

positional arguments:
  {AMC,ACURA,ALFA,ASTON,AUDI,BMW,BENTL,BUGATTI,BUICK,CAD,CHEV,CHRY,DAEW,DATSUN,DELOREAN,DODGE,EAGLE,FIAT,FER,FISK,FORD,FREIGHT,GMC,GENESIS,GEO,AMGEN,HONDA,HYUND,INFIN,ISU,JAG,JEEP,KARMA,KIA,LAM,ROV,LEXUS,LINC,LOTUS,MAZDA,MINI,MAS,MAYBACH,MCLAREN,MB,MERC,MIT,NISSAN,OLDS,PLYM,PONT,POR,RAM,RR,SRT,SAAB,SATURN,SCION,SUB,SUZUKI,TESLA,TOYOTA,VOLKS,VOLVO,YUGO,SMART}
                        A code representing the car make
  zip_code              ZIP code of the area to search listings for

optional arguments:
  -h, --help            show this help message and exit
  --search-radius SEARCH_RADIUS
                        A search radius (in miles) within the given ZIP code
  --limit LIMIT         Limit the total number of entries to search for
```

### Examples
Download URLs for all Porsche listings within 100 miles (default) of the 77056 zip code (output truncated for brevity)

`python cars/main.py POR 77056`
```
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=555304984
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=549029457
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=553937810
...
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=556808514
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=542778710
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=556608600
```

Download URLs for all Jaguar listings in the 78254 zip code for a 20 mile radius

`python cars/main.py JAG 78254 --search-radius 20`
```
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=555182522
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=555481342
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=553690777
...
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=555481327
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=551052772
https://www.autotrader.com/cars-for-sale/vehicledetails.xhtml?listingId=555872157
```

This is a work in progress so stay tuned for more updates in the future!
