.. python-wim documentation knowledge file, created by
   Benjamin Bengfort on Wed Feb 6 14:44:23 2013.

Knowledge
*********

The following sections describe the knowledge base used in conjunction with Wordnet to rapidly 
produce WIMs on demand with the python module. This knowledge is loaded into the `Knowledge` object
in the `frames` module.



===========================================================================
Somebody ----s somebody to INFINITIVE
===========================================================================

AGENT HEAD BENEFICIARY X THEME::
    (CL
      (NP=subject,somebody )
      (VP=head
        (NP=directobject,somebody )
        (TO=token:"to" )
        (VP=infinitive )))

**Example:** "We require our secretary to be on time."::

    (S
      (CL
        (NP (N (PRO (PRP We))))
        (VP
          (V (VBP require))
          (NP (N (PRO (POSSPRO (PRPS our)))) (N (NN secretary)))
          (TO to)
          (VP (V (VB be)) (PP (PREP (IN on)) (NP (N (NN time)))))))
      (PUNCT .))


===========================================================================
Somebody ----s that CLAUSE
===========================================================================

AGENT HEAD X THEME
(CL (NP=subject,somebody ) (VP=head (PP (PREP=token:"that" ) (CL ))))

Example: "They confirm that there was a traffic accident."
(S
  (CL
    (NP (N (PRO (PRP They))))
    (VP
      (V (VBP confim))
      (PP
        (PREP (IN that))
        (CL
          (NP (EX there))
          (VP
            (V (VBD was))
            (NP (DET a) (N (N (NN traffic)) (N (NN accident)))))))))
  (PUNCT .))


===========================================================================
Somebody ----s whether INFINITIVE
===========================================================================

AGENT HEAD X THEME
(CL
  (NP=subject,somebody )
  (VP=head (PP (PREP=token:"whether" ) (CL (VP=infinitive )))))

Example: "They ask whether she can sing."
(S
  (CL
    (NP (N (PRO (PRP They))))
    (VP
      (V (VBP ask))
      (PP
        (PREP (IN whether))
        (CL
          (NP (N (PRO (PRP she))))
          (VP (MD can) (VP (V (VB sing))))))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody of something
===========================================================================

AGENT HEAD BENEFICIARY X THEME
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,somebody )
    (PP (PREP=token:"of" ) (NP=indirectobject,something ))))

Example: "I absolve you of this."
(S
  (CL
    (NP (N (PRO (PRP I))))
    (VP
      (V (VBP absolve))
      (NP (NP (N (PRO (PRP you)))))
      (PP (PREP (IN of)) (NP (DET this)))))
  (PUNCT .))


===========================================================================
Something ----s something Adjective/Noun
===========================================================================

AGENT HEAD BENEFICIARY THEME
(CL
  (NP=subject,something )
  (VP=head )
  (NP=directobject,something (NP )))

Example: "The shot rendered her immobile."
(S
  (CL
    (NP (DET The) (N (NN shot)))
    (VP
      (V (VBD rendered))
      (NP (N (N (PRO (POSSPRO (PRPS her)))) (N (NN immobile))))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody into V-ing something
===========================================================================

AGENT HEAD BENEFICIARY X THEME X
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,somebody )
    (PP
      (PREP=token:"into" )
      (CL (VP=gerund,indirectobject (NP=something ))))))

Example: "They talked him into writing the letter."
(S
  (CL
    (NP (N (PRO (PRP They))))
    (VP
      (V (VBD talked))
      (NP (N (PRO (PRP him))))
      (PP
        (PREP (IN into))
        (CL (VP (V (VBG writing)) (NP (DET the) (N (NN letter))))))))
  (PUNCT .))


===========================================================================
Somebody ----s something PP
===========================================================================

AGENT HEAD THEME SCOPE
(CL
  (NP=subject,somebody )
  (VP=head (NP=directobject,something ) (PP )))

Example: "She shipped everything to Alaska."
(S
  (CL
    (NP (N (PRO (PRP She))))
    (VP
      (V (VBD shipped))
      (NP (N (NN everything)))
      (PP (TO to) (NP (N (NNP Alaska))))))
  (PUNCT .))


===========================================================================
Somebody's (body part) ----s
===========================================================================

EXPERIENCER THEME HEAD
(CL
  (NP (N=somebody,possessive ) (N=subject,ont:"body_part.n.01" ))
  (VP=head ))

Example: "My arm stings."
(S
  (CL
    (NP (N (PRO (POSSPRO (PRPS My)))) (N (NN arm)))
    (VP (V (VBZ stings))))
  (PUNCT .))


===========================================================================
Somebody ----s something
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (NP=directobject,something )))

Example: "The man hit the building."
(S
  (CL
    (NP (DET The) (N (NN man)))
    (VP (V (VBD hit)) (NP (DET the) (N (NN building)))))
  (PUNCT .))


===========================================================================
Somebody ----s PP
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (PP )))

Example: "He looks under the table."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBZ looks))
      (PP (PREP (IN under)) (NP (DET the) (N (NN table))))))
  (PUNCT .))


===========================================================================
Somebody ----s
===========================================================================

AGENT HEAD
(CL (NP=subject,somebody ) (VP=head ))

Example: "He falls."
(S (CL (NP (N (PRO (PRP He)))) (VP (V (VBZ falls)))) (PUNCT .))


===========================================================================
Somebody ----s Adjective
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (ADJP=directobject )))

Example: "He sees red."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP (V (VBZ sees)) (ADJP (ADJ (JJ red)))))
  (PUNCT .))


===========================================================================
Somebody ----s something on somebody
===========================================================================

AGENT HEAD THEME LOCATION BENEFICIARY
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,something )
    (PP (PREP=token:"on" ) (NP=indirectobject,somebody ))))

Example: "He put a ring on her."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBD put))
      (NP (DET a) (N (NN ring)))
      (PP (PREP (IN on)) (NP (N (PRO (PRP her)))))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (NP=directobject,somebody )))

Example: "The man hit the woman."
(S
  (CL
    (NP (DET The) (N (NN man)))
    (VP (V (VBD hit)) (NP (DET the) (N (NN woman)))))
  (PUNCT .))


===========================================================================
Something ----s something
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,something ) (VP=head (NP=directobject,something )))

Example: "The bullet hit the wall."
(S
  (CL
    (NP (DET The) (N (NN bullet)))
    (VP (V (VBD hit)) (NP (DET the) (N (NN wall)))))
  (PUNCT .))


===========================================================================
Somebody ----s VERB-ing
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (CL (VP=directobject,gerund ))))

Example: "I remember jumping."
(S
  (CL
    (NP (N (PRO (PRP I))))
    (VP (V (VBP remember)) (CL (VP (V (VBG jumping))))))
  (PUNCT .))


===========================================================================
Somebody ----s to somebody
===========================================================================

AGENT HEAD X BENEFICIARY
(CL
  (NP=subject,somebody )
  (VP=head (PP (TO=token:"to" ) (NP=directobject,somebody ))))

Example: "He speaks to her."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP (V (VBZ speaks)) (PP (TO to) (NP (N (PRO (PRP her)))))))
  (PUNCT .))


===========================================================================
It is ----ing
===========================================================================

X X HEAD
(CL (NP=subject,token:"it" ) (VP=head,token:"is" (VP=gerund )))

Example: "It is raining."
(S
  (CL
    (NP (N (PRO (PRP It))))
    (VP (V (VBZ is)) (VP (V (VBG raining)))))
  (PUNCT .))


===========================================================================
Somebody ----s on something
===========================================================================

AGENT HEAD X THEME
(CL
  (NP=subject,somebody )
  (VP=head (PP (PREP=token:"on" ) (NP=directobject,something ))))

Example: "We clashed on gay marriage."
(S
  (CL
    (NP (N (PRO (PRP We))))
    (VP
      (V (VBD clashed))
      (PP
        (PREP (IN on))
        (NP (ADJP (ADJ (JJ gay))) (N (NN marriage))))))
  (PUNCT .))


===========================================================================
Somebody ----s something with something
===========================================================================

AGENT HEAD THEME X INSTRUMENT
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,something )
    (PP (PREP=token:"with" ) (NP=indirectobject,something ))))

Example: "The man hit the building with the hammer."
(S
  (CL
    (NP (DET The) (N (NN man)))
    (VP
      (V (VBD hit))
      (NP (DET the) (N (NN building)))
      (PP (PREP (IN with)) (NP (DET the) (N (NN hammer))))))
  (PUNCT .))


===========================================================================
Somebody ----s to INFINITIVE
===========================================================================

AGENT HEAD X THEME
(CL
  (NP=subject,somebody )
  (VP=head (CL (VP (TO=token:"to" ) (VP=infinitive )))))

Example: "They expect to move."
(S
  (CL
    (NP (N (PRO (PRP They))))
    (VP (V (VBP expect)) (CL (VP (TO to) (VP (V (VB move)))))))
  (. .))


===========================================================================
Somebody ----s something from somebody
===========================================================================

AGENT HEAD THEME X BENEFICIARY
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,something )
    (PP (PREP=token:"from" ) (NP=indirectobject,somebody ))))

Example: "He took the ring from her."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBD took))
      (NP (DET the) (N (NN ring)))
      (PP (PREP (IN from)) (NP (N (PRO (PRP her)))))))
  (PUNCT .))


===========================================================================
Something ----s Adjective/Noun
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,something ) (VP=head (ADJP=directobject )))

Example: "The turtle turns red."
(S
  (CL
    (NP (DET The) (N (NN turtle)))
    (VP (V (VBZ turns)) (ADJP (ADJ (JJ red)))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody something
===========================================================================

AGENT HEAD BENEFICIARY THEME
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,somebody )
    (NP=indirectobject,something )))

Example: "He gave her a ring."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBD gave))
      (NP (N (PRO (PRP her))))
      (NP (DET a) (N (NN ring)))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody INFINITIVE
===========================================================================

AGENT HEAD BENEFICIARY THEME
(CL
  (NP=subject,somebody )
  (VP=head (NP=directobject,somebody ) (VP=infinitive )))

Example: "We require our secretary be on time."
(S
  (CL
    (NP (N (PRO (PRP We))))
    (VP
      (V (VB require))
      (NP (N (PRO (POSSPRO (PRPS our)))) (N (NN secretary)))
      (VP (V (VB be)) (PP (PREP (IN on)) (NP (N (NN time)))))))
  (PUNCT .))


===========================================================================
Somebody ----s something to somebody
===========================================================================

AGENT HEAD THEME X BENEFICIARY
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,something )
    (PP (TO=token:"to" ) (NP=indirectobject,somebody ))))

Example: "He gave the ring to her."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBD gave))
      (NP (DET the) (N (NN ring)))
      (PP (TO to) (NP (N (PRO (PRP her)))))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody PP
===========================================================================

AGENT HEAD THEME SCOPE
(CL
  (NP=subject,somebody )
  (VP=head (NP=directobject,somebody ) (PP )))

Example: "She sent her kids to camp."
(S
  (CL
    (NP (N (PRO (PRP She))))
    (VP
      (V (VBD sent))
      (NP (N (PRO (POSSPRO (PRPS her)))) (N (NNS kids)))
      (PP (TO to) (NP (N (NN camp))))))
  (PUNCT .))


===========================================================================
Something ----s INFINITIVE
===========================================================================

AGENT HEAD X THEME
(CL (NP=subject,something ) (VP=head (VP=directobject,infinitive )))

Example: "This helps prevent accidents."
(S
  (CL
    (NP (DET This))
    (VP
      (V (VBZ helps))
      (VP (V (VB prevent)) (NP (N (NNS accidents))))))
  (PUNCT .))


===========================================================================
Something ----s
===========================================================================

AGENT HEAD
(CL (NP=subject,something ) (VP=head ))

Example: "The ball falls."
(S (CL (NP (DET The) (N (NN ball))) (VP (V (VBZ falls)))) (PUNCT .))


===========================================================================
Something ----s somebody
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,something ) (VP=head (NP=directobject,somebody )))

Example: "The bullet hit the man."
(S
  (CL
    (NP (DET The) (N (NN bullet)))
    (VP (V (VBD hit)) (NP (DET the) (N (NN man)))))
  (PUNCT .))


===========================================================================
Somebody ----s somebody with something
===========================================================================

AGENT HEAD THEME X INSTRUMENT
(CL
  (NP=subject,somebody )
  (VP=head
    (NP=directobject,somebody )
    (PP (PREP=token:"with" ) (NP=indirectobject,something ))))

Example: "He hit her with the hammer."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP
      (V (VBD hit))
      (NP (N (PRO (PRP her))))
      (PP (PREP (IN with)) (NP (DET the) (N (NN hammer))))))
  (PUNCT .))


===========================================================================
It ----s that CLAUSE
===========================================================================

AGENT HEAD X THEME
(CL (NP=subject ) (VP=head (PP (PREP=token:"that" ) (CL ))))

Example: "She proved that she could jump high."
(S
  (CL
    (NP (N (PRO (PRP She))))
    (VP
      (V (VBD proved))
      (PP
        (PREP (IN that))
        (CL
          (NP (N (PRO (PRP she))))
          (VP (MD could) (VP (V (VB jump)) (ADJP (ADJ (JJ high)))))))))
  (PUNCT .))


===========================================================================
Somebody ----s INFINITIVE
===========================================================================

AGENT HEAD THEME
(CL (NP=subject,somebody ) (VP=head (VP=directobject,infinitive )))

Example: "I dared not jump."
(S
  (CL
    (NP (N (PRO (PRP I))))
    (VP (V (VBD dared)) (RB not) (VP (V (VB jump)))))
  (PUNCT .))


===========================================================================
Something is ----ing PP
===========================================================================

AGENT X HEAD THEME
(CL (NP=subject,something ) (VP=head,token:"is" (VP=gerund (PP ))))

Example: "The ball is falling on the table."
(S
  (CL
    (NP (DET The) (N (NN ball)))
    (VP
      (V (VBZ is))
      (VP
        (V (VBG falling))
        (PP (PREP (IN on)) (NP (DET the) (N (NN table)))))))
  (PUNCT .))


===========================================================================
Something ----s to somebody
===========================================================================

AGENT HEAD X THEME
(CL
  (NP=subject,something )
  (VP=head (PP (TO=token:"to" ) (NP=directobject,somebody ))))

Example: "He looks to her."
(S
  (CL
    (NP (N (PRO (PRP He))))
    (VP (V (VBZ looks)) (PP (TO to) (NP (N (PRO (PRP her)))))))
  (PUNCT .))


