*Initialisation et Déploiement local de l'application Web

Utilisez la commande suivante pour installer les dépendances du projet django : 
$ pip install -r requirements.txt

Ensuite installez le module curses avec:
$ python -m install windows_curses-2.3.0-cp310-cp310-win_amd64.whl
    °Vous pouvez aussi le téléchager à l'adresse https://pypi.org/project/windows-curses/#files
    °Utilisez à présent la commande:
    $ python -m install 'chemind_acces/windows_curses-version-win_amd64.whl'

Vous pouvez maintenant déployer le serveur avec : 
$ python manage.py runserver 
    °Vous devez être à la racine du projet 
    °Cette commande vous permettra seulement d'utiliser l'application Web, pas d'interagir avec la maquette

Pour interagir avec la maquette, vous devez déployer votre serveur sur la même adresse IP que celle où les modules ESP8266 envoient et reçoivent les données. Pour ce faire, vous pouvez soit adapter l'adresse contenue dans le code arduino à celle de votre réseau, soit adapter votre adresse à celle des ESP8266 La commande finale est donc:

$ python manage.py runserver xxx.xxx.x.x:xxxx
    (avec xxx.xxx.xx.xx:xxxx l'adresse IP)
Pour modifier l'adresse dans le code Ardino, allez aux ligne 127 du fichier functions_OOOR et 119 de functions_OOOL

*Initialisation et utilisation du code Arduino 
Suivez les procédures du lien suivant: https://www.raspberryme.com/solved-correction-de-linstallation-de-la-carte-arduino-ide-esp32-et-esp8266/

    °Vous pouvez aussi adapter votre adresse IP à celle des ESP8266: https://www.trendnet.com/langfr/press/resource-library/how-to-set-static-ip-address
    °Attenttion, ceci vous rend plus vulbérable!!


*Fonctionnement du système:

Sur la plateforme Web, accédez à http/xxx.xxx.xx.xx:xxxx/safecar et connectez vous avec les identifiants:

SSID: maxime Password: maxime pour l'utilisateur DGTT 

SSID: ruben_honfovou Password: ruben_honfovou pour un propriétaire

Cette une application responsive et intuitive: Apprenez et amusez-vous :)

Lien GitHub: https://github.com/Maxpro-dk/Safecar/tree/main