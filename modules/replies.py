class Replies:

    greetings = []
    do_you_know = []
    csgo = []
    anti_swear = []
    flowers = []

    def __init__(self):
        self.greetings = ["Marhaba","Grüß Gott","Namaskar","Zdraveite","Hola","Hafa adai","Nǐ hǎo","Dobar dan","God dag","Hallo","Hoi","hyvää päivää","Bonjour","Dia dhuit","Guten tag","Yasou","Shalom","Namaste","Jo napot","Góðan dag","Nde-ewo","Selamat siang","Salve","Konnichiwa","Ahn nyong ha se yo","Salve","Sveiki","Moïen","Bonġu","Niltze","Namastē","Hallo","Salam","Cześć","Olá","Bună ziua","Zdravstvuyte","Zdravo","Ahoj","Hola","Hujambo","Hallå","Ia orna","Sawasdee","Avuxeni","Merhaba","Zdravstvuyte","Assalamo aleikum","xin chào","Shwmae","Sawubona","¿Qué tal","hello","hi","hey","whatsup","sup","yo","yoyo","yoyoyo","nihao","ni hao","Hi auntie",
        ]
        self.do_you_know = [
            "開始一件事，可能是沖動。堅持一件事，絕對是本事。_~",
            "如果你沒有梅花的清香，牡丹的華貴，不如就做一朵太陽花：溫暖向陽，努力生長，不卑不亢，我就是我，做最真的自己，_！",
            "生活就像一杯白開水，你每天都在喝，不要羨慕別人喝的飲料有各種顏色，其實未必有你的白開水解渴，人生不是靠心情活著，而要靠心態去生活。調整心態看生活，處處都是陽光！_！",
            "成長是分兩半的：一半在上帝手中，那是宿命；另一半在自己手中，那是拼命。_！",
            "早上起來你有兩個選擇，蓋上被子做你未完成的夢，掀開被子完成你未完成的夢。_！",
            "沒有人可以回到過去重新開始，但誰都可以從今天開始，書寫一個全然不同的結局。願你的今天充滿希望和幸福，_！",
            "再長的路，一步一步也能走完；再短的路，不邁開雙腳也無法到達。快去為自己的夢想努力吧！_！",
            "生活總有一些事，需要自己去體會，才能懂得；總有一些人，需要時間看清，才會理解；無所謂聚散，無所謂得失，不奢求太多，不刻意追尋，自己的路自己走，自己的心自己懂，無人可代替。_！",
            "只要心是晴朗的，人生就沒有雨天。給自己一份好心情，讓世界對著你微笑：給別人一份好心情，讓生活對我們微笑。_！",
            "上帝是公平的，若你還不夠幸福，只是你做的還不夠。_！",
            "你知道嗎？在非洲，每六十秒，就有一分鐘過去。_！",
            "你知道嗎？凡是每天喝水的人，有高機率在100年內死去。_！",
            "你知道嗎？當你吃下吃下廿碗白飯，換算竟相當於吃下了二十碗白飯的熱量。_！",
            "你知道嗎？台灣人在睡覺時，大多數的美國人都在工作。_。",
            "你知道嗎？當蝴蝶在南半球拍了兩下翅膀，牠就會稍微飛高一點點。_！",
            "你知道嗎？據統計，未婚生子的人數中有高機率為女性。_。",
            "你知道嗎？只要每天省下買一杯奶茶的錢，十天後就能買十杯奶茶。_！",
            "你知道嗎？當你的左臉被人打，那你的左臉就會痛。_。",
            "有煩惱時，就泡一杯黑咖啡！就像把所有的煩惱都溶進了咖啡一樣！喝一口！恩～所有煩惱都回來了！。_！",
            "你知道嗎？踏入虎年，首名出生的，是一名嬰兒。_！",
            "不再斥責，昨日的遺憾，不再苛求，虛無地攀比，不再剋制，本能的喜歡，不再丟棄，最初的純粹！_！",
            "與其，焦慮地活，不如，自由地笑，從今天起，更愛惜自己，仁慈的，温柔的，與困境中的自己，慢慢地化敵為友，讓內心秩序井然，讓關係柔和温暖，不為難，不怠慢，以簡單應對複雜，讓花盛開，讓該來的來！_！",
            "開始一件事，可能是衝動；堅持一件事，絕對是本事！選擇比努力更重要，當你足夠努力的時候，你才擁有選擇的權利或更多更好的選擇！_！",
            "讓你猶豫不決的一切註定就不是你的！不論人還是事。左右搖擺，説明你心不定。進退兩難，證明你降不住。真正適合你的，一定會讓你內心篤定。有些東西真的要看緣分，而緣分其實是一份心安。_！",
            "生活總用兩種方式考驗一個人，要麼什麼事也不發生，要麼什麼事都一起發生。加油！_！"
        ]
        self.csgo = [
            "仲打呢垃圾game?",
            "想跌rank?",
            "no",
            "on9 game",
            "https://tenor.com/view/rage-ragequit-punchcomputer-agar-agario-gif-23509069",
            "https://tenor.com/view/csgo-dance-gif-22778488",
            "https://tenor.com/view/skilled-cs-go-dance-shoot-grooves-gif-17023908",
            "https://tenor.com/view/s1mple-major-csgo-stockholm-pgl-gif-23720618",
            "https://tenor.com/view/csgo-eagle-gun-ranks-stars-gif-17028894",
            "https://tenor.com/view/csgo-dog-bee-dog-goober-gif-23167707",
            "https://tenor.com/view/twistzz-russ-team-liquid-team-liquid-csgo-csgo-liquid-gif-16748754",
            "https://tenor.com/view/dance-joy-cs-csgo-moves-gif-16638170"
        ]
        self.anti_swear = [
            "打冷震",
            "https://tenor.com/view/freeze-shock-stun-surprised-stiff-gif-12214058",
            "https://tenor.com/view/cursing-no-easeup-calm-down-gif-14438497",
            "https://tenor.com/view/captain-america-marvel-avengers-gif-14328153",
            "https://tenor.com/view/your-language-is-offensive-watch-your-mouth-zach-galifianakis-gif-13885320",
            "https://tenor.com/view/you-cant-talk-to-me-like-that-marjorine-butters-stotch-south-park-s9e9-gif-22282852"
        ]
        self.flowers = [
            "https://tenor.com/view/lotus-flower-blossom-gif-14518322",
            "https://tenor.com/view/lotus-in-rain-rain-lotus-pink-lotus-awsome-lotus-gif-22367055",
            "https://tenor.com/view/blossoming-lotus-flower-flow-gif-14722639",
            "https://tenor.com/view/zen-lotus-lotus-position-calm-clarity-gif-5383607",
            "https://tenor.com/view/lotus-sun-shine-lotus-sun-pink-lotus-water-with-sunray-gif-22380274",
            "https://tenor.com/view/flowers-pond-lily-gif-11634264"
        ]
