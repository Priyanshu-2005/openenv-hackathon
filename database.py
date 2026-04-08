MOCK_INTERNET = {
    "task_easy": [
        {
            "claim": "The Great Wall of China is visible from the Moon with the naked eye.",
            "search_results": {
                "great wall china visible moon": (
                    "[1] https://nasa.gov/ask-astronaut/great-wall "
                    "[2] https://myths-debunked.org/great-wall-moon"
                ),
                "can you see great wall from space": (
                    "[1] https://nasa.gov/ask-astronaut/great-wall"
                ),
            },
            "articles": {
                "https://nasa.gov/ask-astronaut/great-wall": (
                    "NASA astronauts have confirmed multiple times that the Great Wall of China "
                    "is NOT visible from the Moon. The wall is only about 15 feet wide, which "
                    "is far too narrow to be resolved by the human eye from orbital distance, "
                    "let alone from the Moon (238,900 miles away)."
                ),
                "https://myths-debunked.org/great-wall-moon": (
                    "DEBUNKED: The claim that the Great Wall is visible from the Moon has been "
                    "repeatedly denied by every astronaut who has visited the Moon. The wall is simply too thin."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "Humans only use 10% of their brains.",
            "search_results": {
                "humans use 10 percent brain": (
                    "[1] https://neuroscience-journal.org/brain-usage-myth "
                    "[2] https://science-facts.net/ten-percent"
                ),
                "how much of brain do we use": (
                    "[1] https://neuroscience-journal.org/brain-usage-myth"
                ),
            },
            "articles": {
                "https://neuroscience-journal.org/brain-usage-myth": (
                    "The 10% myth is one of the most pervasive misconceptions in neuroscience. "
                    "Functional magnetic resonance imaging (fMRI) reveals that even while sleeping, "
                    "almost all parts of the brain show some level of baseline activity. Every part "
                    "of the brain has a known function."
                ),
                "https://science-facts.net/ten-percent": (
                    "It's a myth. Brain damage to almost any area causes severe, lasting effects, "
                    "which wouldn't be the case if we only used 10%. Evolutionarily, an organ that "
                    "consumes 20% of our energy wouldn't be 90% useless."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "Goldfish have a three-second memory span.",
            "search_results": {
                "goldfish 3 second memory": (
                    "[1] https://marinebiology.edu/goldfish-cognition "
                    "[2] https://pet-myths.org/goldfish-memory"
                ),
                "how long is goldfish memory": (
                    "[1] https://marinebiology.edu/goldfish-cognition"
                ),
            },
            "articles": {
                "https://marinebiology.edu/goldfish-cognition": (
                    "Research at various universities has repeatedly demonstrated that goldfish "
                    "and other fish can remember information for up to five months. They can be "
                    "trained to push levers for food and can distinguish between different shapes, "
                    "colors, and sounds."
                ),
                "https://pet-myths.org/goldfish-memory": (
                    "The idea that goldfish have a three-second memory is completely unsubstantiated. "
                    "They are actually quite intelligent for their size and have associative memory "
                    "lasting months."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "Swallowing chewing gum takes seven years to digest.",
            "search_results": {
                "swallowing gum 7 years digest": (
                    "[1] https://gastroenterology-news.org/gum-digestion "
                    "[2] https://health-myths.com/swallowed-gum"
                ),
                "what happens if swallow gum": (
                    "[1] https://gastroenterology-news.org/gum-digestion"
                ),
            },
            "articles": {
                "https://gastroenterology-news.org/gum-digestion": (
                    "While it is true that your stomach cannot completely digest the synthetic resins "
                    "in chewing gum, it does not remain in your system for seven years. It simply "
                    "moves intact through your digestive tract and is excreted in stool within a few "
                    "days, just like other indigestible matter."
                ),
                "https://health-myths.com/swallowed-gum": (
                    "The '7-year' rule is a myth often told by parents to stop kids from swallowing "
                    "gum. Medical professionals confirm it passes through the body normally."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "Cracking your knuckles causes arthritis.",
            "search_results": {
                "cracking knuckles causes arthritis": (
                    "[1] https://rheumatology-board.org/knuckle-cracking "
                    "[2] https://medical-myths.net/knuckles"
                ),
                "does cracking knuckles bad for you": (
                    "[1] https://rheumatology-board.org/knuckle-cracking"
                ),
            },
            "articles": {
                "https://rheumatology-board.org/knuckle-cracking": (
                    "Multiple peer-reviewed studies have compared habitual knuckle crackers with "
                    "non-crackers and found no difference in the prevalence of osteoarthritis. The "
                    "popping sound is simply gas bubbles bursting in the synovial fluid."
                ),
                "https://medical-myths.net/knuckles": (
                    "Dr. Donald Unger notoriously cracked the knuckles of his left hand only for "
                    "over 60 years, never cracking his right. He found no arthritis in either hand, "
                    "winning an Ig Nobel Prize for his self-experiment. Knuckle cracking is harmless."
                ),
            },
            "ground_truth": "false",
        },
    ],
    "task_medium": [
        {
            "claim": "Honey never spoils and 3,000-year-old honey found in Egyptian tombs was still edible.",
            "search_results": {
                "honey never spoils egyptian tombs": (
                    "[1] https://archaeology-journal.org/egyptian-honey-discovery "
                    "[2] https://food-myths.blog/honey-forever "
                    "[3] https://health-debunk.com/honey-lies"
                ),
                "ancient honey edible preservation": (
                    "[1] https://archaeology-journal.org/egyptian-honey-discovery "
                    "[2] https://food-myths.blog/honey-forever"
                ),
            },
            "articles": {
                "https://archaeology-journal.org/egyptian-honey-discovery": (
                    "PEER-REVIEWED PUBLICATION — Journal of Archaeological Science. "
                    "Archaeologists discovered sealed ceramic jars of honey dating to 1000 BCE. "
                    "Laboratory analysis confirmed the honey had undergone minimal chemical degradation. "
                    "Honey's low water activity and acidic pH create a potent antimicrobial environment. "
                    "Properly sealed honey resists spoilage indefinitely."
                ),
                "https://food-myths.blog/honey-forever": (
                    "STOP BELIEVING THIS NONSENSE! I'm a mom of three and I KNOW food. Honey "
                    "absolutely DOES spoil — I left a jar open in my kitchen and it grew mold "
                    "within 3 months!! The 'Egyptian tomb honey' story is just clickbait."
                ),
                "https://health-debunk.com/honey-lies": (
                    "FACT CHECK by HealthDebunk Staff: "
                    "The claim that honey 'never spoils' is MISLEADING. We tested store-bought "
                    "honey and found that when left UNSEALED, it ferments. "
                    "VERDICT: FALSE. (Note: We did not evaluate the specific sealed tomb honey claim)."
                ),
            },
            "ground_truth": "true",
        },
        {
            "claim": "Bananas are completely safe, but they are naturally highly radioactive due to potassium-40.",
            "search_results": {
                "bananas radioactive potassium 40": (
                    "[1] https://nuclear-science.org/banana-equivalent-dose "
                    "[2] https://clean-eating.blog/toxic-bananas-myth "
                    "[3] https://truth-in-food.net/banana-radiation-hoax"
                ),
                "are bananas naturally radioactive": (
                    "[1] https://nuclear-science.org/banana-equivalent-dose"
                ),
            },
            "articles": {
                "https://nuclear-science.org/banana-equivalent-dose": (
                    "Because bananas are rich in potassium, and a small fraction of naturally occurring "
                    "potassium is the radioactive isotope potassium-40 (K-40), bananas are technically "
                    "radioactive. This phenomenon is often used to explain radiation doses to the public "
                    "(the Banana Equivalent Dose). However, the dose is extremely small and completely safe."
                ),
                "https://clean-eating.blog/toxic-bananas-myth": (
                    "People are saying bananas are radioactive to scare you away from natural foods! "
                    "This is an absolute lie fabricated by the processed food industry. Bananas are pure "
                    "and natural, nothing radioactive about them. Don't fall for the fear-mongering!"
                ),
                "https://truth-in-food.net/banana-radiation-hoax": (
                    "FACT CHECK: We rate the claim that 'bananas are radioactive' as FALSE. "
                    "Radiation comes from nuclear plants and X-rays, not fruit. If bananas were radioactive, "
                    "they would glow in the dark. Stop spreading scientific disinformation."
                ),
            },
            "ground_truth": "true",
        },
        {
            "claim": "The average person unknowingly swallows about 8 spiders a year in their sleep.",
            "search_results": {
                "average person swallows 8 spiders year sleep": (
                    "[1] https://entomology-institute.org/spider-myths "
                    "[2] https://creepy-facts.blog/spiders-in-sleep "
                    "[3] https://sleep-science.org/bugs-while-sleeping"
                ),
                "swallowing spiders in your sleep true or false": (
                    "[1] https://entomology-institute.org/spider-myths"
                ),
            },
            "articles": {
                "https://entomology-institute.org/spider-myths": (
                    "This is an urban legend that was actually fabricated in a magazine article in 1993 "
                    "specifically to demonstrate how quickly false information spreads on the internet. "
                    "Spiders have no reason to approach a sleeping human, and our breathing/snoring "
                    "vibrations would scare them away."
                ),
                "https://creepy-facts.blog/spiders-in-sleep": (
                    "YES! It's true! Scientific studies have shown that spiders love warm, dark places, "
                    "and an open human mouth is perfect. The average person eats 8 spiders a year without "
                    "even waking up. Sweet dreams! 🕷️"
                ),
                "https://sleep-science.org/bugs-while-sleeping": (
                    "While it is theoretically possible to swallow a bug while sleeping, the '8 spiders' "
                    "statistic is completely fabricated. We consulted with numerous arachnologists who "
                    "confirmed that spiders avoid humans, seeing us as a threat, not a hiding spot."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "A day on the planet Venus is actually longer than its year.",
            "search_results": {
                "day on venus longer than year": (
                    "[1] https://nasa.gov/venus-facts "
                    "[2] https://astronomy-skeptics.com/venus-day-myth "
                    "[3] https://flat-earth-cosmos.org/venus-lies"
                ),
                "venus rotation orbit time compare": (
                    "[1] https://nasa.gov/venus-facts"
                ),
            },
            "articles": {
                "https://nasa.gov/venus-facts": (
                    "Venus has an extremely slow rotation on its axis. It takes Venus 243 Earth days to "
                    "complete one rotation (a Venusian day). However, it only takes 225 Earth days for "
                    "Venus to complete one orbit around the Sun (a Venusian year). Therefore, a day on "
                    "Venus is strictly longer than its year."
                ),
                "https://astronomy-skeptics.com/venus-day-myth": (
                    "This makes NO logical sense. By definition, a year is the time it takes to go around "
                    "the sun, and a day is the time of rotation. A day cannot mathematically be longer "
                    "than a year. NASA is playing with words and confusing people again. FALSE."
                ),
                "https://flat-earth-cosmos.org/venus-lies": (
                    "The mainstream science community claims Venus's day is longer than its year. "
                    "This is physically impossible in any functional solar system model. They are "
                    "just making up numbers to hide the fact they haven't actually measured it."
                ),
            },
            "ground_truth": "true",
        },
        {
            "claim": "Carrots can significantly improve your eyesight and help you see perfectly in the dark.",
            "search_results": {
                "carrots improve eyesight see dark": (
                    "[1] https://nutrition-myths.org/carrots-ww2 "
                    "[2] https://natural-healing-eyes.com/carrot-miracle "
                    "[3] https://optometry-board.org/vitamin-a-vision"
                ),
                "do carrots help you see at night": (
                    "[1] https://nutrition-myths.org/carrots-ww2"
                ),
            },
            "articles": {
                "https://nutrition-myths.org/carrots-ww2": (
                    "This myth originated as World War II propaganda. The British Royal Air Force "
                    "developed a secret radar technology to shoot down German bombers at night. To "
                    "keep the radar a secret, the UK government released press stories claiming their "
                    "pilots ate massive amounts of carrots to achieve exceptional night vision."
                ),
                "https://natural-healing-eyes.com/carrot-miracle": (
                    "Throw away your glasses! Big Pharma doesn't want you to know that eating 5 raw "
                    "carrots a day can permanently fix your vision and give you night vision capabilities "
                    "comparable to an owl. True story!"
                ),
                "https://optometry-board.org/vitamin-a-vision": (
                    "While carrots contain Vitamin A, which is essential for general eye health, eating "
                    "excessive amounts will not give you 'perfect' vision or superhuman night vision. "
                    "If you already have a balanced diet, more carrots won't improve your eyesight at all."
                ),
            },
            "ground_truth": "false",
        },
    ],
    "task_hard": [
        {
            "claim": "A 2024 Stanford study proved that remote workers are 47% less productive than office workers.",
            "search_results": {
                "stanford study remote workers productivity 47%": (
                    "[1] https://business-insider.fake/stanford-remote-work-study "
                    "[2] https://stanford.edu/research/remote-productivity-2024 "
                    "[3] https://stanford.edu/notices/corrections-2024"
                ),
                "remote work productivity study 2024": (
                    "[1] https://business-insider.fake/stanford-remote-work-study "
                    "[2] https://stanford.edu/research/remote-productivity-2024"
                ),
            },
            "articles": {
                "https://business-insider.fake/stanford-remote-work-study": (
                    "HEADLINE: Stanford Confirms Remote Work Kills Productivity — 47% Drop Found. "
                    "A new Stanford study by Professor Nicholas Bloom has definitively proven that remote "
                    "workers are 47% less productive. 'The data is unambiguous,' Bloom said."
                ),
                "https://stanford.edu/research/remote-productivity-2024": (
                    "Bloom, N. 'The Impact of Hybrid Work'. Quarterly Journal of Economics. "
                    "ABSTRACT: We report results from a randomized controlled trial (n=1,612). Employees "
                    "assigned to work from home exhibited no statistically significant change in performance "
                    "review scores or promotion rates. The primary finding is a null result on productivity."
                ),
                "https://stanford.edu/notices/corrections-2024": (
                    "ERROR 404 — The requested resource is no longer available. "
                    "The Stanford Research Communications archive underwent a server migration. "
                    "[System WebCache Snapshot Recovered: '...press office regrets the premature publication of unverified productivity metrics. "
                    "We clarify that Professor Bloom did NOT report a 47% drop in remote productivity; this figure was erroneously extrapolated "
                    "by a third-party business blog and does not represent the study's null findings.']"
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "A massive 2023 MIT study found that moving to a 4-day workweek decreases employee turnover by 30%.",
            "search_results": {
                "mit study 4 day workweek turnover 30%": (
                    "[1] https://corporate-news.net/4-day-workweek-fails "
                    "[2] https://mit.edu/sloan/research/4-day-week-impact "
                    "[3] https://mit.edu/sloan/errata"
                ),
                "4 day workweek employee retention study MIT": (
                    "[1] https://mit.edu/sloan/research/4-day-week-impact"
                ),
            },
            "articles": {
                "https://corporate-news.net/4-day-workweek-fails": (
                    "The dream is dead. MIT researchers have found that the 4-day workweek is a disaster "
                    "for companies. According to the 2023 global study, companies adopting the model saw "
                    "employee turnover skyrocket by 30% as staff struggled to fit 40 hours of work into 32 hours."
                ),
                "https://mit.edu/sloan/research/4-day-week-impact": (
                    "Sloan Management Review: 'Global Trials of the 32-Hour Workweek'. "
                    "ABSTRACT: In the largest trial of its kind, 61 companies moved to a 4-day, 32-hour "
                    "workweek with no reduction in pay. Results after 12 months showed revenue remained "
                    "stable or improved. Crucially, self-reported burnout dropped significantly, and "
                    "companies experienced a 30% DECREASE in employee turnover compared to the prior year."
                ),
                "https://mit.edu/sloan/errata": (
                    "Please note that several third-party media outlets have entirely reversed the findings "
                    "of our 2023 turnover study. We found a 30% reduction, not an increase."
                ),
            },
            "ground_truth": "true",
        },
        {
            "claim": "Research from the University of Oxford confirms that consuming a bar of dark chocolate daily stimulates weight loss.",
            "search_results": {
                "oxford research dark chocolate daily weight loss": (
                    "[1] https://health-magazine.fake/chocolate-diet "
                    "[2] https://oxford.ac.uk/research/dietary-studies/chocolate-trial "
                    "[3] https://nature.com/articles/diet-science-journalism-flaws"
                ),
                "can eating chocolate help you lose weight": (
                    "[1] https://health-magazine.fake/chocolate-diet"
                ),
            },
            "articles": {
                "https://health-magazine.fake/chocolate-diet": (
                    "Guilt-free indulgence! A groundbreaking study out of Oxford University proves that "
                    "dieters who eat one 100g bar of dark chocolate every day actually lose weight 10% "
                    "faster than those who abstain. The epicatechins in cocoa apparently turbo-charge metabolism!"
                ),
                "https://oxford.ac.uk/research/dietary-studies/chocolate-trial": (
                    "Journal of Nutritional Science (2015). 'The effects of daily cocoa supplementation.' "
                    "We conducted a 3-week study with 15 participants. The chocolate group lost weight slightly "
                    "faster (p=0.04). However, note that with only 15 people and evaluating 18 different "
                    "health metrics, this is a statistically meaningless, p-hacked result intentionally designed "
                    "to demonstrate how bad dietary science can produce 'significant' but false findings."
                ),
                "https://nature.com/articles/diet-science-journalism-flaws": (
                    "Commentary: The 'chocolate diet' hoax. Researchers intentionally ran a garbage study "
                    "with too few participants just to see if major media outlets would publish it without "
                    "reading the methodology. They did. The claim that chocolate causes weight loss is a "
                    "deliberate scientific prank."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "A major Harvard nutritional meta-analysis concluded that moderate red wine consumption actively prevents heart attacks.",
            "search_results": {
                "harvard study red wine prevents heart attacks": (
                    "[1] https://wine-lovers.blog/harvard-heart-health "
                    "[2] https://hsph.harvard.edu/nutritionsource/alcohol-cardiovascular "
                    "[3] https://who.int/news-room/statements/alcohol"
                ),
                "red wine health benefits cardiovascular": (
                    "[1] https://hsph.harvard.edu/nutritionsource/alcohol-cardiovascular"
                ),
            },
            "articles": {
                "https://wine-lovers.blog/harvard-heart-health": (
                    "Drink up! Harvard scientists have published a massive meta-analysis proving that "
                    "drinking 1-2 glasses of red wine a night actively prevents myocardial infarctions "
                    "(heart attacks). The antioxidants clear out your arteries!"
                ),
                "https://hsph.harvard.edu/nutritionsource/alcohol-cardiovascular": (
                    "While some observational studies in the 1990s showed a correlation between moderate "
                    "wine consumption and lower heart disease rates, recent massive genomic studies have "
                    "overturned this. The apparent benefit was because 'moderate drinkers' generally "
                    "had higher socioeconomic status and exercised more. Alcohol, including wine, does "
                    "not 'prevent' heart attacks, and any cardiovascular benefit is vastly outweighed "
                    "by cancer risks."
                ),
                "https://who.int/news-room/statements/alcohol": (
                    "World Health Organization Statement (2023): There is NO safe level of alcohol consumption "
                    "that improves health. The concept that moderate drinking offers protection against "
                    "cardiovascular disease is not supported by current scientific consensus."
                ),
            },
            "ground_truth": "false",
        },
        {
            "claim": "A 2022 Nature study confirms that while the global polar bear population has doubled since 1950, sea ice loss is now causing rapid declines in crucial sub-populations.",
            "search_results": {
                "polar bear population doubled since 1950 climate study": (
                    "[1] https://climate-skeptic.net/polar-bears-thriving "
                    "[2] https://nature.com/articles/polar-bear-demographics-2022 "
                    "[3] https://polarbearsinternational.org/research-fact-check"
                ),
                "are polar bears actually endangered population data": (
                    "[1] https://nature.com/articles/polar-bear-demographics-2022"
                ),
            },
            "articles": {
                "https://climate-skeptic.net/polar-bears-thriving": (
                    "The climate alarmists are wrong again. A peer-reviewed 2022 study in Nature proves "
                    "that polar bears aren't starving — their global population has actually doubled "
                    "from 12,000 in 1950 to over 26,000 today! Global warming isn't hurting them at all."
                ),
                "https://nature.com/articles/polar-bear-demographics-2022": (
                    "ABSTRACT: We review multi-decadal population data. It is true that estimated global "
                    "numbers rose from ~12,000 in the 1950s to ~26,000 today. However, this increase is "
                    "entirely attributed to the 1973 international ban on unregulated commercial hunting. "
                    "Current data shows that sea ice loss is now causing rapid declines in several crucial sub-populations."
                ),
                "https://polarbearsinternational.org/research-fact-check": (
                    "FACT CHECK: Comparing current numbers to 1950s numbers is wildly misleading. The "
                    "species was nearly hunted to extinction before the 1973 treaty. While they recovered "
                    "from hunting, climate change remains an existential threat as their ice habitat disappears."
                ),
            },
            "ground_truth": "true",
        },
    ],
}
