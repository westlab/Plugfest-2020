for file in `\find rule_json -name '*.json'`; do
  fname=`echo $file|sed -E 's/^rule_json\/(\w+)\.json$/\1/g'`
  `./json_parser.out $file ./commands/$fname.txt`
  
done
