import glob, os
os.chdir('./res')
for file in glob.glob("*.fb2"):
    print(file)
