# src
e governance project

cd D:\D_files\ME\Sem4\src\app\ 

python api.py


SRC/
│
├── app/                     ← Production Flask app
│   ├── api.py
│
├── models/                  ← Runtime AI files
│   ├── chunks.pkl
│   ├── embeddings.npy
│   ├── index.faiss
│
├── scripts/                 ← Offline scripts (IMPORTANT)
│   ├── prepare_embeddings.py
│   ├── rebuild_index.py
│   ├── train_model.py
│   └── visual.py
│
├── templates/
│   ├── index.html
│   ├── services.html
│   ├── schemes.html
│   └── departments.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── data/                    ← Raw data files
│
├── fine-tuned-tamilnadu-model/  ← HuggingFace saved model
│
├── requirements.txt
├── Dockerfile
└── README.md