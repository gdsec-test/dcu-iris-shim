import re

blacklist = {
    'Moon@indyvibe.us': 1,
    'incident-report@bitninja.io':1,
    'clientrelations@resellerclub.com': 1,
    'web.newupdcom@newsletter.updated-news.com': 1,
    'noreply@justdeals.com': 1,
    'contact@emailworkz.com': 1,
    'news@portalmedestetica.com.ar': 1,
    'newsletter@advisingnewsfinance.com': 1,
    'newsletter@bondonews.com': 1,
    'newsletter@clubnordictoday.com': 1,
    'newsletter@crunchbase.com': 1,
    'newsletter@dagensmailsaa.com': 1,
    'newsletter@deliveringnewsino.com': 1,
    'newsletter@e.datamattic.com': 1,
    'newsletter@ed-mime.com': 1,
    'newsletter@eriknewsfyt.com': 1,
    'newsletter@financenorgoo.com': 1,
    'newsletter@firstnordicconsumer.com': 1,
    'newsletter@globaldata.pt': 1,
    'newsletter@goverdeals.com': 1,
    'newsletter@guidenorddiscount.com': 1,
    'newsletter@lifecare-news.com': 1,
    'newsletter@munmailmorning.com': 1,
    'Newsletter@newsletter.kopp-verlag.de': 1,
    'newsletter@nordensgodetilbudnu.com': 1,
    'newsletter@nordictopclub.com': 1,
    'newsletter@paylessflights.com.au': 1,
    'newsletter@pelicanweek.com': 1,
    'newsletter@permabuis.com': 1,
    'newsletter@personalinboxinfo.com': 1,
    'newsletter@sendmarker.com': 1,
    'newsletter@servicegroupub.com': 1,
    'newsletter@sinun-tarjouksesi.com': 1,
    'newsletter@sparpengeviadd.com': 1,
    'newsletter@starconsume.com': 1,
    'newsletter@starringconsumers.com': 1,
    'newsletter@svandiceridag.com': 1,
    'newsletter@svenskamailsnaa.com': 1,
    'newsletter@tagginbox.com': 1,
    '89@prbusinessfirm.com': 1
}


invalid_email_subject = [re.compile('We received your feedback'), re.compile('The NIH Information Security Program has received your e-mail'), re.compile('Your phishing report was received.')]
