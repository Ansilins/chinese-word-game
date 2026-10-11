# Writes src/hsk1-words.json and src/hsk2-words.json: [characters, pinyin, English, topic].
# Word lists: HSK 2.0 levels 1 and 2 from github.com/drkameleon/complete-hsk-vocabulary (MIT).
# Pinyin is the dictionary (citation) form; the game works out tone changes in speech itself.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
P, N, F, T, W, H, S, Sc, Wt, B, Ho, Sh, Q, D, V, L = ("Phrases", "Numbers & Measure Words", "People & Family", "Food & Drink",
  "Time & Dates", "Home & Things", "Places & Travel", "School & Work", "Weather & Animals", "Body & Health", "Hobbies & Sport",
  "Shopping & Money", "Question Words", "Describing Words", "Verbs", "Little Words")
WH = "Where Things Are"
HSK1 = [
 ("爱","ài","to love",V),("八","bā","eight",N),("爸爸","bàba","dad",F),("杯子","bēizi","cup, glass",H),("北京","Běijīng","Beijing",S),
 ("本","běn","(measure word for books)",N),("不","bù","not, no",L),("不客气","bù kèqi","you're welcome",P),("菜","cài","dish, vegetables",T),
 ("茶","chá","tea",T),("吃","chī","to eat",V),("出租车","chūzūchē","taxi",S),("打电话","dǎ diànhuà","to make a phone call",V),
 ("大","dà","big",D),("的","de","(possessive particle, like 's)",L),("点","diǎn","o'clock",W),("电脑","diànnǎo","computer",H),
 ("电视","diànshì","TV",H),("电影","diànyǐng","film, movie",Ho),("东西","dōngxi","thing, stuff",H),("都","dōu","all, both",L),
 ("读","dú","to read (aloud)",V),("对不起","duìbuqǐ","sorry",P),("多","duō","many, much",D),("多少","duōshao","how many, how much",Q),
 ("儿子","érzi","son",F),("二","èr","two",N),("饭馆","fànguǎn","restaurant",S),("飞机","fēijī","plane",S),("分钟","fēnzhōng","minute",W),
 ("高兴","gāoxìng","happy, glad",D),("个","gè","(general measure word)",N),("工作","gōngzuò","to work, job",Sc),("狗","gǒu","dog",Wt),
 ("汉语","Hànyǔ","Chinese (language)",Sc),("好","hǎo","good",D),("喝","hē","to drink",V),("和","hé","and, with",L),("很","hěn","very",L),
 ("后面","hòumiàn","behind, at the back",WH),("回","huí","to go back, return",V),("会","huì","can (know how to)",V),
 ("火车站","huǒchēzhàn","train station",S),("几","jǐ","how many (small numbers)",Q),("家","jiā","home, family",F),
 ("叫","jiào","to be called, to call",V),("今天","jīntiān","today",W),("九","jiǔ","nine",N),("开","kāi","to open, to drive",V),
 ("看","kàn","to look, watch, read",V),("看见","kànjiàn","to see",V),("块","kuài","(measure word for money: yuan)",Sh),("来","lái","to come",V),
 ("老师","lǎoshī","teacher",Sc),("了","le","(particle: done, or a change)",L),("冷","lěng","cold",Wt),("里","lǐ","inside, in",WH),
 ("零","líng","zero",N),("六","liù","six",N),("妈妈","māma","mom",F),("吗","ma","(question particle)",L),("买","mǎi","to buy",Sh),
 ("猫","māo","cat",Wt),("没","méi","not (have), didn't",L),("没关系","méi guānxi","it doesn't matter",P),("米饭","mǐfàn","cooked rice",T),
 ("名字","míngzi","name",F),("明天","míngtiān","tomorrow",W),("哪","nǎ","which",Q),("那","nà","that",L),("呢","ne","(particle: and you? what about…?)",L),
 ("能","néng","can, be able to",V),("你","nǐ","you",L),("年","nián","year",W),("女儿","nǚ'ér","daughter",F),("朋友","péngyou","friend",F),
 ("漂亮","piàoliang","pretty",D),("苹果","píngguǒ","apple",T),("七","qī","seven",N),("前面","qiánmiàn","in front, ahead",WH),
 ("钱","qián","money",Sh),("请","qǐng","please; to invite",P),("去","qù","to go",V),("热","rè","hot",Wt),("人","rén","person, people",F),
 ("认识","rènshi","to know (a person), to meet",V),("日","rì","day, date",W),("三","sān","three",N),("商店","shāngdiàn","shop, store",Sh),
 ("上","shàng","on, above, up",WH),("上午","shàngwǔ","morning (before noon)",W),("少","shǎo","few, little",D),("什么","shénme","what",Q),
 ("十","shí","ten",N),("时候","shíhou","time, when",W),("是","shì","to be (is, am, are)",V),("书","shū","book",Sc),("谁","shéi","who",Q),
 ("水","shuǐ","water",T),("水果","shuǐguǒ","fruit",T),("睡觉","shuìjiào","to sleep",V),("说话","shuōhuà","to speak, talk",V),("四","sì","four",N),
 ("岁","suì","years old",N),("他","tā","he, him",L),("她","tā","she, her",L),("太","tài","too (much), very",L),("天气","tiānqì","weather",Wt),
 ("听","tīng","to listen",V),("同学","tóngxué","classmate",Sc),("喂","wéi","hello (on the phone)",P),("我","wǒ","I, me",L),
 ("我们","wǒmen","we, us",L),("五","wǔ","five",N),("喜欢","xǐhuan","to like",V),("下","xià","under, below, down",WH),
 ("下午","xiàwǔ","afternoon",W),("下雨","xià yǔ","to rain",Wt),("先生","xiānsheng","Mr., sir; husband",F),("现在","xiànzài","now",W),
 ("想","xiǎng","to want to, to think, to miss",V),("小","xiǎo","small, little",D),("小姐","xiǎojiě","Miss, young lady",F),
 ("些","xiē","some",N),("写","xiě","to write",V),("谢谢","xièxie","thank you",P),("星期","xīngqī","week",W),("学生","xuésheng","student",Sc),
 ("学习","xuéxí","to study, learn",Sc),("学校","xuéxiào","school",Sc),("一","yī","one",N),("衣服","yīfu","clothes",H),("医生","yīshēng","doctor",B),
 ("医院","yīyuàn","hospital",B),("椅子","yǐzi","chair",H),("有","yǒu","to have, there is",V),("月","yuè","month, moon",W),
 ("再见","zàijiàn","goodbye",P),("在","zài","at, in; to be (somewhere)",L),("怎么","zěnme","how",Q),("怎么样","zěnmeyàng","how is it? how about…?",Q),
 ("这","zhè","this",L),("中国","Zhōngguó","China",S),("中午","zhōngwǔ","noon",W),("住","zhù","to live (somewhere)",V),
 ("桌子","zhuōzi","table, desk",H),("字","zì","character, word",Sc),("昨天","zuótiān","yesterday",W),("坐","zuò","to sit; to take (a bus)",V),
 ("做","zuò","to do, to make",V),
]
HSK2 = [
 ("吧","ba","(particle: let's…, I suppose)",L),("白","bái","white",D),("百","bǎi","hundred",N),("帮助","bāngzhù","to help",V),
 ("报纸","bàozhǐ","newspaper",H),("比","bǐ","than, compared to",L),("便宜","piányi","cheap",Sh),("别","bié","don't",L),
 ("唱歌","chàng gē","to sing",Ho),("出","chū","to go out, come out",V),("穿","chuān","to wear, put on",V),("船","chuán","boat, ship",S),
 ("次","cì","time(s) (how often)",N),("从","cóng","from",L),("错","cuò","wrong",D),("打篮球","dǎ lánqiú","to play basketball",Ho),
 ("大家","dàjiā","everyone",F),("但是","dànshì","but",L),("到","dào","to arrive; to, until",V),("得","de","(particle: how well something is done)",L),
 ("弟弟","dìdi","younger brother",F),("第一","dìyī","first",N),("懂","dǒng","to understand",V),("房间","fángjiān","room",H),
 ("非常","fēicháng","very, extremely",L),("服务员","fúwùyuán","waiter, attendant",Sc),("高","gāo","tall, high",D),("告诉","gàosu","to tell",V),
 ("哥哥","gēge","older brother",F),("给","gěi","to give; for",V),("公共汽车","gōnggòng qìchē","bus",S),("公斤","gōngjīn","kilogram",N),
 ("公司","gōngsī","company",Sc),("贵","guì","expensive",Sh),("还","hái","still, also",L),("孩子","háizi","child",F),("好吃","hǎochī","tasty",T),
 ("号","hào","number; day of the month",W),("黑","hēi","black, dark",D),("红","hóng","red",D),("欢迎","huānyíng","welcome",P),
 ("回答","huídá","to answer",V),("机场","jīchǎng","airport",S),("鸡蛋","jīdàn","egg",T),("件","jiàn","(measure word for clothes, matters)",N),
 ("教室","jiàoshì","classroom",Sc),("介绍","jièshào","to introduce",V),("姐姐","jiějie","older sister",F),("近","jìn","near, close",WH),
 ("进","jìn","to enter, come in",V),("就","jiù","just, right away; then",L),("觉得","juéde","to think, to feel",V),("咖啡","kāfēi","coffee",T),
 ("开始","kāishǐ","to begin",V),("考试","kǎoshì","exam",Sc),("可能","kěnéng","maybe, possible",L),("可以","kěyǐ","can, may",V),
 ("课","kè","class, lesson",Sc),("快","kuài","fast; soon",D),("快乐","kuàilè","happy",D),("累","lèi","tired",B),
 ("离","lí","away from (distance)",WH),("两","liǎng","two (before a measure word)",N),("路","lù","road, way",S),("旅游","lǚyóu","to travel, tour",S),
 ("卖","mài","to sell",Sh),("慢","màn","slow",D),("忙","máng","busy",D),("每","měi","every, each",L),("妹妹","mèimei","younger sister",F),
 ("门","mén","door",H),("男人","nánrén","man",F),("您","nín","you (polite)",L),("牛奶","niúnǎi","milk",T),("女人","nǚrén","woman",F),
 ("旁边","pángbiān","beside, next to",WH),("跑步","pǎobù","to run, jog",Ho),("票","piào","ticket",S),("妻子","qīzi","wife",F),
 ("起床","qǐchuáng","to get up",V),("千","qiān","thousand",N),("晴","qíng","sunny, clear",Wt),("去年","qùnián","last year",W),
 ("让","ràng","to let, to make (someone do)",V),("上班","shàngbān","to go to work",Sc),("身体","shēntǐ","body, health",B),
 ("生病","shēngbìng","to get sick",B),("生日","shēngrì","birthday",W),("时间","shíjiān","time",W),("事情","shìqing","thing, matter",H),
 ("手表","shǒubiǎo","wristwatch",H),("手机","shǒujī","mobile phone",H),("送","sòng","to give (a gift), to see off",V),("所以","suǒyǐ","so, therefore",L),
 ("它","tā","it",L),("踢","tī","to kick",Ho),("题","tí","question (on a test)",Sc),("跳舞","tiàowǔ","to dance",Ho),("外","wài","outside",WH),
 ("完","wán","to finish",V),("玩","wán","to play, have fun",Ho),("晚上","wǎnshang","evening",W),("为","wèi","for",L),("问","wèn","to ask",V),
 ("问题","wèntí","question, problem",Sc),("希望","xīwàng","to hope",V),("洗","xǐ","to wash",V),("西瓜","xīguā","watermelon",T),
 ("向","xiàng","towards",WH),("小时","xiǎoshí","hour",W),("笑","xiào","to laugh, smile",V),("新","xīn","new",D),("姓","xìng","surname; to be called (surname)",F),
 ("休息","xiūxi","to rest",V),("雪","xuě","snow",Wt),("颜色","yánsè","colour",D),("眼睛","yǎnjing","eye",B),("羊肉","yángròu","lamb, mutton",T),
 ("药","yào","medicine",B),("要","yào","to want; will",V),("也","yě","also, too",L),("一起","yīqǐ","together",L),("已经","yǐjīng","already",L),
 ("意思","yìsi","meaning",Sc),("因为","yīnwèi","because",L),("阴","yīn","cloudy, overcast",Wt),("游泳","yóuyǒng","to swim",Ho),
 ("右边","yòubian","right side",WH),("鱼","yú","fish",T),("元","yuán","yuan (unit of money)",Sh),("远","yuǎn","far",WH),
 ("运动","yùndòng","sport, exercise",Ho),("再","zài","again",L),("早上","zǎoshang","early morning",W),("张","zhāng","(measure word for flat things)",N),
 ("长","cháng","long",D),("丈夫","zhàngfu","husband",F),("找","zhǎo","to look for",V),("着","zhe","(particle: ongoing state, -ing)",L),
 ("真","zhēn","really, truly",L),("正在","zhèngzài","in the middle of (doing)",L),("知道","zhīdào","to know (a fact)",V),
 ("准备","zhǔnbèi","to prepare, get ready",V),("自行车","zìxíngchē","bicycle",S),("走","zǒu","to walk, to leave",V),("最","zuì","most",L),
 ("左边","zuǒbian","left side",WH),
]
for name, rows in (("hsk1-words.json", HSK1), ("hsk2-words.json", HSK2)):
    seen = set()
    for r in rows:
        assert len(r) == 4 and r[0] not in seen, r
        seen.add(r[0])
    with open(os.path.join(HERE, name), "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(list(r), ensure_ascii=False) for r in rows) + "\n]\n")
    print(name, len(rows))
