from PIL import Image
import os
import sys

def main(argv):
    inpath = os.path.join(os.getcwd(),argv[1])
    outpath = os.path.splitext(inpath)[0] + ".png"
    print("%s -> %s" % (inpath,outpath))
    try:
        image = Image.open(inpath)
        image.save(outpath, format="png")
    except Exception as e:
        raise

if __name__ == '__main__':
    main(sys.argv)
