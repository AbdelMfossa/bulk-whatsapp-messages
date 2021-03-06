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
# import de OS et de SYS
import os
from sys import platform

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

    # Depending on the OS, the terminal is cleared before the code is executed
    if platform == "linux" or platform == "linux2":
        os.system("clear")
    elif platform == "win32":
        os.system("cls")

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
    print("****     USING OF WHATSAPP BULK MESSENGER - DGSN     *****")
    print("****                                                 *****")
    print("**********************************************************")
    print("**********************************************************")
    print(style.RESET)

    if total <= 1:
        print(style.RED + 'We found ' + str(total) + ' candidate' + style.RESET)
    else:
        print(style.RED + 'We found ' + str(total) + ' candidates' + style.RESET)

    delay = 30
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    print('Une fois que votre navigateur s\'ouvre, connectez-vous ?? Whatsapp Web.')
    driver.get('https://web.whatsapp.com')
    input(style.MAGENTA + "APR??S que la connexion ?? Whatsapp Web soit termin??e et que vos messages soient visibles, appuyez sur ENTR??E...." + style.RESET)

    for idx, candidat in enumerate(candidats):

        me_and_parents = [candidat.telephone, candidat.telephone_pere, candidat.telephone_mere]
        status_code = ""
        status_msg = ""
        first_go = False

        for c, number in enumerate(me_and_parents):

            message = "{}: Epreuves ??crites {} le {} d??s 6h30 ?? {}, salle {}, table {}.".format(candidat.nom, candidat.concours, candidat.date_exam, candidat.etablissement, candidat.salle, candidat.table)

            if not number:
                status_code = "| "
                status_msg = "| "
                continue

            phone = "+" + str(number)
            print(style.YELLOW + '{}/{} - {} => Envoi du message ?? {}.'.format((idx+1), total, (c+1), phone) + style.RESET)

            try:
                url = 'https://web.whatsapp.com/send?phone=' + phone + '&text=' + message
                sent = False
                for i in range(2):
                    if not sent:
                        driver.get(url)
                        try:
                            click_btn = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='_4sWnG']")))
                        except Exception as e:
                            print(style.RED + f"\n??chec d'envoi du message ?? : {phone}, r??essayer ({i+1}/2)")
                            print("Assurez-vous que votre t??l??phone et votre ordinateur sont connect??s ?? l'internet...")
                            print("S'il y a une alerte sur le navigateur, veuillez la fermer." + style.RESET)
                            status_code += "|400"
                            status_msg += "|message not sent"
                            nb_error += 1
                        else:
                            sleep(1)
                            click_btn.click()
                            sent=True
                            sleep(3)
                            print(style.GREEN + 'Message envoy?? ?? : ' + phone + style.RESET)
                            
                            status_code += "|200"
                            status_msg += "|message sent"
                            if c == 0:
                                first_go = True
                            nb_send += 1

            except Exception as e:
                print(style.RED + '??chec d\'envoi du message ?? ' + phone + str(e) + style.RESET)

        if first_go:
            candidat.go = True
            candidat.date_envoi = datetime.now().strftime('%H:%M:%S')
            candidat.status_code = status_code
            candidat.status_msg = status_msg
            candidat.save()
        else:
            candidat.status_code = status_code
            candidat.status_msg = status_msg
            candidat.save()

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
                                 f'Aucun message ?? envoyer aux EGPX.')
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
                                 f'Aucun message ?? envoyer aux EIP.')
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
                                 f'Aucun message ?? envoyer aux EOP.')
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
                                 f'Aucun message ?? envoyer aux ECP.')
    else:
        nb_total = len(candidats)
        result = send_messages(candidats)
        msg(request, "ECP", nb_total, result)
    return redirect('home')
