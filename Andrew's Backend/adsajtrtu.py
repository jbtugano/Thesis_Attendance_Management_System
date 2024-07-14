import pandas as pd
import datetime
from deepface import DeepFace

"""
data = [{'STUDENT NAME': 'Escandor, Andrew T.', 'STUDENT NUMBER': '2015-2-01350', 'PROGRAM': 'BS CpE', 'SECTION': 'ARCH 201', 'PROGRESS STATUS': 0}, {'STUDENT NAME': 'Escandor, Dummy Data 1.', 'STUDENT NUMBER': '2024-2-29604', 'PROGRAM': 'Tourism', 'SECTION': 'ME 201', 'PROGRESS STATUS': 4}, {'STUDENT NAME': 'drew22', 'STUDENT NUMBER': '2024-2-26638', 'PROGRAM': 'CivilEng', 'SECTION': 'ARCH 201', 'PROGRESS STATUS': 0}, {'STUDENT NAME': 'drew276', 'STUDENT NUMBER': '33723', 'PROGRAM': 'CivilEng', 'SECTION': 'ME 201', 'PROGRESS STATUS': 2}, {'STUDENT NAME': 'drew294', 'STUDENT NUMBER': '81366', 'PROGRAM': 'IT', 'SECTION': 'ARCH 201', 'PROGRESS STATUS': 0}, {'STUDENT NAME': 'drew42', 'STUDENT NUMBER': '2024-2-99967', 'PROGRAM': 'CivilEng', 'SECTION': 'ME 201', 'PROGRESS STATUS': 0}, {'STUDENT NAME': 'drew516', 'STUDENT NUMBER': '64188', 'PROGRAM': 'Tourism', 'SECTION': 'ME 201', 'PROGRESS STATUS': 2}, {'STUDENT NAME': 'drew66', 'STUDENT NUMBER': '2024-2-76512', 'PROGRAM': 'Compu123', 'SECTION': 'ME 201', 'PROGRESS STATUS': 0}, {'STUDENT NAME': 'drew76', 'STUDENT NUMBER': '2024-2-78138', 'PROGRAM': 'Tourism', 'SECTION': 'ME 201', 'PROGRESS STATUS': 0}]

df = pd.DataFrame(data)

file_name = f"FULL SEMESTER-ESCANDOR-{datetime.datetime.now().strftime('%B%d%Y')}"
# {faculty name} - {date_today}
print(file_name)
df.to_excel(f'{file_name}.xlsx', index=False) """

metrics = [
    'cosine',
    'euclidean',
    'euclidean_l2'
]
s = DeepFace.verify(img1_path='static/uploads/measured_data/310.jpg', img2_path='static/uploads/copied_ref/20231456/Sofhia, Marriel 4 20231456.jpg',
                    detector_backend='ssd', model_name='DeepID', distance_metric=metrics[0])
print(s)

"""
Model - cosine - euclidean - euclidean_l2
VGG-Face - 0.68 - 1.17 - 1.17
Facenet - 0.4 - 10 - 0.8
Facenet512 - 0.3 - 23.56 - 1.04
DeepID - 0.015 - 45 - 0.17



"""