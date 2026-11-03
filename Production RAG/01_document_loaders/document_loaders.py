from langchain_community.document_loaders import (TextLoader, PyPDFLoader, DirectoryLoader)
import os 
from pathlib import Path

cwd = os.getcwd()


def get_file_path(filename):
    return  os.path.join(cwd, "files", filename)


def test_text_loader():

    path = get_file_path("hello.txt")
    loader = TextLoader(path)
    documents = loader.load()

    print (f"Loaded {len(documents)} document(s) from {path}")


    try:

        for doc in documents:
            print(f"Document content: {doc.page_content}")
            print(f"Document metadata: {doc.metadata}")

    finally:
        print("Done loading text documents.")


def test_pdf_loader():
    
    path = get_file_path("sample_employee_handbook.pdf")
    loader = PyPDFLoader(path)
    documents = loader.load()

    print (f"Loaded {len(documents)} document(s) from {path}")

    try:

        for doc in documents:
            print(f"Document content: {doc.page_content}")
            print(f"Document metadata: {doc.metadata}")

    finally:
        print("Done loading PDF documents.")

def test_directory_loader():
    directory_path = os.path.join(cwd, "files")
    loader = DirectoryLoader(directory_path, glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    print(f"Loaded {len(documents)} document(s) from {directory_path}")
    # print(f"File 0 {files[0]}") 

    try:
        for doc in documents:
            print(f"Document content: {doc.page_content}")
            print(f"Document metadata: {doc.metadata['source']}")

    finally:
        print("Done loading documents from directory.")


# test_text_loader()
# test_pdf_loader()
# test_directory_loader()
