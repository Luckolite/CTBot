import json
from os import path

import discord
from discord.ext import commands
from profanity_check import predict

from utils.logging import banned_words


# def get_vars_a():
#     if not path.isfile('./data/censor.json'):
#         print('You need to set the censor config in ./data/ first')
#         exit()
#     with open('./data/censor.json', 'r') as f:
#         censorCFG = json.load(f)  # type: dict
#     with open('./data/config.json', 'r') as f:
#         botCFG = json.load(f)  # type: dict
#     return censorCFG


# def get_vars_b():
#     if not path.isfile('./data/censor.json'):
#         print('You need to set the censor config in ./data/ first')
#         exit()
#     with open('./data/censor.json', 'r') as f:
#         censorCFG = json.load(f)  # type: dict
#     with open('./data/config.json', 'r') as f:
#         botCFG = json.load(f)  # type: dict
#     return botCFG
def get_vars():
    if not path.isfile('./data/censor.json'):
        print('You need to set the censor config in ./data/ first')
        exit()
    with open('./data/censor.json', 'r') as f:
        censorCFG = json.load(f)  # type: dict
    with open('./data/config.json', 'r') as f:
        botCFG = json.load(f)  # type: dict
    return censorCFG, botCFG


def warn(member):
    print("There is no warns system right now")
    member = member  # type: discord.Member


class censor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # type: bot

    # @commands.Cog.listener('on_message_edit')
    # async def domain_filter_OE(self, before, message):
    #     censorCFG = get_vars_a()
    #     botCFG = get_vars_b()
    #     if censorCFG["enabled"] == "False":
    #         return
    #     if censorCFG["filter_domains"] == "False":
    #         return
    #     if censorCFG["domain_whitelist"] != []:
    #         for i in censorCFG["blacklisted_domain_names"]:
    #             if message.content.lower().count(i.lower()) > 0:
    #                 if botCFG["dev-mode"] == "True":
    #                     print(
    #                         f'Message: {message.content} has been blocked because it contains '
    #                         f'{i} {message.content.lower().count(i.lower())} time(s)')
    #                 await message.delete()
    #     else:
    #         for i in censorCFG["domain_whitelist"]:
    #             if message.content.lower().count(i.lower()) > 0:
    #                 if botCFG["dev-mode"] == "True":
    #                     print(f'Message: {message.content} has been blocked because it contains'
    #                           f'{i} {message.content.lower().count(i.lower())} time(s)')

    @commands.Cog.listener('on_message_edit')
    async def profanity_filter_ML_OE(self, before, message: discord.Message):
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["profanity_filter_ml"] == "False":
            return
        prdAry = [message.content]
        if predict(prdAry) == [1]:
            await message.delete()
            if censorCFG["warn_on_censor"] == "True":
                warn(message.author)

    @commands.Cog.listener('on_message')
    async def profanity_filter_ML(self, message: discord.Message):  # OE also done
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["profanity_filter_ml"] == "False":
            return
        prdAry = [message.content]
        if predict(prdAry) == [1]:
            await message.delete()
            if censorCFG["warn_on_censor"] == "True":
                warn(message.author)

    @commands.Cog.listener('on_message_edit')
    async def profanity_filter_OE(self, before, message: discord.Message):
        arrayasstr = "2 girls 1 cup, 2g1c, 4r5e, 5h1t, 5hit, a$$, a$$hole, a_s_s, a2m, a54, a55, a55hole, acrotomophilia, aeolus, ahole, alabama hot pocket, alaskan pipeline, anal, anal impaler, anal leakage, analprobe, anilingus, anus, apeshit, ar5e, areola, areole, arian, arrse, arse, arsehole, aryan, ass, ass fuck, ass fuck, ass hole, assbag, assbandit, assbang, assbanged, assbanger, assbangs, assbite, assclown, asscock, asscracker, asses, assface, assfaces, assfuck, assfucker, ass-fucker, assfukka, assgoblin, assh0le, asshat, ass-hat, asshead, assho1e, asshole, assholes, asshopper, ass-jabber, assjacker, asslick, asslicker, assmaster, assmonkey, assmucus, assmucus, assmunch, assmuncher, assnigger, asspirate, ass-pirate, assshit, assshole, asssucker, asswad, asswhole, asswipe, asswipes, auto erotic, autoerotic, axwound, azazel, azz, b!tch, b00bs, b17ch, b1tch, babeland, baby batter, baby juice, ball gag, ball gravy, ball kicking, ball licking, ball sack, ball sucking, ballbag, balls, ballsack, bampot, bang (one's) box, bangbros, bareback, barely legal, barenaked, barf, bastard, bastardo, bastards, bastinado, batty boy, bawdy, bbw, bdsm, beaner, beaners, beardedclam, beastial, beastiality, beatch, beaver, beaver cleaver, beaver lips, beef curtain, beef curtain, beef curtains, beeyotch, bellend, bender, beotch, bescumber, bestial, bestiality, bi+ch, biatch, big black, big breasts, big knockers, big tits, bigtits, bimbo, bimbos, bint, birdlock, bitch, bitch tit, bitch tit, bitchass, bitched, bitcher, bitchers, bitches, bitchin, bitching, bitchtits, bitchy, black cock, blonde action, blonde on blonde action, bloodclaat, bloody, bloody hell, blow job, blow me, blow mud, blow your load, blowjob, blowjobs, blue waffle, blue waffle, blumpkin, blumpkin, bod, bodily, boink, boiolas, bollock, bollocks, bollok, bollox, bondage, boned, boner, boners, bong, boob, boobies, boobs, booby, booger, bookie, boong, booobs, boooobs, booooobs, booooooobs, bootee, bootie, booty, booty call, booze, boozer, boozy, bosom, bosomy, breasts, Breeder, brotherfucker, brown showers, brunette action, buceta, bugger, bukkake, bull shit, bulldyke, bullet vibe, bullshit, bullshits, bullshitted, bullturds, bum, bum boy, bumblefuck, bumclat, bummer, buncombe, bung, bung hole, bunghole, bunny fucker, bust a load, bust a load, busty, butt, butt fuck, butt fuck, butt plug, buttcheeks, buttfuck, buttfucka, buttfucker, butthole, buttmuch, buttmunch, butt-pirate, buttplug, c.0.c.k, c.o.c.k., c.u.n.t, c0ck, c-0-c-k, c0cksucker, caca, cacafuego, cahone, camel toe, cameltoe, camgirl, camslut, camwhore, carpet muncher, carpetmuncher, cawk, cervix, chesticle, chi-chi man, chick with a dick, child-fucker, chinc, chincs, chink, chinky, choad, choade, choade, choc ice, chocolate rosebuds, chode, chodes, chota bags, chota bags, cipa, circlejerk, cl1t, cleveland steamer, climax, clit, clit licker, clit licker, clitface, clitfuck, clitoris, clitorus, clits, clitty, clitty litter, clitty litter, clover clamps, clunge, clusterfuck, cnut, cocain, cocaine, coccydynia, cock, c-o-c-k, cock pocket, cock pocket, cock snot, cock snot, cock sucker, cockass, cockbite, cockblock, cockburger, cockeye, cockface, cockfucker, cockhead, cockholster, cockjockey, cockknocker, cockknoker, Cocklump, cockmaster, cockmongler, cockmongruel, cockmonkey, cockmunch, cockmuncher, cocknose, cocknugget, cocks, cockshit, cocksmith, cocksmoke, cocksmoker, cocksniffer, cocksuck, cocksuck, cocksucked, cocksucked, cocksucker, cock-sucker, cocksuckers, cocksucking, cocksucks, cocksucks, cocksuka, cocksukka, cockwaffle, coffin dodger, coital, cok, cokmuncher, coksucka, commie, condom, coochie, coochy, coon, coonnass, coons, cooter, cop some wood, cop some wood, coprolagnia, coprophilia, corksucker, cornhole, cornhole, corp whore, corp whore, corpulent, cox, crabs, crack, cracker, crackwhore, crap, crappy, creampie, cretin, crikey, cripple, crotte, cum, cum chugger, cum chugger, cum dumpster, cum dumpster, cum freak, cum freak, cum guzzler, cum guzzler, cumbubble, cumdump, cumdump, cumdumpster, cumguzzler, cumjockey, cummer, cummin, cumming, cums, cumshot, cumshots, cumslut, cumstain, cumtart, cunilingus, cunillingus, cunnie, cunnilingus, cunny, cunt, c-u-n-t, cunt hair, cunt hair, cuntass, cuntbag, cuntbag, cuntface, cunthole, cunthunter, cuntlick, cuntlick, cuntlicker, cuntlicker, cuntlicking, cuntlicking, cuntrag, cunts, cuntsicle, cuntsicle, cuntslut, cunt-struck, cunt-struck, cus, cut rope, cut rope, cyalis, cyberfuc, cyberfuck, cyberfuck, cyberfucked, cyberfucked, cyberfucker, cyberfuckers, cyberfucking, cyberfucking, d0ng, d0uch3, d0uche, d1ck, d1ld0, d1ldo, dago, dagos, dammit, damn, damned, damnit, darkie, darn, date rape, daterape, dawgie-style, deep throat, deepthroat, deggo, dendrophilia, dick, dick head, dick hole, dick hole, dick shy, dick shy, dickbag, dickbeaters, dickdipper, dickface, dickflipper, dickfuck, dickfucker, dickhead, dickheads, dickhole, dickish, dick-ish, dickjuice, dickmilk, dickmonger, dickripper, dicks, dicksipper, dickslap, dick-sneeze, dicksucker, dicksucking, dicktickler, dickwad, dickweasel, dickweed, dickwhipper, dickwod, dickzipper, diddle, dike, dildo, dildos, diligaf, dillweed, dimwit, dingle, dingleberries, dingleberry, dink, dinks, dipship, dipshit, dirsa, dirty, dirty pillows, dirty sanchez, dirty Sanchez, div, dlck, dog style, dog-fucker, doggie style, doggiestyle, doggie-style, doggin, dogging, doggy style, doggystyle, doggy-style, dolcett, domination, dominatrix, dommes, dong, donkey punch, donkeypunch, donkeyribber, doochbag, doofus, dookie, doosh, dopey, double dong, double penetration, Doublelift, douch3, douche, douchebag, douchebags, douche-fag, douchewaffle, douchey, dp action, drunk, dry hump, duche, dumass, dumb ass, dumbass, dumbasses, Dumbcunt, dumbfuck, dumbshit, dummy, dumshit, dvda, dyke, dykes, eat a dick, eat a dick, eat hair pie, eat hair pie, eat my ass, ecchi, ejaculate, ejaculated, ejaculates, ejaculates, ejaculating, ejaculating, ejaculatings, ejaculation, ejakulate, erect, erection, erotic, erotism, escort, essohbee, eunuch, extacy, extasy, f u c k, f u c k e r, f.u.c.k, f_u_c_k, f4nny, facial, fack, fag, fagbag, fagfucker, fagg, fagged, fagging, faggit, faggitt, faggot, faggotcock, faggots, faggs, fagot, fagots, fags, fagtard, faig, faigt, fanny, fannybandit, fannyflaps, fannyfucker, fanyy, fart, fartknocker, fatass, fcuk, fcuker, fcuking, fecal, feck, fecker, feist, felch, felcher, felching, fellate, fellatio, feltch, feltcher, female squirting, femdom, fenian, fice, figging, fingerbang, fingerfuck, fingerfuck, fingerfucked, fingerfucked, fingerfucker, fingerfucker, fingerfuckers, fingerfucking, fingerfucking, fingerfucks, fingerfucks, fingering, fist fuck, fist fuck, fisted, fistfuck, fistfucked, fistfucked, fistfucker, fistfucker, fistfuckers, fistfuckers, fistfucking, fistfucking, fistfuckings, fistfuckings, fistfucks, fistfucks, fisting, fisty, flamer, flange, flaps, fleshflute, flog the log, flog the log, floozy, foad, foah, fondle, foobar, fook, fooker, foot fetish, footjob, foreskin, freex, frenchify, frigg, frigga, frotting, fubar, fuc, fuck, fuck, f-u-c-k, fuck buttons, fuck hole, fuck hole, Fuck off, fuck puppet, fuck puppet, fuck trophy, fuck trophy, fuck yo mama, fuck yo mama, fuck you, fucka, fuckass, fuck-ass, fuck-ass, fuckbag, fuck-bitch, fuck-bitch, fuckboy, fuckbrain, fuckbutt, fuckbutter, fucked, fuckedup, fucker, fuckers, fuckersucker, fuckface, fuckhead, fuckheads, fuckhole, fuckin, fucking, fuckings, fuckingshitmotherfucker, fuckme, fuckme, fuckmeat, fuckmeat, fucknugget, fucknut, fucknutt, fuckoff, fucks, fuckstick, fucktard, fuck-tard, fucktards, fucktart, fucktoy, fucktoy, fucktwat, fuckup, fuckwad, fuckwhit, fuckwit, fuckwitt, fudge packer, fudgepacker, fudge-packer, fuk, fuker, fukker, fukkers, fukkin, fuks, fukwhit, fukwit, fuq, futanari, fux, fux0r, fvck, fxck, gae, gai, gang bang, gangbang, gang-bang, gang-bang, gangbanged, gangbangs, ganja, gash, gassy ass, gassy ass, gay, gay sex, gayass, gaybob, gaydo, gayfuck, gayfuckist, gaylord, gays, gaysex, gaytard, gaywad, gender bender, genitals, gey, gfy, ghay, ghey, giant cock, gigolo, ginger, gippo, girl on, girl on top, girls gone wild, git, glans, goatcx, goatse, god, god damn, godamn, godamnit, goddam, god-dam, goddammit, goddamn, goddamned, god-damned, goddamnit, godsdamn, gokkun, golden shower, goldenshower, golliwog, gonad, gonads, goo girl, gooch, goodpoop, gook, gooks, goregasm, gringo, grope, group sex, gspot, g-spot, gtfo, guido, guro, h0m0, h0mo, ham flap, ham flap, hand job, handjob, hard core, hard on, hardcore, hardcoresex, he11, hebe, heeb, hell, hemp, hentai, heroin, herp, herpes, herpy, heshe, he-she, hircismus, hitler, hiv, ho, hoar, hoare, hobag, hoe, hoer, holy shit, hom0, homey, homo, homodumbshit, homoerotic, homoey, honkey, honky, hooch, hookah, hooker, hoor, hootch, hooter, hooters, hore, horniest, horny, hot carl, hot chick, hotsex, how to kill, how to murdep, how to murder, huge fat, hump, humped, humping, hun, hussy, hymen, iap, iberian slap, inbred, incest, injun, intercourse, jack off, jackass, jackasses, jackhole, jackoff, jack-off, jaggi, jagoff, jail bait, jailbait, jap, japs, jelly donut, jerk, jerk off, jerk0ff, jerkass, jerked, jerkoff, jerk-off, jigaboo, jiggaboo, jiggerboo, jism, jiz, jiz, jizm, jizm, jizz, jizzed, jock, juggs, jungle bunny, junglebunny, junkie, junky, kafir, kawk, kike, kikes, kill, kinbaku, kinkster, kinky, klan, knob, knob end, knobbing, knobead, knobed, knobend, knobhead, knobjocky, knobjokey, kock, kondum, kondums, kooch, kooches, kootch, kraut, kum, kummer, kumming, kums, kunilingus, kunja, kunt, kwif, kwif, kyke, l3i+ch, l3itch, labia, lameass, lardass, leather restraint, leather straight jacket, lech, lemon party, LEN, leper, lesbian, lesbians, lesbo, lesbos, lez, lezza/lesbo, lezzie, lmao, lmfao, loin, loins, lolita, looney, lovemaking, lube, lust, lusting, lusty, m0f0, m0fo, m45terbate, ma5terb8, ma5terbate, mafugly, mafugly, make me come, male squirting, mams, masochist, massa, masterb8, masterbat*, masterbat3, masterbate, master-bate, master-bate, masterbating, masterbation, masterbations, masturbate, masturbating, masturbation, maxi, mcfagget, menage a trois, menses, menstruate, menstruation, meth, m-fucking, mick, microphallus, middle finger, midget, milf, minge, minger, missionary position, mof0, mofo, mo-fo, molest, mong, moo moo foo foo, moolie, moron, mothafuck, mothafucka, mothafuckas, mothafuckaz, mothafucked, mothafucked, mothafucker, mothafuckers, mothafuckin, mothafucking, mothafucking, mothafuckings, mothafucks, mother fucker, mother fucker, motherfuck, motherfucka, motherfucked, motherfucker, motherfuckers, motherfuckin, motherfucking, motherfuckings, motherfuckka, motherfucks, mound of venus, mr hands, muff, muff diver, muff puff, muff puff, muffdiver, muffdiving, munging, munter, murder, mutha, muthafecker, muthafuckker, muther, mutherfucker, n1gga, n1gger, naked, nambla, napalm, nappy, nawashi, nazi, nazism, need the dick, need the dick, negro, neonazi, nig nog, nigaboo, nigg3r, nigg4h, nigga, niggah, niggas, niggaz, nigger, niggers, niggle, niglet, nig-nog, nimphomania, nimrod, ninny, ninnyhammer, nipple, nipples, nob, nob jokey, nobhead, nobjocky, nobjokey, nonce, nsfw images, nude, nudity, numbnuts, nut butter, nut butter, nut sack, nutsack, nutter, nympho, nymphomania, octopussy, old bag, omg, omorashi, one cup two girls, one guy one jar, opiate, opium, orally, organ, orgasim, orgasims, orgasm, orgasmic, orgasms, orgies, orgy, ovary, ovum, ovums, p.u.s.s.y., p0rn, paedophile, paki, panooch, pansy, pantie, panties, panty, pawn, pcp, pecker, peckerhead, pedo, pedobear, pedophile, pedophilia, pedophiliac, pee, peepee, pegging, penetrate, penetration, penial, penile, penis, penisbanger, penisfucker, penispuffer, perversion, phallic, phone sex, phonesex, phuck, phuk, phuked, phuking, phukked, phukking, phuks, phuq, piece of shit, pigfucker, pikey, pillowbiter, pimp, pimpis, pinko, piss, piss off, piss pig, pissed, pissed off, pisser, pissers, pisses, pisses, pissflaps, pissin, pissin, pissing, pissoff, pissoff, piss-off, pisspig, playboy, pleasure chest, pms, polack, pole smoker, polesmoker, pollock, ponyplay, poof, poon, poonani, poonany, poontang, poop, poop chute, poopchute, Poopuncher, porch monkey, porchmonkey, porn, porno, pornography, pornos, pot, potty, prick, pricks, prickteaser, prig, prince albert piercing, prod, pron, prostitute, prude, psycho, pthc, pube, pubes, pubic, pubis, punani, punanny, punany, punkass, punky, punta, puss, pusse, pussi, pussies, pussy, pussy fart, pussy fart, pussy palace, pussy palace, pussylicking, pussypounder, pussys, pust, puto, queaf, queaf, queef, queer, queerbait, queerhole, queero, queers, quicky, quim, racy, raghead, raging boner, rape, raped, raper, rapey, raping, rapist, raunch, rectal, rectum, rectus, reefer, reetard, reich, renob, retard, retarded, reverse cowgirl, revue, rimjaw, rimjob, rimming, ritard, rosy palm, rosy palm and her 5 sisters, rtard, r-tard, rubbish, rum, rump, rumprammer, ruski, rusty trombone, s hit, s&m, s.h.i.t., s.o.b., s_h_i_t, s0b, sadism, sadist, sambo, sand nigger, sandbar, sandbar, Sandler, sandnigger, sanger, santorum, sausage queen, sausage queen, scag, scantily, scat, schizo, schlong, scissoring, screw, screwed, screwing, scroat, scrog, scrot, scrote, scrotum, scrud, scum, seaman, seamen, seduce, seks, semen, sex, sexo, sexual, sexy, sh!+, sh!t, sh1t, s-h-1-t, shag, shagger, shaggin, shagging, shamedame, shaved beaver, shaved pussy, shemale, shi+, shibari, shirt lifter, shit, s-h-i-t, shit ass, shit fucker, shit fucker, shitass, shitbag, shitbagger, shitblimp, shitbrains, shitbreath, shitcanned, shitcunt, shitdick, shite, shiteater, shited, shitey, shitface, shitfaced, shitfuck, shitfull, shithead, shitheads, shithole, shithouse, shiting, shitings, shits, shitspitter, shitstain, shitt, shitted, shitter, shitters, shitters, shittier, shittiest, shitting, shittings, shitty, shiz, shiznit, shota, shrimping, sissy, skag, skank, skeet, skullfuck, slag, slanteye, slave, sleaze, sleazy, slope, slope, slut, slut bucket, slut bucket, slutbag, slutdumper, slutkiss, sluts, smartass, smartasses, smeg, smegma, smut, smutty, snatch, sniper, snowballing, snuff, s-o-b, sod off, sodom, sodomize, sodomy, son of a bitch, son of a motherless goat, son of a whore, son-of-a-bitch, souse, soused, spac, spade, sperm, spic, spick, spik, spiks, splooge, splooge moose, spooge, spook, spread legs, spunk, stfu, stiffy, stoned, strap on, strapon, strappado, strip, strip club, stroke, stupid, style doggy, suck, suckass, sucked, sucking, sucks, suicide girls, sultry women, sumofabiatch, swastika, swinger, t1t, t1tt1e5, t1tties, taff, taig, tainted love, taking the piss, tampon, tard, tart, taste my, tawdry, tea bagging, teabagging, teat, teets, teez, teste, testee, testes, testical, testicle, testis, threesome, throating, thrust, thug, thundercunt, tied up, tight white, tinkle, tit, tit wank, tit wank, titfuck, titi, tities, tits, titt, tittie5, tittiefucker, titties, titty, tittyfuck, tittyfucker, tittywank, titwank, toke, tongue in a, toots, topless, tosser, towelhead, tramp, tranny, transsexual, trashy, tribadism, trumped, tub girl, tubgirl, turd, tush, tushy, tw4t, twat, twathead, twatlips, twats, twatty, twatwaffle, twink, twinkie, two fingers, two fingers with tongue, two girls one cup, twunt, twunter, ugly, unclefucker, undies, undressing, unwed, upskirt, urethra play, urinal, urine, urophilia, uterus, uzi, v14gra, v1gra, vag, vagina, vajayjay, va-j-j, valium, venus mound, veqtable, viagra, vibrator, violet wand, virgin, vixen, vjayjay, vodka, vomit, vorarephilia, voyeur, vulgar, vulva, w00se, wad, wang, wank, wanker, wankjob, wanky, wazoo, wedgie, weed, weenie, weewee, weiner, weirdo, wench, wet dream, wetback, wh0re, wh0reface, white power, whiz, whoar, whoralicious, whore, whorealicious, whorebag, whored, whoreface, whorehopper, whorehouse, whores, whoring, wigger, willies, willy, window licker, wiseass, wiseasses, wog, womb, wop, wrapping men, wrinkled starfish, wtf, xrated, x-rated, xx, xxx, yaoi, yeasty, yellow showers, yid, yiffy, yobbo, zibbi, zoophilia, zubb"
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["profanity_filter"] == "False":
            return
        array = arrayasstr.split(', ')
        for i in array:
            if message.content.lower().count(i.lower()) > 0:
                await message.delete()
                if censorCFG["warn_on_censor"] == "True":
                    warn(message.author)

    @commands.Cog.listener('on_message')
    async def profanity_filter(self, message: discord.Message):  # OE also done
        arrayasstr = "2 girls 1 cup, 2g1c, 4r5e, 5h1t, 5hit, a$$, a$$hole, a_s_s, a2m, a54, a55, a55hole, acrotomophilia, aeolus, ahole, alabama hot pocket, alaskan pipeline, anal, anal impaler, anal leakage, analprobe, anilingus, anus, apeshit, ar5e, areola, areole, arian, arrse, arse, arsehole, aryan, ass, ass fuck, ass fuck, ass hole, assbag, assbandit, assbang, assbanged, assbanger, assbangs, assbite, assclown, asscock, asscracker, asses, assface, assfaces, assfuck, assfucker, ass-fucker, assfukka, assgoblin, assh0le, asshat, ass-hat, asshead, assho1e, asshole, assholes, asshopper, ass-jabber, assjacker, asslick, asslicker, assmaster, assmonkey, assmucus, assmucus, assmunch, assmuncher, assnigger, asspirate, ass-pirate, assshit, assshole, asssucker, asswad, asswhole, asswipe, asswipes, auto erotic, autoerotic, axwound, azazel, azz, b!tch, b00bs, b17ch, b1tch, babeland, baby batter, baby juice, ball gag, ball gravy, ball kicking, ball licking, ball sack, ball sucking, ballbag, balls, ballsack, bampot, bang (one's) box, bangbros, bareback, barely legal, barenaked, barf, bastard, bastardo, bastards, bastinado, batty boy, bawdy, bbw, bdsm, beaner, beaners, beardedclam, beastial, beastiality, beatch, beaver, beaver cleaver, beaver lips, beef curtain, beef curtain, beef curtains, beeyotch, bellend, bender, beotch, bescumber, bestial, bestiality, bi+ch, biatch, big black, big breasts, big knockers, big tits, bigtits, bimbo, bimbos, bint, birdlock, bitch, bitch tit, bitch tit, bitchass, bitched, bitcher, bitchers, bitches, bitchin, bitching, bitchtits, bitchy, black cock, blonde action, blonde on blonde action, bloodclaat, bloody, bloody hell, blow job, blow me, blow mud, blow your load, blowjob, blowjobs, blue waffle, blue waffle, blumpkin, blumpkin, bod, bodily, boink, boiolas, bollock, bollocks, bollok, bollox, bondage, boned, boner, boners, bong, boob, boobies, boobs, booby, booger, bookie, boong, booobs, boooobs, booooobs, booooooobs, bootee, bootie, booty, booty call, booze, boozer, boozy, bosom, bosomy, breasts, Breeder, brotherfucker, brown showers, brunette action, buceta, bugger, bukkake, bull shit, bulldyke, bullet vibe, bullshit, bullshits, bullshitted, bullturds, bum, bum boy, bumblefuck, bumclat, bummer, buncombe, bung, bung hole, bunghole, bunny fucker, bust a load, bust a load, busty, butt, butt fuck, butt fuck, butt plug, buttcheeks, buttfuck, buttfucka, buttfucker, butthole, buttmuch, buttmunch, butt-pirate, buttplug, c.0.c.k, c.o.c.k., c.u.n.t, c0ck, c-0-c-k, c0cksucker, caca, cacafuego, cahone, camel toe, cameltoe, camgirl, camslut, camwhore, carpet muncher, carpetmuncher, cawk, cervix, chesticle, chi-chi man, chick with a dick, child-fucker, chinc, chincs, chink, chinky, choad, choade, choade, choc ice, chocolate rosebuds, chode, chodes, chota bags, chota bags, cipa, circlejerk, cl1t, cleveland steamer, climax, clit, clit licker, clit licker, clitface, clitfuck, clitoris, clitorus, clits, clitty, clitty litter, clitty litter, clover clamps, clunge, clusterfuck, cnut, cocain, cocaine, coccydynia, cock, c-o-c-k, cock pocket, cock pocket, cock snot, cock snot, cock sucker, cockass, cockbite, cockblock, cockburger, cockeye, cockface, cockfucker, cockhead, cockholster, cockjockey, cockknocker, cockknoker, Cocklump, cockmaster, cockmongler, cockmongruel, cockmonkey, cockmunch, cockmuncher, cocknose, cocknugget, cocks, cockshit, cocksmith, cocksmoke, cocksmoker, cocksniffer, cocksuck, cocksuck, cocksucked, cocksucked, cocksucker, cock-sucker, cocksuckers, cocksucking, cocksucks, cocksucks, cocksuka, cocksukka, cockwaffle, coffin dodger, coital, cok, cokmuncher, coksucka, commie, condom, coochie, coochy, coon, coonnass, coons, cooter, cop some wood, cop some wood, coprolagnia, coprophilia, corksucker, cornhole, cornhole, corp whore, corp whore, corpulent, cox, crabs, crack, cracker, crackwhore, crap, crappy, creampie, cretin, crikey, cripple, crotte, cum, cum chugger, cum chugger, cum dumpster, cum dumpster, cum freak, cum freak, cum guzzler, cum guzzler, cumbubble, cumdump, cumdump, cumdumpster, cumguzzler, cumjockey, cummer, cummin, cumming, cums, cumshot, cumshots, cumslut, cumstain, cumtart, cunilingus, cunillingus, cunnie, cunnilingus, cunny, cunt, c-u-n-t, cunt hair, cunt hair, cuntass, cuntbag, cuntbag, cuntface, cunthole, cunthunter, cuntlick, cuntlick, cuntlicker, cuntlicker, cuntlicking, cuntlicking, cuntrag, cunts, cuntsicle, cuntsicle, cuntslut, cunt-struck, cunt-struck, cus, cut rope, cut rope, cyalis, cyberfuc, cyberfuck, cyberfuck, cyberfucked, cyberfucked, cyberfucker, cyberfuckers, cyberfucking, cyberfucking, d0ng, d0uch3, d0uche, d1ck, d1ld0, d1ldo, dago, dagos, dammit, damn, damned, damnit, darkie, darn, date rape, daterape, dawgie-style, deep throat, deepthroat, deggo, dendrophilia, dick, dick head, dick hole, dick hole, dick shy, dick shy, dickbag, dickbeaters, dickdipper, dickface, dickflipper, dickfuck, dickfucker, dickhead, dickheads, dickhole, dickish, dick-ish, dickjuice, dickmilk, dickmonger, dickripper, dicks, dicksipper, dickslap, dick-sneeze, dicksucker, dicksucking, dicktickler, dickwad, dickweasel, dickweed, dickwhipper, dickwod, dickzipper, diddle, dike, dildo, dildos, diligaf, dillweed, dimwit, dingle, dingleberries, dingleberry, dink, dinks, dipship, dipshit, dirsa, dirty, dirty pillows, dirty sanchez, dirty Sanchez, div, dlck, dog style, dog-fucker, doggie style, doggiestyle, doggie-style, doggin, dogging, doggy style, doggystyle, doggy-style, dolcett, domination, dominatrix, dommes, dong, donkey punch, donkeypunch, donkeyribber, doochbag, doofus, dookie, doosh, dopey, double dong, double penetration, Doublelift, douch3, douche, douchebag, douchebags, douche-fag, douchewaffle, douchey, dp action, drunk, dry hump, duche, dumass, dumb ass, dumbass, dumbasses, Dumbcunt, dumbfuck, dumbshit, dummy, dumshit, dvda, dyke, dykes, eat a dick, eat a dick, eat hair pie, eat hair pie, eat my ass, ecchi, ejaculate, ejaculated, ejaculates, ejaculates, ejaculating, ejaculating, ejaculatings, ejaculation, ejakulate, erect, erection, erotic, erotism, escort, essohbee, eunuch, extacy, extasy, f u c k, f u c k e r, f.u.c.k, f_u_c_k, f4nny, facial, fack, fag, fagbag, fagfucker, fagg, fagged, fagging, faggit, faggitt, faggot, faggotcock, faggots, faggs, fagot, fagots, fags, fagtard, faig, faigt, fanny, fannybandit, fannyflaps, fannyfucker, fanyy, fart, fartknocker, fatass, fcuk, fcuker, fcuking, fecal, feck, fecker, feist, felch, felcher, felching, fellate, fellatio, feltch, feltcher, female squirting, femdom, fenian, fice, figging, fingerbang, fingerfuck, fingerfuck, fingerfucked, fingerfucked, fingerfucker, fingerfucker, fingerfuckers, fingerfucking, fingerfucking, fingerfucks, fingerfucks, fingering, fist fuck, fist fuck, fisted, fistfuck, fistfucked, fistfucked, fistfucker, fistfucker, fistfuckers, fistfuckers, fistfucking, fistfucking, fistfuckings, fistfuckings, fistfucks, fistfucks, fisting, fisty, flamer, flange, flaps, fleshflute, flog the log, flog the log, floozy, foad, foah, fondle, foobar, fook, fooker, foot fetish, footjob, foreskin, freex, frenchify, frigg, frigga, frotting, fubar, fuc, fuck, fuck, f-u-c-k, fuck buttons, fuck hole, fuck hole, Fuck off, fuck puppet, fuck puppet, fuck trophy, fuck trophy, fuck yo mama, fuck yo mama, fuck you, fucka, fuckass, fuck-ass, fuck-ass, fuckbag, fuck-bitch, fuck-bitch, fuckboy, fuckbrain, fuckbutt, fuckbutter, fucked, fuckedup, fucker, fuckers, fuckersucker, fuckface, fuckhead, fuckheads, fuckhole, fuckin, fucking, fuckings, fuckingshitmotherfucker, fuckme, fuckme, fuckmeat, fuckmeat, fucknugget, fucknut, fucknutt, fuckoff, fucks, fuckstick, fucktard, fuck-tard, fucktards, fucktart, fucktoy, fucktoy, fucktwat, fuckup, fuckwad, fuckwhit, fuckwit, fuckwitt, fudge packer, fudgepacker, fudge-packer, fuk, fuker, fukker, fukkers, fukkin, fuks, fukwhit, fukwit, fuq, futanari, fux, fux0r, fvck, fxck, gae, gai, gang bang, gangbang, gang-bang, gang-bang, gangbanged, gangbangs, ganja, gash, gassy ass, gassy ass, gay, gay sex, gayass, gaybob, gaydo, gayfuck, gayfuckist, gaylord, gays, gaysex, gaytard, gaywad, gender bender, genitals, gey, gfy, ghay, ghey, giant cock, gigolo, ginger, gippo, girl on, girl on top, girls gone wild, git, glans, goatcx, goatse, god, god damn, godamn, godamnit, goddam, god-dam, goddammit, goddamn, goddamned, god-damned, goddamnit, godsdamn, gokkun, golden shower, goldenshower, golliwog, gonad, gonads, goo girl, gooch, goodpoop, gook, gooks, goregasm, gringo, grope, group sex, gspot, g-spot, gtfo, guido, guro, h0m0, h0mo, ham flap, ham flap, hand job, handjob, hard core, hard on, hardcore, hardcoresex, he11, hebe, heeb, hell, hemp, hentai, heroin, herp, herpes, herpy, heshe, he-she, hircismus, hitler, hiv, ho, hoar, hoare, hobag, hoe, hoer, holy shit, hom0, homey, homo, homodumbshit, homoerotic, homoey, honkey, honky, hooch, hookah, hooker, hoor, hootch, hooter, hooters, hore, horniest, horny, hot carl, hot chick, hotsex, how to kill, how to murdep, how to murder, huge fat, hump, humped, humping, hun, hussy, hymen, iap, iberian slap, inbred, incest, injun, intercourse, jack off, jackass, jackasses, jackhole, jackoff, jack-off, jaggi, jagoff, jail bait, jailbait, jap, japs, jelly donut, jerk, jerk off, jerk0ff, jerkass, jerked, jerkoff, jerk-off, jigaboo, jiggaboo, jiggerboo, jism, jiz, jiz, jizm, jizm, jizz, jizzed, jock, juggs, jungle bunny, junglebunny, junkie, junky, kafir, kawk, kike, kikes, kill, kinbaku, kinkster, kinky, klan, knob, knob end, knobbing, knobead, knobed, knobend, knobhead, knobjocky, knobjokey, kock, kondum, kondums, kooch, kooches, kootch, kraut, kum, kummer, kumming, kums, kunilingus, kunja, kunt, kwif, kwif, kyke, l3i+ch, l3itch, labia, lameass, lardass, leather restraint, leather straight jacket, lech, lemon party, LEN, leper, lesbian, lesbians, lesbo, lesbos, lez, lezza/lesbo, lezzie, lmao, lmfao, loin, loins, lolita, looney, lovemaking, lube, lust, lusting, lusty, m0f0, m0fo, m45terbate, ma5terb8, ma5terbate, mafugly, mafugly, make me come, male squirting, mams, masochist, massa, masterb8, masterbat*, masterbat3, masterbate, master-bate, master-bate, masterbating, masterbation, masterbations, masturbate, masturbating, masturbation, maxi, mcfagget, menage a trois, menses, menstruate, menstruation, meth, m-fucking, mick, microphallus, middle finger, midget, milf, minge, minger, missionary position, mof0, mofo, mo-fo, molest, mong, moo moo foo foo, moolie, moron, mothafuck, mothafucka, mothafuckas, mothafuckaz, mothafucked, mothafucked, mothafucker, mothafuckers, mothafuckin, mothafucking, mothafucking, mothafuckings, mothafucks, mother fucker, mother fucker, motherfuck, motherfucka, motherfucked, motherfucker, motherfuckers, motherfuckin, motherfucking, motherfuckings, motherfuckka, motherfucks, mound of venus, mr hands, muff, muff diver, muff puff, muff puff, muffdiver, muffdiving, munging, munter, murder, mutha, muthafecker, muthafuckker, muther, mutherfucker, n1gga, n1gger, naked, nambla, napalm, nappy, nawashi, nazi, nazism, need the dick, need the dick, negro, neonazi, nig nog, nigaboo, nigg3r, nigg4h, nigga, niggah, niggas, niggaz, nigger, niggers, niggle, niglet, nig-nog, nimphomania, nimrod, ninny, ninnyhammer, nipple, nipples, nob, nob jokey, nobhead, nobjocky, nobjokey, nonce, nsfw images, nude, nudity, numbnuts, nut butter, nut butter, nut sack, nutsack, nutter, nympho, nymphomania, octopussy, old bag, omg, omorashi, one cup two girls, one guy one jar, opiate, opium, orally, organ, orgasim, orgasims, orgasm, orgasmic, orgasms, orgies, orgy, ovary, ovum, ovums, p.u.s.s.y., p0rn, paedophile, paki, panooch, pansy, pantie, panties, panty, pawn, pcp, pecker, peckerhead, pedo, pedobear, pedophile, pedophilia, pedophiliac, pee, peepee, pegging, penetrate, penetration, penial, penile, penis, penisbanger, penisfucker, penispuffer, perversion, phallic, phone sex, phonesex, phuck, phuk, phuked, phuking, phukked, phukking, phuks, phuq, piece of shit, pigfucker, pikey, pillowbiter, pimp, pimpis, pinko, piss, piss off, piss pig, pissed, pissed off, pisser, pissers, pisses, pisses, pissflaps, pissin, pissin, pissing, pissoff, pissoff, piss-off, pisspig, playboy, pleasure chest, pms, polack, pole smoker, polesmoker, pollock, ponyplay, poof, poon, poonani, poonany, poontang, poop, poop chute, poopchute, Poopuncher, porch monkey, porchmonkey, porn, porno, pornography, pornos, pot, potty, prick, pricks, prickteaser, prig, prince albert piercing, prod, pron, prostitute, prude, psycho, pthc, pube, pubes, pubic, pubis, punani, punanny, punany, punkass, punky, punta, puss, pusse, pussi, pussies, pussy, pussy fart, pussy fart, pussy palace, pussy palace, pussylicking, pussypounder, pussys, pust, puto, queaf, queaf, queef, queer, queerbait, queerhole, queero, queers, quicky, quim, racy, raghead, raging boner, rape, raped, raper, rapey, raping, rapist, raunch, rectal, rectum, rectus, reefer, reetard, reich, renob, retard, retarded, reverse cowgirl, revue, rimjaw, rimjob, rimming, ritard, rosy palm, rosy palm and her 5 sisters, rtard, r-tard, rubbish, rum, rump, rumprammer, ruski, rusty trombone, s hit, s&m, s.h.i.t., s.o.b., s_h_i_t, s0b, sadism, sadist, sambo, sand nigger, sandbar, sandbar, Sandler, sandnigger, sanger, santorum, sausage queen, sausage queen, scag, scantily, scat, schizo, schlong, scissoring, screw, screwed, screwing, scroat, scrog, scrot, scrote, scrotum, scrud, scum, seaman, seamen, seduce, seks, semen, sex, sexo, sexual, sexy, sh!+, sh!t, sh1t, s-h-1-t, shag, shagger, shaggin, shagging, shamedame, shaved beaver, shaved pussy, shemale, shi+, shibari, shirt lifter, shit, s-h-i-t, shit ass, shit fucker, shit fucker, shitass, shitbag, shitbagger, shitblimp, shitbrains, shitbreath, shitcanned, shitcunt, shitdick, shite, shiteater, shited, shitey, shitface, shitfaced, shitfuck, shitfull, shithead, shitheads, shithole, shithouse, shiting, shitings, shits, shitspitter, shitstain, shitt, shitted, shitter, shitters, shitters, shittier, shittiest, shitting, shittings, shitty, shiz, shiznit, shota, shrimping, sissy, skag, skank, skeet, skullfuck, slag, slanteye, slave, sleaze, sleazy, slope, slope, slut, slut bucket, slut bucket, slutbag, slutdumper, slutkiss, sluts, smartass, smartasses, smeg, smegma, smut, smutty, snatch, sniper, snowballing, snuff, s-o-b, sod off, sodom, sodomize, sodomy, son of a bitch, son of a motherless goat, son of a whore, son-of-a-bitch, souse, soused, spac, spade, sperm, spic, spick, spik, spiks, splooge, splooge moose, spooge, spook, spread legs, spunk, stfu, stiffy, stoned, strap on, strapon, strappado, strip, strip club, stroke, stupid, style doggy, suck, suckass, sucked, sucking, sucks, suicide girls, sultry women, sumofabiatch, swastika, swinger, t1t, t1tt1e5, t1tties, taff, taig, tainted love, taking the piss, tampon, tard, tart, taste my, tawdry, tea bagging, teabagging, teat, teets, teez, teste, testee, testes, testical, testicle, testis, threesome, throating, thrust, thug, thundercunt, tied up, tight white, tinkle, tit, tit wank, tit wank, titfuck, titi, tities, tits, titt, tittie5, tittiefucker, titties, titty, tittyfuck, tittyfucker, tittywank, titwank, toke, tongue in a, toots, topless, tosser, towelhead, tramp, tranny, transsexual, trashy, tribadism, trumped, tub girl, tubgirl, turd, tush, tushy, tw4t, twat, twathead, twatlips, twats, twatty, twatwaffle, twink, twinkie, two fingers, two fingers with tongue, two girls one cup, twunt, twunter, ugly, unclefucker, undies, undressing, unwed, upskirt, urethra play, urinal, urine, urophilia, uterus, uzi, v14gra, v1gra, vag, vagina, vajayjay, va-j-j, valium, venus mound, veqtable, viagra, vibrator, violet wand, virgin, vixen, vjayjay, vodka, vomit, vorarephilia, voyeur, vulgar, vulva, w00se, wad, wang, wank, wanker, wankjob, wanky, wazoo, wedgie, weed, weenie, weewee, weiner, weirdo, wench, wet dream, wetback, wh0re, wh0reface, white power, whiz, whoar, whoralicious, whore, whorealicious, whorebag, whored, whoreface, whorehopper, whorehouse, whores, whoring, wigger, willies, willy, window licker, wiseass, wiseasses, wog, womb, wop, wrapping men, wrinkled starfish, wtf, xrated, x-rated, xx, xxx, yaoi, yeasty, yellow showers, yid, yiffy, yobbo, zibbi, zoophilia, zubb"
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["profanity_filter"] == "False":
            return
        array = arrayasstr.split(', ')
        for i in array:
            if message.content.lower().count(i.lower()) > 0:
                await message.delete()
                if censorCFG["warn_on_censor"] == "True":
                    warn(message.author)

    @commands.Cog.listener('on_message_edit')
    async def message_char_limit_OE(self, before, message):
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["message_char_limit"] == 0:
            return
        chars = len(message.content)
        if chars >= censorCFG["message_char_limit"]:
            await message.delete()
            if censorCFG["warn_on_censor"]:
                warn(message.author)

    @commands.Cog.listener('on_message_edit')
    async def caps_limit_OE(self, before, message: discord.Message):
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["caps_limit_enabled"] == "False":
            return
        cap_count = 0
        for i in message.content:
            if i.isupper():
                cap_count += 1
        if cap_count >= censorCFG["caps_limit"]:
            await message.delete()
            if censorCFG["warn_on_censor"] == "True":
                warn(message.author)

    @commands.Cog.listener('on_message_edit')
    async def word_filter_OE(self, before, message):
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        elif censorCFG["wordfilter_enabled"] == "False":
            return
        elif message.channel.id in censorCFG["wordfilter_channel_exceptions_array_ids"]:
            return

        for i in censorCFG["blocked_words"]:
            if message.content.lower().count(i.lower()) > 0:
                if botCFG["dev-mode"] == "True":
                    print(
                        f'Message: {message.content} has been blocked because it '
                        f'contains {i} {message.content.lower().count(i.lower())} times')
                    await banned_words(self, message)
                await message.delete()

    # @commands.Cog.listener('on_message')
    # async def domain_filter(self, message: discord.Message):  # OE also done
    #     censorCFG = get_vars_a()
    #     botCFG = get_vars_b()
    #     if censorCFG["enabled"] == "False":
    #         return
    #     if censorCFG["filter_domains"] == "False":
    #         return
    #     if censorCFG["domain_whitelist"] != []:
    #         for i in censorCFG["blacklisted_domain_names"]:
    #             if message.content.lower().count(i.lower()) > 0:
    #                 if botCFG["dev-mode"] == "True":
    #                     print(
    #                         f'Message: {message.content} has been blocked because it contains '
    #                         f'{i} {message.content.lower().count(i.lower())} time(s)')
    #                 await message.delete()
    #     else:
    #         for i in censorCFG["domain_whitelist"]:
    #             if message.content.lower().count(i.lower()) > 0:
    #                 if botCFG["dev-mode"] == "True":
    #                     print(f'Message: {message.content} has been blocked because it contains'
    #                           f'{i} {message.content.lower().count(i.lower())} time(s)')

    @commands.Cog.listener('on_message')
    async def message_char_limit(self, message: discord.Message):  # OE also done
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["message_char_limit"] == 0:
            return
        chars = len(message.content)
        if chars >= censorCFG["message_char_limit"]:
            await message.delete()
            if censorCFG["warn_on_censor"]:
                warn(message.author)

    @commands.Cog.listener('on_message')  # caps limit
    async def caps_limit(self, message: discord.Message):  # OE also done
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        if censorCFG["caps_limit_enabled"] == "False":
            return
        cap_count = 0
        for i in message.content:
            if i.isupper():
                cap_count += 1
        if cap_count >= censorCFG["caps_limit"]:
            await message.delete()
            if censorCFG["warn_on_censor"] == "True":
                warn(message.author)

    @commands.Cog.listener('on_message')  # word filter
    async def word_filter(self, message: discord.Message):  # OE also done
        censorCFG, botCFG = get_vars()
        if censorCFG["enabled"] == "False":
            return
        elif censorCFG["wordfilter_enabled"] == "False":
            return
        elif message.channel.id in censorCFG["wordfilter_channel_exceptions_array_ids"]:
            return

        for i in censorCFG["blocked_words"]:
            if message.content.lower().count(i.lower()) > 0:
                if botCFG["dev-mode"] == "True":
                    print(
                        f'Message: {message.content} has been blocked because it '
                        f'contains {i} {message.content.lower().count(i.lower())} times')
                    await banned_words(self, message)
                    if censorCFG["wordfilter-resp-msg-enabled"] != "False":
                        msg = await message.channel.send(censorCFG["wordfilter-resp-msg"])  # type: discord.Message
                        await msg.delete(delay=censorCFG["wordfilter-resp-msg-del-time"])

                try:
                    await message.delete()
                except Exception as e:
                    print(e)

    @commands.Cog.listener('on_member_update')  # nick censor
    async def nick_censor(self, before, after):
        censorCFG, botCFG = get_vars()

        if censorCFG["enabled"] == "False":
            return
        elif censorCFG["nickname_filter_enabled"] == "False":
            return

        before = before  # type: discord.Member
        after = after  # type: discord.Member
        n = after.nick
        if n:
            for i in censorCFG["blocked_words"]:
                if n.lower().count(i.lower()) > 0:
                    await after.edit(nick=censorCFG["censored_nickname"], reason="CENSORED BY CT BOT")
                    if censorCFG["warn_on_censor"] == "True":
                        warn(after)
                    if botCFG['dev-mode'] == "True":
                        print(f'nick: {n} has been blocked because it contains {i} {n.lower().count(i.lower())} times')


def setup(bot):
    bot.add_cog(censor(bot))
