from django.shortcuts import render
import bs4
import requests

# Create your views here.
def index(request):
    return render(request, 'generic.html')

def word(request):

    word = request.GET['word']

    if word == '':
        return render(request, 'generic.html')

    # the site your are scrapping may be banning the standard header sent by python. 
    # Look into sending a header with a different user agent
    headers = {"User-Agent": "'User-agent': 'Chrome/5.0'",}

    res = requests.get('https://www.macmillandictionary.com/dictionary/british/'+word, headers=headers)
    res2 = requests.get('https://www.thesaurus.com/browse/'+word)
    res3 = requests.get('https://www.tamildict.com/english.php?action=search&word='+word)

    if res:
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        meaning = soup.find_all('span', {'class': 'DEFINITION'})

        meaning1 = ''
        meaningg = ''
            
        if meaning:
            meaning1 = meaning[0].getText
            meaningg = meaning[1].getText
        elif len(meaning) == 1:
            meaning1 = meaning[0].getText
        elif len(meaning) == 1:
            meaningg = meaning[1].getText
        else:
            word = 'Sorry, '+ word + ' Is Not Found In Our Database'
            meaning = ''
            meaning1 = ''

    if res3:
        soup = bs4.BeautifulSoup(res3.text, 'lxml')
        tam_meaning = soup.find_all('td', {'class': 'text_blue'})
        tam_meaning01 = soup.find_all('td', {'class': 'text'})

        if tam_meaning:
            meaning01 = tam_meaning[1].getText()

        else:
            meaning01 = ''
        if tam_meaning:
            meaning02 = tam_meaning01[1].getText()
        else:
            meaning02 = ''
    if tam_meaning:
        tam = meaning01 +', ' + meaning02
    else:
        tam = ''
    # else:
    #     word = 'Sorry,'+ word + 'is not found in our database'
    #     tam_meaning = ''
    #     tam_meaning01 = ''
    #     meaning01 = ''
    #     meaning02 = ''
    #     tam = ''

    if res2:
        soup3 = bs4.BeautifulSoup(res2.text, 'lxml')

        antonyms = soup3.find_all('a',{'class': 'css-15bafsg eh475bn0'}) 
        #synonyms1 = synonyms.find('ul')
        sss = []
        for b in antonyms[0:4]:
            # re = b.text.strip()
            re = b.text
            sss.append(re)
        sv = sss
    else:
        sv = ''




    if res2:
        soup2 = bs4.BeautifulSoup(res2.text, 'lxml')

        synonyms = soup2.find_all('a',{'class': 'eh475bn0'}) 
        #synonyms1 = synonyms.find('ul')
        ss = []
        for b in synonyms[0:4]:
            # re = b.text.strip()
            re = b.text
            ss.append(re)
        se = ss
    else:
        se = ''
        

        

    #     antonyms = soup2.find_all('a', {'class': 'css-lqr09m-ItemAnchor etbu2a31'})
    #     aa = []
    #     for c in antonyms[0:]:
    #         r = c.text
    #         aa.append(r)
    #     ae = aa
    # else:
    #     se = ''
    #     ae = ''


    results = {
        'word' : word,
        'meaning' : [meaning1, meaningg],
        'tam_meaning': tam,
    }

    return render(request, 'word.html', {'se': se, 'results': results, 'sv': sv})
