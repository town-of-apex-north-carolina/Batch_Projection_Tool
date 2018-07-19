import arcpy
from batch_project import BatchProject

def main():
    gdb = arcpy.GetParameterAsText(0)
    shp_direct = arcpy.GetParameterAsText(1)
    shp = arcpy.GetParameterAsText(2)
    fc = arcpy.GetParameterAsText(3)
    coordsys = arcpy.GetParameterAsText(4)
    trans = arcpy.GetParameterAsText(5)

    if gdb:
        BatchProject.from_gdb(gdb, coordsys, trans)

    if shp_direct:
        BatchProject.from_directory(shp_direct, coordsys, trans)

    if shp:
        BatchProject.from_single_shp(shp, coordsys, trans)

    if fc:
        BatchProject.from_single_fc(fc, coordsys, trans)


if __name__ == '__main__':
    main()


