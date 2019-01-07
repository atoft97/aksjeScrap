import bs4 as bs
import urllib.request as r

import pickle

import sys


aksjeselskap = {}

#nøkkel selskapsnavn

#parameter ein dictionery med parameter
#parameter pe, pb, osv
#parameter pe/instri pe

def hentInfoOmEin(aksjeselskap, url, navn):

	aksjeselskap[navn] = {}

	#url = "https://www.nordnet.no/mux/web/marknaden/aktiehemsidan/nyckeltal.html?identifier=1301292&marketplace=15&inhibitTrade=1"
	#url = "https://www.nordnet.no/mux/web/marknaden/aktiehemsidan/nyckeltal.html?identifier=57456&marketplace=15&inhibitTrade=1"

	page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	result = r.urlopen(page).read()
	soup = bs.BeautifulSoup(result, "lxml")

	body = soup.body

	container = body.find('div', id="container")
	

	content = container.find('div', id="content")

	module_onecol = content.find('div', class_="module onecol")

	nyckeltalBg = module_onecol.find('div', class_="nyckeltalBg")

	nyckeltalBgPadding = nyckeltalBg.find("div", class_="nyckeltalBgPadding")

	dein = nyckeltalBgPadding.find_all()
	sektor = (dein[11].text)

	aksjeselskap[navn]["Sektor"] = sektor

	#liste = ["gevinst","gevinst/industri", "pe", "pe/industri", "ps","ps/industri", "pb", "pb/industri", "avkastning", "avkastning/industri"]
	liste = ["Gevinst/Eigenkappital", "P/E",  "P/S", "P/B", "Direkteavkastning"]
	teller = 0

	for element in nyckeltalBgPadding.find_all("div", class_="nyckeltalStapelContainer"):
		verdier = (element.text.strip().split("\n"))

		#print(verdier)

		aksjeselskap[navn][liste[teller]] = float(verdier[0])

		teller += 1

		#aksjeselskap["scatec_solar"][liste[teller]] = float(verdier[4])

		#teller += 1
		
		#break

	#print(aksjeselskap)
	#print(nyckeltalBgPadding)


	#for div in body.find_all(id="container"):
	#	print(div)



#hentInfoOmEin(aksjeselskap)

def finnNokkeltall(aksjeselskap, link, navn):

	url = link

	page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	result = r.urlopen(page).read()
	soup = bs.BeautifulSoup(result, "lxml")

	body = soup.body

	container = body.find("div", id="container")
	navigation = container.find("div", class_="navigation")
	ul = navigation.find("ul")

	liListe = ul.find_all("a")

	link2 = "https://www.nordnet.no/"+liListe[4].get("href")
	print(navn)

	hentInfoOmEin(aksjeselskap, link2, navn)


def hentUrl(aksjeselskap):
	url = "https://www.nordnet.no/mux/web/marknaden/kurslista/aktier.html?marknad=Norge&lista=1_1&large=on&mid=on&small=on&sektor=0&subtyp=price&sortera=aktie&sorteringsordning=stigande"

	page = r.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	result = r.urlopen(page).read()
	soup = bs.BeautifulSoup(result, "lxml")

	body = soup.body

	container = body.find('div', id="container")
	

	content = container.find('div', id="content")

	contentPadding = content.find("div", id="contentPadding")

	tabell = contentPadding.find("table")

	#tbody = tabell.find("tbody")

	grense = 0
	
	for tbody in tabell.find_all("tbody"):

		teller = 0

		


		for tr in tbody.find_all("tr"):

			if (teller < grense):
				teller+=1
				continue

			#print(tr.id)

			nesten = tr.find("td", class_="text")
			navn = nesten.text
			link ="https://www.nordnet.no/" + nesten.find("a").get("href")
			#print(link)

			finnNokkeltall(aksjeselskap, link, navn)




			#print(tr)
			#break

		#print(tbody)

		grense = 2
		#break
	






def lagreDict(aksjeselskap): 
	hentUrl(aksjeselskap)
	pickle.dump(aksjeselskap, open("save.p", "wb"))


lagreDict(aksjeselskap) #kommenter vekk denne når du har lasta da ned ein gong

def hentDict():
	return(pickle.load(open("save.p", "rb")))



#print(hentDict())

aksjeselskap = hentDict()

class selskap():
	#liste = ["Gevinst/Eigenkappital", "P/E",  "P/S", "P/B", "Direkteavkastning"]

	def __init__(self, sektor, ge, pe,ps,pb, avkastning, navn):
		self.sektor = sektor
		self.ge = ge
		self.pe = pe
		self.ps = ps
		self.pb = pb
		self.avkastning = avkastning
		self.navn = navn

	#print metode todo

#split dictane og legg inn i eigene lister

aksjeListe = []

for nokkel, element in aksjeselskap.items():
	#print(element)
	aksje = selskap(element["Sektor"], element['Gevinst/Eigenkappital'], element["P/E"], element["P/S"], element["P/B"], element["Direkteavkastning"], nokkel)
	aksjeListe.append(aksje)


aksjeListe.sort(key=lambda x: x.pe)
#aksjeListe.sort(key=lambda x: x.sektor)



for aksje in aksjeListe:
	#print("Navn:",aksje.navn ," | ", "PE:", aksje.pe)

	sys.stdout.write("{:<6}{:<40}{:<4}{:<30}{:<4}{:<20}{:<8}{:<20}\n".format("Navn:", aksje.navn, "PE:", aksje.pe, "PB:",aksje.pb, "sektor:", aksje.sektor))

	#sys.stdout.write("{:<6}{:<40}{:<4}{:<30}{:<4}{:<20}\n".format("Navn:", aksje.navn, "PE:", aksje.pe, "PB:",aksje.pb))



