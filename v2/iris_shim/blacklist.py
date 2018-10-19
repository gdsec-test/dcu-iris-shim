"""
In this file we should detail the various types of blacklists that we would like to enforce.
This may include reporters that we have blacklisted, subjects that we have blacklisted, or sources that we would like
to never submit Abuse API reports for.

The data structures here are flexible and could be lists, sets, dictionaries, etc.
"""

reporters = {'francis@get.club',
             'noreply@bluehost.com',
             'Moon@indyvibe.us',
             'incident-report@bitninja.io',
             'clientrelations@resellerclub.com',
             'web.newupdcom@newsletter.updated-news.com',
             'noreply@justdeals.com',
             'contact@emailworkz.com',
             'news@portalmedestetica.com.ar',
             'newsletter@advisingnewsfinance.com',
             'newsletter@bondonews.com',
             'newsletter@clubnordictoday.com',
             'newsletter@crunchbase.com',
             'newsletter@dagensmailsaa.com',
             'newsletter@deliveringnewsino.com',
             'newsletter@e.datamattic.com',
             'newsletter@ed-mime.com',
             'newsletter@eriknewsfyt.com',
             'newsletter@financenorgoo.com',
             'newsletter@firstnordicconsumer.com',
             'newsletter@globaldata.pt',
             'newsletter@goverdeals.com',
             'newsletter@guidenorddiscount.com',
             'newsletter@lifecare-news.com',
             'newsletter@munmailmorning.com',
             'Newsletter@newsletter.kopp-verlag.de',
             'newsletter@nordensgodetilbudnu.com',
             'newsletter@nordictopclub.com',
             'newsletter@paylessflights.com.au',
             'newsletter@pelicanweek.com',
             'newsletter@permabuis.com',
             'newsletter@personalinboxinfo.com',
             'newsletter@sendmarker.com',
             'newsletter@servicegroupub.com',
             'newsletter@sinun-tarjouksesi.com',
             'newsletter@sparpengeviadd.com',
             'newsletter@starconsume.com',
             'newsletter@starringconsumers.com',
             'newsletter@svandiceridag.com',
             'newsletter@svenskamailsnaa.com',
             'newsletter@tagginbox.com',
             '89@prbusinessfirm.com'
             }

# TODO determine an appropriate data structure for subjects, are these regexes, strings, etc.
subjects = []
# subjects = [re.compile('We received your feedback'), re.compile('The NIH Information Security Program has received your e-mail'), re.compile('Your phishing report was received.')]
