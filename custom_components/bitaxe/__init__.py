from datetime import timedelta
import aiohttp
import logging
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.event import async_track_time_interval

from .const import DOMAIN, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry):
    ip_address = entry.data["ip_address"]
    device_id = entry.unique_id or ip_address
    scan_interval = entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"BitAxe Sensor Data ({device_id})",
        update_method=lambda: fetch_bitaxe_data(ip_address),
        update_interval=timedelta(seconds=scan_interval),
    )

    await coordinator.async_refresh()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][device_id] = {"coordinator": coordinator}

    # Add option to edit settings after creating instance
    entry.async_on_unload(
        entry.add_update_listener(_options_update_listener)
    )

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    async_track_time_interval(
        hass,
        _update_coordinator(coordinator),
        timedelta(seconds=scan_interval)
    )

    return True

async def _options_update_listener(hass, entry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    hass.data[DOMAIN].pop(entry.unique_id, None)
    return unload_ok

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