"""
In this file we should detail the various types of blacklists that we would like to enforce.
This may include reporters that we have blacklisted, subjects that we have blacklisted, or sources that we would like
to never submit Abuse API reports for.

The data structures here are flexible and could be lists, sets, dictionaries, etc.
"""

emails = {
    'francis@get.club',
    'incident-report@bitninja.io',
    'news@portalmedestetica.com.ar',
    'newsletter@advisingnewsfinance.com',
    'newsletter@crunchbase.com',
    'newsletter@globaldata.pt',
    'newsletter@newsletter.kopp-verlag.de',
    'newsletter@nordensgodetilbudnu.com',
    'newsletter@sendmarker.com',
    'newsletter@sinun-tarjouksesi.com',
    'noreply@bluehost.com',
    'noreply@hotelexclusives.com',
    'noreply@justdeals.com'
}

domains = {
    '2yahoo.com',
    'antihotmail.com',
    'aol.com',
    'bluerazor.com',
    'comcast.net',
    'cox.net',
    'domainaftermarket.com',
    'domaincontrol.com',
    'domainsbyproxy.com',
    'domainspricedright.com',
    'ebay.com',
    'fastmoneyforyou.su',
    'g0daddy.com',
    'gadaddy.com',
    'getnow.su',
    'gmail.com',
    'godaddy.com',
    'godaddy.in',
    'godaddy.ua',
    'godaddyteam.com',
    'hostgator.com',
    'hostgator.com.br',
    'hotmail.com',
    'iana.org',
    'icann.org',
    'izoologic.com',
    'jomax.com',
    'jomax.net',
    'madmimi.com',
    'markmonitor.com',
    'riskiq.net',
    'riskiq.com',
    'securepaynet.net',
    'starfieldtech.com',
    'sucuri.net',
    'tdnam.com',
    'teamgodaddy.com',
    'wildwestdomains.com',
    'yahoo.com',
    'yahoo.com.ar',
    'yahoo.com.br',
    'ultradns.net'
    'ultradns.org',
    'ultradns.info',
    'ultradns.co.uk',
    'dnsmadeeasy.com'
}

subjects = {
    '[my blog] please moderate: hello world',
    'go daddy, llc  domain list suspended for reported abuse',
    'report of .xyz domain suspensions & unsuspensions',
    'we received your feedback',
    'wild west domains, llc  domain list suspended for reported abuse'
    'your phishing report was received'
}
