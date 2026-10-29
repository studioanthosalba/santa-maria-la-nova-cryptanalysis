# Phase 2 -- attacks

Targets: `palma_B` (678 glyphs, the most complete reading) and `palma_A` (584 glyphs, the only reading with word boundaries).

## Self-test: can the attack break a known cipher?

| encrypted control text | score reached | score of the true plaintext | IC recovered | IC plaintext | recovered head | true head |
|---|---|---|---|---|---|---|
| Latin (Vulgate) | -10.4610 | -10.4610 | 0.0732 | 0.0732 | oblatioinves | oblatioinves |
| Czech (Bible Kralicka 1613) | -9.9910 | -9.9910 | 0.0595 | 0.0595 | dechjejichpo | dechjejichpo |
| Italian (Riveduta) | -10.1050 | -10.1050 | 0.0792 | 0.0792 | iornostessoc | iornostessoc |

A substitution preserves the IC exactly, so the IC cannot separate true from false solutions; the informative column is the score reached.  If the solver approaches the score of the true plaintext on control texts of this very length, then its behaviour on the epigraph is evidence about the epigraph rather than about the solver.

## palma_B -- are some glyphs nulls?

| text | best single-glyph IC gain | glyph |
|---|---|---|
| epigraph `palma_B` | 0.0071 | `δ` |
| control: substitution, no nulls (mean of 25) | 0.0058 | - |
| control: substitution + 10% nulls (mean of 25) | 0.0045 | - |

p(best gain >= observed | no nulls) = **0.0769**. A null hypothesis is supported only if deleting the supposed null glyph recovers an IC close to the language value, which is what the nulled control shows and the epigraph does not.

### Control: a text that really has nulls

| stage | IC | length |
|---|---|---|
| original plaintext | 0.0742 | 678 |
| after substitution | 0.0742 | 678 |
| substitution + 15% nulls | 0.0661 | 779 |
| nulls, greedy stripping step 1 | 0.0709 | 726 |
| nulls, greedy stripping step 3 | 0.0826 | 620 |
| no nulls, greedy stripping step 1 | 0.0803 | 626 |
| no nulls, greedy stripping step 3 | 0.0956 | 527 |

Greedy stripping always inflates the IC a little, which is why an increase alone is not evidence of nulls; the calibrated comparison is with this control.

## Do the names of the legend work as polyalphabetic keys?

| key | IC after decryption | trigram repeat | random-key mean | p |
|---|---|---|---|---|
| VLAD | 0.0521 | 0.1300 | 0.1220 | 0.2394 |
| DRACULA | 0.0485 | 0.0960 | 0.1030 | 0.6808 |
| TURBOLO | 0.0469 | 0.0810 | 0.1010 | 0.9601 |
| MARIA | 0.0524 | 0.1350 | 0.1280 | 0.2868 |
| BALSA | 0.0509 | 0.1140 | 0.1310 | 0.9252 |
| FERRILLO | 0.0487 | 0.0860 | 0.0810 | 0.3591 |
| NAPOLI | 0.0499 | 0.0920 | 0.1060 | 0.8828 |
| IESUS | 0.0506 | 0.1480 | 0.1290 | 0.0848 |

The undecrypted text has IC 0.0813 and trigram repeat 0.272; the language range is IC ~ 0.073 and trigram repeat ~ 0.5.  None of the keys brings the decrypted text into that range, and the smallest p-value among them is 0.0848 (key `IESUS`), i.e. indistinguishable from a random key of the same length.

## Simulated-annealing attack on the substitution hypothesis

| reading | language model | score reached | shuffled baseline | natural-text level | Latin words | plaintext head |
|---|---|---|---|---|---|---|
| palma_B | Latin | -13.4520 | -13.9980 | -10.0920 | 6 | ecrveirtissveatdebnidadmir |
| palma_B | Czech | -13.5450 | -13.9980 | -10.2910 | 5 | nzdynadiaooyneimnhtamemjad |
| palma_B | Italian | -13.4310 | -13.9980 | -9.8110 | 6 | icnvienterrviatpiudepapmen |
| palma_A | Latin | -13.5770 | -13.9330 | -10.5670 | 3 | ultisetlijalsempitetcmrenl |
| palma_A | Czech | -13.6280 | -13.9560 | -10.4690 | 3 | vdosleodsyidlembsoeokmhend |
| palma_A | Italian | -13.5450 | -13.9490 | -9.9540 | 4 | ntcerictemotridqecicudgilt |

`score reached` is the mean 5-gram log-probability per window after the search; `shuffled baseline` is what the same glyph multiset scores in random order; `natural-text level` is what a genuine text of the same language and length scores.  A successful attack must land near the natural-text level.

Best candidates in full (line breaks every 40 glyphs, for legibility only):

```
palma_B | Latin (Vulgate):
  ecrveirtissveatdebnidadmirteeseisernietd
  siztsnasuqhearravitisiaegsieieniesxinaiq
  lrxlignahisxunlbleixeetslhinumetabeilctu
  fmegeineaenetiscoxseiganerezateniguvhivb
  iluvbgvntitmvusiamascacorteeinuvldisacet
  evbjectvldscieagvpieanipdeinulotheapoifa
  pievdlinaveupesaiepdechritnaxeeadifpsmas
  lipieqnaxevcaeuciacfanetesplpioahmpfaise
  ciauamurazjuiecaduoitacnreeramipafedcloi
  csnonacpadteneieadeeaplariiocvdaromarepr
  sulustiovcfnpiaeuepsrnaculoanciequaleraa
  pblaelbieifdontesdeoiteueuxecitsdemaetiu
  cxteioaeateetsetearepcfdseceeaeteteaeaei
  psieasetxslecxaetiaecbmlsxtfinesmiliaxta
  tobsteaiemaraetbseeahebsdvmirseirexerisi
  lbmateqasaliuuiixleadsbfaesliaeeaaeitete
  ameisfeadpiucsxoieacapacauppbareeainma

palma_B | Czech (Bible Kralicka 1613):
  nzdynadiaooyneimnhtamemjadinnonaondtanim
  oacioteokpfneddeyaiaoaenboanantanovateap
  udvuabtefaovktuhunavnnioufatkjniehnauzik
  sjnbnatnentniaozrvonabetndnceintabkyfayh
  aukyhbytiaijykoaejeozezrdinnatkyumaoezni
  nyhxnziyumozanebylanetalmnatkurifnelrase
  lanymuateynklnoeanlmnzfdaitevnnemaslojeo
  ualanptevnyzenkzaezsetninolularefjlseaon
  zaekejkdecxkanzemkraieztdnndejalesnmzura
  zotrtezlemintnanemnneluedaarzymedrjednld
  okukoiaryzstlaenknlodtezkuretzanpkeundee
  lhuenuhanasmrtinomnrainknkvnzaiomnjeniak
  zvinareneinnioninednlzsmonznnenininenena
  loaneonivounzveniaenzhjuovisatnojauaevie
  irhoineanjedenihonnefnhomyjadonadnvndaoa
  uhjeinpeoeuakkaavunemohsenouaenneenainin
  ejnaosnemlakzovranezelezekllhednneatje

palma_B | Italian (Riveduta):
  icnvienterrviatpiudepapmentiirierindeitp
  rebtrdarofgiannavetereaizreieideirhedaef
  snhsezdagerhodsusiehiitrsgedomitauiescto
  amiziediaiditercehriezadinibatidezovgevu
  esovuzvdtetmvoreamarcacentiiedovsperacit
  ivuqictvsprceiazvleiadelpiedosetgialeeaa
  leivpsedavioliraeilpicgnetdahiiapealrmar
  seleifdahivcaioceacaaditirlsleeagmlaaeri
  ceaoamonabqoeicapoeetacdniinamelaaipcsee
  crdedaclaptidieiapiialsaneeecvpanemaniln
  rosorteevcadleaioilrndacoseadceifoasinaa
  lusaisueieapedtirpieetioiohicetrpimaiteo
  chtieeaiatiitritianilcapriciiaititiaiaie
  lreiarithrsichaiteaicumsrhtaedirmeseahta
  teurtiaeimanaituriiagiurpvmenrienihinere
  sumatifaraseooeehsiapruaairseaiiaaietiti
  amieraiapleocrheeiacalacaolluaniiaedma

palma_A | Latin (Vulgate):
  ultisetlijalsempitetcmrenltemvsratcumiam
  osfeleazzteezmztberaezvmvezhametqsrvjvie
  qsnfvmehcuizajievubsnevzhizeougqtiedomim
  ozihedctmetjevcfjifrsezfcteosatuaugxjier
  cfvletaudfjxiuzfvltuecadfzenasrenliercvg
  zyiangebanesfmverodficndtaeinlisyxezrobi
  solebntufotveneigrabntuaicueoubariitnvne
  goysnboetiueoconocpamxseiualcgenaurximos
  enobiluvgeutrgrosnolirneiolionvoxeegutlo
  gsomintcvctegfubrneosinfyraucvgorueicuov
  imaanjxasvjeieblgritlgezgccqiuptlipjtego
  sansdominubltsodenteiopjtviuoeoiujsfberp
  sexeoqogjsoeisomodnjjtlfsemtdemmeevjcoin
  cttovesceeqtstltjbaveoiioosesosieubiolne
  cstgedodonasacnnjamierso

palma_A | Czech (Bible Kralicka 1613):
  vdosleodsyidlembsoeokmhendoemzlhiokvmsim
  aluedeiccoeecmcojehieczmzecximeoplhzyzse
  plnuzmexkvsciysezvjlnezcxsceavtposeramsm
  acsxerkomeoyezkuysuhlecukoealiovivtfyseh
  kuzdeoivruyfsvcuzdovekirucenilhendsehkzt
  cgsintejinelumzeharusknroiesndslgfechajs
  ladejnovuaozenesthijnoviskveavjihssonzne
  taglnjaeosveakanakbimflesvidktenivhfsmal
  enajsdvztevohthalnadshnesadsanzafeetvoda
  tlamsnokzkoetuvjhnealsnughivkztahveskvaz
  smiinyfilzyesejdthsodtectkkpsvbodsbyoeta
  linlramsnvjdolarenoesabyozsvaeasvylujehb
  lefeapatylaeslamarnyyodulemoremmeezykasn
  kooazelkeepolodoyjizeassaalelalsevjsadne
  kloteraraniliknnyimsehla

palma_A | Italian (Riveduta):
  ntcerictemotridqecicudgiltcidsrgocundeod
  arzitiobbciibdbcpigoibsdsibeodicurgsmsei
  urlzsdieunebomeisnprlisbeebianfuceivaded
  abeeivucdicmisuzmezgribzuciarocnonfhmeig
  uzsticonvzmhenbzstcniuovzbilorgilteigusf
  bdeolfipolirzdsigavzeulvcoielterdhibgape
  ratiplcnzacsiliefgoplcnoeunianpogeeclsli
  fadrlpaiceniaualauqodhrienotufilonghedar
  ilapetnsfincgfgarlateglieatealsahiifncta
  fradelcusucifznpgliarelzdgonusfagnieunas
  edoolmhorsmieiptfgectfibfuuuenqcteqmcifa
  rolrvadelnptcravilcieaqmcsenaiaenmrzpigq
  rihiauafmraieradavlmmctzridcviddiismuael
  uccasiruiiucrctcmposiaeeaarirareinpeatli
  urcfivavaloroullmodeigra

```

## Vowel-in-clear attack on the photograph-validated reading

Le lettere che *sembrano* vocali (A, E, I, O, V/U) si comportano come vocali: con quell'insieme la quota C3 scende a 0.028, valore naturale. Se il cifrario lascia leggibili le vocali, restano da risolvere solo le consonanti: si prova quindi la scala 2->5 grammi con le vocali inchiodate.

| lettura | modello | vocali fissate | punteggio | testo prodotto (primi 60 glifi) |
|---|---|---|---|---|
| gemini_full | Latin | 5 | -13.5630 | uauiouiraoanemoduasvouaiuaaeiurauaaaooadaaodnoodiiamouaoeame |
| gemini_full | Czech | 5 | -13.6660 | uauiouivaoaledotuansouaiuaaeiuvauaaaooataaotlootiiadouaoeade |
| gemini_full | Italian | 5 | -13.5110 | uauiouiraoanemoluasdouaiuaaeiurauaaaooalaaolnooliiamouaoeame |
| gemini_central | Latin | 5 | -13.3490 | meumiuuonuabmiauobeaiattoxohiuaveniameioairauehaedeosauieraz |
| gemini_central | Czech | 5 | -13.5010 | veuviuuomuatviauoteaiannohojiuazemiaveioaipauejaeseodauiepak |
| gemini_central | Italian | 5 | -13.2340 | teutiuuoquantiauoneaialloropiuabeqiateioaicauepaeseodauiecav |

Per confronto, il punteggio di un testo reale della stessa lunghezza è circa -10 e quello di una permutazione casuale circa -14.

```
gemini_full | Latin (Vulgate):
  uauiouiraoanemoduasvouaiuaaeiurauaaaooad
  aaodnoodiiamouaoeameaoduauoamiuaiianomin
  iasuoueiieadeovimivdociueoaitmarodaueuan
  ruuieauoaroneasamiocainsvaiaiaitpriouisa
  uosaidiarujiiassuasioeadaseobaiuonuiouec
  tuurantofabonauuouairvenisaoreuriuuonuam
  rnauomeaiaassolojiuageniareioaifauejaexe
  otauiefayxrioaaieauuioriauitonaiuuruaiol
  amtuictoisutuailaculioraralsauootisuatia
  uresesesotsimulioairiauuaiiatauiorviaceu
  aanquaiairoriofuturautoetitefrqcauriedot
  aianiiaurmuasgaenaiobaoramuiiasoajdieamo
  iophamatoriauarauaiouiouuoogdanaanovieha
  isuanimanoarraionadjosamraunoiatoiaianai
  abrauouia

gemini_full | Czech (Bible Kralicka 1613):
  uauiouivaoaledotuansouaiuaaeiuvauaaaooat
  aaotlootiiadouaoeadeaotuauoadiuaiialodil
  ianuoueiieateosidistopiueoaimdavotaueual
  vuuieauoavoleanadiopailnsaiaiaimfviouina
  uonaitiavuhiiannuanioeataneokaiuoluiouep
  muuvalmojakolauuouaivselinaoveuviuuoluad
  vlauodeaiaannocohiuareliaveioaijauehaeye
  omauiejabyvioaaieauuioviauimolaiuuvuaioc
  admuipmoinumuaicapuciovavacnauoominuamia
  uvenenenomniducioaiviauuaiiamauiovsiapeu
  aalxuaiaivoviojumuvaumoemimejvxpauvietom
  aialiiauvduanraelaiokaovaduiianoahtieado
  iofzadamoviauavauaiouiouuoortalaalosieza
  inualidaloavvaiolathonadvauloiamoiaialai
  akvauouia

gemini_full | Italian (Riveduta):
  uauiouiraoanemoluasdouaiuaaeiurauaaaooal
  aaolnooliiamouaoeameaoluauoamiuaiianomin
  iasuoueiiealeodimidlopiueoaitmarolaueuan
  ruuieauoaroneasamiopainsdaiaiaithriouisa
  uosailiarugiiassuasioealaseovaiuonuiouep
  tuurantoqavonauuouairdenisaoreuriuuonuam
  rnauomeaiaassocogiuabeniareioaiqauegaeze
  otauieqavzrioaaieauuioriauitonaiuuruaioc
  amtuiptoisutuaicapucioraracsauootisuatia
  uresesesotsimucioairiauuaiiatauiordiapeu
  aantuaiairorioquturautoetiteqrtpaurielot
  aianiiaurmuasbaenaiovaoramuiiasoaglieamo
  iohfamatoriauarauaiouiouuooblanaanodiefa
  isuanimanoarraionalgosamraunoiatoiaianai
  avrauouia

gemini_central | Latin (Vulgate):
  meumiuuonuabmiauobeaiattoxohiuaveniameio
  airauehaedeosauierazdmioaaieauuiomiauiso
  naiuumuaiolabsuicsoitusuailaculiomamalta
  uoosituasiaumetetetostibulioaimiauuaiias
  auio

gemini_central | Czech (Bible Kralicka 1613):
  veuviuuomuatviauoteaiannohojiuazemiaveio
  aipauejaeseodauiepaksvioaaieauuioviauido
  maiuuvuaiolatduibdoinuduailabuliovavalna
  uoodinuadiauvenenenodnitulioaiviauuaiiad
  auio

gemini_central | Italian (Riveduta):
  teutiuuoquantiauoneaialloropiuabeqiateio
  aicauepaeseodauiecavstioaaieauuiotiauido
  qaiuutuaiomanduigdoiluduaimagumiotatamla
  uoodiluadiautelelelodlinumioaitiauuaiiad
  auio

```

## palma_A -- crib search by isomorphy

38 of the cribs were skipped because all their letters are distinct: their pattern is shared by every token of the same length with all-distinct glyphs, so they carry no information.

| language | crib | pattern | isomorphic tokens |
|---|---|---|---|
| Latin | anima | ABCDA | `ntpjn` |
| Latin | filius | ABCBDE | `mrdrpv` |
| Latin | domini | ABCDED | `zmlfpf`, `outnmn` |
| Czech | hriech | ABCDEA | `ircbli` |

Isomorphy is only a *necessary* condition: a crib becomes credible only when several matches imply one single consistent glyph-to-letter mapping.

## The 'Greek vowel' hypothesis (Palma's Greek-labelled reading)

| quantity | value |
|---|---|
| Greek vowel glyphs present | α, ε, η, ι, υ, ω |
| their share of the text % | 33.2000 |
| C3 share under this assignment | 0.4454 |
| mean consonant run | 2.5400 |
| longest consonant run | 9 |

Natural languages keep the C3 share below about 0.10; a much larger value means the Greek letter shapes are not being used as the vowels of the plaintext.

