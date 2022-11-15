import os
import re
from datetime import date
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from threading import Timer

stoppause=float()

# Obtiene el dia actual para general el archivo de log
today = date.today()
diaforlog = today.strftime("%b-%d-%Y")

# Si no existe, crea el archivo. Si existe, entonces agrega una cabecera
# de ejecucion del script
file_object = open(diaforlog + '.txt', 'a')
file_object.write("XXXXXXXXXXXX SCRIPT STARTED XXXXXXXXXXXX\n")
file_object.close()

# Datos del cliente
email = "ana@flautramitesyasesorias.com"
password = "Octher68"

# Carga la pagina de la embajada
driver = webdriver.Chrome()
driver.get("https://ais.usvisa-info.com/en-co/niv/users/sign_in")

# Primeda pagina, introduccion de el usuario y el password.
# Marca el check box y oprime el boton de Sign In llamado commit.
elem = driver.find_element(By.ID, "user_email")
elem.send_keys(email)
elem = driver.find_element(By.ID, "user_password")
elem.send_keys(password)
elem = driver.find_element(By.CLASS_NAME, "icheckbox ")
elem.click()
elem = driver.find_element(By.NAME, "commit")
elem.click()

# Añade datos de login del usuario despues de haber ingresado
file_object = open(diaforlog + '.txt', 'a')
file_object.write("1.- Script iniciado para cliente:................ok\n")
file_object.write(email + "\n")
file_object.write(password + "\n")
file_object.write("2.- Pagina de login ejecutado:...................OK\n")
file_object.close()

# Obtiene los datos de la fecha actual de la cita consular.
# Solo la cita consular, no la ASC ni mas nada.
elem = driver.find_element(By.CLASS_NAME, "consular-appt")
target_string = elem.text

# Elimina las comas que se encuentral en el parrafo, por ejemplo:
# 22 February, 2024, 08:15 Bogota local time at Bogota
# Esas dos comas seran eliminadas.
target_string = target_string.replace(",", "")

# Crea una arreglo con la lista de palabras del parrafo.
word_list = re.split(r"\s+", target_string)
print(word_list)

# Extrae los datos importantes de ese arreglo y los coloca en sus variables.
dia = word_list[2]
mes = word_list[3]
ano = word_list[4]
hora = word_list[5]
elem = driver.find_element(By.LINK_TEXT, "Continue")
elem.click()

# LOGs: escribe la fecha de la cita actual
file_object = open(diaforlog + '.txt', 'a')
file_object.write("4.- Pagina Current Status:...........................OK\n")
file_object.write("5.- Fecha actual de la cita:...................OK\n")
file_object.write(dia + "-")
file_object.write(mes + "-")
file_object.write(ano + "-")
file_object.write(hora + "\n")
file_object.write("6.- Click Continue para take action:......OK\n")
file_object.close()

# Open the accordion
elem = driver.find_element(By.LINK_TEXT, "Reschedule Appointment")
elem.click()

# Tune this for the accordion to give time to finnishe openning and get the elements
stoppause = random.uniform(1, 2)
time.sleep(stoppause)
file_object = open(diaforlog + '.txt', 'a')
file_object.write("7.- Acordion habierto en Reeschedule Appointment........:OK\n")
file_object.close()

# Reschedule Appointment Accordion
elem = driver.find_element(By.XPATH, "/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[4]/div/div/div[2]/p[2]/a")
elem.click()

stoppause = random.uniform(1, 2)
time.sleep(stoppause)

elem = driver.find_element(By.NAME, "commit")
elem.click()

# Reschedule Appointment Button
file_object = open(diaforlog + '.txt', 'a')
file_object.write("8.- Boton de Reeschedule Appointment dentro de acordion.........OK\n")
file_object.close()

stoppause = random.uniform(1, 2)
time.sleep(stoppause)

elem = driver.find_element(By.XPATH, "//input[@id='appointments_consulate_appointment_date']")
elem.click()

stoppause = random.uniform(2, 3)
time.sleep(stoppause)





for x in range(40):
    print("Printing:", x)
    try:
        time.sleep(0.5)
        l = driver.find_elements(By.XPATH, "//div[contains(@class,'ui-datepicker-group-first')]//table//tbody//td//a")
        print("Element exist -" + l)
    except:
        ##Move to the next month. Hover and press the triangle
        nextbutton = driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-circle-triangle-e']")
        achain = ActionChains(driver)
        achain.move_to_element(nextbutton).perform()
        driver.find_element(By.XPATH, "//span[@class='ui-icon ui-icon-circle-triangle-e']").click()
        stoppause = random.uniform(1, 2)
        time.sleep(0.5)
        print("Element does not exist try next month")



"""


if driver.find_element(By.XPATH,"//div[contains(@class,'ui-datepicker-group-first')]//table//tbody//td//a"):
    print("Element exists")
    days = driver.find_element(By.XPATH,"//div[contains(@class,'ui-datepicker-group-first')]//table//tbody//td//a")
    print(days)
else:
    print("NOT EXIST")

stoppause=random.uniform(1, 2)
time.sleep(stoppause)



for day in days:
    date=day.text
    print(date)
    #if date =='25':
    #    day.click()
    #    break


if driver.find_elements_by_css_selector('#element'):
    print "Element exists"


Basically, you get the list of the elements instead of just the element and then count the results; if it's zero, then it doesn't exist. Example:
if driver.find_elements_by_css_selector('#element'):
    print "Element exists"
Notice the "s" in find_elements_by_css_selector to make sure it can be countable.
EDIT: I was checking the len( of the list, but I recently learned that an empty list is falsey, so you don't need to get the length of the list at all, leaving for even simpler code.


Solution without try&catch and without new imports:
if len(driver.find_elements_by_id('blah')) > 0: #pay attention: find_element*s*
    driver.find_element_by_id('blah').click #pay attention: find_element

This will captuire the dates available from column on the left
//div//div[contains(@class,'ui-datepicker-group-first')]//table//tbody//td//a
//div[contains(@class,'ui-datepicker-group-first')]//table//tbody//td//a

forward button
//div//[contains(@class,'ui-icon-circle-triangle-e')]
//div//a[contains(@class,'ui-datepicker-next')]

backward button
//div//[contains(@class,'ui-icon-circle-triangle-w')]
//div//a[contains(@class,'ui-datepicker-prev')]

try:
    main = WebDriverWait(driver,5).until(EC.presence_of_element_located(By.XPATH.,"main"))
    articles = main.find_elements_by_tag_name("articles")
    for article in articles:
        header = article.find_element_by_class_name("entry-title")
        print(header.text)    
or finlally:    
except:
    driver.quit()    # it will quit if it does not work

"""



