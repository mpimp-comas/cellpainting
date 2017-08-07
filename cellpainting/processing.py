#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
##########
Processing
##########

*Created on Thu Jun  1 14:15 2017 by A. Pahl*

Processing results from the CellPainting Assay in the Jupyter notebook.
This module provides the DataSet class and its methods.
Additional functions in this module act on pandas DataFrames.
convert 170512_B03_s5_w149D3C0B4-85CE-42BE-AB4F-1B460BEECC73.tif -resize 200x200 -negate 170512_B03_s5_w1.png

# invert image:
from PIL import Image
import PIL.ImageOps
image = Image.open('your_image.png')
inverted_image = PIL.ImageOps.invert(image)
inverted_image.save('new_name.png')

# resize an image
size = (200, 200)
im = Image.open(infile)
im.thumbnail(size, Image.ANTIALIAS)
im.save(outfile, "JPEG")
"""

import time
import glob
import os.path as op
from collections import Counter
import xml.etree.ElementTree as ET
import pickle

import pandas as pd
import numpy as np

from IPython.core.display import HTML

from . import tools as cpt
from .config import ACT_PROF_PARAMETERS, ACT_CUTOFF_PERC, LIMIT_SIMILARITY_L

try:
    from misc_tools import apl_tools
    AP_TOOLS = True
    #: Library version
    VERSION = apl_tools.get_commit(__file__)
    # I use this to keep track of the library versions I use in my project notebooks
    print("{:45s} (commit: {})".format(__name__, VERSION))

except ImportError:
    AP_TOOLS = False
    print("{:45s} ({})".format(__name__, time.strftime("%y%m%d-%H:%M", time.localtime(op.getmtime(__file__)))))

try:
    from . import resource_paths
except ImportError:
    print("""# Resource Paths not found. You need to create a file `resource_paths.py` in the project dir.
      It has to contain the locations of
        - smiles_path: gzipped tab-delim. file with structure Smiles and Compound_Id.
        - annotations_path: tab-delim. file with annotations to the references.
        - references_path: tab-delim. file to the references to compare against.
        - sim_refs_path: pickle file containing the similar references to every compound.
        - layouts_path: tab-delim. file containing all plate layouts.
    """)

FINAL_PARAMETERS = ['Metadata_Plate', 'Metadata_Well', 'plateColumn', 'plateRow',
                    "Compound_Id", 'Container_Id', "Producer", "Pure_Flag", "Toxic", "Rel_Cell_Count",
                    "Known_Act", "Trivial_Name", 'WellType', 'Conc_uM', "Activity", "Act_Profile",
                    "Plate", "Smiles"]
DROP_FROM_NUMBERS = ['plateColumn', 'plateRow', 'Conc_uM', "Compound_Id"]
DROP_GLOBAL = ["PathName_CellOutlines", "URL_CellOutlines", 'FileName_CellOutlines',
               'ImageNumber', 'Metadata_Site', 'Metadata_Site_1', 'Metadata_Site_2']
DEBUG = False


def debug_print(txt, val):
    if DEBUG:
        txt = txt + ":"
        print("DEBUG   {:20s}".format(txt), val)


class DataSet():
    def __init__(self, log=True):
        self.data = pd.DataFrame()
        self.fields = {"plateColumn": "Metadata_Plate",
                       "WellType": "WellType", "ControlWell": "Control", "CompoundWell": "Compound"}
        self.log = log


    def __getitem__(self, item):
        res = self.data[item]
        if isinstance(res, pd.DataFrame):
            result = DataSet()
            result.data = res
            result.print_log("subset")
        else:
            result = res
        return result


    def __getattr__(self, name):
        """Try to call undefined methods on the underlying pandas DataFrame."""
        def method(*args, **kwargs):
            res = getattr(self.data, name)(*args, **kwargs)
            if isinstance(res, pd.DataFrame):
                result = DataSet()
                result.data = res
                result.print_log(name)
            else:
                result = res
            return result
        return method


    def show(self):
        parameters = [k for k in FINAL_PARAMETERS if k in self.data]
        print("Shape:     ", self.shape)
        print("Parameters:", parameters)
        return HTML(self.data[parameters]._repr_html_())


    def head(self, n=5):
        parameters = [k for k in FINAL_PARAMETERS if k in self.data]
        res = self.data[parameters].head(n)
        result = DataSet()
        result.data = res
        result.print_log("head")
        return result


    def drop_cols(self, cols, inplace=False):
        """Drops the list of columns from the DataFrame.
        Listed columns that are not present in the DataFrame are simply ignored
        (no error is thrown)."""
        if inplace:
            drop_cols(self.data, cols, inplace=True)
            self.print_log("drop cols (inplace)")
        else:
            result = DataSet()
            result.data = drop_cols(self.data, cols, inplace=False)
            result.print_log("drop cols")
            return result


    def keep_cols(self, cols, inplace=False):
        if inplace:
            self.data = self.data[cols]
            self.print_log("keep cols (inplace)")
        else:
            result = DataSet()
            result.data = self.data[cols]
            result.print_log("keep cols")
            return result


    def print_log(self, component, add_info=""):
        if self.log:
            print_log(self.data, component, add_info)


    def load(self, fn, sep="\t"):
        """Read one or multiple result files and concatenate them into one dataset.
        `fn` is a single filename (string) or a list of filenames."""
        self.data = load(fn, sep=sep).data
        self.print_log("load data")


    def write_csv(self, fn, parameters=None, sep="\t"):
        result = self.data.copy()
        if isinstance(parameters, list):
            result = result[parameters]
        result.to_csv(fn, sep=sep, index=False)


    def write_pkl(self, fn):
        self.data.to_pickle(fn)


    def write_parameters(self, fn="parameters.txt"):
        parameters = sorted(self.measurements)
        with open("parameters.txt", "w") as f:
            f.write('"')
            f.write('",\n"'.join(parameters))
            f.write('"')
        print(len(parameters), "parameters written.")


    def describe(self, times_mad=3.0):
        df = numeric_parameters(self.data)
        stats = pd.DataFrame()
        stats["Min"] = df.min()
        stats["Max"] = df.max()
        stats["Median"] = df.median()
        stats["MAD"] = df.mad()
        stats["Outliers"] = df[(((df - df.median()).abs() - times_mad * df.mad()) > 0)].count()
        print(self.shape)
        return stats


    def well_type_from_position(self):
        """Assign the WellType from the position on the plate.
        Controls are in column 11 and 12"""
        result = DataSet(log=self.log)
        result.data = well_type_from_position(self.data)
        result.print_log("well type from pos")
        return result


    def well_from_position(self, well_name="Metadata_Well",
                           row_name="plateRow", col_name="plateColumn"):
        """Assign Metadata_Well from plateRow, plateColumn"""
        result = DataSet(log=self.log)
        result.data = well_from_position(self.data, well_name=well_name,
                                         row_name=row_name, col_name=col_name)
        result.print_log("well from pos")
        return result


    def position_from_well(self, well_name="Metadata_Well",
                           row_name="plateRow", col_name="plateColumn"):
        """Generate plateRow and plateColumn from Metatadata_Well"""
        result = DataSet(log=self.log)
        result.data = position_from_well(self.data, well_name=well_name,
                                         row_name=row_name, col_name=col_name)
        result.print_log("pos from well")
        return result


    def join_layout_384(self, layout_fn, on="Address_384"):
        result = DataSet(log=self.log)
        result.data = join_layout_384(self.data, layout_fn, on=on)
        result.print_log("join layout 384")
        return result


    def join_layout_1536(self, plate, quadrant, on="Address_384", how="inner"):
        """Cell Painting is always run in 384er plates.
        COMAS standard screening plates are format 1536.
        With this function, the 1536-to-384 reformatting file
        with the smiles added by join_smiles_to_layout_1536()
        can be used directly to join the layout to the individual 384er plates."""
        result = DataSet(log=self.log)
        result.data = join_layout_1536(self.data, plate, quadrant, on=on, how=how)
        result.print_log("join layout 1536")
        return result


    def numeric_parameters(self):
        result = DataSet()
        result.data = numeric_parameters(self.data)
        return result


    def flag_toxic(self, cutoff=0.55):
        """Flag data rows of toxic compounds"""
        result = DataSet()
        result.data = flag_toxic(self.data, cutoff=cutoff)
        flagged = result.data["Toxic"].sum()
        result.print_log("flag toxic", "{:3d} flagged".format(flagged))
        return result


    def remove_toxic(self, cutoff=0.55):
        """Remove data rows of toxic compounds"""
        result = DataSet()
        toxic = DataSet()
        result.data, toxic.data = remove_toxic(self.data, cutoff=cutoff)
        result.print_log("remove toxic", "{:3d} removed".format(toxic.shape[0]))
        return result, toxic


    def remove_impure(self, strict=False, reset_index=True):
        """Remove entries with `Pure_Flag == "Fail"`"""
        result = DataSet()
        flagged = DataSet()
        result.data, flagged.data = remove_impure(self.data)
        result.print_log("remove impure", "{:3d} removed".format(flagged.shape[0]))
        return result, flagged


    def remove_outliers(self, times_dev=3.0, group_by=None, method="median"):
        """Returns the filtered dataframe as well as the outliers.
        method can be `median`or `mean` """
        result = DataSet()
        outliers = DataSet()
        result.data, outliers.data = remove_outliers(self.data, times_dev=times_dev,
                                                     group_by=group_by, method=method)
        result.print_log("remove outliers", "{:3d} removed".format(outliers.shape[0]))
        return result, outliers


    def remove_skipped_echo_direct_transfer(self, fn):
        """Remove wells that were reported as skipped in the Echo protocol (xml).
        This functions works with Echo direct transfer protocols.
        Function supports using wildcards in the filename, the first file will be used.
        Returns a new dataframe without the skipped wells."""
        result = DataSet()
        result.data, skipped = remove_skipped_echo_direct_transfer(self.data, fn=fn)
        skipped_str = "(" + ", ".join(skipped) + ")"
        result.print_log("remove skipped", "{:3d} skipped {}".format(self.shape[0] - result.shape[0],
                                                                     skipped_str))
        return result


    def drop_dups(self, cpd_id="Compound_Id"):
        """Drop duplicate Compound_Ids"""
        result = DataSet()
        result.data = self.data.drop_duplicates(cpd_id)
        result.print_log("drop dups")
        return result


    def group_on_well(self, group_by=FINAL_PARAMETERS):
        """Group results on well level."""
        result = DataSet()
        result.data = group_on_well(self.data, group_by=group_by)
        result.print_log("group on well")
        return result


    def join_smiles(self, df_smiles=None):
        """Join Smiles from Compound_Id."""
        result = DataSet()
        result.data = join_smiles(self.data, df_smiles=df_smiles)
        result.print_log("join smiles")
        return result


    def join_annotations(self):
        """Join Annotations from Compound_Id."""
        result = DataSet()
        result.data = join_annotations(self.data)
        result.print_log("join annotations")
        return result


    def poc(self, group_by=None, well_type="WellType", control_name="Control"):
        """Normalize the data set to Percent-Of-Control per group (e.g. per plate)
        based on the median of the controls.
        Parameters:
            group_by (string or None): optional column by which the calculation should be grouped,
            e.g. the column with plate name."""
        result = DataSet()
        result.data = poc(self.data, group_by=group_by)
        self.print_log("POC")
        return result


    def activity_profile(self, mad_mult=3.5, parameters=ACT_PROF_PARAMETERS, only_final=True):
        """Generates the `Act_Profile` column.
        The byte is set when the parameter's value is greater (or smaller)
        than parameter_ctrl.median() + (or -) `mad_mult`* parameter.mad()

        If a list of parameters is given, then the activity profile will be calculated for these parameters.

        If `only_final` == `True`, then only the parameters listed in `FINAL_PARAMETERS` are kept in the output_table.

        Returns a new Pandas DataFrame."""
        result = DataSet()
        result.data = activity_profile(self.data, mad_mult=mad_mult, parameters=parameters,
                                       only_final=only_final)
        result.print_log("activity profile")
        return result


    def relevant_parameters(self, ctrls_mad_rel_min=0.01,
                            ctrls_mad_rel_max=0.10, use_cpds=True, times_mad=3.5):
        result = DataSet()
        result.data = relevant_parameters(self.data, ctrls_mad_rel_min=ctrls_mad_rel_min,
                                          ctrls_mad_rel_max=ctrls_mad_rel_max,
                                          use_cpds=use_cpds, times_mad=times_mad)
        result.print_log("relevant parameters", "{:.3f}/{:.3f}/{:.2f}".format(ctrls_mad_rel_min,
                                                                              ctrls_mad_rel_max,
                                                                              times_mad))
        return result


    def correlation_filter_poc(self, cutoff=0.9, method="pearson"):
        """The correlation removes all highly correlated columns from the dataframe.
        The function was implemented according to the description of the corresponding
        KNIME component.

        Parameters:
            cutoff (float): correlation cutoff
            method (string): "pearson", "kendall", "spearman" (very slow)

        Returns a new DataFrame with only the non-correlated columns"""
        result = DataSet()
        result.data, iterations = correlation_filter_poc(self.data, cutoff=cutoff, method=method)
        result.print_log("correlation filter", "{:3d} iterations".format(iterations))
        return result


    def correlation_filter(self, cutoff=0.9, method="pearson"):
        """The correlation removes all highly correlated columns from the dataframe.
        The function was implemented according to the description of the corresponding
        KNIME component.

        Parameters:
            cutoff (float): correlation cutoff
            method (string): "pearson", "kendall", "spearman" (very slow)

        Returns a new DataFrame with only the non-correlated columns"""
        result = DataSet()
        result.data, iterations = correlation_filter(self.data, cutoff=cutoff, method=method)
        result.print_log("correlation filter", "{:3d} iterations".format(iterations))
        return result


    def add_act_profile_for_control(self, parameters=ACT_PROF_PARAMETERS):
        # Compound_Id DMSO: 245754
        control = {"Compound_Id": 245754, "Trivial_Name": "Control", "Activity": 0,
                   "Act_Profile": "".join(["1"] * len(parameters))}
        ck = control.keys()
        for k in ck:
            if k not in self.data.keys():
                control.pop(k)
        tmp = pd.DataFrame(control)
        result = DataSet()
        result.data = pd.concat(self.data, tmp)
        return result


    def update_similar_refs(self, mode="cpd", write=True):
        """Find similar compounds in references and update the export file.
        The export file of the dict object is in pkl format. In addition,
        a tsv file (or maybe JSON?) is written for use in PPilot.
        This method dpes not return anything, it just writes the result to fle."""
        rem = "" if write else "write is off"
        update_similar_refs(self.data, mode=mode, write=write)
        self.print_log("update similar", rem)


    def update_datastore(self, mode="cpd", write=True):
        """Update the DataStore with the current DataFrame."""
        update_datastore(self.data, mode=mode, write=write)


    def find_similar(self, act_profile, cutoff=0.9, max_num=5):
        """Filter the dataframe for activity profiles similar to the given one.
        `cutoff` gives the similarity threshold, default is 0.9."""
        result = DataSet()
        result.data = find_similar(self.data, act_profile=act_profile, cutoff=cutoff, max_num=max_num)
        result.print_log("find similar")
        return result


    def cpd_similarity(self, cpd1, cpd2):
        """Calculate the similarity of the activity profiles from two compounds
        (identified by `Compound_Id`). Returns value between 0 .. 1"""
        return cpd_similarity(self.data, cpd1, self.data, cpd2)


    def count_active_parameters_occurrences(self, parameters=ACT_PROF_PARAMETERS):
        """Counts the number of times each parameter has been active in the dataset."""
        return count_active_parameters_occurrences(self.data, parameters=ACT_PROF_PARAMETERS)


    @property
    def shape(self):
        return self.data.shape


    @property
    def metadata(self):
        """Returns a list of the those parameters in the DataFrame that are NOT CellProfiler measurements."""
        return metadata(self.data)


    @property
    def measurements(self):
        """Returns a list of the CellProfiler parameters that are in the DataFrame."""
        return measurements(self.data)


def load(fn, sep="\t"):
    """Read one or multiple result files and concatenate them into one dataset.
    `fn` is a single filename (string) or a list of filenames."""
    result = DataSet()
    if isinstance(fn, list):
        result.data = pd.concat((pd.read_csv(f, sep=sep) for f in fn))
    else:
        result.data = pd.read_csv(fn, sep=sep)

    drop = [d for d in DROP_GLOBAL if d in result.data.keys()]
    result.data.drop(drop, axis=1, inplace=True)
    result.print_log("load dataset")
    return result


def load_pkl(fn):
    result = DataSet()
    result.data = pd.read_pickle(fn)
    result.print_log("load pickle")
    return result


def print_log(df, component, add_info=""):
    component = component + ":"
    if len(add_info) > 0:
        add_info = "    ({})".format(add_info)
    print("* {:22s} ({:5d} | {:4d}){}".format(component, df.shape[0], df.shape[1], add_info))


def read_smiles_file(fn, props=['Compound_Id', "Smiles", "Pure_Flag"]):
    """Read in the file with the Compound_Ids and the Simles.
    Return a DataFrame for fast access."""
    result = pd.read_csv(fn, sep="\t")
    result = result[props]
    result = result.apply(pd.to_numeric, errors='ignore')
    return result


def clear_resources():
    try:
        del SMILES
        print("* deleted resource: SMILES")
    except NameError:
        pass
    try:
        del ANNOTATIONS
        print("* deleted resource: ANNOTATIONS")
    except NameError:
        pass
    try:
        del REFERENCES
        print("* deleted resource: REFERENCES")
    except NameError:
        pass
    try:
        del SIM_REFS
        print("* deleted resource: SIM_REFS")
    except NameError:
        pass
    try:
        del DATASTORE
        print("* deleted resource: DATASTORE")
    except NameError:
        pass
    try:
        del LAYOUTS
        print("* deleted resource: LAYOUTS")
    except NameError:
        pass


def load_resource(resource):
    res = resource.lower()[:3]
    glbls = globals()
    if res == "smi":
        if "SMILES" not in glbls:
            # except NameError:
            global SMILES
            print("- loading resource:                        (SMILES)")
            SMILES = read_smiles_file(resource_paths.smiles_path)
            SMILES = SMILES[resource_paths.smiles_cols]
            SMILES = SMILES.apply(pd.to_numeric, errors='ignore')
    elif res == "ann":
        if "ANNOTATIONS" not in glbls:
            global ANNOTATIONS
            print("- loading resource:                        (ANNOTATIONS)")
            ANNOTATIONS = pd.read_csv(resource_paths.annotations_path, sep="\t")
            ANNOTATIONS = ANNOTATIONS.apply(pd.to_numeric, errors='ignore')
    elif res == "ref":
        if "REFERENCES" not in glbls:
            global REFERENCES
            print("- loading resource:                        (REFERENCES)")
            REFERENCES = pd.read_csv(resource_paths.references_path, sep="\t")
    elif res == "sim":
        if "SIM_REFS" not in glbls:
            global SIM_REFS
            print("- loading resource:                        (SIM_REFS)")
            try:
                SIM_REFS = load_obj(resource_paths.sim_refs_path)
            except FileNotFoundError:
                print("  * SIM_REFS not found, creating new one.")
                SIM_REFS = {}
    elif res == "dat":
        if "DATASTORE" not in glbls:
            global DATASTORE
            print("- loading resource:                        (DATASTORE)")
            try:
                DATASTORE = pd.read_csv(resource_paths.datastore_path, sep="\t")
            except FileNotFoundError:
                print("  * DATASTORE not found, creating new one.")
                DATASTORE = pd.DataFrame()
    elif res == "lay":
        if "LAYOUTS" not in glbls:
            global LAYOUTS
            print("- loading resource:                        (LAYOUTS)")
            LAYOUTS = pd.read_csv(resource_paths.layouts_path, sep="\t")
    else:
        raise FileNotFoundError("# unknow resource: {}".format(resource))


def well_type_from_position(df):
    """Assign the WellType from the position on the plate.
    Controls are in column 11 and 12"""
    result = df.copy()
    result["WellType"] = "Compound"
    result["WellType"][(result["plateColumn"] == 11) | (result["plateColumn"] == 12)] = "Control"
    return result


def drop_cols(df, cols, inplace=False):
    """Drops the list of columns from the DataFrame.
    Listed columns that are not present in the DataFrame are simply ignored
    (no error is thrown)."""
    df_keys = df.keys()
    drop = [k for k in cols if k in df_keys]
    if inplace:
        df.drop(drop, axis=1, inplace=True)
    else:
        result = df.drop(drop, axis=1)
        return result


def well_from_position(df, well_name="Metadata_Well",
                       row_name="plateRow", col_name="plateColumn"):
    """Assign Metadata_Well from plateRow, plateColumn"""
    def _well_from_position_series(s):
        return cpt.well_from_position_single(s[0], s[1])

    result = df.copy()
    result[well_name] = result[[row_name, col_name]].apply(_well_from_position_series, axis=1)
    return result


def position_from_well(df, well_name="Metadata_Well",
                       row_name="plateRow", col_name="plateColumn"):
    """Generate plateRow and plateColumn from Metatadata_Well"""
    def _position_from_well_series(well):
        return(pd.Series(cpt.position_from_well_single(well)))

    result = df.copy()
    result[[row_name, col_name]] = result[well_name].apply(_position_from_well_series)
    return result


def join_layout_384(df, layout_fn, on="Address"):
    result = df.copy()
    result[on] = result["Metadata_Well"]
    layout = pd.read_csv(layout_fn)
    result = result.merge(layout, on=on)
    result.drop(on, axis=1, inplace=True)
    result = result.apply(pd.to_numeric, errors='ignore')
    return result


def get_cpd_from_container(df):
    result = pd.concat([df, df["Container_Id"].str.split(":", expand=True)], axis=1)
    result.rename(columns={0: "Compound_Id"}, inplace=True)
    drop_cols(result, [1, 2, 3, 4], inplace=True)
    return result


def join_layout_1536(df, plate, quadrant, on="Address_384", sep="\t", how="inner"):
    """Cell Painting is always run in 384er plates.
    COMAS standard screening plates are format 1536.
    With this function, the 1536-to-384 reformatting file
    with the smiles added by join_smiles_to_layout_1536()
    can be used directly to join the layout to the individual 384er plates."""
    load_resource("LAYOUTS")
    layout = LAYOUTS.copy()
    if not isinstance(quadrant, str):
        quadrant = str(quadrant)
    drop = ["Plate_name_384", "Plate_name_1536", "Address_1536", "Index", 1, 2]
    result = df.copy()
    layout[on] = layout["Plate_name_384"] + layout[on]
    if "Container_ID_1536" in layout.keys():
        layout.rename(columns={"Container_ID_1536": "Container_Id"}, inplace=True)
    if "Conc" in layout.keys():
        layout.rename(columns={"Conc": "Conc_uM"}, inplace=True)
    layout = get_cpd_from_container(layout)
    drop_cols(layout, drop, inplace=True)
    result[on] = plate + "." + quadrant[-1:] + result["Metadata_Well"]
    result = result.merge(layout, on=on, how=how)
    result.drop(on, axis=1, inplace=True)
    result["Container_Id"] = result["Container_Id"] + "_" + result["Metadata_Well"]
    result = result.apply(pd.to_numeric, errors='ignore')
    return result


def write_datastore():
    df = DATASTORE
    df = df.sort_values("Container_Id")
    df.to_csv(resource_paths.datastore_path, index=False, sep="\t")
    print_log(df, "write datastore")


def update_datastore(df2, on="Container_Id", mode="cpd", write=False):
    keep = ["Compound_Id", "Container_Id", "Producer", "Conc_uM", "Activity", "Toxic", "Pure_Flag",
            "Rel_Cell_Count", 'Act_Profile', "Metadata_Well", "Plate", 'Smiles']
    load_resource("DATASTORE")
    df1 = DATASTORE
    df2 = df2.copy()
    df2 = df2[keep]
    if "ref" in mode:
        df2["Is_Ref"] = True
    else:
        df2["Is_Ref"] = False
    df2 = df2[keep]
    df1 = df1.append(df2, ignore_index=True)
    rem = "" if write else "write is off"
    print_log(df2, "update datastore", rem)
    df1 = df1.drop_duplicates(subset=on, keep="last")
    if write:
        write_datastore()


def join_smiles(df, df_smiles=None):
    """Join Smiles from Compound_Id."""
    if df_smiles is None:
        load_resource("SMILES")
        df_smiles = SMILES
    result = df.merge(df_smiles, on="Compound_Id", how="inner")
    result = result.apply(pd.to_numeric, errors='ignore')
    return result


def join_annotations(df):
    """Join Annotations from Compound_Id."""
    load_resource("ANNOTATIONS")
    annotations = ANNOTATIONS
    result = df.merge(annotations, on="Compound_Id", how="left")
    result = result.replace(np.nan, "", regex=True)
    return result


def metadata(df):
    """Returns a list of the those parameters in the DataFrame that are NOT CellProfiler measurements."""
    parameters = [k for k in df.keys()
                  if not (k.startswith("Count_") or k.startswith("Mean_"))]
    return parameters


def measurements(df):
    """Returns a list of the CellProfiler parameters that are in the DataFrame."""
    parameters = [k for k in df.select_dtypes(include=[np.number]).keys()
                  if k.startswith("Count_") or k.startswith("Mean_")]
    return parameters


def numeric_parameters(df):
    result = df.copy()[measurements(df)]
    return result


def flag_toxic(df, cutoff=0.55):
    """Flag data rows of toxic compounds"""
    result = df.copy()
    median_cell_count_controls = df[df["WellType"] == "Control"]["Count_Cells"].median()
    result["Toxic"] = (result["Count_Cells"] < median_cell_count_controls * cutoff)
    result["Rel_Cell_Count"] = (100 * (result["Count_Cells"] / median_cell_count_controls)).astype(int)
    return result


def remove_toxic(df, cutoff=0.55):
    """Remove data rows of toxic compounds"""
    if "Toxic" not in df.keys():
        flagged = flag_toxic(df, cutoff=cutoff)
    else:
        flagged = df.copy()
    result = flagged[~flagged["Toxic"]]
    toxic = flagged[flagged["Toxic"]]
    return result, toxic


def remove_skipped_echo_direct_transfer(df, fn):
    """Remove wells that were reported as skipped in the Echo protocol (xml).
    This functions works with Echo direct transfer protocols.
    Function supports using wildcards in the filename, the first file will be used.
    Returns a new dataframe without the skipped wells."""
    assert fn.endswith(".xml"), "Echo file expected in XML format."
    skipped_wells = []
    try:
        echo_fn = glob.glob(fn)[0]  # use the first glob match
    except IndexError:
        raise FileNotFoundError("Echo file could not be found")
    echo_print = ET.parse(echo_fn).getroot()
    skipped = echo_print.find("skippedwells")
    for well in skipped.findall("w"):
        skipped_wells.append(cpt.format_well(well.get("dn")))
    # print("Skipped wells (will be removed):", skipped_wells)
    # remove the rows with the skipped wells
    #   i.e. keep the rows where Metadata_Well is not in the list skipped_wells
    result = df[~df["Metadata_Well"].isin(skipped_wells)]
    return result, skipped_wells


def remove_impure(df, strict=False, reset_index=True):
    """Remove entries with `Pure_Flag == "Fail"`
    If `strict == True` compound with `Pure_Flag == Warn` are also removed."""
    result = df.copy()
    outliers_list = []
    outl = result[result["Pure_Flag"] == "Fail"]
    result = result[result["Pure_Flag"] != "Fail"]
    outliers_list.append(outl)
    if strict:
        outl = result[result["Pure_Flag"] == "Warn"]
        result = result[result["Pure_Flag"] != "Warn"]
        outliers_list.append(outl)
    outliers = pd.concat(outliers_list)
    if reset_index:
        result = result.reset_index()
        outliers = outliers.reset_index()
        result.drop("index", axis=1, inplace=True)
        outliers.drop("index", axis=1, inplace=True)
    return result, outliers


def remove_outliers(df, times_dev=3.0, group_by=None, method="median", reset_index=True):
    """Returns the filtered dataframe as well as the outliers.
    method can be `median`or `mean` """
    include = [k for k in FINAL_PARAMETERS if k in df.keys()]
    input = df.copy()
    # input = numeric_parameters(df)
    if group_by is None:
        group_by = "temp_group"
        input[group_by] = "data"

    gdata_list = []
    outliers_list = []
    for group in df[group_by].unique():
        gdata = input[input[group_by] == group]
        gdata = numeric_parameters(gdata)
        if method == "median":
            mask = (gdata - gdata.median()).abs() - times_dev * gdata.mad() <= 0
        elif method == "mean":
            mask = (gdata - gdata.mean()).abs() - times_dev * gdata.std() <= 0
        else:
            raise ValueError("Unknown method {}.".format(method))
        good_data = gdata[(mask).all(axis=1)]
        outl_data = gdata[(~(mask).all(axis=1))]  # outliers
        # print(group, ": ", good_data.shape, outl_data.shape)
        gdata_list.append(good_data)
        outliers_list.append(outl_data)
    result = pd.concat(gdata_list)
    outliers = pd.concat(outliers_list)

    if group_by == "temp_group":  # remove the grouping temp col again
        result.drop(group_by, axis=1, inplace=True)
        outliers.drop(group_by, axis=1, inplace=True)
    for k in include:
        result[k] = df[k]
        outliers[k] = df[k]
    if reset_index:
        result = result.reset_index()
        outliers = outliers.reset_index()
    return result, outliers


def group_on_well(df, group_by=FINAL_PARAMETERS):
    """Group results on well level."""
    group_by = list(set(group_by).intersection(set(df.keys())))
    result = df.groupby(by=group_by).median().reset_index()
    return result


def poc(df, group_by=None):
    result = df.copy()
    if group_by is None:  # create a temp grouping column
        group_by = "temp_group"
        result[group_by] = "data"

    plates = set(result[group_by])
    for plate in plates:
        print("Normalizing {}...   ".format(plate), end="")
        controls = result[(result[group_by] == plate) & (result["WellType"] == "Control")].select_dtypes(include=[np.number])
        median = controls.median()
        for col in controls.keys():
            if col in FINAL_PARAMETERS: continue
            result[col] = 100 * result[col] / median[col]
        print("done.")

    if group_by == "temp_group":  # remove the grouping temp col again
        result.drop(group_by, axis=1, inplace=True)
    return result


def activity_profile(df, mad_mult=3.5, parameters=ACT_PROF_PARAMETERS, only_final=True):
    """Generates the `Act_Profile` column.
    The byte is set when the parameter's value is greater (or smaller)
    than parameter_ctrl.median() + (or -) `mad_mult`* parameter.mad()

    If a list of parameters is given, then the activity profile will be calculated for these parameters.

    If `only_final` == `True`, then only the parameters listed in `FINAL_PARAMETERS`
    are kept in the output_table.

    Returns a new Pandas DataFrame."""
    decimals = {"Activity": 1}
    result = df.copy()

    if parameters is None:  # choose all numeric parameters
        act_parameters = measurements(df)
    else:
        act_parameters = parameters.copy()
    assert len(act_parameters) > 0
    # sort parameters alphabetically
    act_parameters.sort()
    controls = df[act_parameters][df["WellType"] == "Control"]

    for key in act_parameters:
        median = controls[key].median()
        times_mad = mad_mult * controls[key].mad()
        lower_bound = median - times_mad
        upper_bound = median + times_mad
        result.loc[df[key].between(lower_bound, upper_bound, inclusive=True), [key]] = 1
        result.loc[df[key] < lower_bound, [key]] = 0
        result.loc[df[key] > upper_bound, [key]] = 2

    result[act_parameters] = result[act_parameters].astype(int)
    result["Activity"] = 100 * (result[act_parameters] != 1).sum(axis=1) / len(act_parameters)
    result["Act_Profile"] = result[act_parameters].astype(str).apply(lambda x: "".join(x), axis=1)

    if only_final:
        drop = []
        for k in result.keys():
            if k not in FINAL_PARAMETERS:
                drop.append(k)
        result.drop(drop, axis=1, inplace=True)
    result = result.round(decimals)
    return result


def relevant_parameters(df, ctrls_mad_rel_min=0.01,
                        ctrls_mad_rel_max=0.1, use_cpds=True, times_mad=3.5):
    """...mad_rel...: MAD relative to the median value"""
    relevant_table = FINAL_PARAMETERS.copy()
    # result = df.copy()
    controls = df[df["WellType"] == "Control"].select_dtypes(include=[pd.np.number])
    compounds = df[df["WellType"] == "Compound"].select_dtypes(include=[pd.np.number])

    ds = controls.mad() / controls.median() >= ctrls_mad_rel_min
    ctrl_set = set([p for p in ds.keys() if ds[p]])
    debug_print("ctrl_set", len(ctrl_set))

    ds = controls.mad() / controls.median() <= ctrls_mad_rel_max
    tmp_set = set([p for p in ds.keys() if ds[p]])
    debug_print("tmp_set", len(tmp_set))


    ctrl_set.intersection_update(tmp_set)
    debug_print("ctrl_set", len(ctrl_set))

    if use_cpds:  # remove also those parameters for which no cpd shows significant activity
        controls = controls[list(ctrl_set)]
        compounds = compounds[list(ctrl_set)]
        # global debug
        # debug =

        ds = compounds.max() - controls.median() - times_mad * controls.mad() > 0
        cpd_max_set = set([p for p in ds.keys() if ds[p]])
        debug_print("cpd_max_set", len(cpd_max_set))

        ds = controls.median() - compounds.min() - times_mad * controls.mad() > 0
        cpd_min_set = set([p for p in ds.keys() if ds[p]])
        debug_print("cpd_min_set", len(cpd_min_set))

        cpd_set = cpd_max_set.union(cpd_min_set)
    else:
        cpd_set = ctrl_set
    debug_print("cpd_set", len(cpd_set))

    relevant_table.extend(list(cpd_set))
    debug_print("relevant_table", len(relevant_table))

    result_keys = list(df.keys())
    keep = []
    for key in result_keys:
        if key in relevant_table:
            keep.append(key)
    result = df[keep]
    debug_print("keep", len(keep))
    return result


def correlation_filter_poc(df, cutoff=0.9, method="pearson"):
    """Reduce the parameter set to only uncorrelated parameters. From a set of correlated
    oarameters only the one with the highest Max(POC) is kept, all others are discarded."""
    assert method in ["pearson", "kendall", "spearman"], 'method has to be one of ["pearson", "kendall", "spearman"]'
    assert "WellType" in df.keys()

    # init the list of the uncorrelated parameters, incl. some string param.
    parameters_uncorr = [p for p in FINAL_PARAMETERS if p in df]

    df_copy = df.copy()
    median_controls = df_copy[df_copy["WellType"] == "Control"].median()
    df_copy = df_copy.select_dtypes(include=[np.number])

    iteration = 0
    while True:
        cm = df_copy.corr(method=method)
        correlated = cm[cm > cutoff]
        ds = correlated.count().sort_values(ascending=False)
        if ds[0] == 1: break  # no more correlations
        iteration += 1

        equal_corr = ds[ds == ds[0]]
        eq_keys = equal_corr.keys()
        # from all columns with the same number of correlated columns,
        # find the column with the highest POC range
        # and keep that preferably

        poc = (df_copy[eq_keys] / median_controls[eq_keys])
        keep_it = (poc.max() - poc.min()).sort_values(ascending=False).keys()[0]

        parameters_uncorr.append(keep_it)
        debug_print("keep_it", keep_it)
        debug_print("num_corr.", len(equal_corr))

        # find the parameters actually correlated to `keep_it`
        parameters_to_remove = list(correlated[keep_it][correlated[keep_it].notnull()].keys())
        debug_print("param_to_rem", parameters_to_remove)

        # remove the correlated parameters:
        df_copy.drop(parameters_to_remove, axis=1, inplace=True)

    parameters_uncorr.extend(df_copy.keys())
    parameters_uncorr = list(set(parameters_uncorr))
    # print("It took {} iterations to remove all correlated parameters.".format(iteration - 1))
    return df[parameters_uncorr], iteration


def correlation_filter(df, cutoff=0.9, method="pearson"):
    assert method in ["pearson", "kendall", "spearman"], 'method has to be one of ["pearson", "kendall", "spearman"]'

    df_copy = df.copy().select_dtypes(include=[np.number])

    # init the list of the uncorrelated parameters, incl. some string param.
    parameters_uncorr = [p for p in FINAL_PARAMETERS if p in df]

    iteration = 0
    while True:
        cm = df_copy.corr(method=method)
        correlated = cm[cm > cutoff]
        ds = correlated.count().sort_values(ascending=False)
        if ds[0] == 1: break  # no more correlations
        iteration += 1

        # from all columns with the same number of correlated columns,
        # find the column with the highest value range
        # and keep that preferably
        num_correlated = ds[0]  # number of correlated columns
        rnge = 0.0
        rnge_key = ""
        for i in range(len(ds)):
            if ds[i] < num_correlated: break  # only compare columns with the same highest correlation
            k = ds.keys()[i]
            debug_print("  k", k)
            r = df_copy[k].max() - df_copy[k].min()
            if r > rnge:
                rnge = r
                rnge_key = k

        keep_it = rnge_key
        parameters_uncorr.append(keep_it)
        debug_print("keep_it", keep_it)
        debug_print("num_corr.", num_correlated)

        # find the parameters actually correlated to `keep_it`
        parameters_to_remove = list(correlated[keep_it][correlated[keep_it].notnull()].keys())
        # The uncorrelated parameter `keep_it` is also in this list and has to be removed from it:
        debug_print("param_to_rem", parameters_to_remove)

        # remove the correlated parameters:
        df_copy.drop(parameters_to_remove, axis=1, inplace=True)

    parameters_uncorr.extend(df_copy.keys())
    parameters_uncorr = list(set(parameters_uncorr))
    # print("It took {} iterations to remove all correlated parameters.".format(iteration - 1))
    return df[parameters_uncorr], iteration


def find_similar(df, act_profile, cutoff=0.6, max_num=3):
    """Filter the dataframe for activity profiles similar to the given one.
    `cutoff` gives the similarity threshold, default is 0.9."""
    decimals = {"Similarity": 3}
    result = df.copy()
    result["Similarity"] = result["Act_Profile"].apply(lambda x: cpt.profile_sim(x,
                                                                                 act_profile))
    result = result[result["Similarity"] >= cutoff]
    result.drop("Act_Profile", axis=1, inplace=True)
    result = result.sort_values("Similarity", ascending=False).head(max_num)
    result = result.round(decimals)
    return result


def write_obj(obj, fn):
    """Save a generic python object through pickling."""
    with open(fn, "wb") as f:
        pickle.dump(obj, f)


def write_sim_refs():
    """Export of sim_refs as pkl and as tsv for PPilot"""
    sim_fn_pkl = resource_paths.sim_refs_path
    sim_fn_pp = op.splitext(resource_paths.sim_refs_path)[0] + ".tsv"
    sim_refs = SIM_REFS
    write_obj(sim_refs, sim_fn_pkl)  # pkl for internal use, the resource should be loaded at this point
    d = {"Container_Id": [], "Highest_Sim": []}
    for container_id in sim_refs:
        similar = sim_refs[container_id]
        if len(similar) > 0:
            highest_sim = similar["Similarity"][0]
        else:
            highest_sim = 0
        d["Container_Id"].append(container_id)
        d["Highest_Sim"].append(highest_sim)
    df = pd.DataFrame(d)
    df.to_csv(sim_fn_pp, sep="\t")  # tsv for PPilot
    print("* {:22s} ({:5d} |  --  )".format("write sim_refs", len(sim_refs)))


def load_obj(fn):
    with open(fn, "rb") as f:
        obj = pickle.load(f)
    return obj


def update_similar_refs(df, mode="cpd", write=True):
    """Find similar compounds in references and update the export file.
    The export file of the dict object is in pkl format. In addition,
    a tsv file (or maybe JSON?) is written for use in PPilot.
    `mode` can be "cpd" or "ref". if `sim_refs`is not None,
    it has to be a dict of the correct format.
    With `write=False`, the writing of the file can be deferred to the end of the processing pipeline,
    but has to be done manually, then, with `write_sim_refs()`."""

    load_resource("REFERENCES")
    load_resource("SIM_REFS")
    df_refs = REFERENCES
    sim_refs = SIM_REFS

    for _, rec in df.iterrows():
        if rec["Activity"] < ACT_CUTOFF_PERC or rec["Toxic"]:
            # no similarites for inactive or toxic compounds
            continue
        act_profile = rec["Act_Profile"]
        max_num = 5
        if "ref" in mode:
            max_num += 1
        similar = find_similar(df_refs, act_profile, cutoff=LIMIT_SIMILARITY_L / 100, max_num=max_num)
        similar = similar[["Container_Id", "Similarity"]]
        if "ref" in mode:
            similar.drop(similar.head(1).index, inplace=True)
        if similar.shape[0] == 0:
            ref_dict = {}
        else:
            ref_dict = similar.to_dict("list")
        sim_refs[rec["Container_Id"]] = ref_dict
    if write:
        # with write=False, the writing can be deferred to the end of the processing pipeline,
        # but has to be done manually, then.
        write_sim_refs()


def cpd_similarity(df1, cpd1, df2, cpd2):
    """Calculate the similarity of the activity profiles from two compounds
    (identified by `Compound_Id`). Returns value between 0 .. 1"""
    act1 = df1[df1["Compound_Id"] == cpd1]["Act_Profile"].values[0]
    act2 = df2[df2["Compound_Id"] == cpd2]["Act_Profile"].values[0]
    return round(cpt.profile_sim(act1, act2), 3)


def count_active_parameters_occurrences(df, parameters=ACT_PROF_PARAMETERS):
    """Counts the number of times each parameter has been active in the dataset."""
    ctr_int = Counter()
    ctr_str = {}
    for _, rec in df.iterrows():
        for idx, b in enumerate(rec["Act_Profile"]):
            if b != "1":
                ctr_int[idx] += 1
    for k, val in ctr_int.items():
        ctr_str[parameters[k]] = val
    return ctr_str
