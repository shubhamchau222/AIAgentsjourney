import httpx
import asyncio

async def fetch_data(state):
    async with httpx.AsyncClient() as client:
        APIBASE= "https://api.weather.gov"
        extension=f"/alerts/active/area/{state}"
        response = await client.get(APIBASE+extension)
        return response.json()
    
def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

# a = asyncio.run(fetch_data("WA"))
async def get_data():
    a= await  fetch_data("WA")
    alerts = [format_alert(feature) for feature in a["features"]]
    for alert in alerts:
        print(alert)
        print("\n"*4)

#get the forcase url 
asyncio.run(get_data())

## Use always await if you want to run function inside the function
## else use asyncio.run()
