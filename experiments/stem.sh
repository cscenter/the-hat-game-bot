mystem -nlid --eng-gr all_mid_utf8.txt | sed 's/\([а-я]*\)=\([A-Z]*\).*$/\1_\2/' | sed 's/\(.*\)??/\1_?/' | sed 's/^[^_]*_\([^SA]\|.\{2,\}\)$//' | tr '\n' ' ' > all_mid_utf8_stemmed.txt
