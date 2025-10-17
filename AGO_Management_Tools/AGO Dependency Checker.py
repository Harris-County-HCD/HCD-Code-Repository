## To Check item dependencies from the ArcGIS Online Dependency Checker,
## please update the item_id variable to match the item you are checking.

from arcgis.gis import GIS
import json

# Connect to ArcGIS Online
gis = GIS("home")

# Item ID to track
item_id = "9c1ee40113044433b6b9f7e1b96a3ce2"
target_item = gis.content.get(item_id)

if not target_item:
    print(f"❌ Item with ID {item_id} not found.")
    exit()

print(f"\n🔍 Checking usage for: {target_item.title} ({target_item.url})\n")

# Content types to search
search_types = [
    "Web Map",
    "Dashboard",
    "Web Mapping Application",
    "StoryMap",# includes Experience Builder & Web AppBuilder
]

used_in = []

for item_type in search_types:
    print(f"\n--- Searching in {item_type}s ---")
    items = gis.content.search(f"type:{item_type}", max_items=1000)

    for app in items:
        try:
            data = app.get_data()
            data_str = json.dumps(data).lower()

            if target_item.itemid.lower() in data_str or (target_item.url and target_item.url.lower() in data_str):
                item_url = f"{gis.url}/home/item.html?id={app.id}"
                used_in.append(app)
                print(f"✔️ Used in {item_type.lower()}: {app.title} ({item_url})")

        except Exception as e:
            print(f"⚠️ Could not read {app.title}: {e}")

if not used_in:
    print("\n❌ This item is not used in any checked content.")
else:
    print(f"\n✅ This item is used in {len(used_in)} item(s).")