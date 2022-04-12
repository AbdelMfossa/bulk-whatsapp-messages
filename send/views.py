from django.core.checks import messages
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from send.models import Candidat

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
import os

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--profile-directory=Default")
options.add_argument("--user-data-dir=/var/tmp/chrome_user_data")


@login_required
def home(request):
    context = {}
    return render(request, 'send/home.html', context)


def send_messages(candidats):
    
    total = len(candidats)
    nb_send = 0
    nb_error = 0

    os.system("")
    os.environ["WDM_LOG_LEVEL"] = "0"
    class style():
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'

    print(style.BLUE)
    print("**********************************************************")
    print("**********************************************************")
    print("****                                                 *****")
    print("****  UTILISATION DE WHATSAPP BULK MESSENGER - DGSN  *****")
    print("****                                                 *****")
    print("**********************************************************")
    print("**********************************************************")
    print(style.RESET)

    if total <= 1:
        print(style.RED + 'Nous avons trouvé ' + str(total) + ' candidat' + style.RESET)
    else:
        print(style.RED + 'Nous avons trouvé ' + str(total) + ' candidats' + style.RESET)

    delay = 30
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print('Une fois que votre navigateur s\'ouvre, connectez-vous à Whatsapp Web.')
    driver.get('https://web.whatsapp.com')
    input(style.MAGENTA + "APRÈS que la connexion à Whatsapp Web soit terminée et que vos messages soient visibles, appuyez sur ENTRÉE...." + style.RESET)

    for idx, candidat in enumerate(candidats):
        me_and_parents = [candidat.telephone, candidat.telephone_pere, candidat.telephone_mere]
        for c, number in enumerate(me_and_parents):

            message = "{}: Epreuves écrites {} le {} dès 6h30 à {}, salle {}, table {}.".format(candidat.nom, candidat.concours, candidat.date_exam, candidat.etablissement, candidat.salle, candidat.table)

            if not number:
                continue

            phone = "+" + str(number)
            print(style.YELLOW + '{}/{} - {} => Envoi du message à {}.'.format((idx+1), total, (c+1), phone) + style.RESET)

            try:
                url = 'https://web.whatsapp.com/send?phone=' + phone + '&text=' + message
                sent = False
                for i in range(2):
                    if not sent:
                        driver.get(url)
                        try:
                            click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_4sWnG']")))
                        except Exception as e:
                            print(style.RED + f"\nÉchec d'envoi du message à : {phone}, réessayer ({i+1}/2)")
                            print("Assurez-vous que votre téléphone et votre ordinateur sont connectés à l'internet...")
                            print("S'il y a une alerte sur le navigateur, veuillez la fermer." + style.RESET)
                        else:
                            sleep(1)
                            click_btn.click()
                            sent=True
                            sleep(3)
                            print(style.GREEN + 'Message envoyé à : ' + phone + style.RESET)
                            
                            candidat.go = True
                            candidat.date_envoi = datetime.now().strftime('%H:%M:%S')
                            candidat.status_code = '200'
                            candidat.status_msg = "message sent"
                            candidat.save()
                            nb_send += 1

            except Exception as e:
                print(style.RED + 'Échec d\'envoi du message à ' + phone + str(e) + style.RESET)
                candidat.status_code = '400'
                candidat.status_msg = "message not sent"
                candidat.save()
                nb_error += 1

    nb = {
        'nb_send': nb_send,
        'nb_error': nb_error
    }

    return nb

def msg(request, concours, nb_total, result):
    if result.get('nb_error') == 0:
        messages.add_message(request, messages.SUCCESS,
                                    f"STATS d\'envoi aux {concours} : <br> \
                                    - Nombre Total : {nb_total}<br> \
                                    - Nombre d'envoi : {result.get('nb_send')}<br> \
                                    - Nombre d'echec : {result.get('nb_error')}" 
        )
    else:
        messages.add_message(request, messages.SUCCESS,
                                    f"STATS d\'envoi aux {concours} : <br> \
                                    - Nombre Total : {nb_total}<br> \
                                    - Nombre d'envoi : {result.get('nb_send')}<br> \
                                    <font style='color:red;'>- Nombre d'echec : {result.get('nb_error')}</font>" 
        )

@login_required
def send_egpx(request):    
    candidats = Candidat.objects.filter(concours__contains = 'EGPX', go = False)[:5000]
    if len(candidats) == 0:
        messages.add_message(request, messages.ERROR,
                                 f'Aucun message à envoyer aux EGPX.')
    else:
        nb_total = len(candidats)
        result = send_messages(candidats)
        msg(request, "EGPX", nb_total, result)
    return redirect('home')

@login_required
def send_eip(request):    
    candidats = Candidat.objects.filter(concours__contains = 'EIP', go = False)[:300]
    if len(candidats) == 0:
        messages.add_message(request, messages.ERROR,
                                 f'Aucun message à envoyer aux EIP.')
    else:
        nb_total = len(candidats)
        result = send_messages(candidats)
        msg(request, "EIP", nb_total, result)
    return redirect('home')

@login_required
def send_eop(request):    
    candidats = Candidat.objects.filter(concours__contains = 'EOP', go = False)
    if len(candidats) == 0:
        messages.add_message(request, messages.ERROR,
                                 f'Aucun message à envoyer aux EOP.')
    else:
        nb_total = len(candidats)
        result = send_messages(candidats)
        msg(request, "EOP", nb_total, result)
    return redirect('home')

@login_required
def send_ecp(request):    
    candidats = Candidat.objects.filter(concours__contains = 'ECP', go = False)
    if len(candidats) == 0:
        messages.add_message(request, messages.ERROR,
                                 f'Aucun message à envoyer aux ECP.')
    else:
        nb_total = len(candidats)
        result = send_messages(candidats)
        msg(request, "ECP", nb_total, result)
    return redirect('home')
