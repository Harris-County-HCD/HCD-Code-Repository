
## Set variables to use thoughout the script
SOURCE_WM_ID = "ad2f33c2bcc44ccbb2c76273e75ca46d"  # Item ID for the source WebMap
TARGET_WM_ID = "ad2f33c2bcc44ccbb2c76273e75ca46d"  # Item ID for the target WebMap
source_layer_name = "Block Group Demographics (AC5 2018 - 2022)"  # Name of layer in the source WebMap
target_layer_name = "Block Group Demographics (AC5 2019 - 2023)"  # Name of layer in the target WebMap

############################################ Getting an item ID ############################################
## Item ID for a webmap can be found at the end of the URL for webmaps
## e.g. https://hccsd.maps.arcgis.com/apps/mapviewer/index.html?webmap=48457bf634d446778e95277848afba15
## The item ID for this webmap would be the numbers at the end of the URL.
## ItemID = 48457bf634d446778e95277848afba15
############################################# Map Layer Names #############################################
# Use the name of your layer in the source/target map. Do not use the name of the feature service.
# If the script doesn't work, try removing layers from group layers
###########################################################################################################

##DO NOT EDIT ANYTHING UNDER THIS POINT
###########################################################################################################
###########################################################################################################

from arcgis.gis import GIS

## access AGOL
agol = GIS("home")  # Connect to ArcGIS Online using the current user's credentials

## get the source WebMap Item
source_wm_item = agol.content.get(SOURCE_WM_ID)  # Retrieve the source WebMap item from AGOL
## get the source WebMap JSON definition
source_wm_data = source_wm_item.get_data()  # Get the JSON data for the source WebMap
## get the popupInfo definition from the source layer
popup_def = [lyr["popupInfo"] for lyr in source_wm_data["operationalLayers"] if lyr["title"] == source_layer_name][0]  # Extract the popupInfo of the specified layer in the source WebMap

## get the target WebMap Item
target_wm_item = agol.content.get(TARGET_WM_ID)  # Retrieve the target WebMap item from AGOL
## get the target WebMap JSON definition
target_wm_data = target_wm_item.get_data()  # Get the JSON data for the target WebMap
## get the index in the operationalLayers that the target layer sits
target_lyr_index = [index for index, lyr in enumerate(target_wm_data["operationalLayers"]) if lyr["title"] == target_layer_name][0]  # Find the index of the specified layer in the target WebMap's operational layers

## update the target layer popupInfo definition
target_wm_data["operationalLayers"][target_lyr_index]["popupInfo"] = popup_def  # Assign the source layer's popupInfo to the target layer

## apply the update
item_properties = {"text" : target_wm_data}  # Prepare the updated JSON definition for submission
target_wm_item.update(item_properties=item_properties)  # Update the target WebMap with the modified data
