from datetime import timedelta
import aiohttp
import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN, PLATFORMS
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    ip_address = entry.data["ip_address"]
    device_id = entry.unique_id or ip_address

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"BitAxe Sensor Data ({device_id})",
        update_method=lambda: fetch_bitaxe_data(ip_address),
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_refresh()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][device_id] = {"coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async_track_time_interval(
        hass,
        _update_coordinator(coordinator),
        timedelta(seconds=30)
    )

    return True

def _update_coordinator(coordinator: DataUpdateCoordinator):
    async def refresh(now):
        await coordinator.async_request_refresh()
    return refresh

async def fetch_bitaxe_data(ip_address):
    url = f"http://{ip_address}/api/system/info"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.debug("Fetched data: %s", data)
                return data
    except Exception as e:
        _LOGGER.error("Error fetching data from BitAxe API: %s", e)
        return None