"""
In this file we should detail the various types of blacklists that we would like to enforce.
This may include reporters that we have blacklisted, subjects that we have blacklisted, or sources that we would like
to never submit Abuse API reports for.

The data structures here are flexible and could be lists, sets, dictionaries, etc.
"""

emails = {
    'francis@get.club',
    'arjay@get.club',
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
    'noreply@justdeals.com',
    'donotreply-abuse@radix.email',
    'agent@warnerbros.copyright-notice.com',
    'info@gobi.com.sg',
    'copyright@digiturk.com.tr'
}

subjects = {
    '[my blog] please moderate: hello world',
    'go daddy, llc  domain list suspended for reported abuse',
    'report of .xyz domain suspensions & unsuspensions',
    'we received your feedback',
    'wild west domains, llc  domain list suspended for reported abuse',
    'your phishing report was received',
    'godaddy monitoring:'
}

# Employs python regex to filter out matching (sub)domains
# ^ = start of line
# (^|\.) = string is either the start of the line or prefaced with a dot
# \\S* = zero or more non-whitespace characters
subdomain_filters = {
    '^(50analytics|bounce|certs|checkspam|img|ns1|ns2|sso|supportcenter|www)\.secureserver\.net',
    '(^|\.)em\.secureserver\.net',  # example match: "em." & "*.em."
    '(gemwbe|smtp|wbeout)\\S*\.secureserver\.net',  # example match: "gemwbe." & "genwbe*."
    '\\S*imagesak\.secureserver\.net',  # example match: "*.imagesak.", "*imagesak." & "imagesak."
    '^mailstore\\S*\.secureserver\.net',  # example match: "mailstore." & "mailstore*."
    '^secureserver\.net',  # exact match on "secureserver.net"
}

# Employs python regex to filter out matching URLs
# (/|\.) = string is either prefaced by a protocol like "http://" or prefaced with a dot
url_filters = {
    '(/|\.)secureserver\.net/whois'  # example match "http://secureserver." & "*.secureserver."
}

# A comprehensive list of GoDaddy domains that may contain a valid login page (source: Phishlabs)
_godaddy_domains = {
    'df.eu',
    'heg.systems',
    'heg.com',
    'bluerazor.com',
    'domainaftermarket.com',
    'domaincontrol.com',
    'domainsbyproxy.com',
    'domainspricedright.com',
    'g0daddy.com',
    'gadaddy.com',
    'jomax.com',
    'jomax.net',
    'madmimi.com',
    'securepaynet.net',
    'sucuri.net',
    'teamgodaddy.com',
    'wildwestdomains.com',
    'godaddyteam.com',
    'aboutgodaddy.com',
    'alphagodaddy.com',
    'godaddy.ac',
    'godaddy.adult',
    'godaddy.ae',
    'godaddy.af',
    'godaddy.ag',
    'godaddy.ai',
    'godaddy.am',
    'godaddycalendar.com',
    'godaddy.app',
    'godaddy.as',
    'godaddy.asia',
    'godaddy.at',
    'godaddy.auto',
    'godaddy.az',
    'godaddy.ba',
    'godaddy.be',
    'godaddy.berlin',
    'godaddy.best',
    'godaddy.bg',
    'godaddy.bi',
    'godaddy.biz',
    'godaddy.blackfriday',
    'godaddy.blog',
    'godaddy.bo',
    'godaddy.boston',
    'godaddyauctions.com',
    'godaddy.bs',
    'godaddy.bt',
    'godaddyabuse.com',
    'godaddyaccountexecutive.com',
    'godaddy.build',
    'godaddy.buzz',
    'godaddyapparel.in',
    'godaddy.by',
    'godaddyauctions.in',
    'godaddy.bz',
    'godaddy.ca',
    'godaddybusinessregistration.com',
    'godaddybusinessregistration.in',
    'godaddy.camp',
    'godaddyapp.com',
    'godaddy.car',
    'godaddy.career',
    'godaddy.cars',
    'godaddy.cc',
    'godaddy.cd',
    'godaddy.cg',
    'godaddy.ch',
    'godaddy.church',
    'godaddy.ci',
    'godaddy.cl',
    'godaddy.click',
    'godaddy.cloud',
    'godaddy.cn',
    'godaddy.co',
    'godaddy.co.com',
    'godaddy.co.cr',
    'godaddy.co.id',
    'godaddy.co.in',
    'godaddy.co.jp',
    'godaddy.co.kr',
    'godaddy.co.lc',
    'godaddy.co.nz',
    'godaddy.co.rs',
    'godaddy.co.th',
    'godaddy.co.ua',
    'godaddy.co.uk',
    'godaddy.co.ve',
    'godaddy.co.vi',
    'godaddy.co.za',
    'godaddy.co.zw',
    'godaddy.college',
    'godaddy.com',
    'godaddy.com.ar',
    'godaddy.com.au',
    'godaddy.com.bd',
    'godaddy.com.br',
    'godaddy.com.co',
    'godaddy.com.ec',
    'godaddy.com.eg',
    'godaddy.com.fj',
    'godaddy.com.gt',
    'godaddy.com.hn',
    'godaddy.com.hr',
    'godaddy.com.jm',
    'godaddy.com.lc',
    'godaddy.com.mt',
    'godaddy.com.mv',
    'godaddy.com.mx',
    'godaddy.com.my',
    'godaddy.com.pe',
    'godaddy.com.pl',
    'godaddy.com.pr',
    'godaddy.com.py',
    'godaddy.com.ru',
    'godaddy.com.sb',
    'godaddy.com.sc',
    'godaddy.com.sg',
    'godaddy.com.sv',
    'godaddy.com.tr',
    'godaddy.com.vc',
    'godaddy.com.ve',
    'godaddycarepackage.com',
    'godaddy.com.vn',
    'godaddy.consulting',
    'godaddy.country',
    'godaddy.courses',
    'godaddy.cr',
    'godaddy.cu',
    'godaddy.cx',
    'godaddy.cz',
    'godaddy.dance',
    'godaddy.de',
    'godaddy.desi',
    'godaddy.dj',
    'godaddy.dk',
    'godaddy.dm',
    'godaddy.do',
    'godaddy.domains',
    'godaddy.download',
    'godaddy.dpml',
    'godaddyvirtualprivateservers.com',
    'godaddysucks.in',
    'godaddysupport.com',
    'godaddytechcenter.com',
    'godaddytechfest.com',
    'godaddysoftware.net',
    'godaddytransfers.in',
    'godaddysoftware.com',
    'godaddywebmail.in',
    'godaddywebmail.com',
    'godaddywebsitebuilder.com',
    'godaddy1.com',
    'godaddytransfer.com',
    'godaddysgirls.in',
    'godaddyradio.com',
    'godaddysales.in',
    'godaddyreseller.com',
    'godaddysample1.com',
    'godaddysample2.com',
    'godaddyssl.com',
    'godaddysebay.com',
    'godaddysample4.com',
    'godaddysample5.com',
    'godaddysmallbusinesscenter.com',
    'godaddysocial.com',
    'godaddysite.in',
    'godaddystore.com',
    'godaddysample3.com',
    'godaddy.earth',
    'godaddyreview.com',
    'godaddyeurope.eu',
    'godaddyringtones.in',
    'godaddydomainservices.in',
    'godaddydomain.com',
    'godaddydomains.in',
    'godaddyemail.com',
    'godaddydomainbuyservice.com',
    'godaddydreamdesignteam.com',
    'godaddydeluxeregistration.in',
    'godaddyevent.com',
    'godaddyexpressemailmarketing.com',
    'godaddyfaxthruemail.com',
    'godaddyexecutive.com',
    'godaddygirls.in',
    'godaddygeodomainmap.com',
    'godaddyemail.in',
    'godaddycommercials.in',
    'godaddyaffiliate.com',
    'godaddybowl.com',
    'godaddycash.com',
    'godaddycashparking.com',
    'godaddycertifieddomains.com',
    'godaddycommercial.com',
    'godaddychopper.in',
    'godaddygo.net',
    'godaddyconnections.com',
    'godaddyconnections.in',
    'godaddycoupon.com',
    'godaddydedicatedhostingip.com',
    'godaddydedicatedservers.com',
    'godaddydeluxeregistration.com',
    'godaddycares.com',
    'godaddyprotectedregistration.com',
    'godaddynewsroom.in',
    'godaddyonlinestorage.com',
    'godaddypremiumdns.com',
    'godaddyprivateregistration.com',
    'godaddyproductadvisor.in',
    'godaddygrid.com',
    'godaddyproducts.in',
    'godaddylogin.com',
    'godaddyquickblogcast.com',
    'godaddyquickshoppingcart.com',
    'godaddyracing.in',
    'godaddyregistryportal.com',
    'godaddyresellers.in',
    'godaddy.ec',
    'godaddyproducts.com',
    'godaddymanagedhosting.com',
    'godaddyreviews.in',
    'godaddyhosting.in',
    'godaddyhostingconnection.com',
    'godaddygo.org',
    'godaddylegal.in',
    'godaddyhostedexchangeemail.com',
    'godaddymobilestaging.com',
    'godaddylegal.com',
    'godaddymobile.com',
    'godaddymarketing.in',
    'godaddy.eg',
    'godaddymatrix.com',
    'godaddymerchants.in',
    'godaddygo.com',
    'godaddyhosting.com',
    'godaddy.es',
    'godaddy.family',
    'godaddy.farm',
    'godaddy.fashion',
    'godaddy.feedback',
    'godaddy.fi',
    'godaddy.fit',
    'godaddy.fm',
    'godaddy.fo',
    'godaddy.fr',
    'godaddy.futbol',
    'godaddy.ga',
    'godaddy.gd',
    'godaddy.gf',
    'godaddy.gg',
    'godaddy.gift',
    'godaddy.gm',
    'godaddy.gop',
    'godaddy.gp',
    'godaddy.gr',
    'godaddy.gs',
    'godaddy.gt',
    'godaddy.guide',
    'godaddy.guitars',
    'godaddy.gy',
    'godaddy.help',
    'godaddy.hk',
    'godaddy.hm',
    'godaddy.hn',
    'godaddy.host',
    'godaddy.hosting',
    'godaddy.ht',
    'godaddy.hu',
    'godaddy.id',
    'godaddy.ie',
    'godaddyauctionmobile.com',
    'godaddybackorder.com',
    'godaddy.im',
    'godaddy.in',
    'godaddy.info',
    'godaddyhr.com',
    'godaddy.ink',
    'godaddy.io',
    'godaddy.is',
    'godaddy.istanbul',
    'godaddy.it',
    'godaddygear.com',
    'godaddy.jetzt',
    'godaddyuniversity.com',
    'godaddy.jobs',
    'godaddy.jp',
    'godaddy.kg',
    'godaddy.kiwi',
    'godaddy.kn',
    'godaddysslcompare.com',
    'godaddydanicapatrick.com',
    'godaddydiscountdomainclub.com',
    'godaddyinternationalizeddomain.com',
    'godaddypremiumlisting.com',
    'godaddyscholarship.com',
    'godaddyspanish.com',
    'godaddywebsiteprotection.com',
    'godaddywhois.com',
    'godaddy.kr',
    'godaddysearchengine.com',
    'godaddy.kz',
    'godaddy.la',
    'godaddy.land',
    'godaddy.lat',
    'godaddy.lc',
    'godaddy.lgbt',
    'godaddy.li',
    'godaddy.life',
    'godaddy.lighting',
    'godaddy.link',
    'godaddy.live',
    'godaddy.lk',
    'GoDaddy.lol',
    'godaddy.london',
    'godaddy.lt',
    'godaddy.lu',
    'godaddy.luxury',
    'godaddy.lv',
    'godaddy.ly',
    'godaddy.ma',
    'godaddy.md',
    'godaddy.me',
    'godaddy.menu',
    'godaddy.mg',
    'godaddy.mn',
    'godaddy.mobi',
    'godaddy.mp',
    'godaddy.mq',
    'godaddy.ms',
    'godaddy.mt',
    'godaddy.mw',
    'godaddy.mx',
    'godaddy.my',
    'godaddy.net',
    'godaddy.net.br',
    'godaddy.net.ua',
    'godaddy.news',
    'godaddy.ng',
    'godaddy.ninja',
    'godaddy.nl',
    'godaddy.no',
    'godaddy.nom.co',
    'godaddy.nu',
    'godaddy.nz',
    'godaddy.onl',
    'godaddy.online',
    'godaddy.org',
    'godaddy.org.uk',
    'godaddy.party',
    'godaddy.pe',
    'godaddy.ph',
    'godaddy.photo',
    'godaddy.photography',
    'godaddy.pics',
    'godaddy.pink',
    'godaddy.pk',
    'godaddy.pl',
    'godaddy.pn',
    'godaddy.porn',
    'godaddy.pr',
    'godaddy.press',
    'godaddy.pro',
    'godaddy.promo',
    'godaddy.protection',
    'godaddy.pt',
    'godaddy.pw',
    'godaddy.qa',
    'godaddy.qpon',
    'godaddy.quebec',
    'godaddy.rent',
    'godaddy.review',
    'godaddy.reviews',
    'godaddy.ro',
    'godaddy.rocks',
    'godaddy.rs',
    'godaddy.rw',
    'godaddy.sb',
    'godaddy.sc',
    'godaddy.se',
    'godaddy.security',
    'godaddy.sexy',
    'godaddy.sg',
    'godaddy.sh',
    'godaddy.shop',
    'godaddy.si',
    'godaddy.site',
    'godaddymerchantaccounts.com',
    'godaddy.sk',
    'godaddy.sm',
    'godaddy.sn',
    'godaddy.so',
    'godaddy.social',
    'godaddy.solutions',
    'godaddy.soy',
    'godaddy.space',
    'godaddy.sr',
    'godaddy.st',
    'godaddy.storage',
    'godaddy.store',
    'godaddy.sucks',
    'godaddy.tattoo',
    'godaddy.tc',
    'godaddy.team',
    'godaddy.tech',
    'godaddy.tg',
    'godaddy.theatre',
    'godaddy.tj',
    'godaddy.tl',
    'godaddy.tm',
    'godaddy.tokyo',
    'godaddy.top',
    'godaddy.trading',
    'godaddy.tv',
    'godaddy.tw',
    'godaddy.ua',
    'godaddy.ug',
    'godaddy.uk',
    'godaddy.us',
    'godaddy.uz',
    'godaddy.vc',
    'godaddy.vegas',
    'godaddy.vg',
    'godaddy.video',
    'godaddy.vn',
    'godaddy.vu',
    'godaddy.website',
    'godaddy.wiki',
    'godaddy.work',
    'godaddy.ws',
    'godaddy.xn--fiqs8s',
    'godaddy.xn--q9jyb4c',
    'godaddy.xxx',
    'godaddy.xyz',
    'godaddy.yoga',
    'insidegodaddy.com',
    'godaddymarketing.com',
    'godaddyresellersite.com',
    'godaddymarketplace.com',
    'godaddyresellers.com',
    'godaddygirls.com',
    'godaddysaves.me',
    'godaddylive.com',
    'godaddyracing.com',
    'godaddysales.com',
    'godaddygirls.info',
    'godaddyreviews.net',
    'debug-godaddyregistryportal.com',
    'dev-godaddyicp.cn',
    'dev-godaddytraininghub.com',
    'dev-godaddyregistryportal.com',
    'godaddyacademy.com',
    'godaddypresents.com',
    'cjgodaddymigration.com',
    'test-godaddyregistryportal.com',
    'godaddyburninhell.com',
    'godaddyemailarchiving.com',
    'godaddycustomercouncil.org',
    'godaddycustomercouncil.net',
    'godaddycustomercouncil.info',
    'godaddycustomercouncil.com',
    'test-godaddytraininghub.com',
    'test-godaddyicp.cn',
    'stg-godaddytraininghub.com',
    'godaddyguides.com',
    'ote-godaddyicp.cn',
    'ote-godaddytraininghub.com',
    'godaddyappraisals.com',
    'test-godaddywp.com',
    'dev-godaddywp.com',
    'godaddywp.com',
    'ote-godaddyregistryportal.com',
    'godaddy-is-satans-son.us'
}

domains = {
    'virustotal.com',
    'phishtank.com',
    'arin.net',
    'netcraft.com',
    'abuse.ch',
    'xarf.org',
    'x-arf.org',
    'lexsi.com',
    'amazon.com',
    'amazon.ca',
    'outlook.com',
    'office.com',
    'skype.com',
    'office365.com',
    'microsoft.com',
    'phishlabs.com',
    'antihotmail.com',
    'aol.com',
    'comcast.net',
    'cox.net',
    'ebay.com',
    'fastmoneyforyou.su',
    'getnow.su',
    'izoologic.com',
    'gmail.com',
    'google.com',
    'youtube.com',
    '1e100.net',  # Google domain
    'facebook.com',
    'whatsapp.com',
    'twitter.com',
    'hostgator.com',
    'hostgator.com.br',
    'hotmail.com',
    'iana.org',
    'icann.org',
    'markmonitor.com',
    'riskiq.net',
    'riskiq.com',
    'starfieldtech.com',
    'tdnam.com',
    'internic.net',
    'yahoo.com',
    'yahoo.com.ar',
    'yahoo.com.br',
    'yahoo.co.jp',
    '2yahoo.com',
    'malwarebytes.com',
    'hosts-files.net',
    'abuseipdb.com',
    'ultradns.net'
    'ultradns.org',
    'ultradns.info',
    'ultradns.co.uk',
    'dnsmadeeasy.com',
    'spamresponse.com',
    'tempestsi.com',
    'tempest.com.br',
    'expressnet.ph',
    'kanegosyo.com',
    'kanegosyo.com.ph',
    'bpiautoloans.com',
    'bpiloans.com',
    'bpiexpressonline.com',
    'bpiautomadness.com',
    'bpihousingloans.com',
    'bpipersonalloans.com',
    'bpi.com.ph',
    'bpiunlock.ph',
    'bpidirect.com',
    'bpithrills.ph',
    'bpicard.ph',
    'bpitravel.ph',
    'openbugbounty.org',
    'crdf.fr',  # French evidence portal
    'zy0.de',  # German evidence portal
    'cert.br',
    'bb.com.br',
    'netflix.com',
    'santander.com.br',
    'avast.com',
    'cloudflare.com',
    'w3.org',
    'fraudwatchinternational.com',
    'banquepopulaire.fr',
    'jpmorganchase.com',
    'nets.eu',
    'linkedin.com',
    'dailymail.co.uk',
    'wsimg.com',
    'abusix.com',
    'itau.com.br',
    'first.org',
    'colcert.gov.co',
    'avg.com',
    'mercadolibre.com',
    'mercadopago.com',
    'group-ib.com',
    'mabanque.bnpparibas',
    'imgur.com',
    'teb.com.tr',
    'deloitte.es',
    'bankofamerica.com',
    'paypal.com',
    'visa.com.ar',
    'mgmmacau.com',
    'mgmchinaholdings.com',
    'mgmgrandmacau.com',
    'mozilla.org',
    'denizbank.com',
    'eharmony.com',
    'urlscan.io',
    'credit-agricole.fr',
    'hsbc.com',
    'hsbc.ca',
    'coinbase.com',
    'banco.bradesco',
    'wikipedia.org',
    'webiron.com',
    'namesilo.com',
    'namecheap.com',
    'spamcop.net',
    'github.com',
    'mailchimp.com',
    'societegenerale.fr',
    'mail.ru',
    'instagram.com',
    'digitalocean.com',
    'name.com',
    'mimecast.com',
    'incibe-cert.es',
    'turkiye.gov.tr',
    'flipkart.com',
    'axur.com',
    'magazineluiza.com.br',
    'list-manage.com',
    'exchangelabs.com',
    '1api.support',
    'buguroo.com',
    'afilias.info',
    'afilias.net',
    'f5.com',
    'lookingglasscyber.com',
    'cert.org',
    'ubibanca.com',
    'hexonet.support',
    'bt.com',
    'usps.com',
    'd3lab.net',
    'abuse204.nl',
    'caixa.gov.br',
    'banorte.com'
}

domains.update(_godaddy_domains)
