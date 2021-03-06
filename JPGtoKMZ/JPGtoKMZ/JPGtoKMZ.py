import os
import simplekml
import exifread

#Tell where the files are
mainDir = "C:\\Users\\goker\\Desktop\\"

#find all the files in the given directory
FileList = os.listdir(mainDir + "EXIF Data")

for file in FileList:
    #Operate only if the file extension is JPG
    if file[len(file)-3:len(file)] == "JPG":
        f = open(mainDir + "EXIF Data\\" + file, 'rb')
        tags = exifread.process_file(f, strict= True, stop_tag = 'GPS GPSLongitude')
        try:
            #get GPS data
            lonDMS = tags['GPS GPSLongitude'].values
            latDMS = tags['GPS GPSLatitude'].values

            #convert DMS to degrees
            lonDec = lonDMS[0] + (lonDMS[1] + lonDMS[2]/60)/60
            latDec = latDMS[0] + (latDMS[1] + latDMS[2]/60)/60

            #create the KML file with photo overlay
            kml = simplekml.Kml()
            #kml.newpoint(name=file[0:len(file)-4], description = file[4:len(file)-4], coords=[(float(lonDec), float(latDec))])  # lon, lat, optional height
            photo = kml.newphotooverlay(name = file[0:len(file)-4])
            photo.camera = simplekml.Camera(longitude=float(lonDec), latitude = float(latDec), altitude=50, altitudemode=simplekml.AltitudeMode.relativetoground)
            photo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/camera.png'
            photo.icon.href = mainDir + "EXIF Data\\" + file
            photo.point.coords = [(float(lonDec), float(latDec))]
            photo.viewvolume = simplekml.ViewVolume(-25,25,-15,15,1)
            kml.save(mainDir + "EXIF KML\\" + file[0:len(file)-4] +".kml")
            print(file[0:len(file)-4] +".kml is done!")

        #If the file has no GPS data
        except KeyError:
            print(file + " has no GPS")