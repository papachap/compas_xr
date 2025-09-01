"""
********************************************************************************
compas_xr.project
********************************************************************************

This package contains classes to manage the XR project including the model
and building plan.

.. currentmodule:: compas_xr.project

Classes
-------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ProjectManager
    ModelExtensions
    BuildingPlanExtensions

"""

from compas_xr.project.model_extensions import ModelExtensions
from compas_xr.project.buildingplan_extensions import BuildingPlanExtensions
from compas_xr.project.project_manager import ProjectManager

__all__ = ["ProjectManager", "ModelExtensions", "BuildingPlanExtensions"]
