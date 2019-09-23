from pyrogram import Client,Filters, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import RPCError
import json
from pyzbar import pyzbar
import cv2
import requests
import re

"""
Creazione Client Telegram
"""
app = Client(
    "Beapple",
    bot_token="719519692:AAF7GqGHCQokgsdcXlkIKb-2_9ZJt3laa5U"
)

"""
Funzioni Json
"""
with open('registrati.json', 'r') as fp:
    registrati = json.load(fp)
def SaveJson(fileName,dictName):
    with open(fileName, 'w') as fp:
        json.dump(dictName, fp,sort_keys=True, indent=4)

iPhonesDict = dict()
collaboratori = ["Anatras02",79484862]

"""
Funzioni Python
"""
@app.on_message(Filters.command(["start","start@BeappleOfficialBot"]))
def start(_,message):
    message.reply(
        f"Ciao **{message.from_user.first_name}**, benvenuto in Beapple!",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Chi siamo?",
                                callback_data=f"ChiSiamo"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "I nostri servizi",
                                callback_data=f"servizi"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Acquista Online",
                                url="https://www.beapple.it/store/"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Contattaci",
                                url="http://m.me/beapplestore"
                            )
                        ]
                    ]
                ),
        quote = False
        )

@app.on_message(Filters.command(["start","start@BeappleOfficialBot"]) & Filters.private, group = 1)
def start(_,message):
    message.reply(
        "Puoi usare il nostro assistente virtuale Beapple a cui potrai chiedere qualsiasi domanda!\nProva ad usarlo scrivendo `Ciao!`",
        quote = False
        )

@app.on_message(Filters.command(["news","news@BeappleOfficialBot"]) & Filters.private)
def news(_,message):
    if str(message.from_user.id) in registrati:
        stato = "Attivo ✅"
    else:
        stato = "Disattivo ❌"

    message.reply(
        f"**{message.from_user.first_name}** da qui potrai scegliere se ricevere o no le news.\nAttualmente il servizio è **{stato}**",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Attiva Servizio di News",
                                callback_data=f"attiva|{message.from_user.id}" 
                               )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Disattiva Servizio di News",
                                callback_data=f"disattiva|{message.from_user.id}" 
                               )
                        ]
                    ]
                )
        )

@app.on_message(Filters.command(["invia","invia@BeappleOfficialBot"]) & Filters.user(collaboratori))
def inviaNews(_,message):
    if message.command[1:] == []:
        message.reply("Non puoi inviare un messaggio vuoto!")
        return 

    flag = False
    for utente in registrati:
        flag = True
        try:
            app.send_message(int(utente),f'Messaggio da **{message.from_user.first_name}**\n\n{message.text.markdown.replace("/invia ","")}')
        except RPCError as e:
            print(e)
            registrati.remove(utente)
            SaveJson("registrati.json",registrati)
            continue

        message.reply(f"Messaggio inviato con successo a **{len(registrati)}** persone",quote = False)
    if flag == False:
        message.reply("Non c'è nessuno che ha attivato le news :(!",quote = False)

@app.on_message(Filters.chat("beapplenews"))
def fromBeApple(_,message):
    for utente in registrati:
        try:
            message.forward(utente, as_copy = True)
        except RPCError as e:
            print(e)
            registrati.remove(utente)
            SaveJson("registrati.json",registrati)
            continue
        
@app.on_message(Filters.private & Filters.photo, group = -1)
def QRCode(_,message):
        message.download(file_name = "/root/BeappleBOT/QRCode")
        img = cv2.imread("/root/BeappleBOT/QRCode")
        stringQRCodes = "**Dentro l'immagine sono presenti questi risultati**"
        barcodes = pyzbar.decode(img)
        flag = False
        for barcode in barcodes:
            flag = True
            barcodeData = barcode.data.decode("utf-8")
            stringQRCodes += f"\n- `{barcodeData}`"

        if flag:
            message.reply(stringQRCodes,quote = False)

@app.on_message(Filters.regex("Cia|👋|Hello",re.IGNORECASE) & Filters.private)
def Ciao(_,message):
    message.reply(
        "Ciao **{}**, piacere di conoscerti 😄!\nIo sono l'assistente virtuale di **Beapple**, di cosa hai bisogno?\nPuoi domandarmi qualsiasi cosa riguardante noi e i telefoni!\nProva ad usarmi scrivendo:\n `Cos' è un telefono ricondizionato?`\n oppure\n `Lo schermo del mio telefono si è rotto, cosa posso fare?`".format(message.from_user.first_name),
        quote = False
        )

@app.on_message(Filters.regex("siete|locate|trova|posizione|trovate",re.IGNORECASE) & Filters.private)
def locazione(_,message):
    message.reply(
        "Il nostro negozio si trova in **Via Oberdan 33** a Pisa!",
        quote = False
        )
    app.send_location(
        message.chat.id,
        latitude = 43.718939,
        longitude = 10.402009
        )

@app.on_message(Filters.regex(r"contatti|contattarvi|chiamarvi|chiamata|telefonico|email|posta elettronica|posta|via|strada",re.IGNORECASE) & Filters.private)
def contatti(_,message):
    message.reply(
        "Puoi contattarci telefonando al numero 050575734 o scrivendo a info@beapple.it o direttamente venendo in negozio!\nTi aspettiamo 😃",
        quote = False
        )
    app.send_contact(
        message.chat.id,
        phone_number = "050575734",
        first_name = "Beapple",
        last_name = "Pisa"
        )

@app.on_message(Filters.regex(r"ricondizionamento|ricondizionato|ricondizionate|ricondizione|ricondizionati|rigenerato|rigenerazione|rigenerate",re.IGNORECASE))
def ricondizionamento(_,message):
    ricondizionamentoMsg = (
        "Con una efficientissima catena di valore del prodotto siamo diventati tra i **primi rivenditori** in Italia 🇮🇹 di telefoni ricondizionati.\n\n"
        "**Cosa significa Ricondizionato?**\n"  
        "Un ricondizionato è uno __smartphone usato__ e riportato allo __stato funzionale iniziale__. Inoltre su ogni acquisto è presente una **garanzia di 6 mesi**.\n\n"  
        "**Ci sono due tipi di Ricondizionati. Grado A e B.**\n" 
        "Il telefono di **Grado A** è in condizioni funzionali ed estetiche pari al nuovo.\n"  
        "Uno Smartphone di **Grado B** è in condizioni funzionali pari al nuovo, ma può presentare leggeri segni di usura.\n"
    )

    message.reply(
        ricondizionamentoMsg,
        quote = False
        )

@app.on_message(Filters.regex(r"ritirate|usato|riciclate|valutazione|valutate|usati|comprate",re.IGNORECASE))
def compraUsato(_,message):
    message.reply(
        "A **Beapple** è possibile **vendere** il tuo usato che verrà valutato in base al __modello__ e alle sue __condizioni__.\nTi aspettiamo in negozio!",
        quote = False
        )

@app.on_message(Filters.regex(r"riparate|riparazioni|ripararmi|rotto|non funzionante|ripararlo|ripararli|riparazione|riparato|funzionante",re.IGNORECASE))
def riparazioni(_,message):
    message.reply(
        "Il tuo dispositivo è danneggiato ed ha bisogno di una **riparazione**?\nTi possiamo aiutare!\n\nIntervenire su un prodotto __non significa solamente cambiare dei componenti__, significa **molto di più**. Chi interviene deve conoscere e avere esperienza specifica di ogni tipo di terminale e deve prevedere e **prevenire eventuali problemi** che si possano manifestare in futuro.\nI nostri tecnici hanno ricevuto l’**abilitazione** da parte di BEAPPLE SRL e proseguono costantemente nel **percorso di aggiornamento** fornito dall’azienda stessa.\n\nPer questo i tecnici che interverranno sul vostro dispositivo sono ritenuti **tra i migliori che esistano in Italia**\n\nPer un listino prezzi clicca [qui 👈🏻](https://www.beapple.it/prezzi/)"
        )

def disponibilità(codice, nomeTelefono):
    iPhones = requests.get(f'http://10.0.0.19:8080/beapple/telegram/prodotti.srvl?codice={codice}').json()

    prezzi = []
    for iPhone in iPhones:
        try:
            prezzi.append(iPhones[iPhone]["price"])
        except KeyError:
            continue

    if not iPhones:
        return f"Mi dispiace, {nomeTelefono} non è disponibile in negozio 😢"
    else:
        try:
            prezzoMinimo = min(prezzi)
            return f"{nomeTelefono} è disponibile in negozio a partire da {int(prezzoMinimo)}€ 😃"
        except ValueError:
            return f"{nomeTelefono} è disponibile in negozio 😃"

@app.on_message(Filters.regex(r"disponibili|disponibilità|ci sono|avviabili|presenti|presente|lo avete|l'avete|l' avete|avete|disponibile|acquistare|comprare",re.IGNORECASE))
def iphones(_,message):
    testo = message.text.lower()

    if "4" in testo and "4s" not in testo and "4 s" not in testo:
        message.reply(disponibilità("apple-iphone-4","iPhone 4"))

    elif "4s" in testo or "4 s" in testo:
        message.reply(disponibilità("apple-iphone-4s","iPhone 4S"))

    elif "5" in testo and "5s" not in testo and "5c" not in testo and "5 s" not in testo and "5 c" not in testo:
        message.reply(disponibilità("apple-iphone-5","iPhone 5")) 

    elif "5s" in testo or "5 s" in testo:
        message.reply(disponibilità("apple-iphone-5s","iPhone 5S"))

    elif "5c" in testo:
        message.reply(disponibilità("apple-iphone-5c","iPhone 5C"))

    elif "6" in testo and "6s" not in testo and "plus" not in testo and "6 s" not in testo:
        message.reply(disponibilità("apple-iphone-6","iPhone 6"))

    elif "6 plus" in testo:
        message.reply(disponibilità("apple-iphone-6plus","iPhone 6 Plus"))

    elif "6s" in testo or "6 s" in testo:
        message.reply(disponibilità("apple-iphone-6s","iPhone 6S"))

    elif "6s plus" in testo or "6 s plus" in testo or "6splus" in testo:
        message.reply(disponibilità("apple-iphone-6splus","iPhone 6S Plus"))

    elif "se" in testo:
        message.reply(disponibilità("apple-iphone-se","iPhone SE"))

    elif "7" in testo and "plus" not in testo:
        message.reply(disponibilità("apple-iphone-7","iPhone 7"))

    elif "7 plus" in testo or "7plus" in testo:
        message.reply(disponibilità("apple-iphone-7plus","iPhone 7 Plus"))

    elif "8" in testo and "plus" not in testo:
        message.reply(disponibilità("apple-iphone-8","iPhone 8"))

    elif "8 plus" in testo or "8plus" in testo:
        message.reply(disponibilità("apple-iphone-8plus","iPhone 8 Plus"))

    elif "x" in testo and "xr" not in testo and "xs" not in testo and "max" not in testo:
        message.reply(disponibilità("apple-iphone-X","iPhone X"))

    elif "xr" in testo or "x r" in testo:
        message.reply(disponibilità("apple-iphone-XR","iPhone XR"))

    elif "xs" in testo or "x s" in testo and "max" not in testo:
        message.reply(disponibilità("apple-iphone-XS","iPhone XS"))

    elif "xs max" in testo or "x s max" in testo:
        message.reply(disponibilità("apple-iphone-XSmax","iPhone XS Max"))

    elif "11" in testo and "pro" not in testo and "max" not in testo:
        message.reply(disponibilità("apple-iphone-11","iPhone 11"))

    elif ("11 pro" in testo or "11pro" in testo) and "max" not in testo:
        message.reply(disponibilità("apple-iphone-11pro","iPhone 11 Pro"))

    elif "11 pro max" in testo or "11 max" in testo or "11pro max" in testo or "11promax" in testo or "11 max pro" in testo or "11 promax" in testo:
        message.reply(disponibilità("apple-iphone-11promax","iPhone 11 Pro Max"))

    elif ("air 1" in testo or "air" in testo or "air1" in testo) and (("2" not in testo) and ("macbook" not in testo)):
        message.reply(disponibilità("apple-ipad-air","iPad Air"))

    elif "air 2" or "air2" in testo and (("1" not in testo)  and ("macbook" not in testo)):
        message.reply(disponibilità("apple-ipad-air2","iPad Air 2"))

    elif "macbook air" in testo:
        message.reply(disponibilità("apple-mackbookair","iPad Air 2"))

    else:
        message.reply("Il dispositivo da te inserito non è esistente, se pensi questo sia un errore contatta @BeappleB")


"""
Callbacks
"""
@app.on_callback_query()
def callback(_,callback_query):
    if "MenùPrincipale" in callback_query.data:
        callback_query.edit_message_text(
        f"Ciao **{callback_query.from_user.first_name}**, benvenuto in Beapple!",
        reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Chi siamo?",
                                callback_data=f"ChiSiamo" 
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "I nostri servizi",
                                callback_data=f"servizi"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Acquista Online",
                                url="https://www.beapple.it/store/"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "Contattaci",
                                url="https://www.beapple.it/mappa/"
                                )
                        ]
                    ]
                ),
            )
    
    if "ChiSiamo" in callback_query.data:
        callback_query.edit_message_text(
            "La nostra azienda ha una storia sulla carta relativamente breve e al contempo ha **esperienza decennale**.\nBeapple proviene dalla confluenza di passioni, formazione, propositi e lungimiranza di tre ragazzi che nel **2017** hanno deciso di dar vita a questo progetto.\n\nAd oggi conta più di **12 mila clienti**, ha rapporti continui con centinaia di aziende in tutta Italia e promuove l’economia locale in ogni posto dove si trova.\nQuello che vogliamo essere è un **punto di riferimento**. Come possiamo esserlo per i nostri genitori, così vogliamo esserlo per chiunque si affidi a noi.\n\nPer più informazioni riguardanti il nostro team premi [qui 👈](https://www.beapple.it/#team)",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Torna Indietro 🔙",
                                callback_data=f"MenùPrincipale" 
                               )
                        ]
                    ]
                )
            )

    if "servizi" in callback_query.data and "servizio" not in callback_query.data:
        callback_query.edit_message_text(
            "Scegli il servizio del quale vuoi avere più informazioni!",
            reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Riparazioni Espresse",
                                callback_data=f"servizio|RipEspresse"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Vendita Computer, Tablet e Cellulari",
                                callback_data=f"servizio|ricondizionamento"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Sviluppo Siti Web",
                                callback_data=f"servizio|sitiWeb"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Sistemi Software",
                                callback_data=f"servizio|sistemiSoftware"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Microsaldatura",
                                callback_data=f"servizio|microsaldatura"
                            )
                        ],
                        [
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Torna Indietro 🔙",
                                callback_data=f"MenùPrincipale" 
                               )
                        ]
                    ]
                )
            )

    if "servizio" in callback_query.data:
        servizio = {
            "RipEspresse": "Qualsiasi terminale è **riparabile**: telefoni, tablet, computer, di tutte le marche, di ogni età 😃!\n\nPer richiederci un preventivo premi [qui 👈](https://www.beapple.it/mappa/)\nPer vedere il listino prezzi premi [qui 👈](https://www.beapple.it/prezzi/)",
            "ricondizionamento": "Abbiamo disponibili **Tablet, Computer 💻 e Telefoni 📱** nuovi e ricondizionati.\nL'esperienza nel settore ci permette di avere **prezzi scontati** fissi di circa il 10% rispetto ai listini classici 😱!\nCon una efficientissima catena di valore del prodotto siamo diventati tra i **primi rivenditori in Italia 🇮🇹** di telefoni ricondizionati.\n\nPer richiederci una quotazione premi [qui 👈](https://www.beapple.it/mappa/)",
            "sitiWeb": "Abbiamo sviluppato e manteniamo **decine di siti web 🌐 in tutta italia**. Grazie ai nostri consigli e al web designing ogni giorno i nostri clienti ricevono **centinaia di migliaia di visite 📈**.",
            "sistemiSoftware": "Grazie all'esperienza di sviluppo del nostro gestionale abbiamo acquisito capacità di consulenza per **sviluppo di programmi** che facilitino la **gestione dati**.",
            "microsaldatura": "Siamo uno dei pochi centri in Italia che svolge **microsaldatura e riparazione di schede madri**.\nCon **tempistiche molto strette** abbiamo all'attivo la felicità di moltissimi clienti 👥     che credevano persi per sempre i loro dati."
        }
        callback_query.edit_message_text(
            servizio[callback_query.data.split("|")[1]],
            reply_markup=InlineKeyboardMarkup(
                    [
                        [  # First row
                            InlineKeyboardButton(  # Generates a callback query when pressed
                                "Torna Indietro 🔙",
                                callback_data=f"servizi" 
                            )
                        ]
                    ]
                )
            )

    if "attiva" in callback_query.data and "disattiva" not in callback_query.data:
        userId = callback_query.data.split("|")[1]
        if userId in registrati:
            callback_query.answer("Il servizio è già attivo, riceverai le news!")
            return

        callback_query.answer("Il servizio è stato attivato!")
        registrati.append(userId)
        SaveJson("registrati.json",registrati)

        if userId in registrati:
            stato = "Attivo ✅"
        else:
            stato = "Disattivo ❌"

        callback_query.edit_message_text(
            f"{callback_query.from_user.first_name} da qui potrai scegliere se ricevere o no le news\nAttualmente il servizio è **{stato}**",
            reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # Generates a callback query when pressed
                                    "Attiva Servizio di News",
                                    callback_data=f"attiva|{callback_query.from_user.id}" 
                                   )
                            ],
                            [
                                InlineKeyboardButton(  # Generates a callback query when pressed
                                    "Disattiva Servizio di News",
                                    callback_data=f"disattiva|{callback_query.from_user.id}" 
                                   )
                            ]
                        ]
                    )
            )

    if "disattiva" in callback_query.data:
        userId = callback_query.data.split("|")[1]
        if userId not in registrati:
            callback_query.answer("Il servizio è già disabilitato!")
            return

        callback_query.answer("Hai disattivato il servizio di news!")
        registrati.remove(userId)
        SaveJson("registrati.json",registrati)

        if userId in registrati:
            stato = "Attivo ✅"
        else:
            stato = "Disattivo ❌"

        callback_query.edit_message_text(
            f"{callback_query.from_user.first_name} da qui potrai scegliere se ricevere o no le news\nAttualmente il servizio è **{stato}**",
            reply_markup=InlineKeyboardMarkup(
                        [
                            [  # First row
                                InlineKeyboardButton(  # Generates a callback query when pressed
                                    "Attiva Servizio di News",
                                    callback_data=f"attiva|{callback_query.from_user.id}" 
                                   )
                            ],
                            [
                                InlineKeyboardButton(  # Generates a callback query when pressed
                                    "Disattiva Servizio di News",
                                    callback_data=f"disattiva|{callback_query.from_user.id}" 
                                   )
                            ]
                        ]
                    )
            )



app.run()