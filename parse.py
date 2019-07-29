import re




class Requirement:
    keywords = r"IF |< |> |= |THEN |-"
    TEST_TYPE = ""
    FILE = ""
    FUNCTION = ""
    INPUT = ""
    OUTPUT = ""
    DESC = ""
    CODE = ""

    def print_all(self):
        print(self.TEST_TYPE)
        print(self.FILE)
        print(self.FUNCTION)
        print(self.INPUT)
        print(self.OUTPUT)
        print(self.DESC)
        print(self.CODE)

    def split_keywords(self):
        print(type(self.CODE[0][0]))
        print(re.split(self.keywords, self.CODE[0][0]))


def get_req_blocks(reqs):
    results = re.findall(r'(?<=REQ\n)((?:.|\n)*?)(?=REQ)', reqs)
    return results


def remove_manual_test(reqs):
    autoTest = []
    for req in reqs:
        if re.match(r'(TEST_TYPE:(?: )*MANUAL)', req) is None:
            autoTest.append(req)
    return autoTest

def classify_reqs(reqs):
    reqObjects = []
    for req in reqs:
        obj = Requirement()
        obj.TEST_TYPE = re.findall(r'(?<=TEST_TYPE)(?: *: *)(.*)', req)
        obj.FILE = re.findall(r'(?<=FILE)(?: *: *)(.*)', req)
        obj.FUNCTION = re.findall(r'(?<=FUNCTION)(?: *: *)(.*)', req)
        obj.INPUT = re.findall(r'(?<=INPUT)(?: *: *)(.*)', req)
        obj.OUTPUT = re.findall(r'(?<=OUTPUT)(?: *: *)(.*)', req)
        obj.DESC = re.findall(r'(?<=DESC)(?: *: *)(.*)', req)
        obj.CODE = re.findall(r'(?<=CODE)(?: *: *\n)((.|\n)*?(?=CODE))', req)
        reqObjects.append(obj)
    return reqObjects

if __name__ == '__main__':
    reqObjects = 0
    with open("requirements.txt") as requirements_f:
        requirements = requirements_f.read()
        requirements = get_req_blocks(requirements)
        autoRequirements = remove_manual_test(requirements)
        reqObjects= classify_reqs(autoRequirements)
        reqObjects[0].split_keywords()
