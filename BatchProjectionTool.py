import arcpy, os


class BatchProject(object):
    arcpy.env.overwriteOutput = True

    def __init__(self, in_features=None, out_features=None, prj_from_str=None, transform=None, ):
        self.prj_from_str = prj_from_str
        self.transform = transform
        self.in_features = in_features
        self.out_features = out_features

    def __iter__(self):
        return self

    def __repr__(self):
        return "Args are [{}, {} , {}, {}]".format(self.in_features, self.out_features, self.prj_from_str, self.transform)

    @staticmethod
    def list_fcs(input_gdb):
        arcpy.env.workspace = input_gdb
        gdb_work = arcpy.env.workspace
        arcpy.Compact_management(gdb_work)
        datasets = arcpy.ListDatasets(feature_type='feature')
        datasets = [''] + datasets if datasets is not None else []
        for ds in datasets:
            in_features = sorted(
                [str(os.path.join(input_gdb, ds, fc)) for fc in arcpy.ListFeatureClasses(feature_dataset=ds)])
            print in_features
            return in_features

    @staticmethod
    def list_shps_in_dir(folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".shp")]

    @classmethod
    def from_directory(cls, project_dir, prj_from_str, transform):
        in_shps = BatchProject.list_shps_in_dir(project_dir)
        out_shps = [os.path.join(project_dir, f.replace(".shp", "_projected.shp")) for f in
                                            in_shps if f.endswith(".shp")]

        for in_shp, out_shp in zip(in_shps, out_shps):
            arcpy.Project_management(in_shp, out_shp, prj_from_str, transform)
            print 'Complete'

    @classmethod
    def from_gdb(cls, input_gdb, prj_from_str, transform):
        in_fcs = BatchProject.list_fcs(input_gdb)
        print in_fcs
        out_fcs = [fc + "_projected" for fc in in_fcs]

        for in_fc, out_fc in zip(in_fcs, out_fcs):
            print(in_fc, out_fc)
            arcpy.Project_management(in_fc, out_fc, prj_from_str, transform)

    @classmethod
    def from_single_shp(cls, in_shp, prj_from_str, transform):
        out_shp = in_shp.replace(".shp", "_projected.shp")
        arcpy.Project_management(in_shp, out_shp, prj_from_str, transform)

    @classmethod
    def from_single_fc(cls, in_fc, prj_from_str, transform):
        gdb, fc = os.path.split(in_fc)
        out_fc = os.path.join(gdb, fc + "_projected")
        arcpy.Project_management(in_fc, out_fc, prj_from_str, transform)


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


