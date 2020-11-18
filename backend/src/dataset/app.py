import json

class Main:

    @staticmethod
    def run():
        print("Hello World...")

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

