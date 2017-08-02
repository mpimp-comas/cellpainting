#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
######
Config
######

*Created on Mon Jun 12 14:10 2017 by A. Pahl*

Configuration variables, e.g. the list of parameters from which to generate the Activity Profile.."""

ACT_PROF_PARAMETERS = [
    "Mean_Cells_AreaShape_Compactness",
    "Mean_Cells_AreaShape_FormFactor",
    "Mean_Cells_AreaShape_MajorAxisLength",
    "Mean_Cells_AreaShape_MeanRadius",
    "Mean_Cells_Correlation_Correlation_ER_Syto",
    "Mean_Cells_Correlation_Correlation_Hoechst_ER",
    "Mean_Cells_Correlation_Correlation_Hoechst_Ph_golgi",
    "Mean_Cells_Correlation_Correlation_Mito_ER",
    "Mean_Cells_Correlation_Correlation_Syto_Ph_golgi",
    "Mean_Cells_Correlation_K_Hoechst_Mito",
    "Mean_Cells_Correlation_K_Hoechst_Ph_golgi",
    "Mean_Cells_Correlation_K_Hoechst_Syto",
    "Mean_Cells_Correlation_K_Mito_Hoechst",
    "Mean_Cells_Correlation_K_Ph_golgi_Hoechst",
    "Mean_Cells_Correlation_K_Ph_golgi_Mito",
    "Mean_Cells_Correlation_K_Ph_golgi_Syto",
    "Mean_Cells_Correlation_K_Syto_Hoechst",
    "Mean_Cells_Correlation_Manders_ER_Hoechst",
    "Mean_Cells_Correlation_Manders_Mito_Hoechst",
    "Mean_Cells_Correlation_Manders_Ph_golgi_Hoechst",
    "Mean_Cells_Correlation_Overlap_Hoechst_ER",
    "Mean_Cells_Correlation_Overlap_Hoechst_Mito",
    "Mean_Cells_Correlation_RWC_ER_Hoechst",
    "Mean_Cells_Correlation_RWC_ER_Ph_golgi",
    "Mean_Cells_Correlation_RWC_ER_Syto",
    "Mean_Cells_Correlation_RWC_Hoechst_Ph_golgi",
    "Mean_Cells_Correlation_RWC_Mito_Ph_golgi",
    "Mean_Cells_Correlation_RWC_Ph_golgi_Hoechst",
    "Mean_Cells_Correlation_RWC_Ph_golgi_Syto",
    "Mean_Cells_Correlation_RWC_Syto_ER",
    "Mean_Cells_Granularity_1_Mito",
    "Mean_Cells_Granularity_1_Ph_golgi",
    "Mean_Cells_Granularity_1_Syto",
    "Mean_Cells_Granularity_2_Mito",
    "Mean_Cells_Granularity_3_ER",
    "Mean_Cells_Granularity_3_Ph_golgi",
    "Mean_Cells_Granularity_3_Syto",
    "Mean_Cells_Granularity_4_ER",
    "Mean_Cells_Granularity_4_Syto",
    "Mean_Cells_Granularity_6_ER",
    "Mean_Cells_Granularity_6_Ph_golgi",
    "Mean_Cells_Granularity_7_ER",
    "Mean_Cells_Neighbors_AngleBetweenNeighbors_Adjacent",
    "Mean_Cells_Neighbors_NumberOfNeighbors_5",
    "Mean_Cells_RadialDistribution_FracAtD_ER_1of4",
    "Mean_Cells_RadialDistribution_FracAtD_ER_3of4",
    "Mean_Cells_RadialDistribution_FracAtD_ER_4of4",
    "Mean_Cells_RadialDistribution_FracAtD_Mito_1of4",
    "Mean_Cells_RadialDistribution_FracAtD_Mito_4of4",
    "Mean_Cells_RadialDistribution_FracAtD_Ph_golgi_1of4",
    "Mean_Cells_RadialDistribution_FracAtD_Ph_golgi_4of4",
    "Mean_Cells_RadialDistribution_FracAtD_Syto_2of4",
    "Mean_Cells_RadialDistribution_FracAtD_Syto_4of4",
    "Mean_Cells_RadialDistribution_MeanFrac_ER_1of4",
    "Mean_Cells_RadialDistribution_MeanFrac_ER_3of4",
    "Mean_Cells_RadialDistribution_MeanFrac_Mito_2of4",
    "Mean_Cells_RadialDistribution_MeanFrac_Mito_4of4",
    "Mean_Cells_RadialDistribution_MeanFrac_Ph_golgi_1of4",
    "Mean_Cells_RadialDistribution_MeanFrac_Syto_1of4",
    "Mean_Cells_RadialDistribution_MeanFrac_Syto_4of4",
    "Mean_Cells_RadialDistribution_RadialCV_ER_4of4",
    "Mean_Cells_RadialDistribution_RadialCV_Mito_1of4",
    "Mean_Cells_RadialDistribution_RadialCV_Mito_2of4",
    "Mean_Cells_RadialDistribution_RadialCV_Ph_golgi_1of4",
    "Mean_Cells_RadialDistribution_RadialCV_Ph_golgi_2of4",
    "Mean_Cells_RadialDistribution_RadialCV_Ph_golgi_3of4",
    "Mean_Cells_RadialDistribution_RadialCV_Ph_golgi_4of4",
    "Mean_Cells_RadialDistribution_RadialCV_Syto_2of4",
    "Mean_Cells_RadialDistribution_RadialCV_Syto_3of4",
    "Mean_Cells_Texture_AngularSecondMoment_Hoechst_10_90",
    "Mean_Cells_Texture_AngularSecondMoment_Mito_10_90",
    "Mean_Cells_Texture_AngularSecondMoment_Ph_golgi_10_0",
    "Mean_Cells_Texture_AngularSecondMoment_Syto_10_90",
    "Mean_Cells_Texture_Contrast_ER_3_0",
    "Mean_Cells_Texture_Contrast_Hoechst_5_90",
    "Mean_Cells_Texture_Contrast_Mito_10_0",
    "Mean_Cells_Texture_Contrast_Mito_3_90",
    "Mean_Cells_Texture_Contrast_Ph_golgi_3_0",
    "Mean_Cells_Texture_Contrast_Syto_10_90",
    "Mean_Cells_Texture_Correlation_ER_10_90",
    "Mean_Cells_Texture_Correlation_Hoechst_10_0",
    "Mean_Cells_Texture_Correlation_Hoechst_10_90",
    "Mean_Cells_Texture_Correlation_Ph_golgi_3_90",
    "Mean_Cells_Texture_Correlation_Syto_10_90",
    "Mean_Cells_Texture_DifferenceEntropy_Mito_10_0",
    "Mean_Cells_Texture_DifferenceEntropy_Syto_5_0",
    "Mean_Cells_Texture_DifferenceVariance_Hoechst_10_90",
    "Mean_Cells_Texture_Entropy_Mito_3_90",
    "Mean_Cells_Texture_Entropy_Ph_golgi_3_0",
    "Mean_Cells_Texture_Gabor_ER_10",
    "Mean_Cells_Texture_Gabor_ER_5",
    "Mean_Cells_Texture_Gabor_Hoechst_10",
    "Mean_Cells_Texture_Gabor_Hoechst_3",
    "Mean_Cells_Texture_Gabor_Mito_5",
    "Mean_Cells_Texture_Gabor_Ph_golgi_10",
    "Mean_Cells_Texture_Gabor_Ph_golgi_5",
    "Mean_Cells_Texture_Gabor_Syto_3",
    "Mean_Cells_Texture_Gabor_Syto_5",
    "Mean_Cells_Texture_InfoMeas2_Mito_10_0",
    "Mean_Cells_Texture_InverseDifferenceMoment_Syto_5_0",
    "Mean_Cells_Texture_SumAverage_Hoechst_5_0",
    "Mean_Cells_Texture_SumAverage_Mito_10_90",
    "Mean_Cells_Texture_SumEntropy_ER_10_90",
    "Mean_Cells_Texture_SumEntropy_Syto_3_90",
    "Mean_Cells_Texture_SumVariance_ER_3_0",
    "Mean_Cells_Texture_SumVariance_Ph_golgi_3_0",
    "Mean_Cells_Texture_SumVariance_Syto_5_0",
    "Mean_Cells_Texture_Variance_Hoechst_3_90",
    "Mean_Cytoplasm_AreaShape_Area",
    "Mean_Cytoplasm_AreaShape_Compactness",
    "Mean_Cytoplasm_AreaShape_Extent",
    "Mean_Cytoplasm_AreaShape_FormFactor",
    "Mean_Cytoplasm_Correlation_Correlation_ER_Ph_golgi",
    "Mean_Cytoplasm_Correlation_Correlation_ER_Syto",
    "Mean_Cytoplasm_Correlation_Correlation_Hoechst_ER",
    "Mean_Cytoplasm_Correlation_Correlation_Hoechst_Mito",
    "Mean_Cytoplasm_Correlation_Correlation_Mito_Ph_golgi",
    "Mean_Cytoplasm_Correlation_Costes_Hoechst_ER",
    "Mean_Cytoplasm_Correlation_K_Hoechst_Mito",
    "Mean_Cytoplasm_Correlation_K_Hoechst_Ph_golgi",
    "Mean_Cytoplasm_Correlation_K_Mito_Hoechst",
    "Mean_Cytoplasm_Correlation_K_Ph_golgi_Hoechst",
    "Mean_Cytoplasm_Correlation_K_Syto_Ph_golgi",
    "Mean_Cytoplasm_Correlation_Manders_ER_Hoechst",
    "Mean_Cytoplasm_Correlation_Manders_Hoechst_ER",
    "Mean_Cytoplasm_Correlation_Manders_Mito_Hoechst",
    "Mean_Cytoplasm_Correlation_Manders_Mito_Syto",
    "Mean_Cytoplasm_Correlation_Manders_Ph_golgi_Mito",
    "Mean_Cytoplasm_Correlation_Overlap_Hoechst_ER",
    "Mean_Cytoplasm_Correlation_Overlap_Hoechst_Syto",
    "Mean_Cytoplasm_Correlation_RWC_ER_Mito",
    "Mean_Cytoplasm_Correlation_RWC_Hoechst_ER",
    "Mean_Cytoplasm_Correlation_RWC_Hoechst_Mito",
    "Mean_Cytoplasm_Correlation_RWC_Hoechst_Syto",
    "Mean_Cytoplasm_Correlation_RWC_Mito_Syto",
    "Mean_Cytoplasm_Correlation_RWC_Ph_golgi_Mito",
    "Mean_Cytoplasm_Correlation_RWC_Syto_Mito",
    "Mean_Cytoplasm_Correlation_RWC_Syto_Ph_golgi",
    "Mean_Cytoplasm_Granularity_2_Ph_golgi",
    "Mean_Cytoplasm_Granularity_3_Mito",
    "Mean_Cytoplasm_Granularity_3_Ph_golgi",
    "Mean_Cytoplasm_Granularity_4_Syto",
    "Mean_Cytoplasm_Granularity_5_Ph_golgi",
    "Mean_Cytoplasm_Granularity_5_Syto",
    "Mean_Cytoplasm_Granularity_6_Syto",
    "Mean_Cytoplasm_RadialDistribution_FracAtD_Mito_2of4",
    "Mean_Cytoplasm_RadialDistribution_FracAtD_Syto_2of4",
    "Mean_Cytoplasm_RadialDistribution_MeanFrac_ER_1of4",
    "Mean_Cytoplasm_RadialDistribution_MeanFrac_Syto_1of4",
    "Mean_Cytoplasm_RadialDistribution_RadialCV_ER_3of4",
    "Mean_Cytoplasm_RadialDistribution_RadialCV_Mito_1of4",
    "Mean_Cytoplasm_RadialDistribution_RadialCV_Ph_golgi_2of4",
    "Mean_Cytoplasm_RadialDistribution_RadialCV_Syto_4of4",
    "Mean_Cytoplasm_Texture_AngularSecondMoment_Hoechst_10_90",
    "Mean_Cytoplasm_Texture_AngularSecondMoment_Ph_golgi_10_0",
    "Mean_Cytoplasm_Texture_AngularSecondMoment_Syto_10_90",
    "Mean_Cytoplasm_Texture_Contrast_ER_10_0",
    "Mean_Cytoplasm_Texture_Contrast_Mito_10_90",
    "Mean_Cytoplasm_Texture_Contrast_Mito_5_0",
    "Mean_Cytoplasm_Texture_Contrast_Ph_golgi_10_0",
    "Mean_Cytoplasm_Texture_Contrast_Syto_10_90",
    "Mean_Cytoplasm_Texture_Correlation_ER_10_0",
    "Mean_Cytoplasm_Texture_Correlation_Hoechst_10_0",
    "Mean_Cytoplasm_Texture_Correlation_Hoechst_10_90",
    "Mean_Cytoplasm_Texture_Correlation_Hoechst_5_0",
    "Mean_Cytoplasm_Texture_Correlation_Hoechst_5_90",
    "Mean_Cytoplasm_Texture_Correlation_Mito_10_90",
    "Mean_Cytoplasm_Texture_Correlation_Mito_5_0",
    "Mean_Cytoplasm_Texture_Correlation_Syto_10_0",
    "Mean_Cytoplasm_Texture_Correlation_Syto_10_90",
    "Mean_Cytoplasm_Texture_Correlation_Syto_5_0",
    "Mean_Cytoplasm_Texture_DifferenceEntropy_Hoechst_3_0",
    "Mean_Cytoplasm_Texture_DifferenceEntropy_Mito_5_90",
    "Mean_Cytoplasm_Texture_DifferenceEntropy_Ph_golgi_10_0",
    "Mean_Cytoplasm_Texture_DifferenceVariance_ER_10_90",
    "Mean_Cytoplasm_Texture_DifferenceVariance_ER_5_0",
    "Mean_Cytoplasm_Texture_DifferenceVariance_Hoechst_3_90",
    "Mean_Cytoplasm_Texture_DifferenceVariance_Mito_10_90",
    "Mean_Cytoplasm_Texture_DifferenceVariance_Ph_golgi_10_0",
    "Mean_Cytoplasm_Texture_Gabor_ER_10",
    "Mean_Cytoplasm_Texture_Gabor_ER_5",
    "Mean_Cytoplasm_Texture_Gabor_Hoechst_5",
    "Mean_Cytoplasm_Texture_Gabor_Mito_10",
    "Mean_Cytoplasm_Texture_Gabor_Mito_3",
    "Mean_Cytoplasm_Texture_Gabor_Ph_golgi_10",
    "Mean_Cytoplasm_Texture_Gabor_Ph_golgi_3",
    "Mean_Cytoplasm_Texture_Gabor_Syto_5",
    "Mean_Cytoplasm_Texture_InfoMeas2_ER_10_0",
    "Mean_Cytoplasm_Texture_InfoMeas2_Hoechst_10_90",
    "Mean_Cytoplasm_Texture_InfoMeas2_Hoechst_3_0",
    "Mean_Cytoplasm_Texture_InfoMeas2_Hoechst_5_90",
    "Mean_Cytoplasm_Texture_InfoMeas2_Mito_5_90",
    "Mean_Cytoplasm_Texture_InfoMeas2_Ph_golgi_5_0",
    "Mean_Cytoplasm_Texture_InfoMeas2_Syto_10_0",
    "Mean_Cytoplasm_Texture_InfoMeas2_Syto_5_90",
    "Mean_Cytoplasm_Texture_InverseDifferenceMoment_ER_10_90",
    "Mean_Cytoplasm_Texture_InverseDifferenceMoment_Mito_10_0",
    "Mean_Cytoplasm_Texture_InverseDifferenceMoment_Ph_golgi_10_90",
    "Mean_Cytoplasm_Texture_InverseDifferenceMoment_Syto_10_90",
    "Mean_Cytoplasm_Texture_SumAverage_Ph_golgi_5_0",
    "Mean_Cytoplasm_Texture_SumEntropy_Syto_3_90",
    "Mean_Cytoplasm_Texture_SumVariance_Mito_3_0",
    "Mean_Cytoplasm_Texture_SumVariance_Ph_golgi_3_90",
    "Mean_Cytoplasm_Texture_Variance_ER_10_90",
    "Mean_Cytoplasm_Texture_Variance_Syto_10_90",
    "Mean_Nuclei_AreaShape_Area",
    "Mean_Nuclei_Correlation_Correlation_ER_Ph_golgi",
    "Mean_Nuclei_Correlation_Correlation_Mito_ER",
    "Mean_Nuclei_Correlation_Correlation_Mito_Ph_golgi",
    "Mean_Nuclei_Correlation_Correlation_Syto_Ph_golgi",
    "Mean_Nuclei_Correlation_K_Hoechst_Mito",
    "Mean_Nuclei_Correlation_K_Mito_Ph_golgi",
    "Mean_Nuclei_Correlation_K_Ph_golgi_Hoechst",
    "Mean_Nuclei_Correlation_RWC_ER_Hoechst",
    "Mean_Nuclei_Correlation_RWC_ER_Syto",
    "Mean_Nuclei_Correlation_RWC_Syto_Mito",
    "Mean_Nuclei_Granularity_1_ER",
    "Mean_Nuclei_Granularity_1_Hoechst",
    "Mean_Nuclei_Granularity_1_Syto",
    "Mean_Nuclei_Granularity_2_ER",
    "Mean_Nuclei_Granularity_2_Hoechst",
    "Mean_Nuclei_Granularity_2_Mito",
    "Mean_Nuclei_Granularity_2_Ph_golgi",
    "Mean_Nuclei_Granularity_2_Syto",
    "Mean_Nuclei_Granularity_3_ER",
    "Mean_Nuclei_Granularity_3_Hoechst",
    "Mean_Nuclei_Granularity_4_Hoechst",
    "Mean_Nuclei_Granularity_5_ER",
    "Mean_Nuclei_Granularity_5_Hoechst",
    "Mean_Nuclei_Granularity_5_Syto",
    "Mean_Nuclei_Granularity_6_Hoechst",
    "Mean_Nuclei_Granularity_6_Mito",
    "Mean_Nuclei_Granularity_7_Hoechst",
    "Mean_Nuclei_Granularity_7_Mito",
    "Mean_Nuclei_Granularity_8_ER",
    "Mean_Nuclei_Granularity_8_Hoechst",
    "Mean_Nuclei_Neighbors_AngleBetweenNeighbors_2",
    "Mean_Nuclei_Neighbors_FirstClosestDistance_2",
    "Mean_Nuclei_Neighbors_SecondClosestDistance_2",
    "Mean_Nuclei_RadialDistribution_FracAtD_ER_1of4",
    "Mean_Nuclei_RadialDistribution_FracAtD_Mito_1of4",
    "Mean_Nuclei_RadialDistribution_FracAtD_Syto_1of4",
    "Mean_Nuclei_RadialDistribution_MeanFrac_Mito_1of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_ER_1of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_ER_3of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Mito_1of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Mito_2of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Mito_3of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Mito_4of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Ph_golgi_1of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Ph_golgi_2of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Ph_golgi_3of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Ph_golgi_4of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Syto_3of4",
    "Mean_Nuclei_RadialDistribution_RadialCV_Syto_4of4",
    "Mean_Nuclei_Texture_AngularSecondMoment_Hoechst_10_0",
    "Mean_Nuclei_Texture_AngularSecondMoment_Hoechst_5_90",
    "Mean_Nuclei_Texture_AngularSecondMoment_Mito_5_0",
    "Mean_Nuclei_Texture_AngularSecondMoment_Ph_golgi_5_0",
    "Mean_Nuclei_Texture_AngularSecondMoment_Syto_3_90",
    "Mean_Nuclei_Texture_Contrast_ER_5_0",
    "Mean_Nuclei_Texture_Contrast_Hoechst_3_0",
    "Mean_Nuclei_Texture_Contrast_Hoechst_3_90",
    "Mean_Nuclei_Texture_Contrast_Hoechst_5_0",
    "Mean_Nuclei_Texture_Contrast_Hoechst_5_90",
    "Mean_Nuclei_Texture_Contrast_Mito_3_0",
    "Mean_Nuclei_Texture_Contrast_Mito_5_0",
    "Mean_Nuclei_Texture_Contrast_Mito_5_90",
    "Mean_Nuclei_Texture_Contrast_Ph_golgi_3_0",
    "Mean_Nuclei_Texture_Contrast_Ph_golgi_5_0",
    "Mean_Nuclei_Texture_Contrast_Syto_10_0",
    "Mean_Nuclei_Texture_Contrast_Syto_10_90",
    "Mean_Nuclei_Texture_Correlation_ER_10_0",
    "Mean_Nuclei_Texture_Correlation_ER_10_90",
    "Mean_Nuclei_Texture_Correlation_ER_3_90",
    "Mean_Nuclei_Texture_Correlation_Hoechst_3_0",
    "Mean_Nuclei_Texture_Correlation_Hoechst_3_90",
    "Mean_Nuclei_Texture_Correlation_Hoechst_5_0",
    "Mean_Nuclei_Texture_Correlation_Hoechst_5_90",
    "Mean_Nuclei_Texture_Correlation_Mito_10_0",
    "Mean_Nuclei_Texture_Correlation_Mito_10_90",
    "Mean_Nuclei_Texture_Correlation_Mito_5_90",
    "Mean_Nuclei_Texture_Correlation_Ph_golgi_10_0",
    "Mean_Nuclei_Texture_Correlation_Ph_golgi_10_90",
    "Mean_Nuclei_Texture_DifferenceEntropy_Mito_3_90",
    "Mean_Nuclei_Texture_DifferenceEntropy_Syto_3_90",
    "Mean_Nuclei_Texture_DifferenceVariance_ER_10_90",
    "Mean_Nuclei_Texture_DifferenceVariance_ER_3_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Hoechst_10_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Hoechst_10_90",
    "Mean_Nuclei_Texture_DifferenceVariance_Mito_10_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Mito_10_90",
    "Mean_Nuclei_Texture_DifferenceVariance_Mito_3_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Ph_golgi_10_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Ph_golgi_3_0",
    "Mean_Nuclei_Texture_DifferenceVariance_Ph_golgi_5_90",
    "Mean_Nuclei_Texture_Entropy_Mito_3_90",
    "Mean_Nuclei_Texture_Entropy_Ph_golgi_10_0",
    "Mean_Nuclei_Texture_Gabor_ER_3",
    "Mean_Nuclei_Texture_Gabor_Hoechst_10",
    "Mean_Nuclei_Texture_Gabor_Hoechst_3",
    "Mean_Nuclei_Texture_Gabor_Hoechst_5",
    "Mean_Nuclei_Texture_Gabor_Mito_10",
    "Mean_Nuclei_Texture_Gabor_Mito_3",
    "Mean_Nuclei_Texture_Gabor_Mito_5",
    "Mean_Nuclei_Texture_Gabor_Ph_golgi_10",
    "Mean_Nuclei_Texture_Gabor_Ph_golgi_3",
    "Mean_Nuclei_Texture_Gabor_Ph_golgi_5",
    "Mean_Nuclei_Texture_Gabor_Syto_3",
    "Mean_Nuclei_Texture_InfoMeas2_ER_10_0",
    "Mean_Nuclei_Texture_InfoMeas2_Ph_golgi_5_90",
    "Mean_Nuclei_Texture_InfoMeas2_Syto_5_90",
    "Mean_Nuclei_Texture_InverseDifferenceMoment_ER_10_90",
    "Mean_Nuclei_Texture_InverseDifferenceMoment_Mito_10_90",
    "Mean_Nuclei_Texture_SumAverage_Ph_golgi_3_0",
    "Mean_Nuclei_Texture_SumEntropy_ER_3_0",
    "Mean_Nuclei_Texture_SumVariance_Hoechst_10_0",
    "Mean_Nuclei_Texture_SumVariance_Hoechst_5_90",
    "Mean_Nuclei_Texture_SumVariance_Mito_3_0",
    "Mean_Nuclei_Texture_SumVariance_Syto_10_0",
    "Mean_Nuclei_Texture_SumVariance_Syto_10_90",
    "Mean_Nuclei_Texture_SumVariance_Syto_5_90",
    "Mean_Nuclei_Texture_Variance_ER_10_90",
    "Mean_Nuclei_Texture_Variance_ER_3_0",
    "Mean_Nuclei_Texture_Variance_Hoechst_5_0",
    "Mean_Nuclei_Texture_Variance_Ph_golgi_3_90",
    "Mean_Nuclei_Texture_Variance_Syto_10_90",
    "Mean_Nuclei_Texture_Variance_Syto_5_0"
]

# ACT_CUTOFF = int(0.033 * len(ACT_PROF_PARAMETERS))
ACT_CUTOFF_PERC = 10.0
LIMIT_CELL_COUNT_H = 75
LIMIT_CELL_COUNT_L = 55
LIMIT_ACTIVITY_H = 50
LIMIT_ACTIVITY_L = ACT_CUTOFF_PERC
LIMIT_SIMILARITY_H = 80
LIMIT_SIMILARITY_L = 60
