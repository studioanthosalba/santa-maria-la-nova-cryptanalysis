
<p align="center">
  <img src="picsreadme/malanova.svg" alt="malanova" width="80%"/>
</p>

This codebase has been developed to power the following research paper:

Palma, C. (2023). Encrypted epigraphy: The case of a mysterious inscription in the Neapolitan church of Santa Maria La Nova. Proceedings of the 6th International Conference on Historical Cryptology HistoCrypt 2023, 139–147. Published on May 30, 2023.

If you are using it for publication purposes, please use the provided citation.

The main available tool for deciphering historical ciphers is currently [CrypTool 2](https://www.cryptool.org/en/ct2/).
It offers a wide choice of de- and encryption algorithms in a beautiful and interactive User Experience.
**Although the provided clear-text languages are updated at every release, they are fix and not customizable.
The major added value of this contribution is providing a workflow for generating n-grams files from customized historical corpora.**


A notable source for downloading historical corpora is [HistCorp](https://www2.lingfil.uu.se/person/pettersson/histcorp/).

<p align="center">
  <img src="picsreadme/histcorp.png" alt="histcorp" width="80%"/>
</p>

The choice can be supported by calculating the Friedman's [Index of Coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence) on the encrypted text.

<p align="center">
  <img src="picsreadme/ioc.png" alt="ioc" width="20%"/>
</p>

The corpus with the most similar Index of Coincidence would be a good candidate for further attacks. This can be easily performed by the function:

<p align="center">
  <img src="picsreadme/generateIOCcorpus.png" alt="generateIOCcorpus" width="70%"/>
</p>

Another possibility would be the AZdecrypt integrated function ”Languages” -> select ”File” -> ”Batch n-grams (substitution)” -> open ”Languages.azd” under ”Languages”.

<p align="center">
  <img src="picsreadme/AZdecrypt.png" alt="AZdecrypt" width="80%"/>
</p>

To include in the chi-squared test the customized languages/corpora, the "languages.azd" file should be placed in the AZdecrypt\N-grams\N-gram normalization\ folder and can be edited to include them. Look at the other normalization files in that folder as to how your data should look. 

After selecting an historical corpus, it is necessary to pre-process it. The present codebase provides also functions to achieve this (cleaning, removing spaces, removing special characters, ecc.) in the module "NLP.py". The following function performs then the transformation into a N-Grams file suitable for AZDecrypt.

<p align="center">
  <img src="picsreadme/ngramsAZ.png" alt="ngramsAZ" width="80%"/>
</p>

The output file will enlist each N-gram immediately followed by its log value, a number between
0 and 255 obtained by:

<p align="center">
  <img src="picsreadme/logten.png" alt="logten" width="40%"/>
</p>

All N-grams followed by ”000” could be removed. The GUI library used for AZdecrypt
does not support Unicode. Hence, only languages
that can be represented in ASCII are visually
supported. A workaround for this problem is
substituting Unicode with ASCII and then providing a ASCII to Unicode mapping table in the
n-gram .ini file. The .ini format is used for simple
text files containing initialization parameters. In
AZdecrypt, it accompains in the ”Ngrams” folder
every N-gram file. Its appearance for Persian, a
language not supported by Unicode, is:

N-gram size=b5

N-gram factor=90.11

Entropy weight=1

Alphabet=#<*)576%4$

,3:-+?1;0(2&"!8’/.>9=

Temperature=700


, whereby in the first line the ”b” stands for ”binary”12. It should be deleted for all non-binary
formatted N-grams files. The alphabet line shall
contain all characters present in the related N-
grams file. The temperature variable refers to
the probability of accepting a modification with a
lower fitness. It continuously decreases, emulating
the process of annealing in metallurgy, therefore
the name.
The strategy adopted in my study to avoid unsupported characters is transposing the corpus into
Latin characters before generating the N-grams
file. This is achieved by the functions contained
into the file ”Replace.py”, and at the state of the
art are available for Greek, Coptic and Cyrillic.
Other alphabets can be mapped easily following
the same model used for the other ”Replace” functions.

<p align="center">
  <img src="picsreadme/AZdecrypttable.png" alt="AZdecrypttable" width="100%"/>
</p>

As you can notice from the overwiew above, the AZDecrypt environment is quite intutive to use as well. After pasting the encrypted text in the window on the left and selecting a decryption method from the menu-list, you have to select a candidate language from:

File -> Load N-Grams,

then click "Solve".

Enjoy decryption!
