import json
import lxml.etree as et
import os
import sys
import pandas as pd

class Main:

    @staticmethod
    def run():
        main = Main()
        main.process(pd.read_csv(sys.argv[1])).to_csv("metadata.csv")
        main.create_citation_graph(sys.argv[2]).to_csv("citation_graph.csv")

    def _get_keywords(self, body):
        prefix = "Category / Keywords: "
        for item in body:
            if item["body"].startswith(prefix):
                return item["body"][len(prefix):].strip()
        return "Not found"
    
    def _get_extension(self, body):
        prefix = "Available format(s):"
        for item in body:
            if item["body"].startswith(prefix):
                content = item["body"][len(prefix):].lower()
                if "pdf" in content:
                    return "pdf"
                if "ps" in content:
                    return "ps"
        return "invalid"
    
    def _get_abstract(self, body):
        prefix = "Abstract: "
        abstract = ""
        for item in body:
            if item["body"].startswith("Category / Keywords: "):
                break
            abstract += item["body"]
        return abstract[len(prefix):].strip()

    def _cleanup_title(self, title):
        try:
            title = str(title)
            title = title.strip()
            title = ' '.join(title.split())
            return title
        except Exception as e:
            print(e)

    def process(self, articles):
        articles['body'] = articles['body'].apply(json.loads)
        articles['extension'] = articles['body'].apply(self._get_extension)
        articles['abstract'] = articles['body'].apply(self._get_abstract)
        articles['keywords'] = articles['body'].apply(self._get_keywords)
        articles['url'] = articles['article-href'] + "." + articles['extension']
        articles['title'] = articles['title'].apply(self._cleanup_title)
        articles['authors'] = articles['authors'].apply(str)
        articles = articles.drop(['article-href', 'body', 'extension', 'web-scraper-order', 'web-scraper-start-url', 'article'], axis=1)
        return articles


    def process_citation(self, root):
        # root = et.fromstring(xml_content)
        return map(lambda x: self._cleanup_title(x.text), root.xpath(".//article-title"))


    def create_citation_graph(self, path):
        all_deps = list()
        for filename in os.listdir(path):
            if filename.endswith(".cermxml"):
                root = et.parse(os.path.join(path, filename)).getroot()
                dep = list(self.process_citation(root))
                if len(dep) <= 1:
                    continue
                all_deps.append({
                    "title": dep[0],
                    "refs": dep[1:],
                    })
            else:
                continue
        return pd.DataFrame(all_deps)
