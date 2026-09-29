from typing import List, Any
import numpy as np
from typing import *
import sqlite3
from financial_reports.backend.utils.LLMRequest import LLMRequest
import sys, os, json

llm = LLMRequest()

def create_vector_db(datatype:str, source: str):
    data = json.load(open(source, 'r', encoding='utf-8'))
    new_data = []
    
    for item in data:
        embedding = llm.embedding_model(item['brief'])
        new_data.append([embedding, item['info']])
    
    if datatype == 'sqlite3':
        db = sqlite3.connect('vector_data.db')
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vector_data (
                No INTEGER PRIMARY KEY AUTOINCREMENT,
                embedding BLOB,
                info TEXT,
                type TEXT,
                detail TEXT
            )
        ''')
        for embedding, info in new_data:
            embedding_bytes = np.array(embedding, dtype=np.float32).tobytes()
            cursor.execute("INSERT INTO vector_data (embedding, info, type) VALUES (?, ?, ?)", 
                           (embedding_bytes, info, datatype))
        db.commit()
        db.close()
    elif datatype == 'csv':
        import csv
        with open('vector_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['embedding', 'info', 'type'])
            for embedding, info in new_data:
                writer.writerow([json.dumps(embedding.tolist()), info, datatype])
        

class VectorDatabase:
    """
    Mock vector database for demonstration.
    Replace with actual vector DB integration (e.g., FAISS, Pinecone, Azure Cognitive Search, etc.).
    """
    def __init__(self, datatype: str, sqlite3db: str = "vector_data.db", csvdata: str = "vector_data.csv"):
            db = sqlite3.connect(sqlite3db)
            self.db = db
            # get Columns: row num, broad info
            self.data = [] # [(embedding, rownum)]
            cursor = db.cursor()
            cursor.execute("SELECT embedding, info FROM vector_data where type = 'text'")
            rows = cursor.fetchall()
            for row in rows:
                embedding = np.frombuffer(row[0], dtype=np.float32)
                self.data.append((embedding, row[1]))

    def add(self, embedding: np.array, metadata: Any):
        self.data.append((embedding, metadata))

    def search(self, query_embedding: np.array, top_k: int = 5):
        # Simple L2 distance search for demonstration
        def l2_distance(a, b):
            return np.linalg.norm(a - b)

        results = sorted(
            self.data,
            key=lambda item: l2_distance(query_embedding, item[0])
        )
        return results[:top_k]
    
    def add_row(self, info, type, detail):
        """
        Add a new row to the vector database.
        info: The information to be added.
        type: The type of the information (e.g., 'text', 'image').
        """
        cursor = self.db.cursor()
        llm_requester = LLMRequest()
        embedding = llm_requester.embedding_model(info)
        embedding_bytes = embedding.tobytes()
        lastNo = cursor.execute("SELECT MAX(No) FROM vector_data").fetchone()[0]
        if lastNo is None:
            lastNo = 0
        cursor.execute("INSERT INTO vector_data (No, embedding, info, type, detail) VALUES (?, ?, ?, ?, ?)", 
                       (lastNo + 1, embedding_bytes, info, type, detail))
        


class RAG:
    def __init__(self, vector_db: VectorDatabase):
        self.vector_db = vector_db

    def search_by_embedding(self, embed: List[float], top_k: int = 5):
        """
        Search for relevant data in the vector database using the provided embedding.
        Returns top_k results.
        """
        return self.vector_db.search(embed, top_k=top_k)
    

if __name__ == "__main__":
    vector_db = VectorDatabase()
    rag = RAG(vector_db)
    
    # Example usage
