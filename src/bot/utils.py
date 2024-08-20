from geopy.geocoders import Nominatim


async def make_context_text(obj):
    context = (f"<b>{obj.title}</b>\n\n"
               f"{obj.description}\n"
               f"{obj.address}")
    return context


async def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="my_geopy_app_v1.0")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.address
    return address
