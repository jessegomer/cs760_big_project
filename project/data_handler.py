import os



class DataHandler(object):
    def __init__(self):
        self.full_path = r"C:/Users/jesse/PycharmProjects/cs760_big_project"
        self.files = {}
        for author in os.listdir(self.full_path + "/data"):
            self.files[author] = dict([(f.replace(".txt", ""), f) for f in os.listdir(self.full_path + "/data/" + author)])

    def load_file(self, author, title):
        return file(self.full_path + "/data/" + author + "/" + self.files[author][title])

    def load_author(self, author):
        titles = self.files[author].keys()
        files = []
        for t in titles:
            files.append(self.load_file(author, t))
        return files


