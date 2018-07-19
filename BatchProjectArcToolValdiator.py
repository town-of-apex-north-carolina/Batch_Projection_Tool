
import arcpy, os
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    def list_fcs(input_gdb):

        arcpy.env.workspace = input_gdb
        gdb_work = arcpy.env.workspace
        arcpy.Compact_management(gdb_work)
        datasets = arcpy.ListDatasets(feature_type='feature')
        datasets = [''] + datasets if datasets is not None else []
        for ds in datasets:
            in_features = [str(os.path.join(input_gdb, fc)) for fc in arcpy.ListFeatureClasses(feature_dataset=ds)]

            return in_features

    if self.params[0].value is not None and self.params[4] is not None:
        fc_list = list_fcs(self.params[0].valueAsText)
        desc = arcpy.Describe(fc_list[0]).spatialReference
        extent = arcpy.Describe(fc_list[0]).extent

        sr = arcpy.SpatialReference()
        sr.loadFromString(self.params[4].valueAsText)
        to_sr = arcpy.SpatialReference(sr.factoryCode)

        transformations = arcpy.ListTransformations(desc, to_sr, extent)

        self.params[5].value = transformations[0]

    if self.params[1].value is not None and self.params[4] is not None:
        shp_list = [os.path.join(self.params[1].valueAsText, f) for f in os.listdir(self.params[1].valueAsText) if
                    f.endswith(
            ".shp")]
        desc = arcpy.Describe(shp_list[0]).spatialReference
        extent = arcpy.Describe(shp_list[0]).extent

        sr = arcpy.SpatialReference()
        sr.loadFromString(self.params[4].valueAsText)
        to_sr = arcpy.SpatialReference(sr.factoryCode)

        transformations = arcpy.ListTransformations(desc, to_sr, extent)

        self.params[5].value = transformations[0]

    if self.params[2].value is not None and self.params[4] is not None:
        desc = arcpy.Describe(self.params[2].value).spatialReference
        extent = arcpy.Describe(self.params[2].value).extent

        sr = arcpy.SpatialReference()
        sr.loadFromString(self.params[4].valueAsText)

        to_sr = arcpy.SpatialReference(sr.factoryCode)
        transformations = arcpy.ListTransformations(desc, to_sr, extent)
        self.params[5].value = transformations[0]

    if self.params[3].value is not None and self.params[4] is not None:
        desc = arcpy.Describe(self.params[3].valueAsText).spatialReference
        extent = arcpy.Describe(self.params[3].valueAsText).extent

        sr = arcpy.SpatialReference()
        sr.loadFromString(self.params[4].valueAsText)

        to_sr = arcpy.SpatialReference(sr.factoryCode)
        transformations = arcpy.ListTransformations(desc, to_sr, extent)
        self.params[5].value = transformations[0]

    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""

    return

