import exiv2
from gmplot import gmplot
import webbrowser
from decimal import Decimal, getcontext

def dms_to_decimal(degrees, minutes, seconds):
    print(degrees[0], minutes[0]/60.0, round(seconds[0]/1000000.0/3600.0,4))
    decimal_degrees = degrees[0] + minutes[0] / 60.0 + seconds[0]/1000000.0 / 3600.0
    return decimal_degrees

def get_gps_coordinates(image_path):
    try:
        # Abrir la imagen
        image = exiv2.ImageFactory.open(image_path)
        image.readMetadata()
        
        # Obtener datos EXIF
        data = image.exifData()

        # Verificar si hay datos GPS disponibles
        if 'Exif.GPSInfo.GPSLatitude' in data and 'Exif.GPSInfo.GPSLongitude' in data:
            
            # Obtener coordenadas de latitud y longitud
            latitude = data['Exif.GPSInfo.GPSLatitude'].getValue()            
            print(data['Exif.GPSInfo.GPSLatitude'])            
            longitude = data['Exif.GPSInfo.GPSLongitude'].getValue()
            print(data['Exif.GPSInfo.GPSLongitude'])
            
            # Convertir coordenadas de DMS a decimal
            latitude_decimal = dms_to_decimal(latitude[0], latitude[1], latitude[2])
            
            lat_dir = data['Exif.GPSInfo.GPSLatitudeRef'].toString()        
            if lat_dir == "S":
                latitude_decimal = -latitude_decimal
                print('daddy')
                
            longitude_decimal = dms_to_decimal(longitude[0], longitude[1], longitude[2])
            
            long_dir = data['Exif.GPSInfo.GPSLongitudeRef'].toString()
            if long_dir == 'W':
                longitude_decimal = -longitude_decimal

            return latitude_decimal, longitude_decimal
        else:
            print("No se encontraron datos de GPS en la imagen.")
            return None
    
    except Exception as e:
        print(f"Error al leer los metadatos EXIF: {e}")
        return None

# Ruta de la imagen con datos EXIF
image_path = 'test.jpg'

# Obtener coordenadas GPS
gps_coordinates = get_gps_coordinates(image_path)

""" Typically, latitude and longitude coordinates are in the range of:

Latitude: -90 to +90 degrees
Length: -180 to +180 degrees
"""

if gps_coordinates:
    latitude, longitude = gps_coordinates
    print(f"Coordenadas GPS:\nLatitud: {round(latitude, 4)}\nLongitud: {round(longitude, 4)}")
    
    gmap = gmplot.GoogleMapPlotter(round(latitude, 4), round(longitude, 4), zoom=12)
    print(latitude, longitude)
    gmap.marker(round(latitude, 4), round(longitude, 4), color="cornflowerblue")

    gmap.draw("location.html")

    webbrowser.open("location.html", new=2)
