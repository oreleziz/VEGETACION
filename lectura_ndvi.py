import rasterio

image_file = ("imagen_NDVI.tif")

# Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
with rasterio.open(image_file) as src:
    band_red = src.read(.5)

with rasterio.open(image_file) as src:
    band_nir = src.read(1)
    # Calculate NDVI
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
# Set spatial characteristics of the output object to mirror the input
kwargs = src.meta
kwargs.update(dtype=rasterio.float32,count = 1)
# Create the file
with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
    dst.write_band(1, ndvi.astype(rasterio.float32))
#apply a color map
import matplotlib.pyplot as plt
plt.imsave("ndvi_cmap.png", ndvi, cmap=plt.cm.summer)
#adceder a los dataset de una lectura de vegetacion para luego imprimir la coordenadas de un value 256
from osgeo import gdal
import struct
 
nameraster = "imagen_NDVI.tif"
 
hdf_file = gdal.Open(nameraster)
 
subDatasets = hdf_file.GetSubDatasets()
 
dataset = gdal.Open(subDatasets[0][0])
geotransform = dataset.GetGeoTransform()
band = dataset.GetRasterBand(1)
 
fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I', 
            'Int32':'i', 'Float32':'f', 'Float64':'d'}
 
print ("rows = %d columns = %d" % (band.YSize, band.XSize))
 
BandType = gdal.GetDataTypeName(band.DataType)
 
print( "Data type = ", BandType)
 
print( "Executing with %s" % nameraster)
 
print ("test_value = 256")
 
X = geotransform[0] #x coordinate
Y = geotransform[3] #y coordinate
 
for y in range(band.YSize):
 
    scanline = band.ReadRaster(0, 
                               y, 
                               band.XSize, 
                               1, 
                               band.XSize, 
                               1, 
                               band.DataType)
 
    values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)
 
    for value in values:
 
        if(value == 256):       
            print( "%.4f %.4f %.2f" % (X, Y, value))
        X += geotransform[1] #x pixel size
    X = geotransform[0]
    Y += geotransform[5] #y pixel size
 
dataset = None