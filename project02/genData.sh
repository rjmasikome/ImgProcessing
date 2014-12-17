#!/bin/bash
printf "WARNING! This will take around 40 - 60 minutes. \nIf you are sure, please do some other activity in the meantime. \n(e.g. drinking coffee)\n\n"

read -r -p "Are you sure? [y/N] " response
if [[ $response =~ ^([yY][eE][sS]|[yY])$ ]]
then
sed -i '/task4(img)/c\#task4(img)' 2-1.py
sed -i '/img, filename = get_img()/c\# img, filename = get_img()' 2-1.py
sed -i '/#filename = \"bauckhage.jpg\"/c\filename = \"bauckhage.jpg\"' 2-1.py
sed -i '/#img = Image.open(filename)/c\img = Image.open(filename)' 2-1.py

for i in {1..10}
do
   sed -i '/m_size = get_mask_size()/c\m_size = 3' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 5' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 7' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 9' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 11' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 13' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 15' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 17' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 19' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
   sed -i '/m_size = get_mask_size()/c\m_size = 21' 2-1.py
   python 2-1.py
   sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py
done

sed -i '/#task4(img)/c\task4(img)' 2-1.py
sed -i '/m_size = get_mask_size()/c\m_size = 3' 2-1.py
python 2-1.py
sed -i '/m_size = 3/c\m_size = get_mask_size()' 2-1.py

sed -i '/filename = \"bauckhage.jpg\"/c\#filename = \"bauckhage.jpg\"' 2-1.py
sed -i '/img = Image.open(filename)/c\#img = Image.open(filename)' 2-1.py
sed -i '/# img, filename = get_img()/c\img, filename = get_img()' 2-1.py
else
    exit 0
fi