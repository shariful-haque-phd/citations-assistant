import argparse,pickle
from pathlib import Path
import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def docs(folder):
    out=[]
    for p in Path(folder).rglob("*"):
        if p.suffix.lower()==".pdf":
            for n,page in enumerate(PdfReader(str(p)).pages,1):
                txt=" ".join((page.extract_text() or "").split())
                if txt: out.append({"source":str(p),"page":n,"text":txt})
        elif p.suffix.lower() in {".md",".txt"}:
            out.append({"source":str(p),"page":1,"text":" ".join(p.read_text(errors="replace").split())})
    return out

def build(folder,out):
    d=docs(folder)
    if not d: raise ValueError("No manuals found.")
    vec=TfidfVectorizer(stop_words="english",ngram_range=(1,2)); mat=vec.fit_transform([x["text"] for x in d])
    Path(out).mkdir(parents=True,exist_ok=True)
    with open(Path(out)/"manuals.pkl","wb") as f:pickle.dump({"docs":d,"vec":vec,"mat":mat},f)

def ask(out,q,k=4):
    with open(Path(out)/"manuals.pkl","rb") as f:d=pickle.load(f)
    s=cosine_similarity(d["vec"].transform([q]),d["mat"])[0]
    for rank,i in enumerate(np.argsort(s)[::-1][:k],1):
        x=d["docs"][int(i)]
        print(f"[{rank}] {x['source']} p.{x['page']} | score {s[i]:.3f}\n{x['text'][:900]}\n")

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("index");a.add_argument("folder");a.add_argument("--index-dir",default="index")
    q=sub.add_parser("ask");q.add_argument("index_dir");q.add_argument("question");q.add_argument("--top-k",type=int,default=4)
    x=ap.parse_args();build(x.folder,x.index_dir) if x.cmd=="index" else ask(x.index_dir,x.question,x.top_k)
if __name__=="__main__":main()
