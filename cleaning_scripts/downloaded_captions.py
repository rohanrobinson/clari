import glob
import sys
import os

def generate_caption(input_path, class_name):
    lecture = []

    with open(input_path, 'r') as file:
        for line in file:
            if line.startswith( 'Soroush Vosoughi' ):
                lecture.append(line[18:].strip())
        
    output_folder = "static/texts"
    file_name = input_path.split('/')[-1][:-4]

    output_path = output_folder+"/"+file_name+".txt"
        
    with open(output_path, 'w') as filehandle:
        filehandle.write('\n'.join(caption_text))
    print(file_name,"done")

source_folder = "panopto_captions/"+sys.argv[1]
input_paths = glob.glob(source_folder+"/*.rtf")    
for input_path in input_paths:
    generate_caption(input_path, sys.argv[1])
