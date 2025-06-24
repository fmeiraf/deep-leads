from src.types import EvalParams, Lead, LeadResults, ResearchParams

EDMONTON_HUMAN_NUTRITION_RESEARCH_UNIT__VERY_NARROW_SCOPE = EvalParams(
    query_params=ResearchParams(
        who_query="professors",
        what_query="Human Nutrition",
        where_query="Human Nutrition Research Unit at University of Alberta",
        context_query="professors and researchers who are leading a lab or a team of researchers",
    ),
    expected_results=LeadResults(
        leads=[
            Lead(
                name="Carla Prado",
                email="carla.prado@ualberta.ca",
                phone="780-492-7934",
                website="https://www.drcarlaprado.com/",
                background_summary="Distinguished University Professor, Canada Research Chair in Integrative Nutrition, Body Composition, and Energy Metabolism (Tier 1), Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
            ),
            Lead(
                name="Diana Mager",
                email="mager@ualberta.ca",
                phone="780-492-7687",
                website="https://apps.ualberta.ca/directory/person/mager",
                background_summary="Ms. Diana Mager is currently appointed as Adjunct Professor in the Department of Pediatrics in the Faculty of Medicine & Dentistry.",
            ),
        ]
    ),
)

EDMONTON_ALES_RESEARCHERS__MID_BROAD_SCOPE = EvalParams(
    query_params=ResearchParams(
        who_query="professors",
        what_query="all fields",
        where_query="Department of Agricultural, Food & Nutritional Science at University of Alberta",
        context_query="professors and researchers who are leading a lab or a team of researchers",
    ),
    expected_results=LeadResults(
        leads=[
            Lead(
                name="David Bressler",
                email="dbressle@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-4986",
                website="http://bresslerlab.ualberta.ca/",
                background_summary="Research interests are accessible through his Google Scholar profile.",
            ),
            Lead(
                name="Erick R. da Silva Santos",
                email="ericksantos@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone=None,
                website="https://www.ualberta.ca/",
                background_summary="""PhD in Agronomy from the University of Florida, USA (2021). MSc in Agronomy from the 
University of Florida, USA (2017). BSc in Animal Science from the Federal Rural University of Pernambuco, Brazil 
(2015). Area of Study: Forages and Grasslands.""",
            ),
            Lead(
                name="Thava Vasanthan",
                email="tv3@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-2898",
                website="https://www.ualberta.ca/",
                background_summary="""Ph.D in Food Science, 1989-1994, Memorial University of Newfoundland, Canada. M.Sc in 
Food Technology, 1986-1988, University of Reading, United Kingdom. B.Sc in Agriculture - Food Science and 
Technology Major, 1982-1986, University of Peradeniya, Sri Lanka. Research focuses on value-added processing of 
grains and tubers with an emphasis on fractionation, characterization and utilization of carbohydrates, especially 
starch and mixed linkage beta-glucans.""",
            ),
            Lead(
                name="Marleny Aranda Saldana",
                email="marleny.saldana@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sciences - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-8018",
                website="https://www.ualberta.ca/",
                background_summary="""PhD in Process Engineering with a focus on Food/Bio-Engineering Processing, 
Sub/supercritical fluid processing, Bioactives, and Natural health products. Recipient of multiple awards including
the Killam Annual Professorship Award and McCalla Professorship, with extensive research on emerging processing 
technologies and more.""",
            ),
            Lead(
                name="Gleise Medeiros da Silva",
                email="gleise.silva@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor and BCRC - Hays Chair in Beef Production Systems, Faculty of Agricultural, 
Life and Environmental Science - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-0237",
                website="https://www.ualberta.ca/",
                background_summary="""Gleise M. Silva joined the Department of Agricultural, Food & Nutritional Science at 
the University of Alberta in August 2021 as an Assistant Professor and BCRC Hays Chair in Beef Production Systems. 
She obtained her MS and PhD degrees at the University of Florida, where she conducted several research trials in 
beef cattle nutrition and management. The focus of her research was on management of recently weaned beef calves, 
evaluation of feed additives, mitigation of environmental stress, and nutrition of the pregnant cow. As the BCRC - 
Hays Chair in Beef Production Systems at the University of Alberta, her research goals are to identify sustainable 
nutritional and management strategies able to enhance cattle health and performance, therefore, increasing 
profitability in the cow-calf sector.""",
            ),
            Lead(
                name="Roopesh Syamaladevi",
                email="roopeshms@ualberta.ca",
                title="Associate Professor",
                headline="""Associate Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="(780) 492-8413",
                website="https://foodsafetyengineering.ualberta.ca/",
                background_summary="""Roopesh Syamaladevi, PhD, is an Associate Professor at the University of Alberta, 
specializing in process engineering research to improve safety, quality, and utilization of water, food, and the 
environment. His research focuses on sanitation, disinfection, food processing engineering, antimicrobial 
applications, wastewater treatment, and agricultural applications using atmospheric cold plasma technologies.""",
            ),
            Lead(
                name="Hiwot Haileslassie",
                email="hhailesl@ualberta.ca",
                title="Associate Lecturer",
                headline="""Associate Lecturer, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="(780) 492-7742",
                website="https://www.ualberta.ca/",
                background_summary="""Hiwot Haileslassie is an Associate Lecturer at the Faculty of Agricultural, Life and 
Environmental Sciences, specializing in Ag, Food & Nutrition Science. She teaches various courses related to 
nutrition principles and cultural ecology of food.""",
            ),
            Lead(
                name="Spencer Proctor",
                email="proctor@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-4672",
                website="https://mcvd.ualberta.ca/",
                background_summary="""Dr. Spencer Proctor trained as a physiologist and cardiovascular scientist in both 
Australia and Canada. He was appointed to the Alberta Institute for Human Nutrition at the University of Alberta in
2004 and founded the Metabolic and Cardiovascular Diseases (MCVD) Laboratory. Dr. Proctor’s research program spans 
a unique continuum of expertise in the areas of nutrition, metabolism, physiology, behaviour, food health and 
chronic disease.""",
            ),
            Lead(
                name="Rudolph Fredua-Agyeman",
                email="freduaag@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Brassica and Pulse Genetics, Faculty of Agricultural, Life and Environmental
Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-3685",
                website="https://scholar.google.ca/citations?hl=en&user=bhxGC3EAAAAJ",
                background_summary="""The main goal of my research in the “Brassica and Pulse Genetics Program” (BPGP) at the
UoA is to enhance crop production and agricultural sustainability from the cellular, genetic, biochemical, and 
molecular perspectives.""",
            ),
            Lead(
                name="Aman Ullah",
                email="ullah2@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Science - Ag, Food & Nutri Sci Dept; 
Associate Dean (Academic), Faculty of Agricultural, Life and Environmental Sci - Deans Office""",
                phone="780-492-4845",
                website="https://apps.ualberta.ca/directory/person/ullah2",
                background_summary="""Dr. Ullah holds a PhD (with Distinction) from the University of Genova, Italy, and has 
extensive research interests in the utilization of lipids, polymers, and materials chemistry. His major 
responsibilities include the synthesis of monomers, biopolymers, and biocomposites from renewable resources. Dr. 
Ullah has received numerous awards for his contributions to research and teaches several courses related to food 
chemistry and biomaterials.""",
            ),
            Lead(
                name="Burim Ametaj",
                email="bametaj@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-9841",
                website="https://www.ualberta.ca/",
                background_summary="""Dr. Ametaj received his doctorate degree in nutritional immunology from Iowa State 
University and did three postdoctoral trainings at Iowa State University, Purdue University, and Cornell University
before joining University of Alberta in 2004. His research interest is in the area of nutritional immunology. His 
long-term goals are to study the relationship between nutrition and immune responses and their contribution in 
development of production diseases in ruminant animals as well as in developing new strategies to curb down the 
high incidence of transition diseases in dairy cattle.""",
            ),
            Lead(
                name="Michael Dyck",
                email="mkdyck@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="780-492-0047",
                website="https://www.ualberta.ca/",
                background_summary="""Dr Dyck's research program focuses on the development and application of molecular 
techniques and reproductive technologies, in collaboration with the pork production industry, to improve breeding 
efficiency in swine. He was co-lead on the Pan-Canadian NSERC Strategic Research Network “EmbryoGENE” and is 
currently leading Genome Canada funded research on the genomics of swine health.""",
            ),
            Lead(
                name="Malinda Thilakarathna",
                email="thilakar@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="(780) 492-9966",
                website="https://plantmicrobe.ualberta.ca",
                background_summary="""PhD (Biology), Dalhousie University; PDF (Plant Microbial Interactions, Agronomy), 
University of Guelph. Research focuses on technologies that reduce synthetic nitrogen fertilizers by using natural 
biological resources. Key areas include assessment of beneficial microbes for nitrogen fixation, alleviating 
abiotic stress in plants, and understanding nitrogen transfer mechanisms.""",
            ),
            Lead(
                name="Wendy Wismer",
                email="wwismer@ualberta.ca",
                title="Associate Professor",
                headline="""Associate Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept; Associate Chair, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-492-2923",
                website="https://gradpositions.ales.ualberta.ca/2021/05/11/identifying-food-related-benefits-of-hunting-to-mbivalent-hunters/",
                background_summary="""Wendy Wismer, PhD, specializes in Sensory and Consumer Science within Food Science. Her
research focuses on food product taste acceptance and explores consumer perceptions of innovative food products. 
She is particularly interested in taste and smell changes in cancer patients and seeks to develop tailored food 
products to support their dietary needs. Wendy holds a PhD in Food Science, an MSc in Consumer Studies, and a BSc 
in Food Science, all from reputable institutions.""",
            ),
            Lead(
                name="Carolyn Fitzsimmons",
                email="cfitzsim@ualberta.ca",
                title="PhD",
                headline="Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="780-248-1700",
                website="https://apps.ualberta.ca/directory/person/cfitzsim",
                background_summary="""My interests lie in how biological systems influence the development of lean meat and 
fat tissues, specifically looking through the window of gene expression. I am also interested in permanent gene 
expression changes that can be programmed in the next generation due to nutrition and/or other factors affecting 
the parental generation (epigenetics).""",
            ),
            Lead(
                name="Brasathe Jeganathan",
                email="jeganath@ualberta.ca",
                title="Assistant Lecturer",
                headline="""Assistant Lecturer, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="780-492-3829",
                website="https://apps.ualberta.ca/directory/person/jeganath",
                background_summary=None,
            ),
            Lead(
                name="Linda Gorim",
                email="gorim@ualberta.ca",
                title="Assistant Professor & WGRF Chair in Cropping Systems",
                headline="Department of Agricultural, Food and Nutritional Science at the University of Alberta",
                phone="780-492-8814",
                website="https://apps.ualberta.ca/directory/person/gorim",
                background_summary="""Dr. Linda Gorim is an Assistant Professor specializing in Cropping Systems in the 
Faculty of Agricultural, Life and Environmental Sciences at the University of Alberta. Her research focuses on 
agronomy, nutrient use efficiency, abiotic stresses, and sustainable cropping systems. Dr. Gorim has a PhD in Crop 
Water Stress Management from the University of Hohenheim in Stuttgart, Germany, and has numerous publications 
addressing various aspects of crop productivity, soil health, and agronomic challenges. She is dedicated to 
teaching and mentoring students, preparing them for careers in the agricultural sector.""",
            ),
            Lead(
                name="Ning Xiang",
                email="nxiang@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="780-492-4610",
                website="http://www.afns.ualberta.ca/Graduate.aspx",
                background_summary="""Ning Xiang holds a PhD from Purdue University, West Lafayette, USA, and specializes in 
Cellular Agriculture and cultivated meat technology. His research focuses on advancing techniques for producing 
animal-derived products without traditional animal farming, using cell culture and tissue engineering.""",
            ),
            Lead(
                name="Daniel Barreda",
                email="d.barreda@ualberta.ca",
                title="Professor",
                headline="""Professor, University of Alberta""",
                phone="780-492-0375",
                website="https://apps.ualberta.ca/directory/person/dbarreda",
                background_summary="""Daniel Barreda holds a BSc in Microbiology and Biochemistry from the University of 
Victoria, a PhD in Physiology and Cell Biology from the University of Alberta, and completed a Postdoc in Medical 
Immunology at the University of Pennsylvania. His research focuses on Immunology, particularly the relationship 
between hosts, pathogens, and the environment. He has received numerous teaching and research awards, including the
University of Alberta Provost Award for Early Achievement of Excellence in Undergraduate Teaching and the NACTA 
Teaching Award of Merit. His laboratory conducts interdisciplinary research, collaborating with academia, industry,
and government, and has published extensively in the field of immunology and animal health. He teaches various 
courses related to veterinary immunology and zoonoses at the University of Alberta.""",
            ),
            Lead(
                name="Stephen Strelkov",
                email="strelkov@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="780-492-1969",
                website="https://apps.ualberta.ca/directory/person/strelkov",
                background_summary="""Dr. Stephen Strelkov holds a PhD from the University of Manitoba and specializes in 
Plant Pathology as the Associate Chair of Graduate Programs. His research focuses on host-parasite interactions, 
specifically the role of host-specific toxins in fungal pathogenicity and plant disease development. Key areas of 
research include the purification and characterization of toxins produced by fungal pathogens affecting wheat and 
canola, and the development of integrated management strategies for these diseases.""",
            ),
            Lead(
                name="Rene Jacobs",
                email="rjacobs@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-2343",
                website="https://www.ualberta.ca/",
                background_summary="""Dr. René Jacobs was trained in biochemistry and molecular biology at both the Memorial 
University of Newfoundland and the University of Alberta. In 2009, He was appointed to the Department of 
Agricultural, Food and Nutritional Science at the University of Alberta. Dr. Jacobs’ research program incorporates 
'state of the science' in vivo techniques, biochemical analysis and nutrigenomics as part of a comprehensive, 
multidisciplinary approach seeking to understand the complex interactions involved in the etiology of obesity, T2DM
and other chronic diseases.""",
            ),
            Lead(
                name="Jianping Wu",
                email="jwu3@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-6885",
                website="https://apps.ualberta.ca/directory/person/jwu3",
                background_summary="""Professor Jianping Wu has a PhD from Jiangnan University, China, and focuses on food 
proteins and bioactive peptides. His research aims to improve protein sustainability and enhance human health 
through multiple interrelated fields. He teaches advanced food protein chemistry, agri-chemical analysis, food 
product development, and innovations in food science.""",
            ),
            Lead(
                name="Guanqun (Gavin) Chen",
                email="gc24@ualberta.ca",
                title="Associate Professor",
                headline="""Associate Prof & CRC2 in Plant Lipid Biotechnology, Faculty of Agricultural, Life and 
Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-492-3148",
                website="https://plb.ualberta.ca/",
                background_summary="""Guanqun (Gavin) Chen is an Associate Professor and Canada Research Chair in Plant Lipid
Biotechnology at the University of Alberta. He holds a PhD from The University of Hong Kong and is recognized for 
his work in enhancing seed oil production, utilizing lipid biotechnology, and exploring the potential of oilseed 
crops and oleaginous microorganisms.""",
            ),
            Lead(
                name="Anne Laarman",
                email="alaarman@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="(780) 492-8228",
                website="https://scholar.google.com/citations?user=UFAXX7sAAAAJ&hl=en&authuser=1",
                background_summary="""Research team focused on improving nutrient absorption in cows and calves to enhance 
health and productivity. Areas of study include nutrition, physiology, ruminant absorption physiology, gut 
development, and diet adaptation. Offering research opportunities and various courses related to animal nutrition 
and husbandry.""",
            ),
            Lead(
                name="Catherine Field",
                email="catherine.field@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-2597",
                website="https://orcid.org/0000-0001-7285-4767",
                background_summary="""PhD, FCAHS, CRC Tier 1 Chair in Human Nutrition and Metabolism. Research focuses on the
effect of nutrition on the immune system with interests in polyunsaturated fats' role in infant immune development,
fatty acids in breast cancer treatment, and the nutritional status of mothers related to mental""",
            ),
            Lead(
                name="Carla Prado",
                email="carla.prado@ualberta.ca",
                title="Distinguished University Professor",
                headline="""Canada Research Chair in Integrative Nutrition, Body Composition, and Energy Metabolism (Tier 1),
Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-7934",
                website="https://www.drcarlaprado.com/",
                background_summary="""Dr. Carla Prado is a Distinguished University Professor and Registered Dietitian at the
University of Alberta. She holds a Tier 1 Canada Research Chair in Integrative Nutrition, Body Composition, and 
Energy Metabolism. Dr. Prado directs the Human Nutrition Research Unit, known as one of the top research and 
training facilities for body composition and energy metabolism assessments worldwide. Her current research program 
focuses on investigating the prevalence and health outcomes of abnormal body composition phenotypes in patients 
with diverse chronic conditions, particularly cancer, and developing targeted nutrition interventions to optimize 
body composition. She has received numerous accolades, including being named one of Canada’s Top 40 under 40 and 
distinguished as a Highly Cited Researcher.""",
            ),
            Lead(
                name="Richard Uwiera",
                email="ruwiera@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-0107",
                website="https://apps.ualberta.ca/directory/person/ruwiera",
                background_summary="""Dr Uwiera's research interests include the development of new animal models (rodents, 
small animals and livestock), investigating the physiological, and immunological mechanisms involved in maintaining
a healthy gut in livestock species and understanding changes in gut function that leads to intestinal injury and 
inflammatory. He is also involved in many regional, national, international collaborative efforts by providing 
veterinary, anaesthetic, clinical-medical, surgical, immunological and gross and histopathological expertise.""",
            ),
            Lead(
                name="Sheau-Fang Hwang",
                email="sh20@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sciences - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-6693",
                website="https://apps.ualberta.ca/directory/person/sh20",
                background_summary="""Sheau-Fang Hwang is a Professor at the Faculty of Agricultural, Life and Environmental 
Sciences, specializing in plant pathology with a focus on diseases of canola and pulse crops. Her research includes
clubroot management, blackleg issues, and developing yield loss models, alongside supervising graduate students. 
She has received multiple awards for her contributions to plant disease management.""",
            ),
            Lead(
                name="Clover Bench",
                email=None,
                title="Associate Professor",
                headline="""Division Director, Animal Sci, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & 
Nutri Sci Dept""",
                phone=None,
                website=None,
                background_summary="""PhD in Applied Ethology, University of Saskatchewan. M.S. in Applied Domestic Animal 
Behavior, University of California, Davis. B.S. in Animal Science, University of California, Davis. Research 
interests include the study of animal well-being, housing system design and management, welfare assessment, the 
ontogeny of behavior traits, and micro-behavior biometrics. Leads the Applied Ethology Research Group focused on 
applied ethology and animal behaviour.""",
            ),
            Lead(
                name="Michael Gaenzle",
                email="mgaenzle@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-0774",
                website="http://www.afns.ualberta.ca/Graduate.aspx",
                background_summary="""Michael Gänzle is a Professor in the Faculty of Agricultural, Life and Environmental 
Sciences, specializing in Food Microbiology and Probiotics. He holds degrees of Dr. rer. nat. from Universität 
Hohenheim and Technische Universität München. He is the Canada Research Chair (Tier I) in Food Microbiology and 
Probiotics and a Clarivate Highly Cited Researcher (2021-2024). He is a Fellow of the Royal Society of Canada, 
Academy of Sciences, Division of Biological Sciences. He serves as Associate Editor for several journals and on 
editorial boards, focusing on research related to lactic acid bacteria and innovative food processing methods.""",
            ),
            Lead(
                name="Martin Zuidhof",
                email="mzuidhof@ualberta.ca",
                title="Professor",
                headline="""Professor, Poultry Systems Modeling and Precision Feeding, Faculty of Agricultural, Life and 
Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-248-1655",
                website="https://apps.ualberta.ca/directory/person/mzuidhof",
                background_summary="""Dr. Zuidhof was the first in the world to develop a transformative precision feeding 
system to control individual feed intake in group-housed chickens. Over the last 10 years, his research team has 
been able to consistently achieve very high flock uniformity (coefficient of variation for body weight less than 
2%). The system is also proving to be an excellent way to remove confounding body weight variation from experiments
so as to better elucidate physiological and metabolic mechanisms that contribute to reproductive success in 
poultry.""",
            ),
            Lead(
                name="Paul Stothard",
                email="stothard@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-492-5242",
                website="https://sites.ualberta.ca/~stothard/index.html",
                background_summary="""PhD in molecular biology and genetics from the University of Alberta. Research areas 
include bioinformatics, genomics, and genetics, focusing on understanding genetic traits in animals, cataloging 
genome variations, metagenomic diagnostics, and user-friendly software development for bacterial genome 
interpretation.""",
            ),
            Lead(
                name="Caroline Richard",
                email="cr5@ualberta.ca",
                title="Associate Professor",
                headline="""Associate Professor of Human Nutrition at Faculty of Agricultural, Life and Environmental 
Sciences""",
                phone="780-248-1827",
                website="https://sites.google.com/ualberta.ca/carolinerichardlab",
                background_summary="""Caroline Richard is an Associate Professor in the Faculty of Agricultural, Life and 
Environmental Sciences, specializing in Nutritional Immunology. She holds a PhD in Nutrition & Metabolism and an 
MSc in Clinical Nutrition from Laval University, and is a Canada Research Chair. Her research focuses on 
establishing evidence-based nutritional recommendations for managing obesity-related immune dysfunction and 
understanding the relationship between diet and immune function in obesity.""",
            ),
            Lead(
                name="Dr. Nat Kav",
                email="nat@ualberta.ca",
                title="Vice Dean & Professor",
                headline="""Vice Dean & Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci
Dept""",
                phone=None,
                website="https://apps.ualberta.ca/directory/person/nat",
                background_summary="""Dr. Nat Kav holds a Ph.D. in Biochemistry from the University of Calgary. His research 
involves using proteomics- and genomics-based techniques to identify and validate genes for crop improvement 
through biotechnology. He has served in various academic leadership positions and has a keen interest in 
agricultural biotechnology, teaching courses related to biochemistry and plant sciences.""",
            ),
            Lead(
                name="Lingyun Chen",
                email="lingyun.chen@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept, 
Division Director (Food Sci.)""",
                phone="780-492-0038",
                website="https://scholar.google.ca/citations?hl=en&user=rEeGJSMAAAAJ&view_op=list_works&sortby=pubdate",
                background_summary="""Dr. Chen's research has been focused on plant protein structures underlying its 
functional properties. The generated knowledge has been applied to develop plant protein ingredients of improved 
functionalities, texture and nutritional properties for food applications. The concept of designing functional 
organization from molecular level has also led to the fabrication of biodegradable materials based on biopolymers 
with multiple functions for nutraceutical delivery, biomedical and environmental applications.""",
            ),
            Lead(
                name="John Basarab",
                email="jbasarab@ualberta.ca",
                title="Associate Professor",
                headline="""Associate Professor, Livestock Genetics/Genomics at the University of Alberta""",
                phone="(780) 499-5431",
                website=None,
                background_summary="""John Basarab has over 30 years of experience in beef cattle production and management. 
His research focuses on improving feed efficiency, DNA pooling for genotyping, and management strategies to enhance
cattle resilience to climate change. He has authored over 300 scientific articles and has a PhD in Animal Genetics 
and Biochemistry from the University of Alberta.""",
            ),
            Lead(
                name="Ben Willing",
                email="willing@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-8908",
                website="https://scholar.google.ca/citations?user=Zze3qewAAAAJ&hl=en&oi=ao",
                background_summary="""PhD in Animal and Poultry Science from the University of Saskatchewan and postdoctoral 
research in Microbiology from the Swedish University of Agricultural Science and in Microbiology and Immunology at 
the University of British Columbia. Research focuses on the microbiology of nutrigenomics, exploring the role of 
symbiotic microbes in the gastrointestinal tract and their effects on host physiology and health as influenced by 
diet.""",
            ),
            Lead(
                name="Urmila Basu",
                email=None,
                title="Ph.D.",
                headline="""Faculty Service Officer at Faculty of Agricultural, Life and Environmental Sciences - Ag, Food & 
Nutrition Sciences Department Central Labs""",
                phone=None,
                website=None,
                background_summary="""Dr. Urmila Basu provides leadership to the operation of core research and teaching labs
and facilities with over 20 years of extensive experience at the University of Alberta. Her work involves resource 
management, budgets and forecasts, and collaborative research projects in functional genomics and proteomics aimed 
at crop and livestock improvement. She has also played an active role in enhancing student engagement through 
teaching graduate and undergraduate courses.""",
            ),
            Lead(
                name="Changxi Li",
                email=None,
                title="AAFC Professor and AAFC Chair in Bovine Genomics",
                headline="""AAFC Professor and AAFC Chair in Bovine Genomics, Faculty of Agricultural, Life and Environmental
Sci - Ag, Food & Nutri Sci Dept""",
                phone=None,
                website=None,
                background_summary="""PhD, University of Alberta. My team conducts research in bovine quantitative genetics 
and functional genomics. Our current research interests include identification and characterization of genes for 
economically important traits in beef cattle, investigation of genetic mechanisms regulating growth and efficiency,
and development of genomic tools for industry improvement.""",
            ),
            Lead(
                name="Vera Mazurak",
                email="vmazurak@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-8048",
                website="https://apps.ualberta.ca/directory/person/vmazurak#Contact",
                background_summary="""Vera Mazurak is a Professor in the Faculty of Agricultural, Life and Environmental 
Sciences at the University of Alberta, specializing in Nutrition and Metabolism. She has a PhD in Nutrition and 
Metabolism from the University of Alberta, and her research focuses on lipid metabolism in disease, nutritional 
requirements for cancer patients, and the impact of nutrients on gene expression related to cancer progression.""",
            ),
            Lead(
                name="Edward Bork",
                email="ebork@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-3843",
                website="https://apps.ualberta.ca/directory/person/ebork",
                background_summary="""Professor Bork holds a PhD from Utah State University and specializes in Rangeland 
Ecology and Management, focusing on improving the productivity and sustainability of rangeland ecosystems.""",
            ),
            Lead(
                name="Ruurd Zijlstra",
                email="zijlstra@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-492-8593",
                website="https://apps.ualberta.ca/directory/person/zijlstra",
                background_summary="""Research interest in ingredient evaluation and feed processing, creating a decision 
model to optimize feed processing following ingredient evaluation for predictable performance of agricultural 
species. Involves validation of quality characteristics of feed ingredients using laboratory technologies and 
improving digestibility through feed processing techniques.""",
            ),
            Lead(
                name="Masahito Oba",
                email="moba@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-7007",
                website="https://apps.ualberta.ca/directory/person/moba",
                background_summary="""Masahito Oba conducts research related to dairy production science, focusing on animal 
nutrition, feeding practices, and their effects on dairy cattle productivity and health.""",
            ),
            Lead(
                name="Diana Mager",
                email="mager@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-7687",
                website="https://www.ualberta.ca/",
                background_summary="""Mp. Diana Mager is currently appointed as Adjunct Professor in the Department of 
Pediatrics in the Faculty of Medicine & Dentistry.""",
            ),
            Lead(
                name="Gurcharn Brar",
                email="gurcharn.brar@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Wheat Breeding & Genetics, Faculty of Agricultural, Life and Environmental 
Sci - Ag, Food & Nutri Sci Dept""",
                phone="780-492-3767",
                website="https://apps.ualberta.ca/directory/person/gurcharn",
                background_summary=None,
            ),
            Lead(
                name="Cameron Carlyle",
                email=None,
                title="Associate Professor",
                headline="""Associate Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept. Director (Plant Biosystems), Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="carlyle1@ualberta.ca",
                website="https://apps.ualberta.ca/directory/person/carlyle1",
                background_summary="""Areas of study include Grassland Ecology and Rangeland Ecology and Management.""",
            ),
            Lead(
                name="Sabina Valentine",
                email="sparkes@ualberta.ca",
                title="Assistant Lecturer",
                headline="""Assistant Lecturer, Faculty of Agricultural, Life and Environmental Science - Ag, Food & Nutri 
Sci Dept""",
                phone="(780) 492-4835",
                website="https://apps.ualberta.ca/directory/person/sparkes",
                background_summary="""I have enjoyed teaching Nutrition and Well Being (Nutritiion 100; in lecture format and
on line), Clinical Nutrition (Nutrition 468), Advanced Clinical Nutrition (Nutrition 476), Applied Food Theory 
(NUFS 250), Health Education, and Nutrition and Chronic Disease (NUTR 452). I have also enjoyed working as a 
Clinical Dietitian for the past 20 years. I believe that there are three essential elements that are conducive to 
learning. The instructor’s role is to act as a guide, students must have access activities that apply what they 
have learned, and students should be able to have choices and let their curiosity direct their learning.""",
            ),
            Lead(
                name="Habibur Rahman",
                email="hrahman@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-3869",
                website="https://apps.ualberta.ca/directory/person/hrahman",
                background_summary="""PhD in Canola Genetics & Molecular Breeding from Copenhagen University. Research 
focuses on plant genetics and breeding, specifically the development of canola germplasm to enhance seed yield, 
disease resistance, and oil quality. Involved in molecular breeding using genomics and biotechnology.""",
            ),
            Lead(
                name="Jean Buteau",
                email="jbuteau@ualberta.ca",
                title="Professor",
                headline="""Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept; 
Division Dir - Human Nutrition, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept""",
                phone="(780) 492-8386",
                website="https://www.ualberta.ca/",
                background_summary="""PhD in Biochemistry from University of Montreal. Research interests include diabetes, 
obesity, and nutritional and hormonal regulation of beta-cell mass and function. Focused on identifying novel 
molecular mechanisms governing beta-cell differentiation, proliferation, and survival.""",
            ),
            Lead(
                name="Donna Vine",
                email="dvine@ualberta.ca",
                title="Professor & Interim Academic Lead, Dietetics Specialization",
                headline="Professor in Human Nutrition at the University of Alberta",
                phone="(780) 492-4393",
                website="https://pcos.together.ualberta.ca/",
                background_summary="""Dr. Donna Vine is a passionate Principle Investigator in Women’s Health Research, 
focusing on Polycystic Ovary Syndrome (PCOS) and its health impacts. She is involved in comprehensive research to 
improve health care for individuals with PCOS, promoting awareness and advocating for better health outcomes.""",
            ),
            Lead(
                name="Catherine Chan",
                email="cbchan@ualberta.ca",
                title="Professor",
                headline="Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="(780) 492-9939",
                website="https://orcid.org/0000-0003-3882-0592",
                background_summary="""PhD, Physiology, University of British Columbia. Research areas include Human 
Nutrition, Physiology, and Metabolism with a focus on obesity and type 2 diabetes, exploring dietary effects on 
metabolism, insulin signaling and developing lifestyle programs for diabetes management.""",
            ),
            Lead(
                name="Heidi Bates",
                email="hbates@ualberta.ca",
                title="Faculty Service Officer",
                headline="Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci Dept",
                phone="780-492-9482",
                website="/catalogue/instructor/hbates",
                background_summary="""Heidi Bates is a Faculty Service Officer involved in various courses related to 
nutrition and foodservice systems management. She offers practical experiences in nutrition care, community 
nutrition, and professional practice in clinical dietetics.""",
            ),
            Lead(
                name="Boyd Mori",
                email="bmori@ualberta.ca",
                title="Assistant Professor",
                headline="""Assistant Professor, Faculty of Agricultural, Life and Environmental Sci - Ag, Food & Nutri Sci 
Dept""",
                phone="(780) 492-6412",
                website="https://scholar.google.com/citations?user=PcL5K94AAAAJ&hl=en&oi=ao",
                background_summary="""My research is focused on the development of integrated pest management (IPM) for 
insect pests in field and horticultural agroecosystems. Specifically, my research strives to provide growers with 
sustainable pest control strategies that reduces the reliance on insecticides and conserves beneficial species 
(i.e. natural enemies and pollinators). To this end, I meld basic and applied research incorporating behavioural, 
chemical, and molecular ecology to understand and exploit the biology of insect pests, their host plants and 
natural enemies. Currently, I have three major focal areas: 1) chemical ecology – to develop insect monitoring and 
management tools; 2) population genetics – to track insect invasions and dispersal/migration of insect pests; 3) 
insect-insect and insect-plant interactions – to identify key interactions that may lead to the development of 
alternative management strategies.""",
            ),
        ]
    ),
)
