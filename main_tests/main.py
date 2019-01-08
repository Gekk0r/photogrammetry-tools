import numpy
import gdal

file = "zacler.tif"
# ds = gdal.Open(file, 1)
# band = ds.GetRasterBand(1)
# arr = band.ReadAsArray()

gdal.AllRegister()
rast_src = gdal.Open(file, 1)
gt = rast_src.GetGeoTransform()
gtl = list(gt)
gtl[0] = 632500.000000000000000
gtl[3] = 990017.937500000000000
rast_src.SetGeoTransform(tuple(gtl))
rast_src.FlushCache()
rast_src = None
# rast_src = None

ds = gdal.Open(file)
band = ds.GetRasterBand(1)
arr = band.ReadAsArray()
[cols, rows] = arr.shape
# arr_min = arr.Min()
# arr_max = arr.Max()
# arr_mean = int(arr.mean())
# arr_out = numpy.where((arr < arr_mean), 10000, arr)
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create("prova.tif", rows, cols, 1, gdal.GDT_UInt16)
a = ds.GetGeoTransform()
outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
outdata.SetGeoTransform(tuple(gtl))
outdata.SetProjection(ds.GetProjection())##sets same projection as input
outdata.GetRasterBand(1).WriteArray(ds.GetRasterBand(1).ReadAsArray())

outdata.GetRasterBand(1).SetNoDataValue(10000)##if you want these values transparent
outdata.FlushCache() ##saves to disk!!
outdata = None
band=None
ds=None

# [cols, rows] = arr.shape
# arr_min = arr.Min()
# arr_max = arr.Max()
# arr_mean = int(arr.mean())
# arr_out = numpy.where((arr < arr_mean), 10000, arr)
# driver = gdal.GetDriverByName("GTiff")
# outdata = driver.Create(outFileName, rows, cols, 1, gdal.GDT_UInt16)
# outdata.SetGeoTransform(ds.GetGeoTransform())##sets same geotransform as input
# outdata.SetProjection(ds.GetProjection())##sets same projection as input
# outdata.GetRasterBand(1).WriteArray(arr_out)
# outdata.GetRasterBand(1).SetNoDataValue(10000)##if you want these values transparent
# outdata.FlushCache() ##saves to disk!!
# outdata = None
# band=None
# ds=None