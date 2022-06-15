import os, json, urllib.parse
from PIL import Image
from tqdm import tqdm

def resize_image(pic_path):
    # open
    pic = Image.open(pic_path).convert('RGB')
    
    # resize
    pic_75x75 = pic.resize((75, 75))
    pic_1024x768 = pic.resize((1024, 768))

    # save
    pic_name, ext = pic_path.rsplit('.', 1)
    
    pic_name = 'new_images/' + pic_name.split('/', 1)[-1]
    
    os.makedirs(pic_name.rsplit('/', 1)[0], exist_ok=True)

    pic_75x75.save(pic_name + '_75x75.' + ext)
    pic_1024x768.save(pic_name + '_1024x768.' + ext)

    return (pic_name + '_75x75.' + ext, pic_name + '_1024x768.' + ext)

# open json file
species = json.load(open('species.json', 'r'))

# log-list
missing = []

for specie in tqdm(species):
    # iterate save lists
    full_pic_75x75, full_pic_1024x768 = [], []
    
    # split the images by the ','
    for pic_path in specie['FULL_PIC'].split(','):
        pic_path = pic_path.lstrip('/')
        
        # check if image is available
        if os.path.exists(pic_path) and pic_path:
            # resize image and output the new images names
            pic_75x75, pic_1024x768 = resize_image(pic_path)
            # append the new names
            full_pic_75x75.append(pic_75x75)
            full_pic_1024x768.append(pic_1024x768)
        
        # incase of images with url encodings fix (35 error)
        elif os.path.exists(urllib.parse.unquote(pic_path)) and pic_path:
            # resize image and output the new images names
            pic_75x75, pic_1024x768 = resize_image(urllib.parse.unquote(pic_path))
            # append the new names
            full_pic_75x75.append(pic_75x75)
            full_pic_1024x768.append(pic_1024x768)
        
        # add to log, images that dont match - most properly files with ',' in its name
        else:
            missing.append(f'ID: {specie["ID"]}, image: {pic_path}')
    
    # save to json
    specie['FULL_PIC_75x75'] = ','.join(full_pic_75x75)
    specie['FULL_PIC_1024x768'] = ','.join(full_pic_1024x768)

with open('species.json', 'w') as f:
    json.dump(species, f, indent=2, ensure_ascii=False)

with open('full__missing_images.txt', 'w') as f:
    f.write('\n'.join(missing))