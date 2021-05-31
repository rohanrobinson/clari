from bs4 import BeautifulSoup
import glob
import sys
import os

def generate_caption(input_path, class_name):
    with open(input_path, 'r') as file:
        text1 = file.read()
    
    soup = BeautifulSoup(text1, 'html.parser')
    captions = soup.find_all(class_= "event-text")
    
    caption_text = []
    for caption in captions:
        text = caption.find('span').text
        text = text.split(':')[-1]
        caption_text.append(text)
        
    output_folder = "cleaned_captions/"+class_name
    file_name = input_path.split('/')[-1][:-4]

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    output_path = output_folder+"/"+file_name+".txt"
        
    with open(output_path, 'w') as filehandle:
        filehandle.write('\n'.join(caption_text))
    print(file_name,"done")

source_folder = "panopto_captions/"+sys.argv[1]
input_paths = glob.glob(source_folder+"/*.rtf")    
for input_path in input_paths:
    generate_caption(input_path, sys.argv[1])
