# Bitaxe Home Assistant Integration

[![HACS](https://img.shields.io/badge/HACS-Custom-blue.svg)](https://hacs.xyz/)
[![Latest Release](https://img.shields.io/github/v/release/DerMiika/Bitaxe-HA-Integration)](https://github.com/DerMiika/Bitaxe-HA-Integration/releases)
[![Stars](https://img.shields.io/github/stars/DerMiika/Bitaxe-HA-Integration)](https://github.com/DerMiika/Bitaxe-HA-Integration/stargazers)


This is a custom integration for Bitaxe miners in Home Assistant.

## Features

- **Real-time Monitoring**: Keep track of power, temperature, hashrate, and other mining metrics in real-time.
- **Easy Configuration**: Configure your Bitaxe device effortlessly through Home Assistant's user interface.

## Manual Installation

1. Navigate to your Home Assistant configuration directory. This is usually the `/config` directory in your Home Assistant setup.

2. Clone the repository directly into the `custom_components` folder (create the folder if it doesn't exist):
   ```bash
   mkdir -p custom_components
   git clone https://github.com/DerMiika/Bitaxe-HA-Integration.git /config/custom_components/bitaxe
   ```

3.  Restart Home Assistant.

## HACS Installation

1. Open the HACS section in your Home Assistant.

2. Go to **Integrations** and select **Add Repository**.

3. Enter the URL for this repository: `https://github.com/DerMiika/Bitaxe-HA-Integration`.

4. Install the integration and follow the configuration steps.

## Configuration

To set up the integration, follow these steps:

1. Go to Settings > Devices & Services > Add Integration.
2. Search for "Bitaxe" and select it.
3. Enter the IP address of your Bitaxe miner.
4.  Choose a name for your Bitaxe miner (this can be any name you prefer).
5.  Complete the setup.

## Version
This is version (v1.3.0) compatible with HACS!

## Screenshots

### Setup Screen
<img src="custom_components/bitaxe/images/Setup.png" alt="Setup Screen" style="max-width: 100%; height: auto;">

### Sensor Data Screen
<img src="custom_components/bitaxe/images/Sensor.png" alt="Sensor Data Screen" style="max-width: 100%; height: auto;">

