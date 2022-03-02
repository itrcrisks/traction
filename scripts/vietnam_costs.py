# -*- coding: utf-8 -*-
"""Estimate costs and benefits, either under fixed parameters or under a sensitivity analysis,
varying the cost components.
"""
import os
import sys
import pandas as pd
import numpy as np

def damage_costs_per_area_vietnam(x, rehab_costs,length_factor,national=False):
    """Estimate the total cost and benefits for a road segment. This function is used within a
    pandas apply

    Parameters
    ----------
    x
        a row from the road segment dataframe that we are considering
    rehab_costs
        rehabilitation costs after a disaster

    Returns
    -------
    uncer_output : list
        outcomes for the initial adaptation costs of this road segment
    tot_uncer_output : list
        outcomes for the total adaptation costs of this road segment
    rel_share : list
        relative share of each factor in the initial adaptation cost of this road segment
    tot_rel_share : list
        relative share of each factor in the total adaptation cost of this road segment
    bc_ratio : list
        benefit cost ratios for this road segment

    """
    # Identify terrain type of the road
    if x.terrain.lower().strip() == 'mountain' or x.asset_type == 'Bridge':
        ter_type = 'mountain'
    elif x.terrain.lower().strip() == 'flat':
        ter_type = 'flat'

    rehab_costs['rate_m'] = length_factor*rehab_costs.basic_cost
    # Identify asset type, which is the main driver of the costs
    if (x.asset_type == 'Expressway') | ((national == True) & (x.road_class == 1)):
        rehab_cost = rehab_costs.loc[('Expressway', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('Expressway', ter_type), 'design_width']
    elif (x.asset_type == 'National roads') | ((national == True) & (x.road_class == 2)):
        rehab_cost = rehab_costs.loc[('National  2x Carriageway', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('National  2x Carriageway', ter_type), 'design_width']
    elif (x.asset_type == 'National roads') | ((national == True) & (x.road_class == 3)):
        rehab_cost = rehab_costs.loc[('National  1x Carriageway', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('National  1x Carriageway', ter_type), 'design_width']
    elif (x.asset_type == 'Provincial roads') | ((national == True) & (x.road_class == 4)):
        rehab_cost = rehab_costs.loc[('Provincial', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('Provincial', ter_type), 'design_width']
    elif ((x.asset_type == 'Urban roads/Named roads') | (x.asset_type == 'Boulevard')) | ((national == True) & (x.road_class == 5)):
        rehab_cost = rehab_costs.loc[('District', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('District', ter_type), 'design_width']
    elif (x.asset_type == 'Other roads') | ((national == True) & (x.road_class == 6)):
        rehab_cost = rehab_costs.loc[('Commune', ter_type), 'rate_m']
        rehab_corr = rehab_costs.loc[('Commune', ter_type), 'design_width']
    elif x.asset_type == 'Bridge':
        rehab_cost = rehab_costs.rate_m.max()
        rehab_corr = rehab_costs.design_width.max()
    else:
        rehab_cost = rehab_costs.rate_m.min()
        rehab_corr = rehab_costs.design_width.min()

    rehab_cost = x.width*rehab_cost/rehab_corr

    return rehab_cost
