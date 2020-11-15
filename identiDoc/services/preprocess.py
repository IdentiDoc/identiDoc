# for convertinf jpg to png
import sys
from PIL import Image
import logging
# where the input file are stored, can be updated as required
input_filepath= "input/"
# where the output file is stored, can be updated as required
output_filepath="converted/"

def convert_to_png(filename):
    filepath=input_filepath+filename
    image = Image.open(filepath)
    next_file=next_filename()
    new_filename = output_filepath+next_file+".png"
    image.save(new_filename)
    log_this("convert_to_png",filename,next_file+".png")

# reads log to determine next output filename for next file
def next_filename():
    file = open("log/preprocess.log", "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    line_count= str(line_count)
    return line_count

# logs the conversion to /log/preprocess.log
# ideally it would query database to see nextfilename or use timestamp/datestamp as filename
# since database is not yet implimented, this is temporary solution to read # of files
# here #of lines in log = # of files yet converted
def log_this(method_type,filename,new_filename):
    logger = logging.getLogger('preprocess_log')
    hdlr = logging.FileHandler('log/preprocess.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    message = method_type+","+filename+","+new_filename
    logger.info(message)

# main function
# this makes function calls to deskew, brighten image, etc as required

def main():
    provided_filename=sys.argv[1]
    convert_to_png(provided_filename)

main()