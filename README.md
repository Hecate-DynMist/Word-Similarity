# Word-Similarity

### Quick get start

```bash
$ pip install -r requirements.txt

# matching same words and name entities extraction
$ python Similarity.py same 
# matching similar words and name entities extraction
$ python Similarity.py similar
# matching same words by flashtext and name entities extraction
$ python Similarity.py flash
```

#### Time Spent for Same Words Match

Training on 1000 articles

| Method    | Time    |      |
| --------- | ------- | ---- |
| Brutal    | 508.354 |      |
| FlashText | 1.112   |      |
|           |         |      |

