import pickle, re, glob, json, time

# read the list
with open('list.pkl', 'rb') as f:
    filenames = pickle.load(f)

def clean_line(image, fn, fh1, fh2, fh3):
    for p_name in ['THUMB_PIC','FULL_PIC']:
        out = []
        for img in image[p_name].split(','):
            img = img.replace(':','_').replace('%20',' ').replace('%2B','+').replace('%',' ').strip()
            
            if img.startswith('/images/') and '/full.jpg' not in img:
                img = img+'/full.jpg'
                out.append(img)
            
            if not img.startswith('/images/') or img in filenames:
                pass

            else:
                print(f'ID ({image["ID"]}) "{p_name}" in "{fn}", Image Path: "{img}", Not Found')
                print(f'ID ({image["ID"]}) "{p_name}" in "{fn}", Image Path: "{img}", Not Found', file=fh1)
                image[p_name] = ",".join(out)

    if len(image['FULL_PIC'])<2:
        print(f'ID ({image["ID"]}) in "{fn}", No FULL_PIC exist')
        print(f'ID ({image["ID"]}) in "{fn}", No FULL_PIC exist', file=fh2)
    
    if len(image['DESCRIPTION'])<2:
        print(f'ID ({image["ID"]}) in "{fn}", No DESCRIPTION exist')
        print(f'ID ({image["ID"]}) in "{fn}", No DESCRIPTION exist', file=fh3)
    
    return image

# cleaning
fh1 = open('file_log.txt','w')
fh2 = open('FULL_PIC_log.txt','w')
fh3= open('DESCRIPTION_log.txt','w')

for i in range(1,5):
    with open(f'species{i}.json','r',encoding="utf-8") as fr:
        with open(f'new_species{i}.json','w',encoding="utf-8") as fw:
            o_txt = re.sub(r'([",])(/\d+/)',
                         r'\1/images\2',
                         fr.read().replace('.jpg"\n','.jpg",\n').replace('full.jpg/','full.jpg,/'))
            print(o_txt, file=fw)
    
    images = json.loads(o_txt)
    
    for ii in range(len(images)):
        images[ii] = clean_line(images[ii], f'new_species{i}.json', fh1, fh2, fh3)
        
    # json.dump(images,open(f'new_species{i}.json', 'w', encoding="utf-8"), indent=4)

for ff in [fh1, fh2, fh3]:
    ff.close()
