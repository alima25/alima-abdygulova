myfamily = ("mother", "father", "sister", "brother", "sister")

print("Type of myfamily:", type(myfamily))

# 2.
print("First sister:", myfamily[2])  
print("Second sister:", myfamily[4]) 

# 3. 
try:
    myfamily.append("me")  
except AttributeError as e:
    print("Error:", e, "- Tuples do not support append()")

# 4. 
try:
    myfamily.pop()  
except AttributeError as e:
    print("Error:", e, "- Tuples do not support pop()")


