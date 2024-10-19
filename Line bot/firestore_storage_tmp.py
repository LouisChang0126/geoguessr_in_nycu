# firestore
import firebase_admin
from firebase_admin import credentials, firestore, storage

# 初始化 Firebase Admin SDK，並正確設置 Storage bucket 名稱
cred = credentials.Certificate('serviceAccount.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'meichu-hacker.appspot.com'
})

# 初始化 Firestore 客戶端
db = firestore.client()

# 抓取 Firebase Storage 內的檔案
def get_storage_file(file_path, destination_path):
    # 取得指定的 Storage bucket
    bucket = storage.bucket()
    blob = bucket.blob(file_path)  # 建立對檔案的引用
    blob.download_to_filename(destination_path)  # 下載檔案
    print(f'File downloaded to {destination_path}')

# 示例：下載 Firebase Storage 的檔案
get_storage_file('building/1.png', 'aaaaaaaaaaaa.png')  # 檔案路徑應該包含正確的子目錄
