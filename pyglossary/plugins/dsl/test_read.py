# -*- coding: utf-8 -*-
from unittest import TestCase

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from dsl import read
from pyglossary.glossary import Glossary

def test_word(self, before, after):
    g = Glossary()
    read(g, '../../../../dsl_to_json/dictionary/tests/' + before, 'utf8')
    self.assertEqual(after, g._data[0][1])

class TestRead(TestCase):

    def test_word_abalone(self):
        before = 'En-Ru-Apresyan_abalone.dsl'
        after = '{"text":"abalone","def":[{"area":"зоол.","ts":",æbə\'ləʋnı","trn":[{"tr":[{"text":"морское ушко (<i>Haliotis spp.</i>; <i>съедобный моллюск</i>)"}]}],"class":"n"}]}'
        test_word(self, before, after)

    def test_word_abaft(self):
        before = 'En-Ru-Apresyan_abaft.dsl'
        after = '''{"text":"abaft","def":[{"trn":[{"tr":[{"text":"на корме <i>или</i> по направлению к корме"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"1","class":"adv"},{"trn":[{"tr":[{"text":"сзади","syn":[{"text":"позади"}]},{"text":"за"}],"ex":[{"text":"abaft the beam","tr":"позади траверза"}]}],"area":"мор.","ts":"ə'bɑ:ft","numB":"2","class":"prep"}]}'''
        test_word(self, before, after)

    def test_word_abampere(self):
        before = 'En-Ru-Apresyan_abampere.dsl'
        after = '''{"text":"abampere","def":[{"trn":[{"tr":[{"text":"единица силы тока СГСМ"}]}],"ts":"æ'bæmpeə","class":"n"}]}'''
        test_word(self, before, after)

    def test_word_abandon(self):
        before = 'En-Ru-Apresyan_abandon.dsl'
        after = '''{"text":"abandon","hom":[{"numRB":"I","def":[{"trn":[{"tr":[{"text":"абандон"}]}],"area":"страх.","ts":"ə'bændən","numB":"1","class":"n"},{"trn":[{"num":"1","tr":[{"text":"отказываться"},{"text":"оставлять"}],"ex":[{"text":"to abandon the attempt","tr":"отказаться от попытки, прекратить попытки"},{"text":"to abandon (all) hope","tr":"оставить (всякую) надежду"},{"text":"abandon hope all ye who enter here (<i>Dante</i>)","tr":"оставь надежду всяк сюда входящий"},{"text":"the search was abandoned","tr":"поиски были прекращены"},{"text":"to abandon a custom","tr":"не сохранить /предать забвению/ обычай"},{"text":"immigrants slow to abandon their native languages","tr":"иммигранты, неохотно отказывающиеся от своего родного языка"}]},{"num":"2","tr":[{"text":"сдавать"}],"ex":[{"text":"to abandon the city to the enemy","tr":"сдать город врагу"},{"text":"to abandon oneself to the conqueror's mercy","tr":"сдаться на милость победителя"}]},{"num":"3","tr":[{"text":"покидать","syn":[{"text":"оставлять"}]},{"text":"самовольно уходить (<i>с поста </i><i data-abbr>и т. п.</i>)"}],"ex":[{"text":"to abandon smb.","tr":"бросить кого-л."},{"text":"to abandon the sinking ship","tr":"покинуть тонущий корабль"},{"text":"courage abandoned him","tr":"мужество покинуло его"}]},{"num":"4","tr":[{"text":"<i data-abbr>юр.</i> отказаться (<i>от собственности, от права </i><i data-abbr>и т. п.</i>)"}]},{"num":"5","tr":[{"text":"закрывать"},{"text":"консервировать (<i>предприятие </i><i data-abbr>и т. п.</i>)"}],"ex":[{"text":" <i data-abbr>♢</i> to abandon oneself to smth.","tr":"предаваться чему-л.; отдаваться чему-л."},{"text":"to abandon oneself to passion [despair]","tr":"предаваться страсти [отчаянию]"},{"text":"to be abandoned to smth.","tr":"предаваться чему-л.; испытывать что-л."},{"text":"to be abandoned to grief [despair]","tr":"предаться горю [отчаянию]"}]}],"ts":"ə'bændən","numB":"2","class":"v"}]},{"numRB":"II","def":[{"trn":[{"num":"1","tr":[{"text":"<i data-abbr>книжн.</i> развязность; несдержанность"}],"ex":[{"text":"to do smth. with /at, in/ (complete) abandon","tr":"делать что-л., (совершенно) забыв обо всём /отдавшись порыву/"}]},{"num":"2","tr":[{"text":"импульсивность"},{"text":"энергия"}],"ex":[{"text":"to sing with abandon","tr":"петь с чувством, забыться в песне"},{"text":"to wave one's hand with abandon","tr":"энергично размахивать рукой"},{"text":"he spoke with complete abandon","tr":"он говорил, забыв обо всём; его словно прорвало"}]}],"ts":"ə'bændən","class":"n"}]}]}'''
        test_word(self, before, after)

    def test_word_abandonment(self):
        before = 'En-Ru-Apresyan_abandonment.dsl'
        after = '''{"text":"abandonment","hom":[{"numRB":"I","def":[{"trn":[{"num":"1","tr":[{"text":"оставление"}],"sense":"1"},{"num":"1","tr":[{"text":"<i data-abbr>юр.</i> оставление жены, ребёнка"}],"sense":"2"},{"num":"2","tr":[{"text":"заброшенность","syn":[{"text":"запущенность"}]}]},{"num":"3","tr":[{"text":"<i data-abbr>юр.</i> отказ (<i>от права, иска</i>)"}],"sense":"1"},{"num":"3","tr":[{"text":"<i data-abbr>страх.</i> абандон"}],"sense":"2"}],"ts":"ə'bændənmənt","class":"n"}]},{"numRB":"II","def":[{"com":"<i>= abandon</i><sup>2 </sup>","ts":"ə'bændənmənt"}]}]}'''
        test_word(self, before, after)

    def test_word_was(self):
        before = 'En-Ru-Apresyan_was.dsl'
        after = '''{"text":"was","def":[{"ts":"wɒz (полная форма); wəz,wz (редуцированные формы)","trn":[{"tr":[{"text":"<i>1-е и 3-е </i><i data-abbr>л.</i> <i data-abbr>ед.</i> <i data-abbr>ч.</i><i> прошедшего времени </i><i data-abbr>гл.</i> be"}]}]}]}'''
        test_word(self, before, after)

    def test_word_be(self):
        before = 'En-Ru-Apresyan_be.dsl'
        after = '''{"text":"be","def":[{"hom":[{"numR":"I","trn":[{"num":"1","tr":[{"text":"быть","syn":[{"text":"существовать"}]}],"ex":[{"text":"I think, therefore I am","tr":"я мыслю, следовательно, я существую"},{"text":"the greatest genius that ever was","tr":"величайший гений, который когда-либо существовал"},{"text":"to be no more","tr":"<i data-abbr>возвыш.</i> скончаться, умереть; прекратить существование"},{"text":"Troy is no more","tr":"Трои больше не существует"},{"text":"to be, or not to be - that is the question (<i>Shakespeare</i>)","tr":"быть или не быть, вот в чём вопрос"}]},{"num":"2","tr":[{"text":"быть","syn":[{"text":"находиться"}]},{"text":"присутствовать"},{"text":"пребывать"}],"ex":[{"text":"he will be here all the year","tr":"он будет (находиться) здесь весь год"},{"text":"is he often in town?","tr":"часто ли он бывает в городе?"},{"text":"I was before you in the queue","tr":"я стоял перед вами в очереди"},{"text":"the horse was below in the hold","tr":"лошадь поместили в трюме"},{"text":"he was at the ceremony","tr":"он присутствовал на церемонии"},{"text":"the key is in the lock","tr":"ключ (находится) в замке"},{"text":"I'll be down in a minute","tr":"я сейчас спущусь"},{"text":"output is considerably below last year's level","tr":"выпуск продукции намного ниже прошлогоднего /значительно ниже прошлогоднего, значительно упал по сравнению с прошлогодним/"}],"sense":"1"},{"num":"2","tr":[{"text":"быть","syn":[{"text":"оставаться"}]}],"ex":[{"text":"don't be long!","tr":"не задерживайся!, приходи скорее!"},{"text":"what a time you have been!","tr":"как ты долго!"},{"text":"he was a long time reaching the shore","tr":"ему понадобилось много времени, чтобы достичь берега"}],"sense":"2"},{"num":"3","tr":[{"text":"происходить","syn":[{"text":"случаться"},{"text":"совершаться"}]}],"ex":[{"text":"it was yesterday","tr":"это было /произошло, случилось, состоялось/ вчера"},{"text":"when is the wedding to be?","tr":"когда должна состояться /будет/ свадьба?"},{"text":"the New Year is on Sunday this time","tr":"в этот раз Новый год приходится /падает/ на воскресенье"},{"text":"how is it that you were there?","tr":"как получилось, что вы оказались там?"}]},{"num":"4","tr":[{"text":"равняться","syn":[{"text":"составлять"}]}],"ex":[{"text":"twice two is four","tr":"дважды два - четыре"},{"text":"let <i>x </i>be ten","tr":"предположим, (что) <i>x</i> равняется десяти"}],"sense":"1"},{"num":"4","tr":[{"text":"<i data-abbr>разг.</i> стоить"}],"ex":[{"text":"how much is it?","tr":"сколько это стоит?"},{"text":"what are these shoes?","tr":"сколько стоят эти ботинки?"},{"text":"this book is five shillings","tr":"эта книга стоит пять шиллингов"}],"sense":"2"},{"num":"4","tr":[{"text":"значить","syn":[{"text":"стоить"}]}],"ex":[{"text":"it is nothing to me","tr":"мне это ничего не стоит, для меня это ничего не составляет /не значит/"},{"text":"what is all that to me?","tr":"что мне всё это?, какое мне до этого дело?"}],"sense":"3"},{"num":"5","tr":[{"text":"<i data-abbr>возвыш.</i> сопутствовать (<i>в восклицательных предложениях как пожелание</i>)"}],"ex":[{"text":"success (be) to your efforts!","tr":"желаю успеха в ваших начинаниях!, да сопутствует вам удача!"},{"text":"victory be yours!","tr":"желаю (вам) победы!"}]}]},{"numR":"II Б","trn":[{"num":"1","tr":[{"text":"<i>there is </i>имеется, есть"}],"ex":[{"text":"there are many English books in our library","tr":"в нашей библиотеке (имеется) много английских книг"},{"text":"there is plenty of time","tr":"времени вполне достаточно, ещё есть масса времени"},{"text":"there are no roads","tr":"дорог нет"},{"text":"there will be dancing","tr":"будут танцы"},{"text":"there was once an old man ...","tr":"жил-был однажды старик ..."}]},{"num":"2","tr":[{"text":"<i>to have been </i>"}]},{"num":"2","tr":[{"text":"посещать","syn":[{"text":"бывать"}]}],"ex":[{"text":"has he been to London?","tr":"он бывал в Лондоне?"},{"text":"I've been there!","tr":"а) я там был!; б) <i data-abbr>разг.</i> это мне известно!"}],"sense":"1"},{"num":"2","tr":[{"text":"<i data-abbr>разг.</i> заходить, быть"}],"ex":[{"text":"has anyone been?","tr":"кто-нибудь заходил?, был кто-нибудь?"},{"text":"has the post [the milkman] been?","tr":"была ли почта [был ли /приходил/ молочник]?"}],"sense":"2"},{"num":"3","tr":[{"text":"<i>to be at smth. </i><i data-abbr>разг.</i> "}]},{"num":"3","tr":[{"text":"намереваться сделать <i>или</i> сказать что-л."}],"ex":[{"text":"I don't understand what exactly he is at","tr":"я не понимаю, что именно он хочет сказать"},{"text":"what would you be at?","tr":"каковы ваши намерения?"}],"sense":"1"},{"num":"3","tr":[{"text":"нападать","syn":[{"text":"набрасываться на что-л."}]}],"ex":[{"text":"the mice are at the cheese again","tr":"мыши опять добрались до сыра"}],"sense":"2"},{"num":"3","tr":[{"text":"брать без спроса"}],"ex":[{"text":"he's been at my shaving things again","tr":"он опять брал (без спроса) мои бритвенные принадлежности"}],"sense":"3"},{"num":"4","tr":[{"text":"<i>to be at smb. </i><i data-abbr>разг.</i> приставать к кому-л."}],"ex":[{"text":"she's always at me","tr":"она всегда меня пилит"}]},{"num":"5","tr":[{"text":"<i>to be above smth. /doing smth./ </i>быть выше чего-л.; не опускаться до чего-л."}],"ex":[{"text":"to be above suspicion","tr":"быть выше /вне/ подозрений"},{"text":"to be above criticism","tr":"быть выше всякой критики, быть безупречным"},{"text":"he is above reproach","tr":"его не за что упрекнуть"},{"text":"he is above such matters","tr":"он такими делами не занимается, он до такого (дела) не унизится"},{"text":"he is above taking bribes","tr":"брать взятки - ниже его достоинства"}]},{"num":"6","tr":[{"text":"<i>to be beneath smth., smb. </i>быть ниже чего-л., кого-л."}],"ex":[{"text":"to be beneath contempt [attention]","tr":"не заслуживать (даже) презрения [внимания]"},{"text":"it is beneath you /your dignity/","tr":"это ниже вашего достоинства"}]},{"num":"7","tr":[{"text":"<i>to be beyond smth., smb. </i>быть за пределами чего-л., возможностей кого-л."}],"ex":[{"text":"his behaviour is beyond my endurance","tr":"я не могу больше терпеть его поведение"},{"text":"he is not beyond redemption","tr":"он ещё может исправиться"},{"text":"this is beyond a joke","tr":"это уже не шутка"},{"text":"it was beyond expectation","tr":"такого нельзя было ожидать, на такое нельзя было надеяться"},{"text":"I am beyond caring","tr":"мне уже всё равно"},{"text":"what you say is beyond me","tr":"мне совершенно непонятно то, что ты говоришь"}]},{"num":"8","tr":[{"text":"<i>to be abreast of smth. </i>быть в курсе чего-л."}],"ex":[{"text":"he's abreast of developments in his field","tr":"он в курсе последних достижений в своей области"}]},{"num":"9","tr":[{"text":"<i>to be after smb. </i>преследовать, пытаться поймать кого-л."}],"ex":[{"text":"the police were after him","tr":"полиция преследовала его"}]},{"num":"10","tr":[{"text":"<i>to be after smth. </i>покушаться на что-л., стремиться завладеть чем-л."}],"ex":[{"text":"he's after my job","tr":"он метит на моё место"},{"text":"he's after her money","tr":"он охотится за её деньгами"}]},{"num":"11","tr":[{"text":"<i>to be about to do smth. </i>собираться, намереваться сделать что-л."}],"ex":[{"text":"he was about to send for you","tr":"он собирался послать за вами"},{"text":"she was about to speak, but changed her mind","tr":"она хотела было заговорить, но передумала"}]},{"num":"12","tr":[{"text":"<i>to be against smth. </i>противоречить чему-л., идти вразрез с чем-л."}],"ex":[{"text":"lying is against my principles","tr":"не в моих правилах врать"}]},{"num":"13","tr":[{"text":"<i>to be for smth. </i>стоять <i>или</i> быть за"}],"ex":[{"text":"who is for going home?","tr":"кто за то, чтобы идти домой?"}]},{"num":"14","tr":[{"text":"<i>to be for some place </i>отправляться, ехать куда-л."}],"ex":[{"text":"are you for Bristol?","tr":"вы едете в Бристоль?"}]},{"num":"15","tr":[{"text":"<i>to be on smb. </i>"}]},{"num":"15","tr":[{"text":"<i data-abbr>разг.</i> быть оплаченным кем-л."}],"ex":[{"text":"put your money away, it's on me","tr":"убери деньги, я угощаю"},{"text":"the drinks are on the house","tr":"хозяин (<i>бара, ресторана </i><i data-abbr>и т. п.</i>) угощает"},{"text":"the tickets are on me","tr":"я плачу за билеты"}],"sense":"1"},{"num":"15","tr":[{"text":"внезапно наступить","syn":[{"text":"подоспеть (<i>о праздниках, выборах </i><i data-abbr>и т. п.</i>)"}]}],"ex":[{"text":"the wet season was on us","tr":"неожиданно на нас обрушился сезон дождей"},{"text":"Christmas was on us","tr":"наступило рождество"}],"sense":"2"},{"num":"16","tr":[{"text":"<i>to be on smth. </i>входить в состав, быть членом (<i>комиссии </i><i data-abbr>и т. п.</i>)"}],"ex":[{"text":"he is on the board","tr":"он входит в состав правления"}]},{"num":"17","tr":[{"text":"<i>to be on smb., smth. </i>быть поставленным на кого-л., что-л."}],"ex":[{"text":"my money is on this horse","tr":"я поставил на эту лошадь"}]},{"num":"18","tr":[{"text":"<i>to be up to smth. </i>"}]},{"num":"18","tr":[{"text":"замышлять","syn":[{"text":"затевать что-л."}]}],"ex":[{"text":"the boys are up to smth.","tr":"мальчики что-то затевают"},{"text":"he is up to no good","tr":"он затевает что-то скверное, от него хорошего не жди"}],"sense":"1"},{"num":"18","tr":[{"text":"быть осведомлённым о чём-л."}],"ex":[{"text":"the police must be up to all the dodges","tr":"полиции должно быть известно обо всех уловках"}],"sense":"2"},{"num":"19","tr":[{"text":"<i>not to be up to </i>(<i>doing</i>)<i> smth. </i>не быть в состоянии сделать что-л., не справиться с чем-л."}],"ex":[{"text":"I am not up to going to the theatre tonight","tr":"я не в состоянии пойти сегодня вечером в театр"},{"text":"he is not up to his job","tr":"он не справляется со своей работой"},{"text":"he is not up to his father as a scholar","tr":"как учёный он значительно уступает (своему) отцу"}]},{"num":"20","tr":[{"text":"<i>to be up to smb. </i>быть возложенным на кого-л. (<i>об ответственности</i>); зависеть от кого-л."}],"ex":[{"text":"it is up to him to decide","tr":"от него зависит решение, он должен решить"},{"text":"it is up to you to choose","tr":"вы выбираете /решаете/"},{"text":"whether you learn or not is entirely up to you","tr":"учиться или нет - твоё дело"}]},{"num":"21","tr":[{"text":"<i>to be up against smth., smb. </i>столкнуться с чем-л., кем-л.; встретить отпор"}],"ex":[{"text":"he's up against some real opposition","tr":"он будет иметь дело с сильной оппозицией"},{"text":"he's up against it","tr":"<i data-abbr>разг.</i> он столкнулся с большими трудностями"}]},{"num":"22","tr":[{"text":"<i>to be up for smth. </i>"}]},{"num":"22","tr":[{"text":"быть поднятым","syn":[{"text":"возникать"},{"text":"рассматриваться (<i>о вопросе </i><i data-abbr>и т. п.</i>)"}]}],"ex":[{"text":"to be up for review","tr":"пересматриваться"},{"text":"to be up for debate","tr":"обсуждаться, быть поставленным на обсуждение"}],"sense":"1"},{"num":"22","tr":[{"text":"рассматривать в суде","syn":[{"text":"судить"}]}],"ex":[{"text":"he was up in court for this","tr":"его за это судили"}],"sense":"2"},{"num":"22","tr":[{"text":"предназначаться к продаже"}],"ex":[{"text":"to be up for auction","tr":"продаваться на аукционе /с молотка/"}],"sense":"3"},{"num":"22","tr":[{"text":"быть выдвинутым кандидатом","syn":[{"text":"быть претендентом (<i>на должность, пост </i><i data-abbr>и т. п.</i>)"}]}],"ex":[{"text":"he's up for admission to the society at the next meeting","tr":"его будут принимать в кружок на следующем собрании"}],"sense":"4"},{"num":"23","tr":[{"text":"<i>to be with smb. </i>"}]},{"num":"23","tr":[{"text":"поддерживать кого-л."}],"ex":[{"text":"we're with you all the way","tr":"мы пойдём с тобой до конца"},{"text":"she is at one with her husband","tr":"она заодно со (своим) мужем"}],"sense":"1"},{"num":"23","tr":[{"text":"понимать","syn":[{"text":"следить за тем"},{"text":"что говорят"}]}],"ex":[{"text":"are you still with me - or shall I go over it again?","tr":"ты следишь за ходом моей мысли или мне повторить ещё раз?"}],"sense":"2"},{"num":"24","tr":[{"text":"<i>to be with smb., smth. </i>работать у кого-л., где-л. (<i>по найму</i>)"}],"ex":[{"text":"I'm with a shipping firm","tr":"я работаю в транспортной фирме"}]}]},{"numR":"III А","trn":[{"num":"1","tr":[{"text":"<i>как глагол-связка </i>"}]},{"num":"1","tr":[{"text":"быть"}],"ex":[{"text":"he is a teacher","tr":"он учитель"},{"text":"are they English?","tr":"они англичане?"},{"text":"ten yards is a lot","tr":"десять ярдов - это очень много"},{"text":"his is a fine house","tr":"его дом чудесный, у него прекрасный дом"},{"text":"our task is to finish the work in time","tr":"наша задача - вовремя кончить работу"},{"text":"she has been a mother to me","tr":"она мне была вместо матери"},{"text":"she is twenty","tr":"ей двадцать лет"},{"text":"today is the tenth","tr":"сегодня десятое (число)"},{"text":"tomorrow is Friday","tr":"завтра пятница"},{"text":"the wall is six foot high","tr":"стена имеет шесть футов в высоту"},{"text":"what is it?","tr":"а) что это?; б) в чём дело?"},{"text":"to see things as they are","tr":"видеть вещи такими, какие они есть"},{"text":"if I were you ...","tr":"если бы я был на вашем месте ..."},{"text":"seeing is believing","tr":"увидеть - (это) значит убедиться /поверить/"}],"sense":"1"},{"num":"1","tr":[{"text":"находиться в (<i>каком-л.</i>) состоянии; чувствовать, ощущать (<i data-abbr>что-л.</i>)"}],"ex":[{"text":"I am cold [hot]","tr":"мне холодно [жарко]"},{"text":"he is asleep [alive, tired]","tr":"он спит [жив, устал]"},{"text":"he is glad [nervous, silent, happy]","tr":"он рад [нервничает, молчит, счастлив]"},{"text":"he is absent","tr":"он отсутствует"},{"text":"he is in trouble","tr":"он попал в беду, у него неприятности"},{"text":"he is at work [at play]","tr":"он работает [играет]"},{"text":"isn't he lucky?","tr":"везёт же ему!"}],"sense":"2"},{"num":"2","tr":[{"text":"<i>с последующим инфинитивом выражает </i>"}]},{"num":"2","tr":[{"text":"<i>долженствование, обусловленное договорённостью, планом</i>:"}],"ex":[{"text":"he is to come at six","tr":"он должен прийти в шесть (часов)"},{"text":"he was to come at six","tr":"он должен был прийти в шесть"},{"text":"he was to have come at six","tr":"он должен был прийти в шесть (<i>но не пришёл</i>)"},{"text":"when am I to come?","tr":"когда мне приходить?, когда мне нужно прийти?"},{"text":"the house is to let","tr":"дом сдаётся в аренду"},{"text":"he was never to see her again","tr":"ему больше никогда не суждено было её увидеть"},{"text":"it was not to be","tr":"этому не суждено было сбыться /осуществиться/"},{"text":"they are not to be trusted","tr":"им нельзя доверять"},{"text":"such men are to be pitied rather than despised","tr":"таких людей надо не презирать, а жалеть"}],"sense":"1"},{"num":"2","tr":[{"text":"<i>возможность</i>:"}],"ex":[{"text":"he was nowhere to be found","tr":"его нигде нельзя было найти /отыскать/"},{"text":"not a cloud was to be seen","tr":"не видно было ни облачка"},{"text":"how am I to get through all this work today?","tr":"как я смогу справиться со всей этой работой сегодня?"}],"sense":"2"},{"num":"2","tr":[{"text":"<i>намерение, желание </i>(<i>в условных предложениях</i>):"}],"ex":[{"text":"if we are to come in time, we must start at once","tr":"если мы хотим прийти вовремя, нам надо сразу отправляться"}],"sense":"3"},{"num":"3","tr":[{"text":"<i data-abbr>уст.</i> <i>в сочетании с </i><i data-abbr>p. p.</i><i> глаголов </i>to come, to fall, to sit, to run, to get<i> и </i><i data-abbr>др.</i>:"}],"ex":[{"text":"winter was come","tr":"зима наступила"},{"text":"the sun was risen","tr":"солнце встало"}]}]},{"numR":"III Б","trn":[{"num":"1","tr":[{"text":"<i>в сочетании с </i><i data-abbr>pres. p.</i><i> служит для образования длительной формы</i>:"}],"ex":[{"text":"he was talking to his son at the time","tr":"в тот момент он беседовал с сыном"},{"text":"he is working","tr":"он (сейчас) работает"},{"text":"this question is being discussed","tr":"этот вопрос сейчас обсуждается"}]},{"num":"2","tr":[{"text":"<i>в сочетании с </i><i data-abbr>p. p.</i><i> переходных и ряда непереходных глаголов служит для образования пассивной формы</i>:"}],"ex":[{"text":"this was made by my son","tr":"это было сделано моим сыном"},{"text":"they will be punished","tr":"они будут наказаны, их накажут"},{"text":"such questions are settled by the committee","tr":"такие вопросы решаются комитетом"},{"text":"he was asked to come","tr":"его попросили прийти"},{"text":"this book was much spoken of","tr":"об этой книге много говорили"},{"text":" <i data-abbr>♢</i> to be above one /one's head/","tr":"<i data-abbr>разг.</i> быть выше чьего-л. понимания"},{"text":"to be at it","tr":"шалить, проказничать"},{"text":"the children are at it again","tr":"дети опять принялись за своё"},{"text":"to be hard at it /at work/","tr":"<i data-abbr>разг.</i> а) быть очень занятым; б) напряжённо работать"},{"text":"they were hard at it /at work/ the whole night","tr":"они работали изо всех сил всю ночь напролёт"},{"text":"to be at one with smb.","tr":"быть с кем-л. заодно"},{"text":"to be beside oneself with grief [anxiety, alarm, <i data-abbr>etc</i>]","tr":"потерять голову от горя [волнения, беспокойства <i data-abbr>и т. п.</i>]"},{"text":"to be beside oneself with rage","tr":"выйти из себя, разгневаться"},{"text":"to be beside the point","tr":"не иметь отношения (<i>к данному вопросу, делу </i><i data-abbr>и т. п.</i>)"},{"text":"for the time being","tr":"пока"},{"text":"the manager for the time being","tr":"временно исполняющий обязанности заведующего"},{"text":"somebody will be in for it","tr":"кому-то попадёт /влетит, нагорит/"},{"text":"far be it from me to do this","tr":"я вовсе не собираюсь /я далёк от того, чтобы/ делать это"},{"text":"be (that) as it may","tr":"как бы то ни было; пусть будет что будет"},{"text":"let it be!","tr":"оставь это в покое!, пусть всё остаётся как есть!"},{"text":"so be it","tr":"да будет так, пусть так и будет"},{"text":"how are you?","tr":"а) как вы поживаете?; б) как вы себя чувствуете?"},{"text":"you never know where you are with him","tr":"никогда не знаешь, что он может сделать /как он поступит, как себя с ним вести, чего от него ждать/"},{"text":"be yourself!, be your age!","tr":"не глупи!, не валяй дурака!"},{"text":"you've been and gone and done it!","tr":"<i data-abbr>сл.</i> ну и наделали вы дел!, ну натворили же вы!"},{"text":"I'll be!","tr":"<i data-abbr>амер.</i> <i data-abbr>сл.</i> вот те на!, господи боже мой!, ну и ну! (<i>восклицание, выражающее удивление</i>)"}]}]}],"com":"<i> (</i><i data-abbr>ед.</i><i data-abbr>ч.</i><i> was, </i><i data-abbr>мн.</i><i data-abbr>ч.</i><i> were; been; </i><i data-abbr>наст.</i><i data-abbr>вр.</i><i> 1-е </i><i data-abbr>л.</i><i data-abbr>ед.</i><i data-abbr>ч.</i><i> am, 3-е </i><i data-abbr>л.</i><i data-abbr>ед.</i><i data-abbr>ч.</i><i> is, 2-е </i><i data-abbr>л.</i><i data-abbr>ед.</i><i data-abbr>ч.</i><i> и 1-е, 2-е, 3-е </i><i data-abbr>л.</i><i data-abbr>мн.</i><i data-abbr>ч.</i><i> are; </i><i data-abbr>уст.</i><i> 2-е </i><i data-abbr>л.</i><i data-abbr>ед.</i><i data-abbr>ч.</i><i data-abbr>наст.</i><i data-abbr>вр.</i><i> art)</i>","ts":"bi: (полная форма); bı (редуцированная форма)","area":"v"}]}'''
        test_word(self, before, after)
