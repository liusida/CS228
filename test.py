import os
print(next(os.walk("userData")))
print(os.walk("userData").next())
for root, dirs, files in os.walk("userData"):
    print(files)
