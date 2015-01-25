#from timeit import timeit

#print(timeit('all_regex_permutations("(1*|e*.(2)).0()**")',
             #'from regex_functions import all_regex_permutations',
             #number=1))

from regex_functions import *

# Extra test cases from a forum post by Wilbur Hsu
print('\nis_regex extra tests:')
print(is_regex('((1.(0|2)*).((1*.(2.e*))*.0))') == True)
print(is_regex('(((0*.(0|e)*)*.(((1.e*))*.0)).0)') == False)
print(is_regex('((0*.(0**|e)*)*.(((0*|(1.e*))*.0)**.1*))') == True)
print(is_regex('(((0*.(0**|e)*)*.(((0*|(1.e*))*.0)**.1*)).'
               '((2*.(0*|1*)).(((0*|(2*.e*))*.0)**.e*)))') == True)
print(is_regex('(((0*.(0**|e)*)*.(((0*|(1.e*))*.0)*.1*)*)).'
               '((2*.(0*|1*)).(((0*|(2*.e*))*.0)**.e*)))') == False)
print(is_regex('((1.(1*|(0|e**))*.(0*|(1.e*))*.0)*.1)).'
               '((2*.(0*)).(((0*|(2*.e*))*.0)**.e*)))') == False)

# Extra test cases from a formum post by G Kala
print('\nregex_match extra tests:')
print(regex_match(Leaf('1'), '1') ==  True)
print(regex_match(Leaf('1'), '10') ==  False)
print(regex_match(Leaf('e'), '') ==  True)
print(regex_match(Leaf('0'), '0') ==  True)
print(regex_match(Leaf('0'), '1') ==  False)
print(regex_match(StarTree(Leaf('0')), '') ==  True)
print(regex_match(StarTree(Leaf('0')), '000') ==  True)
print(regex_match(StarTree(Leaf('0')), '000010') ==  False)
print(regex_match(BarTree(Leaf('1'), StarTree(Leaf('0'))), '1') ==  True)
print(regex_match(BarTree(Leaf('1'), StarTree(Leaf('0'))), '0000') == True)
print(regex_match(BarTree(Leaf('1'), StarTree(Leaf('0'))), '01') ==  False)
print(regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '0') ==  True)
print(regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '111110') == True)
print(regex_match(DotTree(StarTree(Leaf('1')), Leaf('0')), '1') ==  False)