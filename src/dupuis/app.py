import collections
import json
from pathlib import Path

from sanic import Sanic
from sanic import response

import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances


def flatten_values(d):
    if isinstance(d, collections.MutableMapping):
        return '\n'.join(map(flatten_values, d.values()))
    elif isinstance(d, list):
        return '\n'.join(map(flatten_values, d))
    else:
        return str(d or '')


def load_json(filepath):
    with Path(filepath).open() as fp:
        for talk in json.load(fp):
            yield talk


MatchingDocumentPair = collections.namedtuple('MatchingDocumentPair',
                                              ['doc_a', 'doc_b', 'distance', 'common_tokens', 'text_a', 'text_b'])

def match(source_a, source_b, ngram_range=(1, 1), token_pattern=r"(?u)\b\S+\b"):
    vectorizer = TfidfVectorizer(ngram_range=ngram_range, token_pattern=token_pattern)
    texts_a = [flatten_values(d).strip() for d in source_a]
    texts_b = [flatten_values(d).strip() for d in source_b]
    try:
        X = vectorizer.fit_transform(texts_a + texts_b)
    except:
        return

    tokens = vectorizer.get_feature_names()
    vectors_a, vectors_b = X[:len(texts_a),:], X[len(texts_a):,:]
    distances = cosine_distances(vectors_a, vectors_b)

    def _common_tokens(a, b):
        common_features = vectors_a[a].multiply(vectors_b[b]).toarray().flatten()
        common_tokens = [tokens[k] for k in np.argsort(common_features)
                         if common_features[k] > 0]
        common_tokens.reverse()
        return common_tokens

    row_ind, col_ind = linear_sum_assignment(distances)
    for i, j in zip(row_ind, col_ind):
        yield MatchingDocumentPair(source_a[i], source_b[j], distances[(i,j)], _common_tokens(i, j),
                                   texts_a[i], texts_b[j])


app = Sanic("Dupuis")

@app.route("/match", methods=['GET'])
async def get_matches(request):
    file1, file2 = request.args.get('file1'), request.args.get('file2')
    enabled_columns = list(request.args.getlist('columns[]', ['title']))
    def _filter(record):
        return {k: v for k, v in record.items() if k in enabled_columns}

    source_1 = list(load_json(file1))
    source_2 = list(load_json(file2))
    available_columns = list(set(k for doc in source_1+source_2 for k in doc))

    matches = match(source_a=list(map(_filter, source_1)),
                    source_b=list(map(_filter, source_2)))

    return response.json({
        'bestMatches': [
            m._asdict() for m in sorted(matches, key=lambda m: m.distance)
        ],
        'availableColumns': sorted(available_columns),
        'enabledColumns': enabled_columns
    })


@app.route("/", methods=['GET'])
def home(request):
    return response.file('templates/app.html', mime_type='text/html; charset=utf-8')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, auto_reload=True)
