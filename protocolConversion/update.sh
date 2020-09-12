for file in `\find rule_json -name '*.json'`; do
  #echo $file
  fname=`echo $file|gsed -E 's/^rule_json\/(\w+)\.json$/\1/g'`
  #echo $fname
  `./json_parser.out $file ./commands/$fname.txt`
  
done