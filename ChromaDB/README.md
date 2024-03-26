# ChromaDB
Populates the chromaDB hosted at a specified location with data in the segment.json file

## File Structure
```
.
└── ChromaDB/
    ├── chromaBuild.py
    ├── segment.json
    ├── Dockerfile.chromadb
    └── docker-compose.yaml

```

## Run
```bash
    cd ChromaDB
    docker compose up --build
```


## segment.json structure
segment.json is the Insurance handbook manually segmented section by section

```json
[
    {
        "id": 0, // increment
        "document": "", // this is the content
        "metadata": {
          "page": "#", 
          "section": "",
          "subsection": "",
          "type": "paragraph"
        }
      }
      ...
]
```
