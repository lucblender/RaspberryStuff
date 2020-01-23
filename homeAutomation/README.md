# Home automation System with Raspberry Pi

## Description

Here is a quick description on how to install a little home automation system on a Raspberry Pi.

The different componant are: 
- Zwave.me, OpenHab, MyOpenHab
    - For devices binding and use with GoogleHome
- InfluxDb (using docker) and Grafana
    - Persistence and visualisation of data

##  Prerequisites

### Zwave.me
Documentation can be found [here](https://z-wave.me/z-way/download-z-way/).

```
wget -q -O - https://storage.z-wave.me/RaspbianInstall | sudo bash
```
Zwave.me server accessible on _http://raspberryHostname.local:8083_

### OpenHab

Documentation can be found [here](https://www.openhab.org/download/).
```
wget -qO - 'https://bintray.com/user/downloadSubjectPublicKey?username=openhab' | sudo apt-key add -
sudo apt-get install apt-transport-https
echo 'deb https://dl.bintray.com/openhab/apt-repo2 stable main' | sudo tee /etc/apt/sources.list.d/openhab2.list
sudo apt-get update && sudo apt-get install openhab2
```
Zwave.me server accessible on _http://raspberryHostname.local:8080_

### Docker and InfluxDB
Documentation for docker can be found [here](https://docs.docker.com/install/linux/docker-ce/debian/) and for the influx docker [here](https://hub.docker.com/_/influxdb).

Docker installation:
```
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common
url -fsSL https://download.docker.com/linux/raspbian/gpg | sudo apt-key add -
 
sudo add-apt-repository \
   "deb [arch=armhf] https://download.docker.com/linux/raspbian \
   $(lsb_release -cs) \
   stable"
sudo apt-get install docker-ce

```

**To note: add-apt-repository can lead to error! In that case, add the repository with the following command:**
```
echo "deb [arch=armhf] https://download.docker.com/linux/raspbian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list

 ```

Download influxdb docker:
```
sudo docker pull influxdb
```

### Grafana
Documentation can be found [here](https://grafana.com/grafana/download?platform=arm).

```
wget https://dl.grafana.com/oss/release/grafana-rpi_6.3.5_armhf.deb
sudo dpkg -i grafana-rpi_6.3.5_armhf.deb
```

## Link system together
### Use Zwave.me things in openhab
After pairing your favorite Zwave thing on Zwave.me, you would maybe like to access them in openHab. On openHab, you'll have to install the **_Zway Binding_** add on. Then you can add a new Thing called Z-Way server and enter configure it with the Zwave.me address http://raspberryHostname.local:8083. When the Z-Way Server is connected, you can add all your Z-wave thing in openhab. 

To note that the Z-way server is using polling to retreive data and the minimum time is 60. But if we want to set a data to a z-wave thing, push will be use with no time limitation.

When your Zwave.me things are added, you can link their channel to item, this step is important if you want to monitore the things channel and for example, link them with Google Home or InfluxDb.

### Use openhab thing with Google Home

To use openhab with Google Home we will pass by the openHAB cloud called my openHAB. You'll have to add the addon called **_openHAB Cloud Connector_** ([documentation](https://www.openhab.org/addons/integrations/openhabcloud/)). When the addon is installed, you can connect on https://myopenhab.org, create an account and fill two parameters :
- UUID	found in: /var/lib/openhab2/uuid
- Secret	found in: /var/lib/openhab2/openhabcloud/secret

Now you'll have to make the item you want accessible by the openhab cloud ([documentation](https://www.openhab.org/docs/ecosystem/google-assistant/)). To do so we need to modify the /etc/openhab2/items/home.items file. As example, here is my configuration:
```
Switch FoxxSwitch "Fan" <switch> { ga="Switch" }

Group g_bedroom_temperature "Bedroom Thermostat" { ga="Thermostat"}
Number Philio2Temperature4 "Bedroom Temperature" (g_bedroom_temperature) { ga="thermostatTemperatureAmbient" }
```
This configuration use two item, one who is a Zwave plug switch and the other one a Zwave temperature sensor. 
Then on the google home app, you'll need to add your myOpenhab account. When it's done, you'll see automatically the new things appearing when you setup a new device.

### Use data Persistence with influx

To add persistance of data with influx db, we need to install the following addon: _**InfluxDB (v 1.0) Persistence**_ ([documentation](https://www.openhab.org/addons/persistence/influxdb/)).
With the addon installed, you'll have to configure influx and openhab. First in finlux you will have to create a openhab database and an openhab user with your favorite sql software as shown here:
```
create database openhab
create user openhab with password 'your password'
grant all on openhab to openhab
```
Then you'll have to modify the configuration of the influxdb persistence addon located: _/etc/openhab2/services/influxdb.cfg_. We already use the default username and database name so we only need to modifiy the configuration as shown here:
```
# The database URL, e.g. http://127.0.0.1:8086 or https://127.0.0.1:8084 .
# Defaults to: http://127.0.0.1:8086
# url=http(s)://<host>:<port>

# The name of the database user, e.g. openhab.
# Defaults to: openhab
# user=<user>

# The password of the database user.
password=your password

# The name of the database, e.g. openhab.
# Defaults to: openhab
# db=<database>

```
Finally, we have to modify the _/etc/openhab2/persistence/influxdb.persist_ file to tell the addon which openhab item we want to save in influxdb and with which strategy. Here is an example:

```
Strategies {
    everyMinute : "0 * * * * ?"
    everyHour   : "0 0 * * * ?"
    everyDay    : "0 0 0 * * ?"
}

Items {
    Philio2In1SensorTemperatureAndHumidityPhilioTechnologyCorp_PhilioTechnologyCorpTemperature5, Philio2In1SensorTemperatureAndHumidityPhilioTechnologyCorp_PhilioTechnologyCorpHumidity5, Philio2In1SensorTemperatureAndHumidityPhilioTechnologyCorp_PhilioTechnologyCorpBattery5, FoxxProjectSmartSwitchGen5Aeotec_AeotecSwitch4, AeotecElectricMeter6_Energy, AeotecElectricMeter6_Current, AeotecElectricMeter6_Power, AeotecElectricMeter6_Voltage   : strategy = everyChange, everyMinute
}
```

With that, the item described in the influxdb.persist file will be saved in influx and so available in grafana.
