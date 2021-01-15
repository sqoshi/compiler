#!/usr/bin/bash

red='\033[0;31m'
blue='\033[0;34m'
green='\033[0;32m'
reset='\033[0m'

for dir in "$2"*; do
  for prog in ${dir}/*.imp; do
    python "$1" ${prog} "compiled_program.txt"
    for data in ${dir}/input*.txt; do
      result=${data/input/output}
      # shellcheck disable=SC2006
      restxt=$(./"$3" compiled_program.txt <${data})
      sample_cost=$(echo "$restxt" | tail -1 | grep -oP '\(\K[^\)]+' | sed "s/^[^ ]* //")
      echo "$restxt" | grep -E ">" | grep -Eo "[[:digit:]]*" >"program_output.txt"
      if ! cmp "program_output.txt" ${result} >/dev/null 2>&1; then
        echo -e "${red}Error in test ${dir} for input ${data} ${reset}"
        echo "Correct output:"
        cat ${result}
        echo "Generated output:"
        cat "program_output.txt"
      else
        echo -e "${green}Test ${blue}${prog##*/} ${green}passed for input ${data##*/} in time ${blue}${sample_cost}${green}.${reset}" | sed -e 's/; w tym/,/' #>> results.txt
      fi
    done
  done
done

