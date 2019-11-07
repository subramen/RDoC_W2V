
-- GET DESCRIPTORNAME AND QUALIFIERS OF KNOWLEDGE SAMPLE
select distinct 
        meshheading.pmid, 
        meshheading.descriptorname, 
        meshheading.descriptorname_ui,
        qua	lifier.value,
        publicationtype.value,
        keywords.value,
        keywords.majortopicyn
 from medcit_meshheadinglist_meshheading meshheading inner join medcit_meshheadinglist_meshheading_qualifiername qualifier
        on meshheading.pmid = qualifier.pmid and meshheading.medcit_meshheadinglist_meshheading_order = qualifier.medcit_meshheadinglist_meshheading_order
     inner join medcit_art_publicationtypelist_publicationtype publicationtype on meshheading.pmid = publicationtype.pmid
     left outer join medcit_keywordlist_keyword keywords on meshheading.pmid = keywords.pmid 
 where meshheading.pmid in (10459405, 26115223, 27940392, 28293209, 28427115, 28452130, 28543944, 28555873, 28571798, 28587654, 28590684, 28592475, 28594292, 28594633, 28594866, 28594925, 28595115, 28595276, 28611707, 28615380, 20395400, 28675115, 19931549, 24076207, 16204321, 27173662, 20866019, 16247114, 29555429, 25414863, 21269779, 23073641, 22491355, 30265859, 24151118, 30760585, 28013055, 16115784, 21855571, 14998902, 20371819, 25451788, 21656765, 20964748, 29902666, 16971899, 20189314, 28784793, 26747839, 26377804, 20720535, 28893930, 29223783, 26995802, 17604912, 27808542, 15772862, 26329286, 20977330, 27197727, 12238739, 20455126, 30694221, 24843744, 30173702, 9850002, 24275670, 28981834, 30076574, 24733508, 23386529, 29552751, 28863419, 20955863, 25254619, 30123880, 19788771, 21330230, 27406185, 27575924, 29732933, 25499772, 17888398, 30140087, 28316567, 29729300, 29778506)
;


-- DESCRIPTORS
-- 'Developmental Disabilities', 'Hearing Loss', 'Sensorineural', 'Otitis Media', 'Depressive Disorder', 'Major', 'Alcohol Drinking', 'Smoking', 'Stress Disorders', 'Post-Traumatic', 'Anxiety', 'Corticosterone', 'Stress', 'Physiological', 'Amygdala', 'Diet', 'Protein-Restricted', 'Fear', 'Hippocampus', 'Image Processing', 'Computer-Assisted', 'Magnetic Resonance Imaging', 'Oxygen', 'Photic Stimulation', 'Serotonin', 'Tryptophan', 'Attention', 'Conditioning (Psychology)', 'Diazepam', 'Diphenhydramine', 'Evoked Potentials', 'Auditory', 'Evoked Potentials', 'Somatosensory', 'Hypnotics and Sedatives', 'Affective Symptoms', 'Crime', 'Crime Victims', 'Dissociative Disorders', 'Rape', 'Theft', 'Citalopram', 'Electroshock', 'Reflex', 'Startle', 'Serotonin Uptake Inhibitors', 'Arousal', 'Awareness', 'Expressed Emotion', 'Hydrocortisone', 'Saliva', 'Anxiety Disorders', 'Depressive Disorder', 'Neoplasm Recurrence', 'Local', 'Ovarian Neoplasms', 'Palliative Care', 'Quality of Life', 'Reaction Time', 'Space Perception', 'Antidepressive Agents', 'Second-Generation', 'Cannabis', 'Fluoxetine', 'Marijuana Abuse', 'Extinction', 'Psychological', 'Receptor', 'Cannabinoid', 'CB1', 'Family', 'Stress', 'Psychological', 'Brain Mapping', 'Oxytocin', 'Psychomotor Performance', 'Deep Brain Stimulation', 'Depression', 'Movement Disorders', 'Personality Disorders', 'Combat Disorders', 'Patient Acceptance of Health Care', 'United States', 'Veterans', 'Chronic Disease', 'Pain', 'Affect', 'Blinking', 'Down-Regulation', 'Alabama', 'Disasters', 'Florida', 'Water Pollution', 'Chemical', 'Behavior', 'Animal', 'Hypothalamo-Hypophyseal System', 'Pituitary-Adrenal System', 'Predatory Behavior', 'Brain', 'Neuroimaging', 'Phobic Disorders', 'Septal Nuclei', 'Conditioning', 'Classical', 'Learning', 'Memory', 'Nurses', 'Methadyl Acetate', 'Naloxone', 'Narcotic Antagonists', 'Narcotics', 'Neurosecretory Systems', 'Substance Withdrawal Syndrome', 'Behavior Control', 'Feeding Behavior', 'Food Preferences', 'Abortion', 'Spontaneous', 'Australia', 'Mental Health', 'Postpartum Period', 'Women's Health', 'Panic Disorder', 'Muscle', 'Skeletal', 'Basolateral Nuclear Complex', 'Neural Pathways', 'Form Perception', 'Patients', 'Alcoholic Intoxication', 'Alcoholism', 'Binge Drinking', 'Mental Disorders', 'Temperance', 'Psychophysiologic Disorders', 'Tinnitus', 'Hearing Loss', 'Mucopolysaccharidosis I', 'Sleep Apnea', 'Obstructive', 'Cannabinoids', 'Galvanic Skin Response', 'Attentional Bias', 'Emotions', 'Eye Movements', 'Heart Rate', 'Speech', 'Attention Deficit Disorder with Hyperactivity', 'Color Perception', 'Tic Disorders', 'Acetylcholinesterase', 'Aggression', 'Anabolic Agents', 'Androgens', 'Oxidative Stress', 'Stanozolol', 'Testosterone', 'Circadian Rhythm', 'Energy Metabolism', 'Gene Expression', 'Immunity', 'Leucine', 'Muscle Proteins', 'Protein Biosynthesis', 'Ribosomes', 'RNA', 'Messenger', 'RNA Processing', 'Post-Transcriptional', 'Anticipation', 'Psychological', 'Electric Stimulation'

-- QUALIFIERS
-- 'etiology', ' complications', ' therapy', ' physiopathology', ' psychology', ' epidemiology', ' blood', ' blood supply', ' physiology', ' adverse effects', ' methods', ' metabolism', ' deficiency', ' drug effects', ' pharmacology', ' administration & dosage', ' diagnosis', ' drug therapy', ' pathology', ' therapeutic use', ' genetics', ' ethics', ' statistics & numerical data', ' economics', ' analogs & derivatives'

-------- MAIN QUERY ----------------
with selectedMesh as (
   select distinct 
        meshheading.pmid, 
        meshheading.descriptorname
   from medcit_meshheadinglist_meshheading meshheading 
   where meshheading.descriptorname in ('Developmental Disabilities', 'Hearing Loss', 'Sensorineural', 'Otitis Media', 'Depressive Disorder', 'Major', 'Alcohol Drinking', 'Smoking', 'Stress Disorders', 'Post-Traumatic', 'Anxiety', 'Corticosterone', 'Stress', 'Physiological', 'Amygdala', 'Diet', 'Protein-Restricted', 'Fear', 'Hippocampus', 'Image Processing', 'Computer-Assisted', 'Magnetic Resonance Imaging', 'Oxygen', 'Photic Stimulation', 'Serotonin', 'Tryptophan', 'Attention', 'Conditioning (Psychology)', 'Diazepam', 'Diphenhydramine', 'Evoked Potentials', 'Auditory', 'Evoked Potentials', 'Somatosensory', 'Hypnotics and Sedatives', 'Affective Symptoms', 'Crime', 'Crime Victims', 'Dissociative Disorders', 'Rape', 'Theft', 'Citalopram', 'Electroshock', 'Reflex', 'Startle', 'Serotonin Uptake Inhibitors', 'Arousal', 'Awareness', 'Expressed Emotion', 'Hydrocortisone', 'Saliva', 'Anxiety Disorders', 'Depressive Disorder', 'Neoplasm Recurrence', 'Local', 'Ovarian Neoplasms', 'Palliative Care', 'Quality of Life', 'Reaction Time', 'Space Perception', 'Antidepressive Agents', 'Second-Generation', 'Cannabis', 'Fluoxetine', 'Marijuana Abuse', 'Extinction', 'Psychological', 'Receptor', 'Cannabinoid', 'CB1', 'Family', 'Stress', 'Psychological', 'Brain Mapping', 'Oxytocin', 'Psychomotor Performance', 'Deep Brain Stimulation', 'Depression', 'Movement Disorders', 'Personality Disorders', 'Combat Disorders', 'Patient Acceptance of Health Care', 'United States', 'Veterans', 'Chronic Disease', 'Pain', 'Affect', 'Blinking', 'Down-Regulation', 'Alabama', 'Disasters', 'Florida', 'Water Pollution', 'Chemical', 'Behavior', 'Animal', 'Hypothalamo-Hypophyseal System', 'Pituitary-Adrenal System', 'Predatory Behavior', 'Brain', 'Neuroimaging', 'Phobic Disorders', 'Septal Nuclei', 'Conditioning', 'Classical', 'Learning', 'Memory', 'Nurses', 'Methadyl Acetate', 'Naloxone', 'Narcotic Antagonists', 'Narcotics', 'Neurosecretory Systems', 'Substance Withdrawal Syndrome', 'Behavior Control', 'Feeding Behavior', 'Food Preferences', 'Abortion', 'Spontaneous', 'Australia', 'Mental Health', 'Postpartum Period', 'Women''s Health', 'Panic Disorder', 'Muscle', 'Skeletal', 'Basolateral Nuclear Complex', 'Neural Pathways', 'Form Perception', 'Patients', 'Alcoholic Intoxication', 'Alcoholism', 'Binge Drinking', 'Mental Disorders', 'Temperance', 'Psychophysiologic Disorders', 'Tinnitus', 'Hearing Loss', 'Mucopolysaccharidosis I', 'Sleep Apnea', 'Obstructive', 'Cannabinoids', 'Galvanic Skin Response', 'Attentional Bias', 'Emotions', 'Eye Movements', 'Heart Rate', 'Speech', 'Attention Deficit Disorder with Hyperactivity', 'Color Perception', 'Tic Disorders', 'Acetylcholinesterase', 'Aggression', 'Anabolic Agents', 'Androgens', 'Oxidative Stress', 'Stanozolol', 'Testosterone', 'Circadian Rhythm', 'Energy Metabolism', 'Gene Expression', 'Immunity', 'Leucine', 'Muscle Proteins', 'Protein Biosynthesis', 'Ribosomes', 'RNA', 'Messenger', 'RNA Processing', 'Post-Transcriptional', 'Anticipation', 'Psychological', 'Electric Stimulation')
   ), selectedQual as (
     select distinct 
        qualifier.pmid,
        qualifier.value
     from medcit_meshheadinglist_meshheading_qualifiername qualifier inner join selectedMesh on qualifier.pmid = selectedMesh.pmid
     where qualifier.value in ('etiology', ' complications', ' therapy', ' physiopathology', ' psychology', ' epidemiology', ' blood', ' blood supply', ' physiology', ' adverse effects', ' methods', ' metabolism', ' deficiency', ' drug effects', ' pharmacology', ' administration & dosage', ' diagnosis', ' drug therapy', ' pathology', ' therapeutic use', ' genetics', ' ethics', ' statistics & numerical data', ' economics', ' analogs & derivatives')
   )
select medcit.pmid,
	   medcit.art_arttitle,
       abstract.value as abstracttext,
	   abstract.label
from medcit inner join medcit_art_abstract_abstracttext abstract on medcit.pmid = abstract.pmid
where medcit.pmid in (select pmid from selectedQual)
;





