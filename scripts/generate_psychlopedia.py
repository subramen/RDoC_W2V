def collate_psy_definitions():
    """
    Collate psychology terms and their various definitions in a hashmap.
    Format:
        {
            TERM1: { Onto1: Definition of TERM1 in Onto1,
                    Onto3: Definition of TERM1 in Onto3
                }
            .
            .
        }
    
    Ontologies used: APA, MF, MFOMD, suicideo (obtained from NCBO BioPortal)
    """

    apa = pd.read_csv('ontologies\\APAONTO.csv').fillna('') #Preferred Label, Definitions, Alt name
    mf = pd.read_csv('ontologies\\MF.csv').fillna('')
    mfo = pd.read_csv('ontologies\\MFOMD.csv').fillna('')
    sui = pd.read_csv('ontologies\\suicideo.csv').fillna('')

    thes=defaultdict(dict)

    def add_defn(w, dfn, onto):
        if w=='':
            pass
        d=thes[w]
        d[onto]=re.sub(r'\[wikipedia: http\S+\]', '', dfn.replace('\n', ' '), flags=re.IGNORECASE)
        thes[w] = d


    for row in apa.iterrows():
        word = row[1]['Preferred Label']
        defn = row[1]['Definitions']
        if defn=='':
            continue
        syn = [word]+row[1]['Alt name'].split('|')
        for w in syn:
            add_defn(w, defn, 'apa')    

    for row in mf.iterrows():
        word = row[1]['Preferred Label']
        defn = row[1]['Definitions']
        if defn=='':
            continue
        add_defn(word, defn, 'mf')

    for row in mfo.iterrows():
        word = row[1]['Preferred Label']
        defn = row[1]['Definitions']
        if defn=='':
            continue
        syn = [word]+row[1]['Synonyms'].split('|')
        for w in syn:
            add_defn(w, defn, 'mfo')

    for row in sui.iterrows():
        word = row[1]['Preferred Label']
        defn = row[1]['Definitions']
        if defn=='':
            continue
        syn = [word]+row[1]['alternative term'].split('\n')
        for w in syn:
            add_defn(w, defn, 'sui')


    with open('psychThesaurusDict.pkl','wb') as f:
            pickle.dump(thes, f)      