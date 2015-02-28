# lsext

### file format distribution analyzer

## 0.1.3 -- feb 21, 2015

1. employed str.lower since \`.pdf' and \`.PDF' should be the regarded as the same extension.
   and assumed that all extensions' cases should be insignificant.

2. changed function names: \`compose_function' to \`fcompose', \`map_function' to \`fmap'.

## 0.1.2 -- feb 20, 2015

1. completed the refactoring in the core function, \`get_all_info'.

## 0.1.1 -- feb 19, 2015

1. changed to returning chained generators, instead of a list reduced from a list of lists;
   in the the core function \`get_all_info'.

2. please refactor the core function \`get_all_info', such that,
   you can just collect the information specified by the extracting function which is provided as one of the arguments to \`get_all_info'.
   but now i am too exhausted. i have to sleep. let's fix it tomorrow.

3. happy chinese new year! am i a hard-working and responsible employee, one who still keeps coding to deep night even in the new year's day.

## 0.1.0 -- feb 14, 2015

1. rewritten from scratch, using os.walk instead of using recursive os.listdir.

2. added size and number distribution analysis.

3. likely to add the feature of recognizing files based upon their magic numbers rather than the suffixes.
   obviously, this feature will cost more time.

## 0.0.2 -- jan 28, 2015

3. added argument parser and the count functionality (\`-c' switch), just like \`find -type f -name *.pdf | wc -l'.

## 0.0.1 -- jan 2 2015

1. symbolic links will be followed by python's default. no switch to choose currently.

2. \`os.walk' is preferred in next version.
