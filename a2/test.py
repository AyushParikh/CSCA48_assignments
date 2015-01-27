from regex_functions import *

# This test case (by Chengyu (Tyrone) Xiong on the forums)
# takes around 11 seconds to run using my program
# Other people's programs never finish running at all
from timeit import timeit
print(timeit('all_regex_permutations("(1*|e*.(2)).0()**")',
             'from regex_functions import all_regex_permutations',
             number=1))
# Check for correctness
print(len(all_regex_permutations("(1*|e*.(2)).0()**")) == 75600)

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

# Another hard test cast by G Kala
# Hits the maximum recursion depth for most people's programs (but not mine)
print(regex_match(StarTree(DotTree(StarTree(DotTree(StarTree(Leaf('0')), StarTree(Leaf('1')))), StarTree(Leaf('2')))), '0122121212212120121021021210212010000101001020102001020210201020101001000102212200010101002010120120201010210102012020202021010010120010201201202102102100120120012012010102012001200120010110101000101021020101201012021001021012021021021021021021210210210210210210210210210210210210111021012020102021102012022102021021210211021021021021021021021021021021022102102102102122102102102101221021021021021021021210210210210210210210211121212121221212111111111111111111222222222222222220000000000000000001111111111111222222222222222100000000000000000000000000000000000000000000111111111111122222222222222222210210201021012012012012012020102021012012012012002012012012012012012012012021012012021012012012012012012012012012012012012001201201212102112012012012012010120120212102101212021002102102000012121212212120012001100000101010101010101010100102102020202020202102102102100101010011010201212012210120102102102102102202021021021020121021002020210210210212121002102102102021021021210021002102102102100212100201021021210021022002020220102102102000121210012102010102012021021021021212121212100212212121000212121212121002121212112212000021122121212212121212212121000122112121121221212212121212121212121211221000012121202001200212001201200202012112012010121021012010201001201010210021022120110202020202020210101022012010202102022102102021021202102102102210210210210211221021201210212102121021212012020112101212121201212121') == True)
