#-----------------------------------------------------------------------------------------
#
#    Generate plainttext password for WPA2
#
#
#-----------------------------------------------------------------------------------------
# https://www.geeksforgeeks.org/element-wise-concatenation-of-two-numpy-arrays-of-string/
# np.char.add(first_name, last_name)
#-----------------------------------------------------------------------------------------

import numpy as np
from time import perf_counter



charlist = "!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
arr_char = np.array([k for k in charlist])
arr_char.shape      # 92


#-----------------------------------------------------------------------------------------
### if using string dtype
# arr_char = np.array([k for k in charlist], dtype='S')
# arr_char.tostring().decode('utf-8')

# join as single string
arr_two[7195].astype('|S1').tostring().decode('utf-8')

#-------------------------------------------
# TEST - generate columns
arr_two = np.column_stack((np.repeat(arr_char, arr_char.shape[0]), np.tile(arr_char, arr_char.shape[0]) ))

arr_three = np.column_stack( (np.repeat( arr_char, arr_two.shape[0]),
                              np.tile( arr_two, (arr_char.shape[0],1))
                              ))

arr_four = np.column_stack( (np.repeat( arr_char, arr_three.shape[0]),
                             np.tile( arr_three, (arr_char.shape[0],1))
                             ))
#-------------------------------------------


# 2-char
arr_out = np.column_stack((np.repeat(arr_char, arr_char.shape[0]), np.tile(arr_char, arr_char.shape[0]) ))

# 4-char output [DO NOT GO MORE - size memory explosion ]
for k in range(2):
    arr_out = np.column_stack( (np.repeat( arr_char, arr_out.shape[0]),
                                np.tile( arr_out, (arr_char.shape[0],1))
                                ))

arr_out[7164595].astype('|S1').tostring().decode('utf-8')


arr_join = arr_out[:,0]

for i in range(2):
    arr_join = np.char.add(arr_join, arr_out[:,i+1])


#-------------------------------------------
# TEST - slice to smaller
wawa = arr_out[7164595:7164599]
gaga = wawa[:,0]

for i in range(3):
    gaga = np.char.add(gaga, wawa[:,i+1])
#-------------------------------------------


#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

### what if just add successively?

arr_add = np.char.add( np.repeat(arr_char, arr_char.shape[0]),
                       np.tile(arr_char, arr_char.shape[0])
                       )
for k in range(2):          # 4-char output [DO NOT GO MORE - size memory explosion ]
    print(f'size: {arr_add.shape[0]:,}')
    arr_add = np.char.add( np.repeat( arr_char, arr_add.shape[0]),
                           np.tile( arr_add, (arr_char.shape[0]))
                           )




#-----------------------------------------------------------------------------------------
#-------------------------------------------
# FINAL
#-------------------------------------------
arr_add = arr_char

t_start = perf_counter()
for k in range(3):          # 4-char output [DO NOT GO MORE - size memory explosion ]
    print(f'size: {arr_add.shape[0]:,}', end="\t")
    arr_add = np.char.add( np.repeat( arr_char, arr_add.shape[0]),
                           np.tile( arr_add, (arr_char.shape[0]))
                           )
    t_int = perf_counter()
    print(f"Time taken for loop {k}: {t_int - t_start:.3f} seconds")
else:
    print(f'size: {arr_add.shape[0]:,}' +
          f'\n\n{arr_add[7164695:7164699]}' +
          '\n\n  END\n')

t_end = perf_counter()
print(f"Time taken: {t_end - t_start:.3f} seconds")


arr_add.shape # (71639296,)

#------------------------------
# loop through the following line one by one to join into 8 char

# lala = np.char.add( np.repeat( np.array(arr_add[0]), arr_add.shape[0]), arr_add)


#------------------------------
# save to db

conn = duckdb.connect("plaintext_word.duckdb")

conn.sql("""
CREATE TABLE IF NOT EXISTS char4 (
    phrase VARCHAR PRIMARY KEY
    )""")

conn.sql("show tables")
conn.sql("select * from char4")

conn.sql("insert into char4 select * from arr_add")
conn.sql(f"select phrase from char4 limit 20 offset {51_716_452}")

conn.sql("select count(phrase) from char4")


# conn.sql("DROP TABLE IF EXISTS char4")

# wawa = arr_add[6543210:6543310]
# conn.sql("insert into char4 select * from wawa")

conn.close()
