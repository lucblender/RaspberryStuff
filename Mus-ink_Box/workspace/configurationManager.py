import inquirer
import re
import configparser
import subprocess
import os
from colorama import Fore, Style, init

UNDERLINE = "\033[4m"

if os.getuid() != 0:
	print(f"{Fore.RED}This configuration script must be executed as root!")
	exit()
#init colorama
init()

trackingConfigPath = "/home/pi/workspace/conf"
trackingConfigFile = trackingConfigPath+"/"+"musinkConfig.conf"

config = configparser.ConfigParser()
config.read(trackingConfigFile)

configNew = configparser.ConfigParser()
configNew.read(trackingConfigFile)

f=open(trackingConfigFile, "r")
contents =f.read() 
f.close()

enable = config["vumeter"]["enable"]
turningColor = config["vumeter"]["turningColor"]
allLedSame = config["vumeter"]["allLedSame"]
doFFT = config["vumeter"]["doFFT"]
onlyRed = config["vumeter"]["onlyRed"]
ledsNumber = config["vumeter"]["ledsNumber"]
smallScreen = config["e-ink"]["smallScreen"]
host = config["mopidy"]["host"]
port = config["mopidy"]["port"]

services =[ "einkMopidyLibrespot.service","librespot.service","mopidyCustom.service","pulseAudio.service","vumeter.service"]

servicesEnable = []
servicesEnableNew = []

results = subprocess.run(['systemctl', 'list-unit-files'], stdout=subprocess.PIPE)
for result in results.stdout.splitlines():
	for service in services:
		if service in result.decode("utf-8"):
			if "enabled" in result.decode("utf-8"):
				servicesEnable.append(service)
				
	
print(f"{Fore.BLUE}Your current configuration is:\n{Style.RESET_ALL}")
print(contents)
print(f"{Fore.BLUE}Your service configuration from systemct is:\n{Style.RESET_ALL}")
for service in services:
	if service in servicesEnable:
		print(service.ljust(35)+ f"{Fore.GREEN}{Style.BRIGHT}enabled{Style.RESET_ALL}")
	else:
		print(service.ljust(35) + f"{Fore.RED}disabled{Style.RESET_ALL}")

print("\n")

questions = [inquirer.List('modify',
                  message='Do you want to modify your configuration?',
                  choices=['yes', 'no'],
                  default='no'),
]

answers = inquirer.prompt(questions)

if answers["modify"] == "yes":

	print(f"\n{Fore.CYAN}{Style.BRIGHT}{UNDERLINE}Services properties{Style.RESET_ALL}")
	questions = [
	  inquirer.Checkbox('services',
		            message="Wich service should be enabled? ",
		            choices=services,
			    default=servicesEnable
		            ),
	]
	answers = inquirer.prompt(questions)
	servicesEnableNew = answers["services"]

	print(f"\n{Fore.CYAN}{Style.BRIGHT}{UNDERLINE}Vumeter properties{Style.RESET_ALL}")
	questions = [
		inquirer.List('enable',
				message="Enable vumeter?",
				choices=["True", "False"],
				default=enable
		    	),
		inquirer.List('turningColor',
				message="Color should rotate on the vumeter ring?",
				choices=["True", "False"],
				default=turningColor
			    ),
		inquirer.List('allLedSame',
				message="All the leds are the same color?",
				choices=["True", "False"],
				default=allLedSame
			    ),
		inquirer.List('doFFT',
				message="Use FFT for vumeter? (false will use simple average)",
				choices=["True", "False"],
				default=doFFT
			    ),
		inquirer.List('onlyRed',
				message="Get vumeter with only redish colour?",
				choices=["True", "False"],
				default=onlyRed
			    ),
		inquirer.Text('ledsNumber', message="Led number",
				validate=lambda _, x: re.match('^[0-9]{1,6}$', x),
				default=ledsNumber
				)
	]
	answers = inquirer.prompt(questions)
	configNew["vumeter"]["enable"] = answers["enable"]
	configNew["vumeter"]["turningColor"] = answers["turningColor"]
	configNew["vumeter"]["allLedSame"] = answers["allLedSame"]
	configNew["vumeter"]["doFFT"] = answers["doFFT"]
	configNew["vumeter"]["onlyRed"] = answers["onlyRed"]
	configNew["vumeter"]["ledsNumber"] = answers["ledsNumber"]


	print(f"\n{Fore.CYAN}{Style.BRIGHT}{UNDERLINE}E-ink properties{Style.RESET_ALL}")
	questions = [
	  inquirer.List('smallScreen',
		        message="Do you use the small e-ink version? (2.7'' and not 5.83'')",
		        choices=["True", "False"],
			default=smallScreen
		    ),
	]
	answers = inquirer.prompt(questions)
	configNew["e-ink"]["smallScreen"] = answers["smallScreen"]

	print(f"\n{Fore.CYAN}{Style.BRIGHT}{UNDERLINE}Mopidy properties{Style.RESET_ALL}")
	questions = [
		inquirer.Text('host', message="Mopidy server hostname",
				default=host
				),
		inquirer.Text('port', message="Mopidy server port",
				validate=lambda _, x: re.match('^[0-9]{4}$', x),
				default=port
				)
	]
	answers = inquirer.prompt(questions)
	configNew["mopidy"]["host"] = answers["host"]
	configNew["mopidy"]["port"] = answers["port"]

	if servicesEnableNew != servicesEnable:
		print(f"\n{Fore.BLUE}{Style.BRIGHT}{UNDERLINE}Service configuration changed{Style.RESET_ALL}")
		for service in services:
			if service in servicesEnableNew:
				print("systemctl enable "+service)
				os.system("systemctl enable "+service)
			else:
				print("systemctl disable "+service)
				os.system("systemctl disable "+service)
	else:
		print(f"\n{Fore.BLUE}{Style.BRIGHT}{UNDERLINE}Service configuration unchanged{Style.RESET_ALL}")	

	if config!=configNew:
		with open(trackingConfigFile, 'w') as configfile:
			configNew.write(configfile)		
		print(f"\n{Fore.BLUE}{Style.BRIGHT}{UNDERLINE}Configuration changed successfully{Style.RESET_ALL}")
	else:
		print(f"\n{Fore.BLUE}{Style.BRIGHT}{UNDERLINE}Configuration unchanged{Style.RESET_ALL}")

	if servicesEnableNew != servicesEnable or config!=configNew:
		questions = [
		    inquirer.Confirm('reboot',
				  message="Some changes need reboot to take effect, do you want to reboot?")
		]

		answers = inquirer.prompt(questions)
		if answers["reboot"]:
			print("Reboot")
			os.system("reboot")
		
	
else:
	print(f"\n{Fore.RED}Configuration unchanged{Style.RESET_ALL}")

